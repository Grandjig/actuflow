"""Role Schemas."""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class PermissionResponse(BaseModel):
    """Schema for permission response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    resource: str
    action: str
    description: Optional[str] = None


class RoleCreate(BaseModel):
    """Schema for creating a role."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    permission_ids: list[UUID] = []


class RoleUpdate(BaseModel):
    """Schema for updating a role."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = None
    permission_ids: Optional[list[UUID]] = None


class RoleResponse(BaseModel):
    """Schema for role response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    description: Optional[str] = None
    is_system: bool
    permissions: list[PermissionResponse] = []
