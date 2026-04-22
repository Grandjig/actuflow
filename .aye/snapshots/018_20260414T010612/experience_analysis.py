"""Experience Analysis Model."""

import uuid
from datetime import date
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class AnalysisType(str, Enum):
    """Experience analysis type."""
    MORTALITY = "mortality"
    LAPSE = "lapse"
    MORBIDITY = "morbidity"
    EXPENSE = "expense"


class ExperienceAnalysis(BaseModel):
    """Experience study results."""
    
    __tablename__ = "experience_analyses"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    analysis_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    
    study_period_start: Mapped[date] = mapped_column(Date, nullable=False)
    study_period_end: Mapped[date] = mapped_column(Date, nullable=False)
    
    parameters: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    
    # Results
    results: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    
    # Actual vs Expected summary
    total_actual: Mapped[float | None] = mapped_column(nullable=True)
    total_expected: Mapped[float | None] = mapped_column(nullable=True)
    ae_ratio: Mapped[float | None] = mapped_column(nullable=True)
    
    # AI recommendations
    ai_recommendations: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    ai_narrative: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    
    assumption_set_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assumption_sets.id", ondelete="SET NULL"), nullable=True
    )
    
    @property
    def ae_ratio_percent(self) -> float | None:
        return self.ae_ratio * 100 if self.ae_ratio else None
    
    def __repr__(self) -> str:
        return f"<ExperienceAnalysis({self.name}, {self.analysis_type})>"
