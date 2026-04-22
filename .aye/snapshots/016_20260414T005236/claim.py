"""
Claim Model
===========

Insurance claim records.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, DateTime, Float, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, SoftDeleteMixin, AuditMixin

if TYPE_CHECKING:
    from app.models.policy import Policy
    from app.models.user import User


class Claim(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """
    Insurance claim.
    
    Tracks claims from submission through settlement or denial.
    """
    
    __tablename__ = "claim"
    
    # Claim identification
    claim_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )
    
    external_claim_id: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
    )
    
    # Policy relationship
    policy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("policy.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    
    # Coverage (if applicable)
    coverage_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("coverage.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # Claim type and status
    claim_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc="death/disability/hospitalization/accident/etc.",
    )
    
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="open",
        index=True,
        doc="open/under_review/approved/denied/paid/closed",
    )
    
    # Key dates
    claim_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
        doc="Date claim was filed",
    )
    
    incident_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        doc="Date of the incident/loss",
    )
    
    notification_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        doc="Date insurer was notified",
    )
    
    # Financial
    claim_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Amount claimed",
    )
    
    assessed_amount: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(18, 2),
        nullable=True,
        doc="Amount assessed by adjuster",
    )
    
    settlement_amount: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(18, 2),
        nullable=True,
        doc="Final settlement amount",
    )
    
    settlement_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )
    
    payment_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )
    
    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="USD",
    )
    
    # Processing
    adjuster_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    adjuster_notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Denial (if applicable)
    denial_reason: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    denial_code: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    
    # Description
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # AI anomaly detection
    anomaly_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        doc="AI-generated anomaly score (0-1, higher = more suspicious)",
    )
    
    anomaly_reasons: Mapped[Optional[list]] = mapped_column(
        JSONB,
        nullable=True,
        doc="Reasons for anomaly flag",
    )
    
    # Additional data
    claim_data: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        default=dict,
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
        return f"<Claim(id={self.id}, number={self.claim_number})>"
    
    @property
    def is_suspicious(self) -> bool:
        """Check if claim is flagged as potentially suspicious."""
        return self.anomaly_score is not None and self.anomaly_score > 0.7
    
    @property
    def days_to_settle(self) -> Optional[int]:
        """Days from claim date to settlement."""
        if not self.settlement_date:
            return None
        return (self.settlement_date - self.claim_date).days
