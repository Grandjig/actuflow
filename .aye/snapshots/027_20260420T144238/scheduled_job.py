"""
Scheduled Job Model
===================

Scheduled automation jobs.
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.job_execution import JobExecution


class ScheduledJob(Base, TimestampMixin, SoftDeleteMixin):
    """Scheduled automation job."""

    __tablename__ = "scheduled_jobs"

    # Job info
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Job type
    job_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="calculation/report/import/data_check/cleanup",
    )

    # Schedule
    cron_expression: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    timezone: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="UTC",
    )

    # Configuration
    config: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    # Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
    )

    # Execution tracking
    last_run_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    last_run_status: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    next_run_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
    )

    # Failure handling
    max_retries: Mapped[int] = mapped_column(
        Integer,
        default=3,
        nullable=False,
    )

    retry_delay_minutes: Mapped[int] = mapped_column(
        Integer,
        default=5,
        nullable=False,
    )

    # Notifications
    notify_on_success: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    notify_on_failure: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    notification_emails: Mapped[Optional[list]] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Creator
    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    created_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[created_by_id],
    )

    executions: Mapped[list["JobExecution"]] = relationship(
        "JobExecution",
        back_populates="scheduled_job",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )

    def __repr__(self) -> str:
        return f"<ScheduledJob(id={self.id}, name={self.name}, type={self.job_type})>"
