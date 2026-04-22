"""
User Model
==========

User accounts and authentication.
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
    from app.models.notification import Notification


class User(Base, TimestampMixin, SoftDeleteMixin):
    """
    User account model.
    
    Supports both local authentication and Keycloak SSO.
    """
    
    __tablename__ = "user"
    
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
    
    # Password hash (only for local auth, null if using Keycloak)
    password_hash: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    
    # Role
    role_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("role.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    
    # Organization info
    department: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    job_title: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    
    # Account status
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
    
    # Authentication tracking
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    failed_login_attempts: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )
    locked_until: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # External identity (Keycloak)
    keycloak_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
        index=True,
    )
    
    # User preferences
    ai_preferences: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        default=dict,
        doc="User's AI feature preferences and settings",
    )
    
    ui_preferences: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        default=dict,
        doc="UI preferences (theme, default views, etc.)",
    )
    
    notification_preferences: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        default=dict,
        doc="Notification delivery preferences",
    )
    
    # Avatar/profile image URL
    avatar_url: Mapped[Optional[str]] = mapped_column(
        String(500),
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
        lazy="dynamic",
    )
    
    notifications: Mapped[list["Notification"]] = relationship(
        "Notification",
        back_populates="user",
        lazy="dynamic",
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
    
    @property
    def display_name(self) -> str:
        """User's display name."""
        return self.full_name or self.email.split("@")[0]
    
    @property
    def is_locked(self) -> bool:
        """Check if account is currently locked."""
        if self.locked_until is None:
            return False
        return datetime.utcnow() < self.locked_until
    
    def has_permission(self, resource: str, action: str) -> bool:
        """Check if user has a specific permission."""
        if self.is_superuser:
            return True
        if not self.role:
            return False
        return any(
            p.resource == resource and p.action == action
            for p in self.role.permissions
        )
