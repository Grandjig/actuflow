"""
Policy Schemas
==============

Pydantic schemas for policy-related operations.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class PolicyholderBrief(BaseModel):
    """Brief policyholder info for policy responses."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    full_name: str
    date_of_birth: date


class CoverageBase(BaseModel):
    """Base coverage schema."""
    coverage_type: str
    coverage_name: str
    benefit_amount: Decimal
    premium_amount: Decimal = Decimal("0")
    start_date: date
    end_date: Optional[date] = None
    is_rider: bool = False


class CoverageCreate(CoverageBase):
    """Schema for creating a coverage."""
    pass


class CoverageResponse(CoverageBase):
    """Schema for coverage response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    policy_id: UUID


class PolicyBase(BaseModel):
    """Base policy schema."""
    policy_number: str = Field(..., min_length=1, max_length=50)
    product_type: str
    product_code: str
    product_name: Optional[str] = None
    status: str = "active"
    issue_date: date
    effective_date: date
    maturity_date: Optional[date] = None
    sum_assured: Decimal = Field(..., gt=0)
    premium_amount: Decimal = Field(..., ge=0)
    premium_frequency: str = "monthly"
    currency: str = "USD"
    branch_code: Optional[str] = None
    channel: Optional[str] = None
    agent_code: Optional[str] = None


class PolicyCreate(PolicyBase):
    """Schema for creating a policy."""
    policyholder_id: UUID
    external_id: Optional[str] = None
    underwriting_class: Optional[str] = None
    risk_class: Optional[str] = None
    policy_data: Optional[dict[str, Any]] = None
    coverages: list[CoverageCreate] = []


class PolicyUpdate(BaseModel):
    """Schema for updating a policy."""
    product_name: Optional[str] = None
    status: Optional[str] = None
    maturity_date: Optional[date] = None
    termination_date: Optional[date] = None
    premium_amount: Optional[Decimal] = None
    premium_frequency: Optional[str] = None
    branch_code: Optional[str] = None
    channel: Optional[str] = None
    agent_code: Optional[str] = None
    policy_data: Optional[dict[str, Any]] = None


class PolicyResponse(PolicyBase):
    """Schema for policy response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    policyholder_id: UUID
    policyholder: Optional[PolicyholderBrief] = None
    external_id: Optional[str] = None
    termination_date: Optional[date] = None
    underwriting_class: Optional[str] = None
    risk_class: Optional[str] = None
    coverages: list[CoverageResponse] = []
    created_at: datetime
    updated_at: datetime


class PolicyListItem(BaseModel):
    """Schema for policy list item."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    policy_number: str
    product_type: str
    product_code: str
    product_name: Optional[str] = None
    status: str
    policyholder_id: UUID
    policyholder_name: Optional[str] = None
    issue_date: date
    sum_assured: Decimal
    premium_amount: Decimal
    premium_frequency: str
    currency: str


class PolicyFilter(BaseModel):
    """Schema for policy filtering."""
    status: Optional[str] = None
    product_type: Optional[str] = None
    product_code: Optional[str] = None
    policyholder_id: Optional[UUID] = None
    issue_date_from: Optional[date] = None
    issue_date_to: Optional[date] = None
    search: Optional[str] = None


class PolicyStats(BaseModel):
    """Policy statistics."""
    total_policies: int
    active_policies: int
    total_sum_assured: Decimal
    total_premium: Decimal
    by_status: dict[str, int]
    by_product_type: dict[str, int]
