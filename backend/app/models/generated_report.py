"""
Generated Report Model
======================

Generated report records.
"""

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.report_template import ReportTemplate


class GeneratedReport(Base, TimestampMixin):
    """Generated report model."""

    __tablename__ = "generated_reports"

    report_template_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("report_templates.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    reporting_period_start: Mapped[date] = mapped_column(Date, nullable=False)
    reporting_period_end: Mapped[date] = mapped_column(Date, nullable=False)

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="queued",
        index=True,
        doc="queued/generating/completed/failed",
    )

    generated_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    generated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    file_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    parameters: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    ai_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    report_template: Mapped["ReportTemplate"] = relationship("ReportTemplate")
    generated_by: Mapped[Optional["User"]] = relationship("User")

    def __repr__(self) -> str:
        return f"<GeneratedReport(id={self.id}, name={self.name}, status={self.status})>"
