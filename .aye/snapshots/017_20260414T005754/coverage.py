"""
Coverage Model
==============

Coverage/benefit details attached to policies.
"""

import uuid
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.policy import Policy


class Coverage(Base, TimestampMixin):
    """
    Coverage/benefit under a policy.
    
    A policy can have multiple coverages (base + riders).
    """
    
    __tablename__ = "coverage"
    
    # Policy relationship
    policy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("policy.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Coverage identification
    coverage_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )
    
    coverage_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="death/accidental_death/disability/critical_illness/etc.",
    )
    
    coverage_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    # Is this a rider or base coverage?
    is_rider: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    
    # Status
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="active",
        doc="active/terminated/expired",
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
    
    # Financial
    benefit_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )
    
    premium_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Premium allocated to this coverage",
    )
    
    # Waiting period (in days)
    waiting_period_days: Mapped[Optional[int]] = mapped_column(
        nullable=True,
    )
    
    # Benefit period (in months, for disability etc.)
    benefit_period_months: Mapped[Optional[int]] = mapped_column(
        nullable=True,
    )
    
    # Additional data
    coverage_data: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        default=dict,
        doc="Additional coverage-specific attributes",
    )
    
    # Relationships
    policy: Mapped["Policy"] = relationship(
        "Policy",
        back_populates="coverages",
    )
    
    def __repr__(self) -> str:
        return f"<Coverage(id={self.id}, type={self.coverage_type})>"
    
    @property
    def is_active(self) -> bool:
        """Check if coverage is currently active."""
        if self.status != "active":
            return False
        today = date.today()
        if self.start_date > today:
            return False
        if self.end_date and self.end_date < today:
            return False
        return True
