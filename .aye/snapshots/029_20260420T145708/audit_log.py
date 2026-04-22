"""
Audit Log Model
===============

Immutable audit trail.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AuditLog(Base):
    """Audit log model - append only."""

    __tablename__ = "audit_logs"

    # Timestamp
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    # User who performed the action
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    user_email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    # Action details
    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="create/update/delete/approve/reject/login/logout/export",
    )

    resource_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    resource_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        index=True,
    )

    resource_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    # Change details
    old_values: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    new_values: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Context
    ip_address: Mapped[Optional[str]] = mapped_column(
        String(45),
        nullable=True,
    )

    user_agent: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    # Additional context
    metadata: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, action={self.action}, resource={self.resource_type})>"
