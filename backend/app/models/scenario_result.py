"""
Scenario Result Model
=====================

Results from scenario analyses.
"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.scenario import Scenario
    from app.models.calculation_run import CalculationRun


class ScenarioResult(Base, TimestampMixin):
    """Scenario result model."""

    __tablename__ = "scenario_results"

    scenario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scenarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    calculation_run_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("calculation_runs.id", ondelete="SET NULL"),
        nullable=True,
    )

    result_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    values: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    comparison_to_base: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        doc="Difference from base scenario",
    )

    # Relationships
    scenario: Mapped["Scenario"] = relationship("Scenario")
    calculation_run: Mapped[Optional["CalculationRun"]] = relationship("CalculationRun")

    def __repr__(self) -> str:
        return f"<ScenarioResult(id={self.id}, scenario={self.scenario_id})>"
