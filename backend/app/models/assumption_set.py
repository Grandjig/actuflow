"""
Assumption Set Model
====================

Actuarial assumption sets for calculations.
"""

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.assumption_table import AssumptionTable


class AssumptionSet(Base, TimestampMixin, SoftDeleteMixin):
    """Assumption set model."""

    __tablename__ = "assumption_sets"

    # Basic info
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Status workflow
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="draft",
        index=True,
        doc="draft/pending_approval/approved/rejected/archived",
    )

    # Effective dates
    effective_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    expiry_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    # Line of business
    line_of_business: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )

    # Approval workflow
    approved_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    approval_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    approval_notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    rejection_reason: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Creator
    created_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    created_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[created_by_id],
    )

    approved_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[approved_by_id],
    )

    tables: Mapped[list["AssumptionTable"]] = relationship(
        "AssumptionTable",
        back_populates="assumption_set",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<AssumptionSet(id={self.id}, name={self.name}, version={self.version})>"
