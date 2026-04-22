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
    """
    Detailed calculation result for a policy-month.
    
    This table can get very large - consider partitioning by calculation_run_id.
    """
    
    __tablename__ = "calculation_result"
    
    # Parent run
    calculation_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("calculation_run.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Policy
    policy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("policy.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Time dimension
    projection_month: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
        doc="Projection month (0 = valuation date)",
    )
    
    # Result type
    result_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="reserve/cashflow/profit_margin/bel/ra/csm/etc.",
    )
    
    # Result values - flexible structure
    values: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        doc="Result values (can include multiple metrics)",
    )
    
    # AI anomaly detection
    anomaly_flag: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        doc="Flagged as unusual by AI",
    )
    
    anomaly_score: Mapped[Optional[float]] = mapped_column(
        nullable=True,
    )
    
    anomaly_reasons: Mapped[Optional[list]] = mapped_column(
        JSONB,
        nullable=True,
    )
    
    # Relationships
    calculation_run: Mapped["CalculationRun"] = relationship(
        "CalculationRun",
        back_populates="results",
    )
    
    def __repr__(self) -> str:
        return f"<CalculationResult(run={self.calculation_run_id}, policy={self.policy_id}, month={self.projection_month})>"
