"""Assumption Schemas."""

from datetime import date, datetime
from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class AssumptionSetCreate(BaseModel):
    """Schema for creating an assumption set."""
    name: str = Field(..., min_length=1, max_length=255)
    version: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    effective_date: Optional[date] = None
    line_of_business: Optional[str] = None


class AssumptionSetUpdate(BaseModel):
    """Schema for updating an assumption set."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    effective_date: Optional[date] = None


class AssumptionSetResponse(BaseModel):
    """Schema for assumption set response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    version: str
    description: Optional[str] = None
    status: str
    effective_date: Optional[date] = None
    line_of_business: Optional[str] = None
    approved_by_id: Optional[UUID] = None
    approval_date: Optional[datetime] = None
    approval_notes: Optional[str] = None
    rejection_reason: Optional[str] = None
    table_count: Optional[int] = None
    created_by_id: UUID
    created_at: datetime
    updated_at: datetime


class AssumptionSetListResponse(BaseModel):
    """Paginated assumption set list response."""
    items: list[AssumptionSetResponse]
    total: int
    page: int
    page_size: int
    pages: int


class AssumptionTableCreate(BaseModel):
    """Schema for creating an assumption table."""
    table_type: str
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    data: dict[str, Any]
    metadata: Optional[dict[str, Any]] = None


class AssumptionTableUpdate(BaseModel):
    """Schema for updating an assumption table."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    data: Optional[dict[str, Any]] = None
    metadata: Optional[dict[str, Any]] = None


class AssumptionTableResponse(BaseModel):
    """Schema for assumption table response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    assumption_set_id: UUID
    table_type: str
    name: str
    description: Optional[str] = None
    data: dict[str, Any]
    metadata: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime


class AssumptionApprovalRequest(BaseModel):
    """Schema for assumption approval/rejection."""
    approval_notes: Optional[str] = None
    rejection_reason: Optional[str] = None
