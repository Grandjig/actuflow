"""Anomaly Detection Service."""

import json
import logging
import pickle
from typing import Any

import numpy as np
import redis
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from config import settings
from services.llm_client import LLMClient

logger = logging.getLogger(__name__)


class AnomalyService:
    """Service for anomaly detection."""
    
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
        self.llm_client = LLMClient()
    
    async def detect(
        self,
        data: list[dict],
        record_type: str,
        features: list[str],
        context: dict | None = None,
    ) -> list[dict]:
        """Detect anomalies in a batch of records."""
        if not data:
            return []
        
        # Try to load trained model
        model = self._load_model(record_type)
        scaler = self._load_scaler(record_type)
        
        # Prepare feature matrix
        X = self._prepare_features(data, features)
        
        if model is None:
            # Use unsupervised detection on current batch
            model = IsolationForest(
                contamination=settings.ANOMALY_CONTAMINATION,
                random_state=42,
            )
            if len(X) > 10:
                model.fit(X)
        
        if scaler is None:
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
        else:
            X_scaled = scaler.transform(X)
        
        # Get predictions
        predictions = model.predict(X_scaled)
        scores = model.decision_function(X_scaled)
        
        # Normalize scores to 0-1 range (higher = more anomalous)
        normalized_scores = 1 - (scores - scores.min()) / (scores.max() - scores.min() + 1e-10)
        
        results = []
        for i, record in enumerate(data):
            is_anomaly = predictions[i] == -1 and normalized_scores[i] > settings.ANOMALY_THRESHOLD
            
            # Get feature contributions
            contributions = self._get_feature_contributions(record, features, X[i], scaler)
            
            # Get reasons
            reasons = self._get_anomaly_reasons(record, features, contributions) if is_anomaly else []
            
            results.append({
                "record_id": record.get("id"),
                "is_anomaly": is_anomaly,
                "anomaly_score": float(normalized_scores[i]),
                "anomaly_reasons": reasons,
                "feature_contributions": contributions,
            })
        
        return results
    
    async def train_model(
        self,
        data: list[dict],
        record_type: str,
        features: list[str],
        model_name: str,
        contamination: float = 0.1,
    ) -> bool:
        """Train an anomaly detection model."""
        if len(data) < 50:
            logger.warning(f"Not enough data to train model: {len(data)} records")
            return False
        
        try:
            # Prepare features
            X = self._prepare_features(data, features)
            
            # Fit scaler
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Train model
            model = IsolationForest(
                contamination=contamination,
                random_state=42,
                n_estimators=100,
            )
            model.fit(X_scaled)
            
            # Save model and scaler
            self._save_model(model, record_type, model_name)
            self._save_scaler(scaler, record_type, model_name)
            
            # Store feature statistics for explanations
            stats = self._calculate_statistics(X, features)
            self._save_statistics(stats, record_type, model_name)
            
            logger.info(f"Trained anomaly model: {model_name} for {record_type}")
            return True
            
        except Exception as e:
            logger.exception(f"Failed to train model: {e}")
            return False
    
    async def explain_anomaly(
        self,
        record: dict,
        record_type: str,
        features: list[str],
    ) -> dict:
        """Get detailed explanation of why a record is anomalous."""
        # Detect anomaly
        result = (await self.detect([record], record_type, features))[0]
        
        if not result["is_anomaly"]:
            return {
                "is_anomaly": False,
                "anomaly_score": result["anomaly_score"],
                "explanation": "This record does not appear to be anomalous.",
                "contributing_factors": [],
                "similar_normal_records": 0,
            }
        
        # Get statistics for comparison
        stats = self._load_statistics(record_type)
        
        # Build contributing factors
        contributing_factors = []
        for feature in features:
            if feature in record and feature in stats:
                value = record[feature]
                expected_mean = stats[feature]["mean"]
                expected_std = stats[feature]["std"]
                expected_min = stats[feature]["min"]
                expected_max = stats[feature]["max"]
                
                if isinstance(value, (int, float)) and expected_std > 0:
                    z_score = abs(value - expected_mean) / expected_std
                    if z_score > 2:
                        contributing_factors.append({
                            "feature": feature,
                            "value": value,
                            "expected_range": f"{expected_min:.2f} to {expected_max:.2f}",
                            "deviation": f"{z_score:.1f} standard deviations from mean",
                        })
        
        # Generate natural language explanation
        explanation = await self._generate_explanation(record, result, contributing_factors)
        
        return {
            "is_anomaly": True,
            "anomaly_score": result["anomaly_score"],
            "explanation": explanation,
            "contributing_factors": contributing_factors,
            "similar_normal_records": 0,  # Would need database query
        }
    
    async def _generate_explanation(
        self,
        record: dict,
        result: dict,
        factors: list[dict],
    ) -> str:
        """Generate natural language explanation."""
        if not factors:
            return f"This record has an anomaly score of {result['anomaly_score']:.2f}, indicating unusual patterns in the data."
        
        prompt = f"""Explain why the following record was flagged as potentially anomalous in a professional, concise manner.

Record: {json.dumps(record, default=str)}
Anomaly Score: {result['anomaly_score']:.2f}
Contributing Factors:
{json.dumps(factors, indent=2)}

Write a 2-3 sentence explanation suitable for a risk analyst."""
        
        try:
            explanation = await self.llm_client.complete(prompt, max_tokens=200)
            return explanation.strip()
        except Exception as e:
            logger.warning(f"LLM explanation failed: {e}")
            # Fallback
            factor_strs = [f"{f['feature']} ({f['deviation']})" for f in factors[:3]]
            return f"This record was flagged due to unusual values in: {', '.join(factor_strs)}."
    
    def _prepare_features(self, data: list[dict], features: list[str]) -> np.ndarray:
        """Prepare feature matrix from data."""
        rows = []
        for record in data:
            row = []
            for feature in features:
                value = record.get(feature, 0)
                if isinstance(value, (int, float)):
                    row.append(float(value))
                else:
                    row.append(0.0)
            rows.append(row)
        return np.array(rows)
    
    def _get_feature_contributions(
        self,
        record: dict,
        features: list[str],
        feature_values: np.ndarray,
        scaler: StandardScaler | None,
    ) -> dict[str, float]:
        """Calculate feature contributions to anomaly score."""
        contributions = {}
        
        if scaler is not None:
            scaled = scaler.transform(feature_values.reshape(1, -1))[0]
            for i, feature in enumerate(features):
                contributions[feature] = abs(float(scaled[i]))
        else:
            for feature in features:
                contributions[feature] = 0.0
        
        return contributions
    
    def _get_anomaly_reasons(self, record: dict, features: list[str], contributions: dict) -> list[str]:
        """Generate human-readable anomaly reasons."""
        reasons = []
        
        # Sort by contribution
        sorted_features = sorted(contributions.items(), key=lambda x: x[1], reverse=True)
        
        for feature, contribution in sorted_features[:3]:
            if contribution > 1.5:
                value = record.get(feature)
                reasons.append(f"Unusual value for {feature}: {value}")
        
        return reasons if reasons else ["Combination of feature values is unusual"]
    
    def _calculate_statistics(self, X: np.ndarray, features: list[str]) -> dict:
        """Calculate statistics for features."""
        stats = {}
        for i, feature in enumerate(features):
            values = X[:, i]
            stats[feature] = {
                "mean": float(np.mean(values)),
                "std": float(np.std(values)),
                "min": float(np.min(values)),
                "max": float(np.max(values)),
                "median": float(np.median(values)),
            }
        return stats
    
    def _load_model(self, record_type: str) -> IsolationForest | None:
        """Load trained model from Redis."""
        key = f"anomaly_model:{record_type}"
        data = self.redis_client.get(key)
        if data:
            return pickle.loads(data)
        return None
    
    def _save_model(self, model: IsolationForest, record_type: str, model_name: str):
        """Save model to Redis."""
        key = f"anomaly_model:{record_type}"
        self.redis_client.set(key, pickle.dumps(model))
    
    def _load_scaler(self, record_type: str) -> StandardScaler | None:
        """Load scaler from Redis."""
        key = f"anomaly_scaler:{record_type}"
        data = self.redis_client.get(key)
        if data:
            return pickle.loads(data)
        return None
    
    def _save_scaler(self, scaler: StandardScaler, record_type: str, model_name: str):
        """Save scaler to Redis."""
        key = f"anomaly_scaler:{record_type}"
        self.redis_client.set(key, pickle.dumps(scaler))
    
    def _load_statistics(self, record_type: str) -> dict:
        """Load statistics from Redis."""
        key = f"anomaly_stats:{record_type}"
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        return {}
    
    def _save_statistics(self, stats: dict, record_type: str, model_name: str):
        """Save statistics to Redis."""
        key = f"anomaly_stats:{record_type}"
        self.redis_client.set(key, json.dumps(stats))
