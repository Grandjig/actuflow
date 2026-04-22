"""AI Service.

Client for communicating with the AI microservice.
"""

import httpx
from typing import Any, Optional

from app.config import settings


class AIServiceUnavailable(Exception):
    """Raised when AI service is unavailable."""
    pass


class AIService:
    """Client for AI microservice."""
    
    def __init__(self):
        self.base_url = settings.AI_SERVICE_URL
        self.timeout = 30.0
    
    async def health_check(self) -> bool:
        """Check if AI service is healthy."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/health",
                    timeout=5.0,
                )
                return response.status_code == 200
        except Exception:
            return False
    
    async def get_features(self) -> dict[str, Any]:
        """Get available AI features."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/features",
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise AIServiceUnavailable(f"AI service unavailable: {e}")
    
    async def parse_natural_language_query(
        self,
        query: str,
        context: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Parse a natural language query."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/parse-query",
                    json={"query": query, "context": context or {}},
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise AIServiceUnavailable(f"AI service unavailable: {e}")
    
    async def generate_narrative(
        self,
        template: str,
        data: dict[str, Any],
        max_length: int = 500,
        tone: str = "professional",
    ) -> dict[str, Any]:
        """Generate narrative text."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/generate-narrative",
                    json={
                        "template": template,
                        "data": data,
                        "max_length": max_length,
                        "tone": tone,
                    },
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise AIServiceUnavailable(f"AI service unavailable: {e}")
    
    async def detect_anomalies(
        self,
        record_type: str,
        data: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Detect anomalies in data."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/detect-anomalies",
                    json={"record_type": record_type, "data": data},
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return response.json().get("anomalies", [])
        except Exception as e:
            raise AIServiceUnavailable(f"AI service unavailable: {e}")
    
    async def get_import_suggestions(
        self,
        import_type: str,
        columns: list[str],
        sample_data: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Get AI suggestions for data import."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/suggest-column-mapping",
                    json={
                        "import_type": import_type,
                        "columns": columns,
                        "sample_data": sample_data,
                    },
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise AIServiceUnavailable(f"AI service unavailable: {e}")
    
    async def get_experience_recommendations(
        self,
        tables: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Get experience study recommendations."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/experience-recommendations",
                    json={"tables": tables},
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return response.json().get("recommendations", [])
        except Exception as e:
            raise AIServiceUnavailable(f"AI service unavailable: {e}")
    
    async def semantic_search(
        self,
        query: str,
        resource_type: Optional[str] = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Perform semantic search."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/semantic-search",
                    json={
                        "query": query,
                        "resource_type": resource_type,
                        "limit": limit,
                    },
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return response.json().get("results", [])
        except Exception as e:
            raise AIServiceUnavailable(f"AI service unavailable: {e}")
