"""
Assumption Schemas
==================

Schemas for assumption sets and tables.
"""

from datetime import date, datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# =============================================================================
# Assumption Set Schemas
# =============================================================================

class AssumptionSetBase(BaseModel):
    """Base assumption set fields."""
    
    name: str = Field(min_length=1, max_length=255)
    version: str = Field(max_length=50)
    description: Optional[str] = None
    effective_date: Optional[date] = None
    expiry_date: Optional[date] = None


class AssumptionSetCreate(AssumptionSetBase):
    """Schema for creating an assumption set."""
    
    parent_id: Optional[UUID] = Field(
        default=None,
        description="Parent set ID if cloning"
    )


class AssumptionSetUpdate(BaseModel):
    """Schema for updating an assumption set."""
    
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    version: Optional[str] = Field(default=None, max_length=50)
    description: Optional[str] = None
    effective_date: Optional[date] = None
    expiry_date: Optional[date] = None


class AssumptionSetResponse(AssumptionSetBase):
    """Schema for assumption set response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    status: str
    
    submitted_at: Optional[datetime] = None
    submitted_by_id: Optional[UUID] = None
    approved_at: Optional[datetime] = None
    approved_by_id: Optional[UUID] = None
    approval_notes: Optional[str] = None
    rejection_notes: Optional[str] = None
    
    parent_id: Optional[UUID] = None
    
    created_at: datetime
    updated_at: datetime
    created_by_id: Optional[UUID] = None
    
    # Computed
    is_editable: Optional[bool] = None
    is_usable: Optional[bool] = None
    table_count: int = 0


class AssumptionSetListItem(BaseModel):
    """Simplified assumption set for list views."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    version: str
    status: str
    effective_date: Optional[date] = None
    created_at: datetime
    table_count: int = 0


class AssumptionSetWithTables(AssumptionSetResponse):
    """Assumption set with related tables."""
    
    tables: list["AssumptionTableResponse"] = []


# =============================================================================
# Assumption Table Schemas
# =============================================================================

class AssumptionTableBase(BaseModel):
    """Base assumption table fields."""
    
    table_type: str = Field(
        pattern="^(mortality|lapse|expense|morbidity|discount_rate|inflation|commission)$"
    )
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    source: Optional[str] = Field(default=None, max_length=255)


class AssumptionTableCreate(AssumptionTableBase):
    """Schema for creating an assumption table."""
    
    assumption_set_id: UUID
    data: dict[str, Any] = Field(description="Table data in JSON format")
    metadata_: Optional[dict[str, Any]] = Field(default=None, alias="metadata")


class AssumptionTableUpdate(BaseModel):
    """Schema for updating an assumption table."""
    
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    source: Optional[str] = None
    data: Optional[dict[str, Any]] = None
    metadata_: Optional[dict[str, Any]] = Field(default=None, alias="metadata")


class AssumptionTableResponse(AssumptionTableBase):
    """Schema for assumption table response."""
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
    id: UUID
    assumption_set_id: UUID
    data: dict[str, Any]
    metadata_: Optional[dict[str, Any]] = Field(default=None, alias="metadata")
    
    created_at: datetime
    updated_at: datetime


# =============================================================================
# Workflow Schemas
# =============================================================================

class AssumptionSubmitRequest(BaseModel):
    """Request to submit assumption set for approval."""
    
    notes: Optional[str] = Field(default=None, max_length=1000)


class AssumptionApprovalRequest(BaseModel):
    """Request to approve/reject assumption set."""
    
    action: str = Field(pattern="^(approve|reject)$")
    notes: Optional[str] = Field(default=None, max_length=1000)


class AssumptionComparison(BaseModel):
    """Comparison between two assumption sets."""
    
    set1_id: UUID
    set1_name: str
    set2_id: UUID
    set2_name: str
    
    differences: list[dict[str, Any]] = Field(
        description="List of differences between the sets"
    )
    summary: dict[str, Any]


# =============================================================================
# AI Recommendations
# =============================================================================

class ExperienceRecommendation(BaseModel):
    """AI-recommended assumption update."""
    
    assumption_type: str
    segment: str
    current_rate: float
    actual_rate: float
    suggested_rate: float
    credibility: float = Field(ge=0, le=1)
    confidence: str = Field(pattern="^(low|medium|high)$")
    data_points: int
    impact: dict[str, Any]
    reasoning: str


# Forward reference update
AssumptionSetWithTables.model_rebuild()
