"""
Calculation Schemas
===================

Schemas for calculation runs and results.
"""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# =============================================================================
# Calculation Run Schemas
# =============================================================================

class CalculationRunCreate(BaseModel):
    """Schema for creating a calculation run."""
    
    run_name: str = Field(min_length=1, max_length=255)
    model_definition_id: UUID
    assumption_set_id: UUID
    
    policy_filter: Optional[dict[str, Any]] = Field(
        default=None,
        description="Filter criteria for policies to include"
    )
    parameters: Optional[dict[str, Any]] = Field(
        default=None,
        description="Run parameters (valuation date, etc.)"
    )


class CalculationRunResponse(BaseModel):
    """Schema for calculation run response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    run_name: str
    run_number: Optional[int] = None
    
    model_definition_id: UUID
    assumption_set_id: UUID
    
    status: str
    progress_percent: int
    progress_message: Optional[str] = None
    
    queued_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    
    triggered_by_id: Optional[UUID] = None
    trigger_type: str
    celery_task_id: Optional[str] = None
    
    policy_filter: Optional[dict[str, Any]] = None
    policies_total: Optional[int] = None
    policies_processed: int
    policies_failed: int
    
    parameters: Optional[dict[str, Any]] = None
    result_summary: Optional[dict[str, Any]] = None
    
    ai_narrative: Optional[str] = None
    
    error_message: Optional[str] = None
    error_details: Optional[dict[str, Any]] = None
    
    created_at: datetime
    updated_at: datetime
    
    # Computed
    is_running: Optional[bool] = None
    is_complete: Optional[bool] = None


class CalculationRunListItem(BaseModel):
    """Simplified calculation run for list views."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    run_name: str
    run_number: Optional[int] = None
    model_name: Optional[str] = None
    assumption_set_name: Optional[str] = None
    status: str
    progress_percent: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    policies_total: Optional[int] = None
    triggered_by_name: Optional[str] = None


class CalculationRunProgress(BaseModel):
    """Real-time progress update."""
    
    run_id: UUID
    status: str
    progress_percent: int
    progress_message: Optional[str] = None
    policies_processed: int
    policies_total: Optional[int] = None
    estimated_completion: Optional[datetime] = None


class CalculationRunFilter(BaseModel):
    """Filter parameters for calculation run list."""
    
    model_definition_id: Optional[UUID] = None
    assumption_set_id: Optional[UUID] = None
    status: Optional[str] = None
    status_in: Optional[list[str]] = None
    trigger_type: Optional[str] = None
    triggered_by_id: Optional[UUID] = None
    
    started_after: Optional[datetime] = None
    started_before: Optional[datetime] = None
    
    search: Optional[str] = None


# =============================================================================
# Calculation Result Schemas
# =============================================================================

class CalculationResultResponse(BaseModel):
    """Schema for calculation result."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    calculation_run_id: UUID
    policy_id: UUID
    projection_month: int
    result_type: str
    values: dict[str, Any]
    
    anomaly_flag: bool
    anomaly_score: Optional[float] = None
    anomaly_reasons: Optional[list[str]] = None
    
    created_at: datetime


class CalculationResultFilter(BaseModel):
    """Filter parameters for calculation results."""
    
    policy_id: Optional[UUID] = None
    policy_ids: Optional[list[UUID]] = None
    result_type: Optional[str] = None
    projection_month_from: Optional[int] = None
    projection_month_to: Optional[int] = None
    anomaly_flagged: Optional[bool] = None


class CalculationResultSummary(BaseModel):
    """Aggregated result summary."""
    
    result_type: str
    total_value: float
    average_value: float
    min_value: float
    max_value: float
    count: int
    anomaly_count: int


class CalculationNarrative(BaseModel):
    """AI-generated narrative for calculation run."""
    
    run_id: UUID
    narrative: str
    generated_at: datetime
    key_findings: list[str]
    recommendations: list[str]


# =============================================================================
# Comparison Schemas
# =============================================================================

class CalculationComparisonRequest(BaseModel):
    """Request to compare calculation runs."""
    
    base_run_id: UUID
    comparison_run_id: UUID
    result_types: Optional[list[str]] = None


class CalculationComparisonResponse(BaseModel):
    """Comparison between calculation runs."""
    
    base_run: CalculationRunListItem
    comparison_run: CalculationRunListItem
    
    differences: dict[str, Any]
    impact_summary: dict[str, Any]
    
    ai_narrative: Optional[str] = None
