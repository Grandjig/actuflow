"""Anomaly Detection API Routes."""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from config import settings
from services.anomaly_service import AnomalyService

logger = logging.getLogger(__name__)
router = APIRouter()


class AnomalyDetectionRequest(BaseModel):
    """Anomaly detection request."""
    data: list[dict]  # Records to check
    record_type: str  # claim, calculation_result, policy
    features: list[str]  # Which fields to analyze
    context: dict | None = None  # Additional context


class AnomalyResult(BaseModel):
    """Anomaly detection result for a single record."""
    record_id: str | None
    is_anomaly: bool
    anomaly_score: float
    anomaly_reasons: list[str]
    feature_contributions: dict[str, float]  # Which features contributed


class AnomalyDetectionResponse(BaseModel):
    """Anomaly detection response."""
    results: list[AnomalyResult]
    anomaly_count: int
    threshold_used: float
    model_type: str


class TrainModelRequest(BaseModel):
    """Train anomaly model request."""
    data: list[dict]
    record_type: str
    features: list[str]
    model_name: str
    contamination: float = Field(default=0.1, ge=0.01, le=0.5)


class TrainModelResponse(BaseModel):
    """Train model response."""
    model_name: str
    record_type: str
    training_samples: int
    features: list[str]
    success: bool
    message: str


class ExplainAnomalyRequest(BaseModel):
    """Explain why a record is anomalous."""
    record: dict
    record_type: str
    features: list[str]


class AnomalyExplanation(BaseModel):
    """Explanation of anomaly."""
    is_anomaly: bool
    anomaly_score: float
    explanation: str  # Natural language explanation
    contributing_factors: list[dict]  # Feature, value, expected range
    similar_normal_records: int


@router.post("/detect", response_model=AnomalyDetectionResponse)
async def detect_anomalies(request: AnomalyDetectionRequest):
    """Detect anomalies in a batch of records."""
    if not settings.AI_ANOMALY_DETECTION:
        raise HTTPException(status_code=404, detail="Anomaly detection feature disabled")
    
    try:
        service = AnomalyService()
        results = await service.detect(
            data=request.data,
            record_type=request.record_type,
            features=request.features,
            context=request.context,
        )
        
        anomaly_count = sum(1 for r in results if r["is_anomaly"])
        
        return AnomalyDetectionResponse(
            results=[AnomalyResult(**r) for r in results],
            anomaly_count=anomaly_count,
            threshold_used=settings.ANOMALY_THRESHOLD,
            model_type="isolation_forest",
        )
        
    except Exception as e:
        logger.exception(f"Error detecting anomalies: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/train", response_model=TrainModelResponse)
async def train_model(request: TrainModelRequest):
    """Train an anomaly detection model on historical data."""
    if not settings.AI_ANOMALY_DETECTION:
        raise HTTPException(status_code=404, detail="Anomaly detection feature disabled")
    
    try:
        service = AnomalyService()
        success = await service.train_model(
            data=request.data,
            record_type=request.record_type,
            features=request.features,
            model_name=request.model_name,
            contamination=request.contamination,
        )
        
        return TrainModelResponse(
            model_name=request.model_name,
            record_type=request.record_type,
            training_samples=len(request.data),
            features=request.features,
            success=success,
            message="Model trained successfully" if success else "Training failed",
        )
        
    except Exception as e:
        logger.exception(f"Error training model: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain", response_model=AnomalyExplanation)
async def explain_anomaly(request: ExplainAnomalyRequest):
    """Get a detailed explanation of why a record is flagged."""
    if not settings.AI_ANOMALY_DETECTION:
        raise HTTPException(status_code=404, detail="Anomaly detection feature disabled")
    
    try:
        service = AnomalyService()
        explanation = await service.explain_anomaly(
            record=request.record,
            record_type=request.record_type,
            features=request.features,
        )
        
        return AnomalyExplanation(**explanation)
        
    except Exception as e:
        logger.exception(f"Error explaining anomaly: {e}")
        raise HTTPException(status_code=500, detail=str(e))
