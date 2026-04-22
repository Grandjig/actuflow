"""
Policyholder Model
==================

Policy owner/insured person information.
"""

import uuid
from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, SoftDeleteMixin, AuditMixin

if TYPE_CHECKING:
    from app.models.policy import Policy
    from app.models.user import User


class Policyholder(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """
    Policyholder/insured person.
    
    Contains personal information and contact details.
    One policyholder can have multiple policies.
    """
    
    __tablename__ = "policyholder"
    
    # External reference
    external_id: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
        index=True,
        doc="External system identifier",
    )
    
    # Personal information
    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    
    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    
    middle_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    
    date_of_birth: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        index=True,
    )
    
    gender: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        doc="Male/Female/Other",
    )
    
    # Underwriting factors
    smoker_status: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        doc="Smoker/Non-smoker/Unknown",
    )
    
    occupation_class: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        doc="Occupational risk class",
    )
    
    # Identification
    national_id: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        doc="National ID/SSN",
    )
    
    passport_number: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    
    # Contact information
    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )
    
    phone: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    
    mobile_phone: Mapped[Optional[str]] = mapped_column(
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
    
    # Relationships
    policies: Mapped[list["Policy"]] = relationship(
        "Policy",
        back_populates="policyholder",
        lazy="dynamic",
    )
    
    def __repr__(self) -> str:
        return f"<Policyholder(id={self.id}, name={self.full_name})>"
    
    @property
    def full_name(self) -> str:
        """Full name of policyholder."""
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        return " ".join(parts)
    
    @property
    def age(self) -> Optional[int]:
        """Current age of policyholder."""
        if not self.date_of_birth:
            return None
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
