"""
Data Import Model
=================

Data import records.
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class DataImport(Base, TimestampMixin):
    """Data import model."""

    __tablename__ = "data_imports"

    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    import_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="policy/policyholder/claim/assumption",
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="uploaded",
        index=True,
        doc="uploaded/analyzing/mapped/processing/completed/failed",
    )

    total_rows: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    processed_rows: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    error_rows: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    column_mapping: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        doc="User-confirmed column mapping",
    )

    ai_suggested_mapping: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        doc="AI-suggested column mapping",
    )

    ai_data_issues: Mapped[Optional[list]] = mapped_column(
        JSONB,
        nullable=True,
        doc="AI-detected data quality issues",
    )

    error_details: Mapped[Optional[list]] = mapped_column(
        JSONB,
        nullable=True,
        doc="Details of import errors",
    )

    uploaded_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    uploaded_by: Mapped[Optional["User"]] = relationship("User")

    def __repr__(self) -> str:
        return f"<DataImport(id={self.id}, file={self.file_name}, status={self.status})>"
