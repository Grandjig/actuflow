"""User Schemas."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class RoleSummary(BaseModel):
    """Embedded role summary."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    permissions: list[str] = []


class UserCreate(BaseModel):
    """Schema for creating a user."""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)
    role_id: Optional[UUID] = None
    department: Optional[str] = None
    job_title: Optional[str] = None
    is_active: Optional[bool] = True


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)
    role_id: Optional[UUID] = None
    department: Optional[str] = None
    job_title: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    """Schema for user response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    email: str
    full_name: str
    role: Optional[RoleSummary] = None
    department: Optional[str] = None
    job_title: Optional[str] = None
    is_active: bool
    is_superuser: bool = False
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class UserListResponse(BaseModel):
    """Paginated user list response."""
    items: list[UserResponse]
    total: int
    page: int
    page_size: int
    pages: int
