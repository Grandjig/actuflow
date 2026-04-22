"""Policy Schemas."""

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, Field


class PolicyBase(BaseModel):
    """Base policy schema."""
    policy_number: str = Field(..., max_length=50)
    product_type: str = Field(..., max_length=50)
    product_code: str = Field(..., max_length=50)
    product_name: Optional[str] = Field(None, max_length=255)
    status: str = Field(default="active", max_length=50)
    issue_date: date
    effective_date: date
    maturity_date: Optional[date] = None
    termination_date: Optional[date] = None
    sum_assured: Decimal = Field(..., ge=0)
    premium_amount: Decimal = Field(..., ge=0)
    premium_frequency: str = Field(..., max_length=20)
    currency: str = Field(default="USD", max_length=3)
    risk_class: Optional[str] = Field(None, max_length=50)
    branch_code: Optional[str] = Field(None, max_length=50)
    term_years: Optional[int] = None


class PolicyCreate(PolicyBase):
    """Schema for creating a policy."""
    policyholder_id: uuid.UUID


class PolicyUpdate(BaseModel):
    """Schema for updating a policy."""
    policy_number: Optional[str] = Field(None, max_length=50)
    product_type: Optional[str] = Field(None, max_length=50)
    product_code: Optional[str] = Field(None, max_length=50)
    product_name: Optional[str] = Field(None, max_length=255)
    status: Optional[str] = Field(None, max_length=50)
    issue_date: Optional[date] = None
    effective_date: Optional[date] = None
    maturity_date: Optional[date] = None
    termination_date: Optional[date] = None
    sum_assured: Optional[Decimal] = Field(None, ge=0)
    premium_amount: Optional[Decimal] = Field(None, ge=0)
    premium_frequency: Optional[str] = Field(None, max_length=20)
    currency: Optional[str] = Field(None, max_length=3)
    risk_class: Optional[str] = Field(None, max_length=50)
    branch_code: Optional[str] = Field(None, max_length=50)
    term_years: Optional[int] = None


class PolicyholderSummary(BaseModel):
    """Summary of policyholder for embedding in policy."""
    id: uuid.UUID
    first_name: str
    last_name: str
    full_name: str
    date_of_birth: Optional[date] = None

    class Config:
        from_attributes = True


class PolicyResponse(PolicyBase):
    """Schema for policy response."""
    id: uuid.UUID
    policyholder_id: uuid.UUID
    policyholder: Optional[PolicyholderSummary] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PolicyListItem(BaseModel):
    """Schema for policy list item (lighter than full response)."""
    id: uuid.UUID
    policy_number: str
    product_type: str
    product_code: str
    product_name: Optional[str] = None
    status: str
    policyholder_id: uuid.UUID
    policyholder_name: Optional[str] = None
    issue_date: date
    maturity_date: Optional[date] = None
    sum_assured: Decimal
    premium_amount: Decimal
    premium_frequency: str
    currency: str
    created_at: datetime

    class Config:
        from_attributes = True


class PolicyFilter(BaseModel):
    """Schema for policy filtering."""
    status: Optional[str] = None
    product_type: Optional[str] = None
    product_code: Optional[str] = None
    policyholder_id: Optional[uuid.UUID] = None
    issue_date_from: Optional[date] = None
    issue_date_to: Optional[date] = None
    sum_assured_min: Optional[Decimal] = None
    sum_assured_max: Optional[Decimal] = None
    search: Optional[str] = None


class PolicyBulkUpdate(BaseModel):
    """Schema for bulk policy update."""
    policy_ids: List[uuid.UUID]
    status: Optional[str] = None
    branch_code: Optional[str] = None


class PolicySummaryStats(BaseModel):
    """Policy summary statistics."""
    total_policies: int
    active_policies: int
    total_sum_assured: Decimal
    total_premium: Decimal
    by_product_type: dict
    by_status: dict
