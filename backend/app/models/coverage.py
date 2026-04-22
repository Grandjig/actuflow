"""
Coverage Model
==============

Policy coverage/benefit details.
"""

import uuid
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.policy import Policy


class Coverage(Base, TimestampMixin):
    """Policy coverage model."""

    __tablename__ = "coverages"

    # Policy reference
    policy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("policies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Coverage details
    coverage_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    coverage_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Financial
    benefit_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    premium_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )

    # Dates
    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    end_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    # Flags
    is_rider: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Additional data
    coverage_data: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Relationships
    policy: Mapped["Policy"] = relationship(
        "Policy",
        back_populates="coverages",
    )

    def __repr__(self) -> str:
        return f"<Coverage(id={self.id}, type={self.coverage_type}, policy={self.policy_id})>"
