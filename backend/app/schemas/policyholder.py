"""Policyholder Schemas."""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr, ConfigDict


class PolicyholderCreate(BaseModel):
    """Schema for creating a policyholder."""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    gender: str
    smoker_status: Optional[str] = "unknown"
    occupation: Optional[str] = None
    occupation_class: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    external_id: Optional[str] = None


class PolicyholderUpdate(BaseModel):
    """Schema for updating a policyholder."""
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    smoker_status: Optional[str] = None
    occupation: Optional[str] = None
    occupation_class: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None


class PolicyholderResponse(BaseModel):
    """Schema for policyholder response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    external_id: Optional[str] = None
    first_name: str
    last_name: str
    full_name: Optional[str] = None
    date_of_birth: date
    gender: str
    smoker_status: Optional[str] = None
    occupation: Optional[str] = None
    occupation_class: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class PolicyholderListResponse(BaseModel):
    """Paginated policyholder list response."""
    items: list[PolicyholderResponse]
    total: int
    page: int
    page_size: int
    pages: int
