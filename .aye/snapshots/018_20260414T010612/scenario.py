"""
Scenario Model
==============

Scenario definitions for stress testing and what-if analysis.
"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, SoftDeleteMixin, AuditMixin

if TYPE_CHECKING:
    from app.models.assumption_set import AssumptionSet
    from app.models.model_definition import ModelDefinition
    from app.models.scenario_result import ScenarioResult
    from app.models.user import User


class Scenario(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """
    Scenario for stress testing and what-if analysis.
    
    Defines adjustments to apply to assumptions for scenario runs.
    """
    
    __tablename__ = "scenario"
    
    # Identification
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Type
    scenario_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="deterministic",
        doc="deterministic/stochastic",
    )
    
    # Category
    category: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        doc="interest_rate/mortality/lapse/expense/combined",
    )
    
    # Base configuration
    base_assumption_set_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("assumption_set.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    base_model_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("model_definition.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # Adjustments to apply
    adjustments: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        doc="Scenario adjustments to apply",
    )
    
    # Status
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="draft",
        doc="draft/active/archived",
    )
    
    # Is this a regulatory scenario?
    is_regulatory: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )
    
    regulatory_reference: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        doc="Regulatory reference (e.g., 'Solvency II SCR Interest Rate Down')",
    )
    
    # Relationships
    base_assumption_set: Mapped[Optional["AssumptionSet"]] = relationship(
        "AssumptionSet",
        foreign_keys=[base_assumption_set_id],
    )
    
    base_model: Mapped[Optional["ModelDefinition"]] = relationship(
        "ModelDefinition",
        foreign_keys=[base_model_id],
    )
    
    results: Mapped[list["ScenarioResult"]] = relationship(
        "ScenarioResult",
        back_populates="scenario",
        lazy="dynamic",
    )
    
    def __repr__(self) -> str:
        return f"<Scenario(id={self.id}, name={self.name})>"
