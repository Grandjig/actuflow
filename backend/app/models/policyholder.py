"""
Policyholder Model
==================

Insurance policyholder/customer data.
"""

import uuid
from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, Date, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.policy import Policy


class Policyholder(Base, TimestampMixin, SoftDeleteMixin):
    """Insurance policyholder model."""

    __tablename__ = "policyholders"

    # Identifiers
    external_id: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
        index=True,
    )

    # Personal info
    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    date_of_birth: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    gender: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        doc="male/female/other",
    )

    # Risk factors
    smoker_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="non_smoker",
        doc="smoker/non_smoker/ex_smoker/unknown",
    )

    occupation: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    occupation_class: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
    )

    # Identification
    id_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    id_number: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    # Contact
    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    phone: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    # Address
    address_line1: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    address_line2: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    city: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    state: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    postal_code: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
    )

    country: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        default="USA",
    )

    # Additional data
    policyholder_data: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Relationships
    policies: Mapped[list["Policy"]] = relationship(
        "Policy",
        back_populates="policyholder",
    )

    def __repr__(self) -> str:
        return f"<Policyholder(id={self.id}, name={self.first_name} {self.last_name})>"

    @property
    def full_name(self) -> str:
        """Get full name."""
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> int:
        """Calculate current age."""
        from datetime import date as d
        today = d.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
