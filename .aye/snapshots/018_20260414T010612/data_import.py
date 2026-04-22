"""
Data Import Model
=================

Tracking of data import jobs.
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class DataImport(Base, TimestampMixin):
    """
    Data import job tracking.
    
    Tracks the upload, mapping, validation, and commit of imported data.
    """
    
    __tablename__ = "data_import"
    
    # File information
    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    file_path: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        doc="S3/MinIO path to uploaded file",
    )
    
    file_size: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        nullable=True,
    )
    
    file_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        doc="csv/xlsx/xls",
    )
    
    # Import type
    import_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="policy/policyholder/claim/assumption/etc.",
    )
    
    # Status
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="uploaded",
        index=True,
        doc="uploaded/mapping/validating/validated/importing/completed/failed/cancelled",
    )
    
    # Progress
    total_rows: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    
    processed_rows: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    
    success_rows: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    
    error_rows: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    
    # Column mapping
    column_mapping: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        doc="User-confirmed column mapping",
    )
    
    # AI suggestions
    ai_suggested_mapping: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        doc="AI-suggested column mapping with confidence scores",
    )
    
    ai_data_issues: Mapped[Optional[list]] = mapped_column(
        JSONB,
        nullable=True,
        doc="AI-detected data quality issues",
    )
    
    # Validation results
    validation_errors: Mapped[Optional[list]] = mapped_column(
        JSONB,
        nullable=True,
        doc="List of validation errors",
    )
    
    # Import options
    import_options: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        doc="Import options (on_duplicate, skip_errors, etc.)",
    )
    
    # Timing
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # User
    uploaded_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    
    # Error
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Relationships
    uploaded_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[uploaded_by_id],
    )
    
    def __repr__(self) -> str:
        return f"<DataImport(id={self.id}, file={self.file_name}, status={self.status})>"
