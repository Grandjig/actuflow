"""User Model."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.role import Role
    from app.models.ai_query_log import AIQueryLog
    from app.models.task import Task
    from app.models.notification import Notification


class User(Base):
    """User model."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Authentication
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Profile
    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
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
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Role
    role_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="SET NULL"),
        nullable=True,
    )

    # SSO/External auth
    keycloak_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
    )

    # AI Preferences
    ai_preferences: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        default=dict,
    )

    # Timestamps
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationships
    role: Mapped[Optional["Role"]] = relationship(
        "Role",
        back_populates="users",
        lazy="joined",
    )
    
    ai_queries: Mapped[List["AIQueryLog"]] = relationship(
        "AIQueryLog",
        back_populates="user",
        foreign_keys="AIQueryLog.user_id",
    )
    
    assigned_tasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="assignee",
        foreign_keys="Task.assigned_to_id",
    )
    
    created_tasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="assigner",
        foreign_keys="Task.assigned_by_id",
    )
    
    notifications: Mapped[List["Notification"]] = relationship(
        "Notification",
        back_populates="user",
        foreign_keys="Notification.user_id",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
