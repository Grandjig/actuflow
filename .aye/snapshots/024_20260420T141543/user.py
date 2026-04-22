"""
User Schemas
============

Pydantic schemas for user-related operations.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    department: Optional[str] = None
    job_title: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str = Field(..., min_length=8)
    role_id: Optional[UUID] = None
    is_active: bool = True
    is_superuser: bool = False


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    department: Optional[str] = None
    job_title: Optional[str] = None
    role_id: Optional[UUID] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8)


class UserResponse(UserBase):
    """Schema for user response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    role_id: Optional[UUID] = None
    role: Optional["RoleResponse"] = None
    is_active: bool
    is_superuser: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class UserListItem(BaseModel):
    """Schema for user list item."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    full_name: str
    department: Optional[str] = None
    role_name: Optional[str] = None
    is_active: bool
    last_login: Optional[datetime] = None


class PermissionResponse(BaseModel):
    """Schema for permission response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    resource: str
    action: str
    description: Optional[str] = None


class RoleBase(BaseModel):
    """Base role schema."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class RoleCreate(RoleBase):
    """Schema for creating a role."""
    permission_ids: list[UUID] = []


class RoleUpdate(BaseModel):
    """Schema for updating a role."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    permission_ids: Optional[list[UUID]] = None


class RoleResponse(RoleBase):
    """Schema for role response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    is_system: bool
    permissions: list[PermissionResponse] = []
    created_at: datetime
    updated_at: datetime


# Update forward reference
UserResponse.model_rebuild()
