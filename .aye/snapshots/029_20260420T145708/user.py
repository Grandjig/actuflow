"""
User Model
==========

User account and authentication.
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.role import Role
    from app.models.task import Task


class User(Base, TimestampMixin, SoftDeleteMixin):
    """User account model."""

    __tablename__ = "users"

    # Basic info
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    hashed_password: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    # Profile
    department: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    job_title: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    # Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Role
    role_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # External auth
    keycloak_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
    )

    # Activity
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Preferences (JSONB)
    ai_preferences: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    ui_preferences: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    notification_preferences: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Relationships
    role: Mapped[Optional["Role"]] = relationship(
        "Role",
        back_populates="users",
        lazy="joined",
    )

    assigned_tasks: Mapped[list["Task"]] = relationship(
        "Task",
        foreign_keys="Task.assigned_to_id",
        back_populates="assigned_to",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"

    def has_permission(self, resource: str, action: str) -> bool:
        """Check if user has a specific permission."""
        if self.is_superuser:
            return True

        if not self.role or not self.role.permissions:
            return False

        for permission in self.role.permissions:
            if permission.resource == resource and permission.action == action:
                return True
            # Admin permission grants all actions on resource
            if permission.resource == resource and permission.action == "admin":
                return True

        return False
