"""
Assumption Schemas
==================

Pydantic schemas for assumption-related operations.
"""

from datetime import date, datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class AssumptionTableBase(BaseModel):
    """Base assumption table schema."""
    table_type: str
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class AssumptionTableCreate(AssumptionTableBase):
    """Schema for creating an assumption table."""
    data: dict[str, Any]
    metadata: Optional[dict[str, Any]] = None


class AssumptionTableUpdate(BaseModel):
    """Schema for updating an assumption table."""
    name: Optional[str] = None
    description: Optional[str] = None
    data: Optional[dict[str, Any]] = None
    metadata: Optional[dict[str, Any]] = None


class AssumptionTableResponse(AssumptionTableBase):
    """Schema for assumption table response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    assumption_set_id: UUID
    data: dict[str, Any]
    metadata: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime


class AssumptionSetBase(BaseModel):
    """Base assumption set schema."""
    name: str = Field(..., min_length=1, max_length=255)
    version: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    effective_date: date


class AssumptionSetCreate(AssumptionSetBase):
    """Schema for creating an assumption set."""
    expiry_date: Optional[date] = None
    line_of_business: Optional[str] = None


class AssumptionSetUpdate(BaseModel):
    """Schema for updating an assumption set."""
    name: Optional[str] = None
    description: Optional[str] = None
    effective_date: Optional[date] = None
    expiry_date: Optional[date] = None


class AssumptionSetResponse(AssumptionSetBase):
    """Schema for assumption set response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
    expiry_date: Optional[date] = None
    approved_by_id: Optional[UUID] = None
    approval_date: Optional[datetime] = None
    approval_notes: Optional[str] = None
    tables: list[AssumptionTableResponse] = []
    created_by_id: UUID
    created_at: datetime
    updated_at: datetime


class AssumptionSetListItem(BaseModel):
    """Schema for assumption set list item."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    version: str
    status: str
    effective_date: date
    table_count: int = 0
    created_by_name: Optional[str] = None
    created_at: datetime


class AssumptionApprovalRequest(BaseModel):
    """Schema for assumption approval request."""
    approval_notes: Optional[str] = None


class AssumptionRejectionRequest(BaseModel):
    """Schema for assumption rejection request."""
    rejection_reason: str


class AssumptionComparisonResult(BaseModel):
    """Schema for assumption comparison result."""
    table_type: str
    table_name: str
    differences: list[dict[str, Any]]


class ExperienceRecommendation(BaseModel):
    """AI-generated experience recommendation."""
    assumption_type: str
    segment: Optional[str] = None
    current_value: float
    recommended_value: float
    confidence: float
    sample_size: int
    rationale: str
