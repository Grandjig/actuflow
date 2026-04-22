"""Notification schemas."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class NotificationBase(BaseModel):
    type: str
    title: str
    message: str
    resource_type: Optional[str] = None
    resource_id: Optional[UUID] = None


class NotificationCreate(NotificationBase):
    user_id: UUID


class NotificationResponse(NotificationBase):
    id: UUID
    user_id: UUID
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
