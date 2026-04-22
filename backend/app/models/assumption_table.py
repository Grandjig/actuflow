"""
Assumption Table Model
======================

Individual assumption tables within a set.
"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.assumption_set import AssumptionSet


class AssumptionTable(Base, TimestampMixin):
    """Assumption table model."""

    __tablename__ = "assumption_tables"

    # Parent set
    assumption_set_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("assumption_sets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Table info
    table_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="mortality/lapse/expense/morbidity/discount_rate/inflation/commission",
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Table data (flexible JSONB structure)
    data: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        doc="Flexible structure for different table types",
    )

    # Metadata about the table structure
    metadata_info: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        doc="Table structure metadata: dimensions, interpolation method, etc.",
    )

    # Relationships
    assumption_set: Mapped["AssumptionSet"] = relationship(
        "AssumptionSet",
        back_populates="tables",
    )

    def __repr__(self) -> str:
        return f"<AssumptionTable(id={self.id}, type={self.table_type}, name={self.name})>"
