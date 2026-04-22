"""Documents API Routes."""

import os
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Query, UploadFile
from pydantic import BaseModel

from app.config import settings
from app.dependencies import CurrentUser, DBSession, Pagination
from app.exceptions import BadRequestError, NotFoundError
from app.models.user import User
from app.schemas.common import PaginatedResponse, SuccessResponse
from app.services.document_service import DocumentService

router = APIRouter()


class DocumentResponse(BaseModel):
    id: UUID
    file_name: str
    file_size: int | None
    content_type: str | None
    document_type: str | None
    related_resource_type: str | None
    related_resource_id: UUID | None
    extraction_confidence: float | None
    page_count: int | None
    has_extracted_data: bool
    
    class Config:
        from_attributes = True


class DocumentDetailResponse(DocumentResponse):
    extracted_text: str | None
    extracted_data: dict | None
    extraction_warnings: list | None


class SemanticSearchResult(BaseModel):
    id: str
    resource_type: str
    title: str
    score: float


@router.get("", response_model=PaginatedResponse[DocumentResponse])
async def list_documents(
    db: DBSession,
    current_user: CurrentUser,
    pagination: Pagination,
    document_type: str | None = Query(None),
    related_resource_type: str | None = Query(None),
    related_resource_id: UUID | None = Query(None),
):
    """List documents."""
    service = DocumentService(db)
    documents, total = await service.list_documents(
        offset=pagination.offset,
        limit=pagination.limit,
        document_type=document_type,
        related_resource_type=related_resource_type,
        related_resource_id=related_resource_id,
    )
    
    total_pages = (total + pagination.page_size - 1) // pagination.page_size
    
    items = [
        DocumentResponse(
            id=d.id,
            file_name=d.file_name,
            file_size=d.file_size,
            content_type=d.content_type,
            document_type=d.document_type,
            related_resource_type=d.related_resource_type,
            related_resource_id=d.related_resource_id,
            extraction_confidence=d.extraction_confidence,
            page_count=d.page_count,
            has_extracted_data=d.extracted_data is not None,
        )
        for d in documents
    ]
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        total_pages=total_pages,
        has_next=pagination.page < total_pages,
        has_prev=pagination.page > 1,
    )


@router.post("/upload", response_model=DocumentDetailResponse, status_code=201)
async def upload_document(
    file: UploadFile,
    db: DBSession,
    current_user: CurrentUser,
    document_type: str | None = Query(None),
    related_resource_type: str | None = Query(None),
    related_resource_id: UUID | None = Query(None),
    extract_data: bool = Query(True, description="Extract text and entities from document"),
):
    """Upload a document."""
    # Validate file type
    allowed_types = [
        "application/pdf",
        "image/png",
        "image/jpeg",
        "image/tiff",
    ]
    
    if file.content_type not in allowed_types:
        raise BadRequestError(
            f"Unsupported file type. Allowed: PDF, PNG, JPEG, TIFF"
        )
    
    # Read file content
    content = await file.read()
    file_size = len(content)
    
    # Validate file size
    if file_size > settings.max_upload_size_bytes:
        raise BadRequestError(
            f"File too large. Maximum size is {settings.MAX_UPLOAD_SIZE_MB}MB"
        )
    
    # TODO: Save file to S3/MinIO
    file_path = f"documents/{current_user.id}/{file.filename}"
    
    service = DocumentService(db)
    
    # Create document record
    document = await service.upload_document(
        file_name=file.filename,
        file_path=file_path,
        file_size=file_size,
        content_type=file.content_type,
        uploaded_by=current_user,
        document_type=document_type,
        related_resource_type=related_resource_type,
        related_resource_id=related_resource_id,
    )
    
    # Extract data if requested
    if extract_data:
        document = await service.extract_document_data(document, content)
    
    return DocumentDetailResponse(
        id=document.id,
        file_name=document.file_name,
        file_size=document.file_size,
        content_type=document.content_type,
        document_type=document.document_type,
        related_resource_type=document.related_resource_type,
        related_resource_id=document.related_resource_id,
        extraction_confidence=document.extraction_confidence,
        page_count=document.page_count,
        has_extracted_data=document.extracted_data is not None,
        extracted_text=document.extracted_text,
        extracted_data=document.extracted_data,
        extraction_warnings=document.extraction_warnings,
    )


@router.get("/{document_id}", response_model=DocumentDetailResponse)
async def get_document(
    document_id: UUID,
    db: DBSession,
    current_user: CurrentUser,
):
    """Get a document."""
    service = DocumentService(db)
    document = await service.get_document(document_id)
    
    if not document:
        raise NotFoundError("Document", document_id)
    
    return DocumentDetailResponse(
        id=document.id,
        file_name=document.file_name,
        file_size=document.file_size,
        content_type=document.content_type,
        document_type=document.document_type,
        related_resource_type=document.related_resource_type,
        related_resource_id=document.related_resource_id,
        extraction_confidence=document.extraction_confidence,
        page_count=document.page_count,
        has_extracted_data=document.extracted_data is not None,
        extracted_text=document.extracted_text,
        extracted_data=document.extracted_data,
        extraction_warnings=document.extraction_warnings,
    )


@router.post("/search", response_model=list[SemanticSearchResult])
async def search_documents(
    query: str,
    db: DBSession,
    current_user: CurrentUser,
    limit: int = Query(10, le=100),
):
    """Search documents using semantic search."""
    service = DocumentService(db)
    results = await service.search_documents(query, limit)
    return [SemanticSearchResult(**r) for r in results]


@router.delete("/{document_id}", response_model=SuccessResponse)
async def delete_document(
    document_id: UUID,
    db: DBSession,
    current_user: CurrentUser,
):
    """Delete a document."""
    service = DocumentService(db)
    document = await service.get_document(document_id)
    
    if not document:
        raise NotFoundError("Document", document_id)
    
    await service.delete_document(document)
    return SuccessResponse(message="Document deleted")
