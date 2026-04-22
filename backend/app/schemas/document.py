"""
Document Schemas
================

Schemas for document management.
"""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DocumentUpload(BaseModel):
    """Schema for document upload metadata."""
    
    document_type: Optional[str] = Field(
        default=None,
        pattern="^(policy_application|claim_form|medical_report|id_document|other)$"
    )
    related_resource_type: Optional[str] = Field(default=None, max_length=100)
    related_resource_id: Optional[UUID] = None


class DocumentResponse(BaseModel):
    """Schema for document response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    file_name: str
    file_path: str
    file_size: Optional[int] = None
    file_type: str
    mime_type: Optional[str] = None
    
    document_type: Optional[str] = None
    related_resource_type: Optional[str] = None
    related_resource_id: Optional[UUID] = None
    
    extracted_text: Optional[str] = None
    extracted_data: Optional[dict[str, Any]] = None
    extraction_confidence: Optional[dict[str, Any]] = None
    
    processing_status: str
    processing_error: Optional[str] = None
    
    uploaded_by_id: Optional[UUID] = None
    uploaded_at: datetime
    
    created_at: datetime
    updated_at: datetime


class DocumentListItem(BaseModel):
    """Simplified document for list views."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    file_name: str
    file_type: str
    file_size: Optional[int] = None
    document_type: Optional[str] = None
    processing_status: str
    uploaded_at: datetime


class DocumentFilter(BaseModel):
    """Filter parameters for document list."""
    
    document_type: Optional[str] = None
    file_type: Optional[str] = None
    related_resource_type: Optional[str] = None
    related_resource_id: Optional[UUID] = None
    processing_status: Optional[str] = None
    uploaded_by_id: Optional[UUID] = None
    
    uploaded_after: Optional[datetime] = None
    uploaded_before: Optional[datetime] = None
    
    search: Optional[str] = Field(
        default=None,
        description="Search in file name and extracted text"
    )


class DocumentSearchResult(BaseModel):
    """Document search result."""
    
    id: UUID
    file_name: str
    document_type: Optional[str] = None
    snippet: str = Field(description="Matching text snippet")
    score: float = Field(ge=0, le=1)
    highlights: list[str] = []
