"""
Notification Schemas
====================

Schemas for user notifications.
"""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class NotificationResponse(BaseModel):
    """Schema for notification response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    type: str
    title: str
    message: str
    priority: str
    
    is_read: bool
    read_at: Optional[datetime] = None
    
    resource_type: Optional[str] = None
    resource_id: Optional[UUID] = None
    action_url: Optional[str] = None
    
    data: Optional[dict[str, Any]] = None
    
    created_at: datetime


class NotificationListItem(BaseModel):
    """Simplified notification for list views."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    type: str
    title: str
    message: str
    priority: str
    is_read: bool
    created_at: datetime


class NotificationMarkRead(BaseModel):
    """Request to mark notifications as read."""
    
    notification_ids: list[UUID]


class NotificationPreferences(BaseModel):
    """User notification preferences."""
    
    email_enabled: bool = True
    email_types: list[str] = Field(
        default_factory=lambda: ["task_assigned", "approval_required", "calculation_complete"]
    )
    
    in_app_enabled: bool = True
    
    digest_frequency: Optional[str] = Field(
        default=None,
        pattern="^(immediate|daily|weekly)$"
    )


class NotificationCreate(BaseModel):
    """Schema for creating a notification (internal use)."""
    
    user_id: UUID
    type: str
    title: str
    message: str
    priority: str = "normal"
    resource_type: Optional[str] = None
    resource_id: Optional[UUID] = None
    action_url: Optional[str] = None
    data: Optional[dict[str, Any]] = None
    send_email: bool = False
