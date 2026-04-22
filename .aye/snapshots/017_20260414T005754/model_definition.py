"""
Model Definition Model
======================

Actuarial calculation model definitions.
"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, SoftDeleteMixin, AuditMixin

if TYPE_CHECKING:
    from app.models.calculation_run import CalculationRun
    from app.models.user import User


class ModelDefinition(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """
    Actuarial model definition.
    
    Defines the calculation graph - what inputs, calculations, and outputs.
    Configuration stored as JSONB for flexibility.
    """
    
    __tablename__ = "model_definition"
    
    # Identification
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Classification
    model_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="reserving/pricing/cashflow/valuation/experience",
    )
    
    line_of_business: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc="term_life/whole_life/universal_life/annuity/health/property/etc.",
    )
    
    # Regulatory standard (if applicable)
    regulatory_standard: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        doc="IFRS17/SolvencyII/USGAAP/LDTI",
    )
    
    # Versioning
    version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="1.0.0",
    )
    
    # Status
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="draft",
        index=True,
        doc="draft/active/archived",
    )
    
    # The calculation configuration (the model itself)
    configuration: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        doc="Calculation graph configuration",
    )
    
    # Required assumption table types
    required_assumptions: Mapped[Optional[list]] = mapped_column(
        JSONB,
        nullable=True,
        default=list,
        doc="List of required assumption table types",
    )
    
    # Default parameters
    default_parameters: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        default=dict,
        doc="Default values for run parameters",
    )
    
    # Is this a system template?
    is_template: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )
    
    # Parent model (for cloning)
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("model_definition.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # Relationships
    calculation_runs: Mapped[list["CalculationRun"]] = relationship(
        "CalculationRun",
        back_populates="model_definition",
        lazy="dynamic",
    )
    
    parent: Mapped[Optional["ModelDefinition"]] = relationship(
        "ModelDefinition",
        remote_side="ModelDefinition.id",
        foreign_keys=[parent_id],
    )
    
    def __repr__(self) -> str:
        return f"<ModelDefinition(id={self.id}, name={self.name})>"
    
    @property
    def is_usable(self) -> bool:
        """Can this model be used in calculations?"""
        return self.status == "active"
