"""
Policy Schemas
==============

Schemas for policy management endpoints.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PolicyBase(BaseModel):
    """Base policy fields."""
    
    policy_number: str = Field(min_length=1, max_length=50)
    product_type: str = Field(pattern="^(life|health|property|casualty)$")
    product_code: str = Field(max_length=50)
    product_name: Optional[str] = Field(default=None, max_length=255)
    
    policyholder_id: UUID
    
    issue_date: date
    effective_date: date
    maturity_date: Optional[date] = None
    expiry_date: Optional[date] = None
    policy_term: Optional[int] = Field(default=None, ge=1, description="Term in months")
    
    sum_assured: Decimal = Field(ge=0, decimal_places=2)
    premium_amount: Decimal = Field(ge=0, decimal_places=2)
    premium_frequency: str = Field(
        default="annual",
        pattern="^(annual|semi-annual|quarterly|monthly|single)$"
    )
    currency: str = Field(default="USD", max_length=3)
    
    risk_class: Optional[str] = Field(default=None, max_length=50)
    branch_code: Optional[str] = Field(default=None, max_length=50)
    agent_code: Optional[str] = Field(default=None, max_length=50)
    channel: Optional[str] = Field(
        default=None,
        pattern="^(direct|agent|broker|bancassurance)$"
    )


class PolicyCreate(PolicyBase):
    """Schema for creating a policy."""
    
    status: str = Field(default="active")
    underwriter_id: Optional[UUID] = None
    policy_data: Optional[dict[str, Any]] = None


class PolicyUpdate(BaseModel):
    """Schema for updating a policy."""
    
    product_name: Optional[str] = Field(default=None, max_length=255)
    status: Optional[str] = None
    status_reason: Optional[str] = Field(default=None, max_length=255)
    
    maturity_date: Optional[date] = None
    expiry_date: Optional[date] = None
    termination_date: Optional[date] = None
    
    premium_amount: Optional[Decimal] = Field(default=None, ge=0)
    premium_due_date: Optional[date] = None
    
    risk_class: Optional[str] = Field(default=None, max_length=50)
    underwriter_id: Optional[UUID] = None
    policy_data: Optional[dict[str, Any]] = None


class PolicyStatusUpdate(BaseModel):
    """Schema for updating policy status."""
    
    status: str = Field(pattern="^(active|lapsed|surrendered|matured|claimed|cancelled)$")
    status_reason: Optional[str] = Field(default=None, max_length=255)
    effective_date: Optional[date] = Field(default=None, description="Status change effective date")


class PolicyResponse(PolicyBase):
    """Schema for policy response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    status: str
    status_reason: Optional[str] = None
    status_date: Optional[date] = None
    termination_date: Optional[date] = None
    premium_due_date: Optional[date] = None
    annualized_premium: Optional[Decimal] = None
    underwriter_id: Optional[UUID] = None
    policy_data: Optional[dict[str, Any]] = None
    
    created_at: datetime
    updated_at: datetime
    created_by_id: Optional[UUID] = None
    
    # Computed properties
    is_active: Optional[bool] = None


class PolicyListItem(BaseModel):
    """Simplified policy for list views."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    policy_number: str
    product_type: str
    product_code: str
    status: str
    policyholder_name: Optional[str] = None
    issue_date: date
    sum_assured: Decimal
    premium_amount: Decimal
    currency: str


class PolicyWithDetails(PolicyResponse):
    """Policy with related data."""
    
    policyholder: Optional["PolicyholderResponse"] = None
    coverages: list["CoverageResponse"] = []
    active_claims_count: int = 0


class PolicyFilter(BaseModel):
    """Filter parameters for policy list."""
    
    policy_number: Optional[str] = None
    product_type: Optional[str] = None
    product_code: Optional[str] = None
    status: Optional[str] = None
    status_in: Optional[list[str]] = None
    policyholder_id: Optional[UUID] = None
    
    issue_date_from: Optional[date] = None
    issue_date_to: Optional[date] = None
    
    sum_assured_min: Optional[Decimal] = None
    sum_assured_max: Optional[Decimal] = None
    
    branch_code: Optional[str] = None
    agent_code: Optional[str] = None
    
    search: Optional[str] = Field(default=None, description="Search across multiple fields")


class PolicyBulkUpdate(BaseModel):
    """Schema for bulk policy updates."""
    
    ids: list[UUID]
    update: PolicyUpdate


class PolicySummaryStats(BaseModel):
    """Summary statistics for policies."""
    
    total_count: int
    active_count: int
    lapsed_count: int
    total_sum_assured: Decimal
    total_annualized_premium: Decimal
    by_product_type: dict[str, int]
    by_status: dict[str, int]


# Forward reference imports
from app.schemas.policyholder import PolicyholderResponse
from app.schemas.coverage import CoverageResponse

PolicyWithDetails.model_rebuild()
