"""
Document Model
==============

Uploaded document records.
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class Document(Base, TimestampMixin):
    """Document model."""

    __tablename__ = "documents"

    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    content_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    document_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        index=True,
        doc="application/claim_doc/policy_doc/assumption_doc",
    )

    # Related resource (optional)
    related_resource_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    related_resource_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)

    # OCR/Extraction
    extracted_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    extracted_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    extraction_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    extraction_warnings: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    page_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Upload info
    uploaded_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    # Relationships
    uploaded_by: Mapped[Optional["User"]] = relationship("User")

    def __repr__(self) -> str:
        return f"<Document(id={self.id}, file={self.file_name})>"
