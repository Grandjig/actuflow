"""
Task Model
==========

Workflow tasks.
"""

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.user import User


class Task(Base, TimestampMixin, SoftDeleteMixin):
    """Workflow task model."""

    __tablename__ = "tasks"

    # Task info
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    task_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="review/approval/data_entry/followup/investigation",
    )

    # Status
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="todo",
        index=True,
        doc="todo/in_progress/completed/blocked",
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="medium",
        doc="urgent/high/medium/low",
    )

    # Assignment
    assigned_to_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    assigned_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Dates
    due_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        index=True,
    )

    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Related resource
    related_resource_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        doc="policy/claim/assumption_set/calculation_run/etc.",
    )

    related_resource_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    # Notes
    completion_notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Automation flag
    auto_generated: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        doc="Was this task created by automation?",
    )

    # Relationships
    assigned_to: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[assigned_to_id],
        back_populates="assigned_tasks",
    )

    assigned_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[assigned_by_id],
    )

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title={self.title}, status={self.status})>"

    @property
    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if self.due_date and self.status not in ["completed"]:
            return date.today() > self.due_date
        return False
