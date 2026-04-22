"""
Calculation Result Model
========================

Detailed calculation outputs.
"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.calculation_run import CalculationRun
    from app.models.policy import Policy


class CalculationResult(Base, TimestampMixin):
    """Calculation result model."""

    __tablename__ = "calculation_results"

    # Parent run
    calculation_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("calculation_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Policy
    policy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("policies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Projection
    projection_month: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    # Result classification
    result_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="reserve/cashflow/profit_margin/etc.",
    )

    # Result values
    values: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    # Anomaly flag
    anomaly_flag: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        doc="AI-detected unusual result",
    )

    anomaly_reason: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    # Relationships
    calculation_run: Mapped["CalculationRun"] = relationship(
        "CalculationRun",
        back_populates="results",
    )

    policy: Mapped["Policy"] = relationship(
        "Policy",
    )

    def __repr__(self) -> str:
        return f"<CalculationResult(id={self.id}, run={self.calculation_run_id}, policy={self.policy_id})>"
