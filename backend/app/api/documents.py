"""
Documents API Routes
====================

Document management endpoints.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy import func, select

from app.dependencies import DBSession, CurrentUser, Pagination, require_permission
from app.models.document import Document
from app.schemas.common import PaginatedResponse
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class DocumentResponse(BaseModel):
    id: UUID
    file_name: str
    file_path: str
    document_type: Optional[str]
    related_resource_type: Optional[str]
    related_resource_id: Optional[UUID]
    uploaded_at: datetime

    class Config:
        from_attributes = True


@router.get("", response_model=PaginatedResponse[DocumentResponse])
async def list_documents(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    document_type: Optional[str] = Query(None),
    related_resource_type: Optional[str] = Query(None),
    related_resource_id: Optional[UUID] = Query(None),
):
    """List documents."""
    query = select(Document)

    if document_type:
        query = query.where(Document.document_type == document_type)
    if related_resource_type:
        query = query.where(Document.related_resource_type == related_resource_type)
    if related_resource_id:
        query = query.where(Document.related_resource_id == related_resource_id)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.offset(pagination.offset).limit(pagination.page_size).order_by(Document.uploaded_at.desc())
    result = await db.execute(query)
    docs = result.scalars().all()

    return PaginatedResponse.create(
        items=docs,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.post("/upload", response_model=DocumentResponse, status_code=201)
async def upload_document(
    db: DBSession,
    file: UploadFile = File(...),
    document_type: Optional[str] = Query(None),
    related_resource_type: Optional[str] = Query(None),
    related_resource_id: Optional[UUID] = Query(None),
    current_user: CurrentUser = Depends(require_permission("document", "create")),
):
    """Upload a document."""
    # TODO: Save file to S3/MinIO
    file_path = f"documents/{file.filename}"

    doc = Document(
        file_name=file.filename,
        file_path=file_path,
        content_type=file.content_type,
        document_type=document_type,
        related_resource_type=related_resource_type,
        related_resource_id=related_resource_id,
        uploaded_by_id=current_user.id,
        uploaded_at=datetime.utcnow(),
    )
    db.add(doc)
    await db.flush()
    await db.refresh(doc)
    return doc


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    db: DBSession,
    document_id: UUID,
    current_user: CurrentUser,
):
    """Get document by ID."""
    result = await db.execute(
        select(Document).where(Document.id == document_id)
    )
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.delete("/{document_id}", status_code=204)
async def delete_document(
    db: DBSession,
    document_id: UUID,
    _: CurrentUser = Depends(require_permission("document", "delete")),
):
    """Delete a document."""
    result = await db.execute(
        select(Document).where(Document.id == document_id)
    )
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    await db.delete(doc)


@router.post("/{document_id}/extract")
async def extract_document_data(
    db: DBSession,
    document_id: UUID,
    current_user: CurrentUser,
):
    """Extract data from document using AI."""
    result = await db.execute(
        select(Document).where(Document.id == document_id)
    )
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # TODO: Call AI service for extraction
    return {
        "document_id": str(document_id),
        "status": "processing",
        "message": "Document extraction queued",
    }
