"""
Scenario Schemas
================

Schemas for scenario management and stress testing.
"""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ScenarioBase(BaseModel):
    """Base scenario fields."""
    
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    scenario_type: str = Field(
        default="deterministic",
        pattern="^(deterministic|stochastic)$"
    )
    category: Optional[str] = Field(
        default=None,
        pattern="^(interest_rate|mortality|lapse|expense|combined)$"
    )


class ScenarioCreate(ScenarioBase):
    """Schema for creating a scenario."""
    
    base_assumption_set_id: Optional[UUID] = None
    base_model_id: Optional[UUID] = None
    adjustments: dict[str, Any] = Field(
        description="Scenario adjustments to apply"
    )
    is_regulatory: bool = False
    regulatory_reference: Optional[str] = Field(default=None, max_length=100)


class ScenarioUpdate(BaseModel):
    """Schema for updating a scenario."""
    
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = Field(
        default=None,
        pattern="^(draft|active|archived)$"
    )
    adjustments: Optional[dict[str, Any]] = None


class ScenarioResponse(ScenarioBase):
    """Schema for scenario response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    base_assumption_set_id: Optional[UUID] = None
    base_model_id: Optional[UUID] = None
    adjustments: dict[str, Any]
    status: str
    is_regulatory: bool
    regulatory_reference: Optional[str] = None
    
    created_at: datetime
    updated_at: datetime
    created_by_id: Optional[UUID] = None


class ScenarioListItem(BaseModel):
    """Simplified scenario for list views."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    scenario_type: str
    category: Optional[str] = None
    status: str
    is_regulatory: bool
    run_count: int = 0


class ScenarioAdjustment(BaseModel):
    """Individual scenario adjustment."""
    
    assumption_type: str
    adjustment_type: str = Field(pattern="^(absolute|relative|replace)$")
    value: float
    segments: Optional[dict[str, Any]] = Field(
        default=None,
        description="Segments to apply adjustment to"
    )


class ScenarioRunRequest(BaseModel):
    """Request to run a scenario."""
    
    base_calculation_run_id: Optional[UUID] = Field(
        default=None,
        description="Base run to compare against"
    )
    policy_filter: Optional[dict[str, Any]] = None
    parameters: Optional[dict[str, Any]] = None


class ScenarioResultResponse(BaseModel):
    """Schema for scenario result."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    scenario_id: UUID
    calculation_run_id: UUID
    base_run_id: Optional[UUID] = None
    
    impact_summary: dict[str, Any]
    ai_narrative: Optional[str] = None
    
    created_at: datetime


class ScenarioComparison(BaseModel):
    """Comparison of multiple scenarios."""
    
    base_run: dict[str, Any]
    scenarios: list[dict[str, Any]]
    comparison_matrix: dict[str, Any]
    ai_narrative: Optional[str] = None
