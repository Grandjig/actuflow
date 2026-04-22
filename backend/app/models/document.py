"""Document Model."""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text, Integer, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.models.base import Base


class Document(Base):
    """Uploaded documents with AI extraction."""

    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # File info
    file_name = Column(String(500), nullable=False)
    file_path = Column(String(1000), nullable=False)  # S3/MinIO path
    file_size = Column(Integer)  # bytes
    content_type = Column(String(100))
    
    # Classification
    document_type = Column(String(100), index=True)  # policy_application, claim_form, medical_report, etc.
    
    # Relationship to other entities
    related_resource_type = Column(String(100), index=True)
    related_resource_id = Column(UUID(as_uuid=True), index=True)
    
    # AI Extraction results
    extracted_text = Column(Text)  # OCR result
    extracted_data = Column(JSONB)  # Structured data extracted by AI
    extraction_confidence = Column(Float)  # Overall confidence score
    extraction_warnings = Column(JSONB)  # Any issues during extraction
    
    # Page info
    page_count = Column(Integer)
    
    # Status
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime)
    
    # Upload info
    uploaded_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    uploaded_by = relationship("User")
