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
    from app.models.model_definition import ModelDefinition
    from app.models.assumption_set import AssumptionSet
    from app.models.calculation_result import CalculationResult
    from app.models.user import User
    from app.models.scenario_result import ScenarioResult


class CalculationRun(Base, TimestampMixin):
    """
    A single execution of an actuarial calculation.
    
    Tracks status, progress, and results of calculation runs.
    """
    
    __tablename__ = "calculation_run"
    
    # Run identification
    run_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    
    run_number: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        doc="Auto-incrementing run number for this model",
    )
    
    # Model and assumptions
    model_definition_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("model_definition.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    
    assumption_set_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("assumption_set.id", ondelete="RESTRICT"),
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
    
    progress_percent: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    
    progress_message: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    
    # Timing
    queued_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    
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
    
    # Trigger information
    triggered_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    trigger_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="manual",
        doc="manual/scheduled/automated/rerun",
    )
    
    # Celery task tracking
    celery_task_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )
    
    # Policy scope
    policy_filter: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        doc="Filter criteria for policies included in run",
    )
    
    policies_total: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    
    policies_processed: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    
    policies_failed: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    
    # Run parameters
    parameters: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        doc="Run parameters (valuation date, reporting basis, etc.)",
    )
    
    # Results
    result_summary: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        doc="Summary statistics of results",
    )
    
    # AI narrative
    ai_narrative: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="AI-generated executive summary of results",
    )
    
    # Error tracking
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    error_details: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )
    
    # Relationships
    model_definition: Mapped["ModelDefinition"] = relationship(
        "ModelDefinition",
        back_populates="calculation_runs",
    )
    
    assumption_set: Mapped["AssumptionSet"] = relationship(
        "AssumptionSet",
        back_populates="calculation_runs",
    )
    
    triggered_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[triggered_by_id],
    )
    
    results: Mapped[list["CalculationResult"]] = relationship(
        "CalculationResult",
        back_populates="calculation_run",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    
    scenario_results: Mapped[list["ScenarioResult"]] = relationship(
        "ScenarioResult",
        back_populates="calculation_run",
        lazy="dynamic",
    )
    
    def __repr__(self) -> str:
        return f"<CalculationRun(id={self.id}, name={self.run_name}, status={self.status})>"
    
    @property
    def is_running(self) -> bool:
        """Is this run currently in progress?"""
        return self.status in ("queued", "running")
    
    @property
    def is_complete(self) -> bool:
        """Has this run finished (successfully or not)?"""
        return self.status in ("completed", "failed", "cancelled")
