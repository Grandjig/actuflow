"""
Notification Model
==================

User notifications.
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class Notification(Base):
    """
    User notification.
    
    Notifications can be in-app, email, or both.
    """
    
    __tablename__ = "notification"
    
    # Recipient
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Notification type
    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="task_assigned/calculation_complete/approval_required/system/etc.",
    )
    
    # Content
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    
    # Priority
    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="normal",
        doc="low/normal/high",
    )
    
    # Status
    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )
    
    read_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Related resource
    resource_type: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    
    resource_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    
    # Action URL (where to navigate when clicked)
    action_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )
    
    # Additional data
    data: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )
    
    # Email sent?
    email_sent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    
    email_sent_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="notifications",
    )
    
    def __repr__(self) -> str:
        return f"<Notification(id={self.id}, type={self.type}, user={self.user_id})>"
