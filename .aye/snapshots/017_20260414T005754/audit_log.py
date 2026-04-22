"""
Audit Log Model
===============

Immutable audit trail for compliance.
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import INET, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class AuditLog(Base):
    """
    Immutable audit log entry.
    
    This table is append-only - no updates or deletes are ever performed.
    Consider table partitioning by timestamp for performance.
    """
    
    __tablename__ = "audit_log"
    
    # Timestamp
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )
    
    # Who
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    
    user_email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Denormalized for queries when user is deleted",
    )
    
    # What action
    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="create/read/update/delete/approve/reject/login/logout/export/etc.",
    )
    
    # What resource
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
        doc="Human-readable resource identifier",
    )
    
    # Change details
    old_values: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        doc="Values before change",
    )
    
    new_values: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        doc="Values after change",
    )
    
    # Additional context
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Request context
    ip_address: Mapped[Optional[str]] = mapped_column(
        INET,
        nullable=True,
    )
    
    user_agent: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    request_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        index=True,
        doc="Correlation ID for request tracing",
    )
    
    # Relationships (optional, for joins)
    user: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[user_id],
    )
    
    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, action={self.action}, resource={self.resource_type}/{self.resource_id})>"
