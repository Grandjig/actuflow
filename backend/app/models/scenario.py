"""
Scenario Model
==============

What-if scenario definitions.
"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.assumption_set import AssumptionSet


class Scenario(Base, TimestampMixin, SoftDeleteMixin):
    """Scenario model."""

    __tablename__ = "scenarios"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    scenario_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="deterministic/stochastic/stress_test/sensitivity",
    )

    base_assumption_set_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("assumption_sets.id", ondelete="RESTRICT"),
        nullable=False,
    )

    adjustments: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        doc="Adjustments to apply to base assumptions",
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="draft",
        doc="draft/active/archived",
    )

    created_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    created_by: Mapped[Optional["User"]] = relationship("User")
    base_assumption_set: Mapped["AssumptionSet"] = relationship("AssumptionSet")

    def __repr__(self) -> str:
        return f"<Scenario(id={self.id}, name={self.name})>"
