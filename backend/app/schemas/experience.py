"""
Experience Analysis Schemas
===========================

Schemas for experience studies and analysis.
"""

from datetime import date, datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ExperienceAnalysisCreate(BaseModel):
    """Schema for creating an experience analysis."""
    
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    analysis_type: str = Field(
        pattern="^(mortality|lapse|morbidity|expense)$"
    )
    study_period_start: date
    study_period_end: date
    
    parameters: dict[str, Any] = Field(
        description="Study configuration (segments, filters, etc.)"
    )
    reference_assumption_set_id: Optional[UUID] = None


class ExperienceAnalysisResponse(BaseModel):
    """Schema for experience analysis response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    description: Optional[str] = None
    analysis_type: str
    
    study_period_start: date
    study_period_end: date
    
    status: str
    parameters: dict[str, Any]
    
    results: Optional[dict[str, Any]] = None
    summary_stats: Optional[dict[str, Any]] = None
    ai_recommendations: Optional[list[dict[str, Any]]] = None
    
    reference_assumption_set_id: Optional[UUID] = None
    
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    created_at: datetime
    updated_at: datetime
    created_by_id: Optional[UUID] = None


class ExperienceAnalysisListItem(BaseModel):
    """Simplified experience analysis for list views."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    analysis_type: str
    study_period_start: date
    study_period_end: date
    status: str
    created_at: datetime


class ExperienceStudyResult(BaseModel):
    """Individual result from experience study."""
    
    segment: str
    segment_values: dict[str, Any]
    
    exposure: float
    actual_count: int
    expected_count: float
    
    actual_rate: float
    expected_rate: float
    ae_ratio: float = Field(description="Actual/Expected ratio")
    
    credibility: float = Field(ge=0, le=1)
    confidence_interval: Optional[dict[str, float]] = None


class AssumptionRecommendation(BaseModel):
    """AI-generated assumption recommendation."""
    
    assumption_type: str
    segment: str
    segment_values: dict[str, Any]
    
    current_rate: float
    suggested_rate: float
    actual_rate: float
    
    credibility: float = Field(ge=0, le=1)
    confidence: str = Field(pattern="^(low|medium|high)$")
    
    data_points: int
    exposure: float
    
    impact_estimate: dict[str, Any] = Field(
        description="Estimated impact on reserves/calculations"
    )
    reasoning: str
    
    accepted: Optional[bool] = None
    accepted_by_id: Optional[UUID] = None
    acceptance_notes: Optional[str] = None
