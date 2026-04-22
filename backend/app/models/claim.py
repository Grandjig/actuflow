"""
Claim Model
===========

Insurance claim data.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, DateTime, Float, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.policy import Policy
    from app.models.user import User


class Claim(Base, TimestampMixin, SoftDeleteMixin):
    """Insurance claim model."""

    __tablename__ = "claims"

    # Identifiers
    claim_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    external_id: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )

    # Policy reference
    policy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("policies.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # Dates
    claim_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    incident_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    notification_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    # Claim details
    claim_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="death/disability/hospitalization/accident/maturity/surrender",
    )

    claimed_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="submitted",
        index=True,
        doc="submitted/under_review/approved/denied/paid/closed",
    )

    # Settlement
    settlement_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    settlement_amount: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(18, 2),
        nullable=True,
    )

    # Adjuster
    adjuster_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    adjuster_notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Denial
    denial_reason: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # AI anomaly detection
    anomaly_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        doc="AI-generated anomaly/suspicion score (0-1)",
    )

    anomaly_reasons: Mapped[Optional[list]] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Additional data
    claim_data: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Relationships
    policy: Mapped["Policy"] = relationship(
        "Policy",
        back_populates="claims",
    )

    adjuster: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[adjuster_id],
    )

    def __repr__(self) -> str:
        return f"<Claim(id={self.id}, number={self.claim_number}, status={self.status})>"
