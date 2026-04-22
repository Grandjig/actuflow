"""
Notification Model
==================

User notifications.
"""

import uuid
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Notification(Base, TimestampMixin):
    """User notification model."""

    __tablename__ = "notifications"

    # Target user
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Notification content
    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="info/warning/error/success/task/approval",
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Status
    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )

    # Related resource
    resource_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    resource_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    # Action URL (optional)
    action_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    def __repr__(self) -> str:
        return f"<Notification(id={self.id}, user={self.user_id}, type={self.type})>"
