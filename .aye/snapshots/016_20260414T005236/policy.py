"""
Policy Model
============

Insurance policy records.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, DateTime, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

try:
    from pgvector.sqlalchemy import Vector
    HAS_PGVECTOR = True
except ImportError:
    HAS_PGVECTOR = False
    Vector = None

from app.models.base import Base, TimestampMixin, SoftDeleteMixin, AuditMixin

if TYPE_CHECKING:
    from app.models.policyholder import Policyholder
    from app.models.coverage import Coverage
    from app.models.claim import Claim
    from app.models.user import User


class Policy(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """
    Insurance policy.
    
    The core entity for policy data management.
    Supports life, health, property, and casualty products.
    """
    
    __tablename__ = "policy"
    
    # Policy identification
    policy_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )
    
    external_policy_id: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
        index=True,
        doc="External system policy ID",
    )
    
    # Product information
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
    
    # Policy status
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="active",
        index=True,
        doc="active/lapsed/surrendered/matured/claimed/cancelled",
    )
    
    status_reason: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Reason for status change",
    )
    
    status_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        doc="Date of last status change",
    )
    
    # Policyholder
    policyholder_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("policyholder.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    
    # Key dates
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
    
    expiry_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )
    
    termination_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )
    
    # Policy term (in years or months)
    policy_term: Mapped[Optional[int]] = mapped_column(
        nullable=True,
        doc="Policy term in months",
    )
    
    # Financial details
    sum_assured: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )
    
    premium_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )
    
    premium_frequency: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="annual",
        doc="annual/semi-annual/quarterly/monthly/single",
    )
    
    premium_due_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        index=True,
    )
    
    annualized_premium: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(18, 2),
        nullable=True,
    )
    
    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="USD",
    )
    
    # Underwriting
    risk_class: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        doc="Underwriting risk classification",
    )
    
    underwriter_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # Distribution
    branch_code: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        index=True,
    )
    
    agent_code: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        index=True,
    )
    
    channel: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        doc="direct/agent/broker/bancassurance",
    )
    
    # Flexible data storage
    policy_data: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        default=dict,
        doc="Additional policy attributes as JSON",
    )
    
    # Semantic search embedding
    if HAS_PGVECTOR:
        embedding: Mapped[Optional[list]] = mapped_column(
            Vector(1536),
            nullable=True,
            doc="Vector embedding for semantic search",
        )
    
    # Relationships
    policyholder: Mapped["Policyholder"] = relationship(
        "Policyholder",
        back_populates="policies",
        lazy="joined",
    )
    
    coverages: Mapped[list["Coverage"]] = relationship(
        "Coverage",
        back_populates="policy",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    
    claims: Mapped[list["Claim"]] = relationship(
        "Claim",
        back_populates="policy",
        lazy="dynamic",
    )
    
    underwriter: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[underwriter_id],
        lazy="joined",
    )
    
    def __repr__(self) -> str:
        return f"<Policy(id={self.id}, number={self.policy_number})>"
    
    @property
    def is_active(self) -> bool:
        """Check if policy is currently active."""
        return self.status == "active"
    
    @property
    def duration_months(self) -> Optional[int]:
        """Duration since issue in months."""
        if not self.issue_date:
            return None
        today = date.today()
        return (today.year - self.issue_date.year) * 12 + (today.month - self.issue_date.month)
    
    @property
    def issue_age(self) -> Optional[int]:
        """Age at policy issue."""
        if not self.policyholder or not self.policyholder.date_of_birth:
            return None
        dob = self.policyholder.date_of_birth
        return self.issue_date.year - dob.year - (
            (self.issue_date.month, self.issue_date.day) < (dob.month, dob.day)
        )


# Composite indexes
Index(
    "idx_policy_product_status",
    Policy.product_type,
    Policy.status,
)

Index(
    "idx_policy_issue_date_status",
    Policy.issue_date,
    Policy.status,
)
