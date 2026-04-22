"""
Calculation Run Model
=====================

Records of calculation executions.
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.model_definition import ModelDefinition
    from app.models.assumption_set import AssumptionSet
    from app.models.calculation_result import CalculationResult


class CalculationRun(Base, TimestampMixin):
    """Calculation run model."""

    __tablename__ = "calculation_runs"

    # Run info
    run_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    # Model and assumptions
    model_definition_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("model_definitions.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    assumption_set_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("assumption_sets.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # Status
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="queued",
        index=True,
        doc="queued/running/completed/failed/cancelled",
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

    duration_seconds: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    # Trigger info
    triggered_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    trigger_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="manual",
        doc="manual/scheduled/automated",
    )

    # Parameters
    policy_filter: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        doc="Filter criteria for policies included in this run",
    )

    parameters: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        doc="Run parameters: valuation_date, reporting_basis, etc.",
    )

    # Results
    policies_count: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    result_summary: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        doc="High-level result totals",
    )

    # AI narrative
    ai_narrative: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="AI-generated executive summary",
    )

    # Relationships
    triggered_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[triggered_by_id],
    )

    model_definition: Mapped["ModelDefinition"] = relationship(
        "ModelDefinition",
    )

    assumption_set: Mapped["AssumptionSet"] = relationship(
        "AssumptionSet",
    )

    results: Mapped[list["CalculationResult"]] = relationship(
        "CalculationResult",
        back_populates="calculation_run",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<CalculationRun(id={self.id}, name={self.run_name}, status={self.status})>"
