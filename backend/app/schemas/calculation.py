"""
Calculation Schemas
===================

Pydantic schemas for calculation-related operations.
"""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class CalculationRunCreate(BaseModel):
    """Schema for creating a calculation run."""
    run_name: str = Field(..., min_length=1, max_length=255)
    model_definition_id: UUID
    assumption_set_id: UUID
    policy_filter: Optional[dict[str, Any]] = None
    parameters: Optional[dict[str, Any]] = None


class CalculationRunResponse(BaseModel):
    """Schema for calculation run response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    run_name: str
    model_definition_id: UUID
    model_name: Optional[str] = None
    assumption_set_id: UUID
    assumption_set_name: Optional[str] = None
    status: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    triggered_by_id: UUID
    trigger_type: str
    policy_filter: Optional[dict[str, Any]] = None
    parameters: Optional[dict[str, Any]] = None
    policies_count: Optional[int] = None
    error_message: Optional[str] = None
    result_summary: Optional[dict[str, Any]] = None
    ai_narrative: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class CalculationRunListItem(BaseModel):
    """Schema for calculation run list item."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    run_name: str
    model_name: Optional[str] = None
    status: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    policies_count: Optional[int] = None
    trigger_type: str


class CalculationProgress(BaseModel):
    """Schema for calculation progress."""
    status: str
    progress_percent: int
    progress_message: str
    policies_processed: int
    policies_total: int
    started_at: Optional[datetime] = None
    estimated_completion: Optional[datetime] = None


class CalculationResultResponse(BaseModel):
    """Schema for calculation result."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    calculation_run_id: UUID
    policy_id: UUID
    projection_month: int
    result_type: str
    values: dict[str, Any]
    anomaly_flag: bool = False
    created_at: datetime


class CalculationResultFilter(BaseModel):
    """Schema for filtering calculation results."""
    policy_id: Optional[UUID] = None
    result_type: Optional[str] = None
    projection_month: Optional[int] = None
    anomaly_only: bool = False


class CalculationSummary(BaseModel):
    """Schema for calculation summary."""
    total_policies: int
    total_reserves: float
    total_premiums: float
    by_product_type: dict[str, dict[str, float]]
    by_status: dict[str, int]
    anomaly_count: int


class CalculationNarrative(BaseModel):
    """Schema for AI-generated calculation narrative."""
    narrative: str
    generated_at: datetime
    key_points: list[str]
    confidence: float


class ModelDefinitionBase(BaseModel):
    """Base model definition schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    model_type: str
    line_of_business: str
    regulatory_standard: Optional[str] = None


class ModelDefinitionCreate(ModelDefinitionBase):
    """Schema for creating a model definition."""
    configuration: dict[str, Any]
    version: str = "1.0.0"


class ModelDefinitionUpdate(BaseModel):
    """Schema for updating a model definition."""
    name: Optional[str] = None
    description: Optional[str] = None
    configuration: Optional[dict[str, Any]] = None
    status: Optional[str] = None


class ModelDefinitionResponse(ModelDefinitionBase):
    """Schema for model definition response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    configuration: dict[str, Any]
    version: str
    status: str
    is_system_model: bool
    created_by_id: UUID
    created_at: datetime
    updated_at: datetime
