"""
Document Model
==============

Uploaded documents with AI extraction.
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

try:
    from pgvector.sqlalchemy import Vector
    HAS_PGVECTOR = True
except ImportError:
    HAS_PGVECTOR = False
    Vector = None

from app.models.base import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.user import User


class Document(Base, TimestampMixin, SoftDeleteMixin):
    """
    Uploaded document with OCR and AI extraction.
    """
    
    __tablename__ = "document"
    
    # File info
    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        doc="S3/MinIO path",
    )
    
    file_size: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        nullable=True,
    )
    
    file_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        doc="pdf/png/jpg/tiff",
    )
    
    mime_type: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    
    # Document type
    document_type: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        index=True,
        doc="policy_application/claim_form/medical_report/id_document/other",
    )
    
    # Related resource
    related_resource_type: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )
    
    related_resource_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        index=True,
    )
    
    # OCR extracted text
    extracted_text: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # AI extracted structured data
    extracted_data: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        doc="Structured data extracted by AI",
    )
    
    extraction_confidence: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        doc="Confidence scores for each extracted field",
    )
    
    # Processing status
    processing_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="uploaded",
        doc="uploaded/processing/completed/failed",
    )
    
    processing_error: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Vector embedding for semantic search
    if HAS_PGVECTOR:
        embedding: Mapped[Optional[list]] = mapped_column(
            Vector(1536),
            nullable=True,
        )
    
    # Upload info
    uploaded_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    
    # Relationships
    uploaded_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[uploaded_by_id],
    )
    
    def __repr__(self) -> str:
        return f"<Document(id={self.id}, name={self.file_name})>"
