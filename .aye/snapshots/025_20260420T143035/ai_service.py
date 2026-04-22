"""AI Service Client.

Client for calling the AI microservice from the backend.
"""

import logging
from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import settings

logger = logging.getLogger(__name__)


class AIServiceUnavailable(Exception):
    """Raised when AI service is unavailable."""
    pass


class AIService:
    """Client for AI microservice."""
    
    def __init__(self):
        self.base_url = settings.AI_SERVICE_URL
        self.enabled = settings.AI_ENABLED
        self.timeout = 30.0
    
    def _check_enabled(self):
        """Check if AI is enabled."""
        if not self.enabled:
            raise AIServiceUnavailable("AI features are disabled")
    
    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=2),
    )
    async def _request(
        self,
        method: str,
        endpoint: str,
        json: dict | None = None,
    ) -> dict:
        """Make request to AI service."""
        self._check_enabled()
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.request(
                    method,
                    f"{self.base_url}{endpoint}",
                    json=json,
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"AI service error: {e.response.status_code}")
                raise AIServiceUnavailable(f"AI service error: {e.response.text}")
            except httpx.RequestError as e:
                logger.error(f"AI service unavailable: {e}")
                raise AIServiceUnavailable("AI service is unavailable")
    
    async def health_check(self) -> bool:
        """Check if AI service is healthy."""
        try:
            result = await self._request("GET", "/health")
            return result.get("status") == "healthy"
        except AIServiceUnavailable:
            return False
    
    async def get_features(self) -> dict:
        """Get enabled AI features."""
        try:
            return await self._request("GET", "/features")
        except AIServiceUnavailable:
            return {"ai_enabled": False, "features": {}}
    
    # NLP Functions
    
    async def parse_natural_language_query(
        self,
        query: str,
        context: dict | None = None,
    ) -> dict:
        """Parse a natural language query."""
        return await self._request(
            "POST",
            "/nlp/parse-query",
            json={"query": query, "context": context},
        )
    
    async def generate_narrative(
        self,
        template: str,
        data: dict,
        max_length: int = 500,
        tone: str = "professional",
    ) -> dict:
        """Generate narrative text from structured data."""
        return await self._request(
            "POST",
            "/nlp/generate-text",
            json={
                "template": template,
                "data": data,
                "max_length": max_length,
                "tone": tone,
            },
        )
    
    async def suggest_column_mapping(
        self,
        source_columns: list[str],
        sample_values: dict,
        target_type: str,
    ) -> list[dict]:
        """Suggest column mappings for data import."""
        return await self._request(
            "POST",
            "/nlp/suggest-mapping",
            json={
                "source_columns": source_columns,
                "sample_values": sample_values,
                "target_type": target_type,
            },
        )
    
    async def analyze_data_quality(self, data: dict) -> list[dict]:
        """Analyze data quality issues."""
        return await self._request(
            "POST",
            "/nlp/analyze-data-quality",
            json=data,
        )
    
    # Embedding Functions
    
    async def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding for text."""
        result = await self._request(
            "POST",
            "/embeddings/generate",
            json={"text": text},
        )
        return result.get("embedding", [])
    
    async def semantic_search(
        self,
        query: str,
        resource_type: str | None = None,
        limit: int = 10,
        threshold: float = 0.7,
    ) -> list[dict]:
        """Search for similar content."""
        return await self._request(
            "POST",
            "/embeddings/search",
            json={
                "query": query,
                "resource_type": resource_type,
                "limit": limit,
                "threshold": threshold,
            },
        )
    
    # Extraction Functions
    
    async def extract_document_data(
        self,
        content_base64: str,
        filename: str,
        document_type: str | None = None,
    ) -> dict:
        """Extract data from a document."""
        return await self._request(
            "POST",
            "/extract/document-base64",
            json={
                "content_base64": content_base64,
                "filename": filename,
                "document_type": document_type,
            },
        )
    
    # Anomaly Detection Functions
    
    async def detect_anomalies(
        self,
        data: list[dict],
        record_type: str,
        features: list[str],
        context: dict | None = None,
    ) -> dict:
        """Detect anomalies in records."""
        return await self._request(
            "POST",
            "/anomaly/detect",
            json={
                "data": data,
                "record_type": record_type,
                "features": features,
                "context": context,
            },
        )
    
    async def explain_anomaly(
        self,
        record: dict,
        record_type: str,
        features: list[str],
    ) -> dict:
        """Get explanation for an anomaly."""
        return await self._request(
            "POST",
            "/anomaly/explain",
            json={
                "record": record,
                "record_type": record_type,
                "features": features,
            },
        )
