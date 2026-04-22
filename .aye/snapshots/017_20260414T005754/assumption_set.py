"""
Assumption Set Model
====================

Versioned collections of actuarial assumptions.
"""

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, SoftDeleteMixin, AuditMixin

if TYPE_CHECKING:
    from app.models.assumption_table import AssumptionTable
    from app.models.user import User
    from app.models.calculation_run import CalculationRun


class AssumptionSet(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """
    A versioned set of actuarial assumptions.
    
    Contains multiple assumption tables (mortality, lapse, etc.).
    Supports approval workflow: draft -> pending_approval -> approved -> archived.
    """
    
    __tablename__ = "assumption_set"
    
    # Identification
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    
    version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        doc="Version identifier (e.g., '2024-Q1', '1.0.0')",
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
        doc="draft/pending_approval/approved/archived",
    )
    
    # Effective period
    effective_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        doc="When assumptions become effective",
    )
    
    expiry_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        doc="When assumptions expire",
    )
    
    # Approval tracking
    submitted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    submitted_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    approved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    approved_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    approval_notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    rejection_notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Parent set (for cloning/versioning)
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("assumption_set.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # Relationships
    tables: Mapped[list["AssumptionTable"]] = relationship(
        "AssumptionTable",
        back_populates="assumption_set",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    
    submitted_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[submitted_by_id],
    )
    
    approved_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[approved_by_id],
    )
    
    parent: Mapped[Optional["AssumptionSet"]] = relationship(
        "AssumptionSet",
        remote_side="AssumptionSet.id",
        foreign_keys=[parent_id],
    )
    
    calculation_runs: Mapped[list["CalculationRun"]] = relationship(
        "CalculationRun",
        back_populates="assumption_set",
        lazy="dynamic",
    )
    
    def __repr__(self) -> str:
        return f"<AssumptionSet(id={self.id}, name={self.name}, version={self.version})>"
    
    @property
    def is_editable(self) -> bool:
        """Can this assumption set be edited?"""
        return self.status == "draft"
    
    @property
    def is_usable(self) -> bool:
        """Can this assumption set be used in calculations?"""
        return self.status == "approved"
