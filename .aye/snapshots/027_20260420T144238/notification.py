"""Notification Schemas."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class NotificationResponse(BaseModel):
    """Schema for notification response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    type: str
    title: str
    message: str
    is_read: bool
    resource_type: Optional[str] = None
    resource_id: Optional[UUID] = None
    created_at: datetime


class NotificationListResponse(BaseModel):
    """Paginated notification list response."""
    items: list[NotificationResponse]
    total: int
    page: int
    page_size: int


class UnreadCountResponse(BaseModel):
    """Unread count response."""
    count: int
