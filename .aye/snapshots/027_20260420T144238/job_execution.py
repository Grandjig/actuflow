"""
Job Execution Model
===================

Records of scheduled job executions.
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.scheduled_job import ScheduledJob


class JobExecution(Base):
    """Job execution record."""

    __tablename__ = "job_executions"

    # Parent job
    scheduled_job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scheduled_jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Timing
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Status
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="running",
        index=True,
        doc="running/completed/failed",
    )

    # Results
    result_summary: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Related resources created
    created_resource_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    created_resource_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    # Relationships
    scheduled_job: Mapped["ScheduledJob"] = relationship(
        "ScheduledJob",
        back_populates="executions",
    )

    def __repr__(self) -> str:
        return f"<JobExecution(id={self.id}, job={self.scheduled_job_id}, status={self.status})>"
