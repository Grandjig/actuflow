"""
Policyholder Schemas
====================

Schemas for policyholder management endpoints.
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class PolicyholderBase(BaseModel):
    """Base policyholder fields."""
    
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    middle_name: Optional[str] = Field(default=None, max_length=100)
    
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(default=None, pattern="^(male|female|other)$")
    
    smoker_status: Optional[str] = Field(
        default=None,
        pattern="^(smoker|non-smoker|unknown)$"
    )
    occupation_class: Optional[str] = Field(default=None, max_length=50)
    
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=50)
    mobile_phone: Optional[str] = Field(default=None, max_length=50)
    
    address_line1: Optional[str] = Field(default=None, max_length=255)
    address_line2: Optional[str] = Field(default=None, max_length=255)
    city: Optional[str] = Field(default=None, max_length=100)
    state: Optional[str] = Field(default=None, max_length=100)
    postal_code: Optional[str] = Field(default=None, max_length=20)
    country: Optional[str] = Field(default="USA", max_length=100)


class PolicyholderCreate(PolicyholderBase):
    """Schema for creating a policyholder."""
    
    external_id: Optional[str] = Field(default=None, max_length=100)
    national_id: Optional[str] = Field(default=None, max_length=50)
    passport_number: Optional[str] = Field(default=None, max_length=50)


class PolicyholderUpdate(BaseModel):
    """Schema for updating a policyholder."""
    
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    middle_name: Optional[str] = Field(default=None, max_length=100)
    
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(default=None, pattern="^(male|female|other)$")
    smoker_status: Optional[str] = None
    occupation_class: Optional[str] = None
    
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    mobile_phone: Optional[str] = None
    
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None


class PolicyholderResponse(PolicyholderBase):
    """Schema for policyholder response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    external_id: Optional[str] = None
    national_id: Optional[str] = None
    
    created_at: datetime
    updated_at: datetime
    
    # Computed
    full_name: Optional[str] = None
    age: Optional[int] = None


class PolicyholderListItem(BaseModel):
    """Simplified policyholder for list views."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    external_id: Optional[str] = None
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    policy_count: int = 0


class PolicyholderWithPolicies(PolicyholderResponse):
    """Policyholder with related policies."""
    
    policies: list["PolicyListItem"] = []
    total_sum_assured: Optional[float] = None
    total_premium: Optional[float] = None


class PolicyholderFilter(BaseModel):
    """Filter parameters for policyholder list."""
    
    external_id: Optional[str] = None
    name: Optional[str] = Field(default=None, description="Search first/last name")
    email: Optional[str] = None
    
    date_of_birth_from: Optional[date] = None
    date_of_birth_to: Optional[date] = None
    
    gender: Optional[str] = None
    smoker_status: Optional[str] = None
    
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    
    search: Optional[str] = Field(default=None, description="Full-text search")


# Forward reference
from app.schemas.policy import PolicyListItem

PolicyholderWithPolicies.model_rebuild()
