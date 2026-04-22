"""
Report Template Model
=====================

Templates for generating reports.
"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, SoftDeleteMixin, AuditMixin

if TYPE_CHECKING:
    from app.models.generated_report import GeneratedReport


class ReportTemplate(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """
    Report template configuration.
    
    Defines what data to include and how to format reports.
    """
    
    __tablename__ = "report_template"
    
    # Identification
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Type
    report_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="regulatory/internal/adhoc",
    )
    
    # Regulatory standard (if applicable)
    regulatory_standard: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        doc="IFRS17/SolvencyII/USGAAP/LDTI",
    )
    
    # Output configuration
    output_format: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PDF",
        doc="PDF/Excel/CSV",
    )
    
    # Template configuration
    template_config: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        doc="Report structure and content configuration",
    )
    
    # AI features
    include_ai_narrative: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    
    ai_narrative_config: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )
    
    # System template (cannot be deleted)
    is_system_template: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    
    # Relationships
    generated_reports: Mapped[list["GeneratedReport"]] = relationship(
        "GeneratedReport",
        back_populates="template",
        lazy="dynamic",
    )
    
    def __repr__(self) -> str:
        return f"<ReportTemplate(id={self.id}, name={self.name})>"
