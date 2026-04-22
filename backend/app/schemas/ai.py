"""AI Schemas."""

from datetime import datetime
from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel, Field


class NaturalLanguageQuery(BaseModel):
    """Schema for natural language query."""
    query: str = Field(..., min_length=1)
    context: Optional[dict[str, Any]] = None


class ParsedIntent(BaseModel):
    """Schema for parsed intent."""
    type: str
    entity: Optional[str] = None
    filters: Optional[dict[str, Any]] = None


class SuggestedAction(BaseModel):
    """Schema for suggested action."""
    action: str
    parameters: dict[str, Any]
    explanation: str


class NaturalLanguageResponse(BaseModel):
    """Schema for natural language response."""
    query: str
    parsed_intent: dict[str, Any]
    explanation: str
    suggested_action: Optional[SuggestedAction] = None
    result_count: Optional[int] = None
    query_id: Optional[str] = None


class QueryFeedback(BaseModel):
    """Schema for query feedback."""
    was_helpful: bool
    feedback: Optional[str] = None


class NarrativeRequest(BaseModel):
    """Schema for narrative request."""
    template: str
    data: dict[str, Any]
    max_length: Optional[int] = 500
    tone: Optional[str] = "professional"


class NarrativeResponse(BaseModel):
    """Schema for narrative response."""
    text: str
    generated_at: Optional[datetime] = None


class SemanticSearchRequest(BaseModel):
    """Schema for semantic search request."""
    query: str
    resource_type: Optional[str] = None
    limit: Optional[int] = 10


class SemanticSearchResponse(BaseModel):
    """Schema for semantic search response."""
    query: str
    results: list[dict[str, Any]]
    total: int
