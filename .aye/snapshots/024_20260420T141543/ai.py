"""
AI Feature Schemas
==================

Schemas for AI-powered features.
"""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# =============================================================================
# Natural Language Query Schemas
# =============================================================================

class NaturalLanguageQuery(BaseModel):
    """Natural language query request."""
    
    query: str = Field(min_length=1, max_length=1000)
    context: Optional[dict[str, Any]] = Field(
        default=None,
        description="Additional context for the query"
    )


class ParsedIntent(BaseModel):
    """AI's interpretation of user intent."""
    
    action: str = Field(description="search/filter/navigate/aggregate/report")
    resource_type: Optional[str] = None
    filters: Optional[dict[str, Any]] = None
    aggregations: Optional[list[str]] = None
    sort: Optional[dict[str, str]] = None
    confidence: float = Field(ge=0, le=1)


class NaturalLanguageResponse(BaseModel):
    """Response to natural language query."""
    
    query_id: UUID
    original_query: str
    interpreted_intent: ParsedIntent
    
    result_count: Optional[int] = None
    results: Optional[list[dict[str, Any]]] = None
    
    summary: Optional[str] = None
    follow_up_suggestions: list[str] = []
    
    executed_at: datetime
    latency_ms: int


class QueryFeedback(BaseModel):
    """User feedback on query result."""
    
    was_helpful: bool
    feedback_text: Optional[str] = Field(default=None, max_length=500)
    correct_interpretation: Optional[dict[str, Any]] = None


class QueryHistoryItem(BaseModel):
    """Item from user's query history."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    query_text: str
    executed_action: Optional[str] = None
    result_count: Optional[int] = None
    was_helpful: Optional[bool] = None
    timestamp: datetime


# =============================================================================
# Document Extraction Schemas
# =============================================================================

class DocumentExtractionRequest(BaseModel):
    """Request to extract data from document."""
    
    document_id: UUID
    extraction_type: Optional[str] = Field(
        default=None,
        description="Type of extraction: policy_application/claim_form/etc."
    )
    fields_to_extract: Optional[list[str]] = Field(
        default=None,
        description="Specific fields to extract"
    )


class ExtractedField(BaseModel):
    """Single extracted field from document."""
    
    field_name: str
    value: Any
    confidence: float = Field(ge=0, le=1)
    location: Optional[dict[str, int]] = Field(
        default=None,
        description="Bounding box in document"
    )
    needs_review: bool = False


class DocumentExtractionResult(BaseModel):
    """Result of document extraction."""
    
    document_id: UUID
    extraction_type: Optional[str] = None
    
    extracted_text: Optional[str] = None
    extracted_fields: list[ExtractedField] = []
    
    overall_confidence: float = Field(ge=0, le=1)
    processing_time_ms: int
    
    warnings: list[str] = []
    errors: list[str] = []


# =============================================================================
# Anomaly Detection Schemas
# =============================================================================

class AnomalyAlert(BaseModel):
    """Anomaly detection alert."""
    
    id: UUID
    resource_type: str
    resource_id: UUID
    resource_name: Optional[str] = None
    
    anomaly_type: str
    anomaly_score: float = Field(ge=0, le=1)
    severity: str = Field(pattern="^(low|medium|high|critical)$")
    
    reasons: list[str]
    details: dict[str, Any]
    
    detected_at: datetime
    reviewed: bool = False
    reviewed_by_id: Optional[UUID] = None
    review_notes: Optional[str] = None
    false_positive: Optional[bool] = None


class AnomalyAlertFilter(BaseModel):
    """Filter for anomaly alerts."""
    
    resource_type: Optional[str] = None
    anomaly_type: Optional[str] = None
    severity: Optional[str] = None
    severity_in: Optional[list[str]] = None
    reviewed: Optional[bool] = None
    false_positive: Optional[bool] = None
    
    detected_after: Optional[datetime] = None
    detected_before: Optional[datetime] = None
    
    score_min: Optional[float] = Field(default=None, ge=0, le=1)


class AnomalyReview(BaseModel):
    """Review submission for anomaly alert."""
    
    false_positive: bool
    review_notes: Optional[str] = Field(default=None, max_length=1000)


# =============================================================================
# Narrative Generation Schemas
# =============================================================================

class NarrativeRequest(BaseModel):
    """Request to generate narrative."""
    
    resource_type: str = Field(
        pattern="^(calculation_run|scenario_result|report|experience_analysis)$"
    )
    resource_id: UUID
    style: str = Field(
        default="executive",
        pattern="^(executive|technical|detailed)$"
    )
    max_length: Optional[int] = Field(default=None, ge=100, le=5000)
    focus_areas: Optional[list[str]] = None


class NarrativeResponse(BaseModel):
    """Generated narrative response."""
    
    resource_type: str
    resource_id: UUID
    
    narrative: str
    key_findings: list[str]
    recommendations: list[str]
    
    generated_at: datetime
    generation_time_ms: int


# =============================================================================
# Semantic Search Schemas
# =============================================================================

class SemanticSearchRequest(BaseModel):
    """Semantic search request."""
    
    query: str = Field(min_length=1, max_length=500)
    resource_types: Optional[list[str]] = Field(
        default=None,
        description="Limit search to specific resource types"
    )
    limit: int = Field(default=10, ge=1, le=100)
    min_score: float = Field(default=0.5, ge=0, le=1)


class SemanticSearchResult(BaseModel):
    """Single semantic search result."""
    
    resource_type: str
    resource_id: UUID
    title: str
    snippet: str
    score: float = Field(ge=0, le=1)
    metadata: Optional[dict[str, Any]] = None


class SemanticSearchResponse(BaseModel):
    """Semantic search response."""
    
    query: str
    results: list[SemanticSearchResult]
    total_found: int
    search_time_ms: int
