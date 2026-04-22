"""
Policy Model
============

Insurance policy data.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.policyholder import Policyholder
    from app.models.coverage import Coverage
    from app.models.claim import Claim


class Policy(Base, TimestampMixin, SoftDeleteMixin):
    """Insurance policy model."""

    __tablename__ = "policies"

    # Policy identifiers
    policy_number: Mapped[str] = mapped_column(
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

    # Product info
    product_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="life/health/property/casualty",
    )

    product_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    product_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    # Status
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="active",
        index=True,
        doc="active/lapsed/surrendered/matured/claimed/cancelled",
    )

    # Policyholder
    policyholder_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("policyholders.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # Dates
    issue_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    effective_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    maturity_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    termination_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    # Financial
    sum_assured: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    premium_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    premium_frequency: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="monthly",
        doc="monthly/quarterly/semi-annual/annual/single",
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="USD",
    )

    # Underwriting
    underwriting_class: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    risk_class: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    # Organization
    branch_code: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        index=True,
    )

    channel: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    agent_code: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    # Additional data
    policy_data: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Relationships
    policyholder: Mapped["Policyholder"] = relationship(
        "Policyholder",
        back_populates="policies",
    )

    coverages: Mapped[list["Coverage"]] = relationship(
        "Coverage",
        back_populates="policy",
        cascade="all, delete-orphan",
    )

    claims: Mapped[list["Claim"]] = relationship(
        "Claim",
        back_populates="policy",
    )

    def __repr__(self) -> str:
        return f"<Policy(id={self.id}, number={self.policy_number}, status={self.status})>"
