"""
Policyholder Schemas
====================

Pydantic schemas for policyholder-related operations.
"""

from datetime import date, datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class PolicyholderBase(BaseModel):
    """Base policyholder schema."""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    gender: str
    smoker_status: str = "non_smoker"
    occupation: Optional[str] = None
    occupation_class: Optional[str] = None


class PolicyholderCreate(PolicyholderBase):
    """Schema for creating a policyholder."""
    external_id: Optional[str] = None
    id_type: Optional[str] = None
    id_number: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: str = "USA"
    policyholder_data: Optional[dict[str, Any]] = None


class PolicyholderUpdate(BaseModel):
    """Schema for updating a policyholder."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    occupation: Optional[str] = None
    occupation_class: Optional[str] = None
    smoker_status: Optional[str] = None
    policyholder_data: Optional[dict[str, Any]] = None


class PolicyholderResponse(PolicyholderBase):
    """Schema for policyholder response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    external_id: Optional[str] = None
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class PolicyholderListItem(BaseModel):
    """Schema for policyholder list item."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    external_id: Optional[str] = None
    full_name: str
    date_of_birth: date
    gender: str
    email: Optional[str] = None
    policy_count: int = 0
