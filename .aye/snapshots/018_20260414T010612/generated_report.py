"""
Generated Report Model
======================

Records of generated reports.
"""

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.report_template import ReportTemplate
    from app.models.user import User


class GeneratedReport(Base, TimestampMixin):
    """
    A generated report instance.
    
    Tracks report generation and stores output file reference.
    """
    
    __tablename__ = "generated_report"
    
    # Template
    report_template_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("report_template.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    
    # Report name
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    # Reporting period
    reporting_period_start: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )
    
    reporting_period_end: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )
    
    # Status
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="generating",
        index=True,
        doc="generating/completed/failed",
    )
    
    # Generation info
    generated_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    generated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Output file
    file_path: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        doc="S3/MinIO path to report file",
    )
    
    file_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    
    file_size: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        nullable=True,
    )
    
    output_format: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PDF",
    )
    
    # Parameters used
    parameters: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )
    
    # AI summary
    ai_summary: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Error info
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Relationships
    template: Mapped[Optional["ReportTemplate"]] = relationship(
        "ReportTemplate",
        back_populates="generated_reports",
    )
    
    generated_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[generated_by_id],
    )
    
    def __repr__(self) -> str:
        return f"<GeneratedReport(id={self.id}, name={self.name})>"
