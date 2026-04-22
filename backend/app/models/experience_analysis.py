"""
Experience Analysis Model
=========================

Experience study results.
"""

import uuid
from datetime import date
from typing import TYPE_CHECKING, Optional
from enum import Enum

from sqlalchemy import Date, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.assumption_set import AssumptionSet


class AnalysisType(str, Enum):
    MORTALITY = "mortality"
    LAPSE = "lapse"
    MORBIDITY = "morbidity"
    EXPENSE = "expense"


class ExperienceAnalysis(Base, TimestampMixin):
    """Experience analysis model."""

    __tablename__ = "experience_analyses"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    analysis_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    study_period_start: Mapped[date] = mapped_column(Date, nullable=False)
    study_period_end: Mapped[date] = mapped_column(Date, nullable=False)

    parameters: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    # Results
    results: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    total_actual: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    total_expected: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ae_ratio: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # AI
    ai_recommendations: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    ai_narrative: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Related assumption set (if comparing)
    assumption_set_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("assumption_sets.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Creator
    created_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    created_by: Mapped[Optional["User"]] = relationship("User")
    assumption_set: Mapped[Optional["AssumptionSet"]] = relationship("AssumptionSet")

    def __repr__(self) -> str:
        return f"<ExperienceAnalysis(id={self.id}, name={self.name}, type={self.analysis_type})>"
