"""
Assumption Table Model
======================

Individual assumption tables within an assumption set.
"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.assumption_set import AssumptionSet


class AssumptionTable(Base, TimestampMixin):
    """
    Individual assumption table (mortality, lapse, etc.).
    
    Data is stored as JSONB for flexibility in table shapes.
    """
    
    __tablename__ = "assumption_table"
    
    # Parent assumption set
    assumption_set_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("assumption_set.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Table identification
    table_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="mortality/lapse/expense/morbidity/discount_rate/inflation/commission",
    )
    
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Source information
    source: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Data source (e.g., 'SOA 2017 CSO', 'Company Experience 2023')",
    )
    
    # Table data - flexible structure
    data: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        doc="Table data in flexible JSON format",
    )
    
    # Metadata about the table
    metadata_: Mapped[Optional[dict]] = mapped_column(
        "metadata",
        JSONB,
        nullable=True,
        default=dict,
        doc="Additional metadata (units, interpolation method, etc.)",
    )
    
    # Relationships
    assumption_set: Mapped["AssumptionSet"] = relationship(
        "AssumptionSet",
        back_populates="tables",
    )
    
    def __repr__(self) -> str:
        return f"<AssumptionTable(id={self.id}, type={self.table_type}, name={self.name})>"
    
    def get_rate(self, **lookup_keys) -> Optional[float]:
        """
        Look up a rate from the table data.
        
        Args:
            **lookup_keys: Keys to look up (e.g., age=35, duration=5, sex='M')
            
        Returns:
            Rate value or None if not found.
        """
        # This is a simplified lookup - actual implementation would depend
        # on the table structure defined in self.data
        rates = self.data.get("rates", [])
        
        for rate_row in rates:
            match = True
            for key, value in lookup_keys.items():
                if rate_row.get(key) != value:
                    match = False
                    break
            if match:
                return rate_row.get("rate") or rate_row.get("value")
        
        return None
