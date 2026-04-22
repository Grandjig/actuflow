"""
Model Definition Model
======================

Actuarial model definitions.
"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.user import User


class ModelDefinition(Base, TimestampMixin, SoftDeleteMixin):
    """Actuarial model definition."""

    __tablename__ = "model_definitions"

    # Basic info
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Model classification
    model_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="reserving/pricing/cashflow/valuation/profit_testing",
    )

    line_of_business: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    regulatory_standard: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        doc="IFRS17/SolvencyII/USGAAP/LDTI",
    )

    # Model configuration (calculation graph)
    configuration: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        doc="Model configuration including calculation graph definition",
    )

    # Version
    version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="1.0.0",
    )

    # Status
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="draft",
        doc="draft/active/deprecated",
    )

    # Flags
    is_system_model: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        doc="System models cannot be deleted",
    )

    # Creator
    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    created_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[created_by_id],
    )

    def __repr__(self) -> str:
        return f"<ModelDefinition(id={self.id}, name={self.name}, type={self.model_type})>"
