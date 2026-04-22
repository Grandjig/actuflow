"""Document Model."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, SoftDeleteMixin

try:
    from pgvector.sqlalchemy import Vector
    HAS_PGVECTOR = True
except ImportError:
    HAS_PGVECTOR = False
    Vector = None

if TYPE_CHECKING:
    from app.models.user import User


class Document(BaseModel, SoftDeleteMixin):
    """Uploaded document with extracted data."""
    
    __tablename__ = "documents"
    
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    content_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    document_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
    related_resource_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    related_resource_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    
    extracted_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    extracted_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    extraction_confidence: Mapped[float | None] = mapped_column(nullable=True)
    extraction_warnings: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    
    page_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
    uploaded_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True, default=dict)
    
    # Vector embedding for semantic search
    if HAS_PGVECTOR:
        embedding: Mapped[list | None] = mapped_column(Vector(384), nullable=True)
    
    def __repr__(self) -> str:
        return f"<Document({self.file_name})>"
