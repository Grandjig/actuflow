"""
User Schemas
============

Schemas for user management endpoints.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Base user fields."""
    
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)
    department: Optional[str] = Field(default=None, max_length=100)
    job_title: Optional[str] = Field(default=None, max_length=100)


class UserCreate(UserBase):
    """Schema for creating a user."""
    
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)
    role_id: Optional[UUID] = None
    is_active: bool = True


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    department: Optional[str] = Field(default=None, max_length=100)
    job_title: Optional[str] = Field(default=None, max_length=100)
    role_id: Optional[UUID] = None
    is_active: Optional[bool] = None


class UserPasswordChange(BaseModel):
    """Schema for changing password."""
    
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)


class UserResponse(UserBase):
    """Schema for user response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    is_active: bool
    is_superuser: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    role: Optional["RoleResponse"] = None


class UserListItem(BaseModel):
    """Simplified user for list views."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    email: str
    full_name: str
    department: Optional[str] = None
    is_active: bool
    role_name: Optional[str] = None


class UserProfile(UserResponse):
    """Extended user profile with preferences."""
    
    ai_preferences: Optional[dict] = None
    ui_preferences: Optional[dict] = None
    notification_preferences: Optional[dict] = None


class UserPreferencesUpdate(BaseModel):
    """Schema for updating user preferences."""
    
    ai_preferences: Optional[dict] = None
    ui_preferences: Optional[dict] = None
    notification_preferences: Optional[dict] = None


# Role schemas
class RoleBase(BaseModel):
    """Base role fields."""
    
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None


class RoleCreate(RoleBase):
    """Schema for creating a role."""
    
    permission_ids: Optional[list[UUID]] = None


class RoleUpdate(BaseModel):
    """Schema for updating a role."""
    
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = None
    permission_ids: Optional[list[UUID]] = None


class RoleResponse(RoleBase):
    """Schema for role response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    is_system: bool
    permissions: list["PermissionResponse"] = []


class PermissionResponse(BaseModel):
    """Schema for permission response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    resource: str
    action: str
    description: Optional[str] = None


# Update forward references
UserResponse.model_rebuild()
RoleResponse.model_rebuild()
