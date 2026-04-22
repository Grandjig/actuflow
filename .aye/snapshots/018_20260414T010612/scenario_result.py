"""
Scenario Result Model
=====================

Results of scenario runs.
"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.scenario import Scenario
    from app.models.calculation_run import CalculationRun


class ScenarioResult(Base, TimestampMixin):
    """
    Result of running a scenario.
    
    Links a scenario to its calculation run and stores impact analysis.
    """
    
    __tablename__ = "scenario_result"
    
    # Scenario
    scenario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scenario.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Calculation run with scenario applied
    calculation_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("calculation_run.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Base run for comparison
    base_run_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("calculation_run.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # Impact summary
    impact_summary: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        doc="Summary of scenario impact vs base",
    )
    
    # AI narrative
    ai_narrative: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Relationships
    scenario: Mapped["Scenario"] = relationship(
        "Scenario",
        back_populates="results",
    )
    
    calculation_run: Mapped["CalculationRun"] = relationship(
        "CalculationRun",
        foreign_keys=[calculation_run_id],
        back_populates="scenario_results",
    )
    
    base_run: Mapped[Optional["CalculationRun"]] = relationship(
        "CalculationRun",
        foreign_keys=[base_run_id],
    )
    
    def __repr__(self) -> str:
        return f"<ScenarioResult(scenario={self.scenario_id}, run={self.calculation_run_id})>"
