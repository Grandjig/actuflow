"""
Report Template Model
=====================

Report template definitions.
"""

from typing import Optional

from sqlalchemy import Boolean, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ReportTemplate(Base, TimestampMixin):
    """Report template model."""

    __tablename__ = "report_templates"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    report_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="reserve_summary/cashflow/regulatory/experience/custom",
    )

    regulatory_standard: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        doc="IFRS17/SolvencyII/USGAAP/LDTI",
    )

    template_config: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        doc="Report layout and content configuration",
    )

    output_format: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PDF",
        doc="PDF/Excel/CSV",
    )

    is_system_template: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    include_ai_narrative: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<ReportTemplate(id={self.id}, name={self.name})>"
