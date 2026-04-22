"""
Experience Analysis Model
=========================

Experience study results and AI recommendations.
"""

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.user import User


class ExperienceAnalysis(Base, TimestampMixin, SoftDeleteMixin):
    """
    Experience analysis study results.
    
    Compares actual experience to assumptions and generates recommendations.
    """
    
    __tablename__ = "experience_analysis"
    
    # Study identification
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Analysis type
    analysis_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="mortality/lapse/morbidity/expense",
    )
    
    # Study period
    study_period_start: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    
    study_period_end: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    
    # Status
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="running",
        index=True,
        doc="running/completed/failed",
    )
    
    # Parameters
    parameters: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        doc="Study configuration (segments, filters, etc.)",
    )
    
    # Results
    results: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        doc="Actual vs Expected results by segment",
    )
    
    # Summary statistics
    summary_stats: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )
    
    # AI recommendations
    ai_recommendations: Mapped[Optional[list]] = mapped_column(
        JSONB,
        nullable=True,
        doc="AI-suggested assumption updates",
    )
    
    # Reference assumption set
    reference_assumption_set_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("assumption_set.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # Timing
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Error
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Creator
    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # Relationships
    created_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[created_by_id],
    )
    
    def __repr__(self) -> str:
        return f"<ExperienceAnalysis(id={self.id}, type={self.analysis_type}, status={self.status})>"
