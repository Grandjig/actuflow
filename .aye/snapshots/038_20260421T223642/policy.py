"""Policy Schemas."""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class PolicyholderSummary(BaseModel):
    """Embedded policyholder summary."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    full_name: Optional[str] = None
    external_id: Optional[str] = None


class PolicyCreate(BaseModel):
    """Schema for creating a policy."""
    policy_number: str = Field(..., min_length=1, max_length=50)
    product_type: str
    product_code: str
    product_name: Optional[str] = None
    policyholder_id: UUID
    issue_date: date
    effective_date: date
    maturity_date: Optional[date] = None
    sum_assured: Decimal = Field(..., ge=0)
    premium_amount: Decimal = Field(..., ge=0)
    premium_frequency: str = "monthly"
    currency: str = "USD"
    risk_class: Optional[str] = None
    branch_code: Optional[str] = None
    status: str = "active"


class PolicyUpdate(BaseModel):
    """Schema for updating a policy."""
    product_name: Optional[str] = None
    maturity_date: Optional[date] = None
    termination_date: Optional[date] = None
    sum_assured: Optional[Decimal] = None
    premium_amount: Optional[Decimal] = None
    premium_frequency: Optional[str] = None
    status: Optional[str] = None
    risk_class: Optional[str] = None


class PolicyResponse(BaseModel):
    """Schema for policy response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    policy_number: str
    product_type: str
    product_code: str
    product_name: Optional[str] = None
    status: str
    policyholder_id: UUID
    policyholder: Optional[PolicyholderSummary] = None
    issue_date: date
    effective_date: date
    maturity_date: Optional[date] = None
    termination_date: Optional[date] = None
    sum_assured: Decimal
    premium_amount: Decimal
    premium_frequency: str
    currency: str
    risk_class: Optional[str] = None
    branch_code: Optional[str] = None
    term_years: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class PolicyListResponse(BaseModel):
    """Paginated policy list response."""
    items: list[PolicyResponse]
    total: int
    page: int
    page_size: int
    pages: int


class PolicyFilter(BaseModel):
    """Policy filter parameters."""
    search: Optional[str] = None
    status: Optional[str] = None
    product_type: Optional[str] = None
    product_code: Optional[str] = None
    policyholder_id: Optional[UUID] = None
    issue_date_from: Optional[str] = None
    issue_date_to: Optional[str] = None


class PolicyStats(BaseModel):
    """Policy statistics."""
    total_policies: int
    active_policies: int
    total_premium: float
    by_status: dict[str, int]
    by_product_type: dict[str, int]
