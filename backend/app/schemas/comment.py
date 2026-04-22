"""
Comment Schemas
===============

Schemas for comments/notes on resources.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CommentBase(BaseModel):
    """Base comment fields."""
    
    content: str = Field(min_length=1, max_length=10000)


class CommentCreate(CommentBase):
    """Schema for creating a comment."""
    
    resource_type: str = Field(max_length=100)
    resource_id: UUID
    parent_id: Optional[UUID] = Field(
        default=None,
        description="Parent comment ID for replies"
    )
    mentions: Optional[list[UUID]] = Field(
        default=None,
        description="User IDs mentioned in comment"
    )


class CommentUpdate(BaseModel):
    """Schema for updating a comment."""
    
    content: Optional[str] = Field(default=None, min_length=1, max_length=10000)


class CommentResponse(CommentBase):
    """Schema for comment response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    resource_type: str
    resource_id: UUID
    user_id: UUID
    user_name: Optional[str] = None
    user_avatar: Optional[str] = None
    
    parent_id: Optional[UUID] = None
    
    is_resolved: bool
    resolved_by_id: Optional[UUID] = None
    
    mentions: Optional[list[UUID]] = None
    
    created_at: datetime
    updated_at: datetime
    
    # Nested replies
    replies: list["CommentResponse"] = []
    reply_count: int = 0


class CommentThread(BaseModel):
    """Thread of comments on a resource."""
    
    resource_type: str
    resource_id: UUID
    comments: list[CommentResponse]
    total_count: int


class CommentResolve(BaseModel):
    """Request to resolve/unresolve a comment."""
    
    resolved: bool


# Update forward reference
CommentResponse.model_rebuild()
