"""
Imports API Routes
==================

Data import management.
"""

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy import func, select
from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from app.dependencies import DBSession, CurrentUser, Pagination, require_permission
from app.models.data_import import DataImport
from app.schemas.common import PaginatedResponse, SuccessResponse

router = APIRouter()


class DataImportResponse(BaseModel):
    id: UUID
    file_name: str
    import_type: str
    status: str
    total_rows: Optional[int]
    processed_rows: Optional[int]
    error_rows: Optional[int]
    column_mapping: Optional[dict]
    ai_suggested_mapping: Optional[dict]
    ai_data_issues: Optional[list]
    uploaded_by_id: UUID
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class ImportMappingUpdate(BaseModel):
    column_mapping: dict


@router.get("", response_model=PaginatedResponse[DataImportResponse])
async def list_imports(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    status_filter: Optional[str] = Query(None, alias="status"),
    import_type: Optional[str] = Query(None),
):
    """List data imports."""
    query = select(DataImport)
    
    if status_filter:
        query = query.where(DataImport.status == status_filter)
    if import_type:
        query = query.where(DataImport.import_type == import_type)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.offset(pagination.offset).limit(pagination.page_size).order_by(DataImport.created_at.desc())
    result = await db.execute(query)
    imports = result.scalars().all()

    return PaginatedResponse.create(
        items=imports,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.post("/upload", response_model=DataImportResponse, status_code=status.HTTP_201_CREATED)
async def upload_import_file(
    file: UploadFile,
    import_type: str,
    db: DBSession,
    current_user: CurrentUser = Depends(require_permission("import", "create")),
):
    """Upload a file for import."""
    # Validate file type
    if not file.filename.endswith((".csv", ".xlsx", ".xls")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV and Excel files are supported",
        )

    # Read file content
    content = await file.read()
    
    # Create import record
    data_import = DataImport(
        file_name=file.filename,
        import_type=import_type,
        status="uploaded",
        uploaded_by_id=current_user.id,
    )
    db.add(data_import)
    await db.flush()

    # TODO: Save file to S3
    # TODO: Dispatch Celery task for analysis

    await db.refresh(data_import)
    return data_import


@router.get("/{import_id}", response_model=DataImportResponse)
async def get_import(
    db: DBSession,
    import_id: UUID,
    current_user: CurrentUser,
):
    """Get import details."""
    result = await db.execute(
        select(DataImport).where(DataImport.id == import_id)
    )
    data_import = result.scalar_one_or_none()
    if not data_import:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Import not found")
    return data_import


@router.put("/{import_id}/mapping", response_model=DataImportResponse)
async def update_mapping(
    db: DBSession,
    import_id: UUID,
    data: ImportMappingUpdate,
    current_user: CurrentUser = Depends(require_permission("import", "update")),
):
    """Update column mapping for an import."""
    result = await db.execute(
        select(DataImport).where(DataImport.id == import_id)
    )
    data_import = result.scalar_one_or_none()
    if not data_import:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Import not found")

    data_import.column_mapping = data.column_mapping
    await db.flush()
    await db.refresh(data_import)
    return data_import


@router.post("/{import_id}/process", response_model=SuccessResponse)
async def process_import(
    db: DBSession,
    import_id: UUID,
    current_user: CurrentUser = Depends(require_permission("import", "update")),
):
    """Start processing an import."""
    result = await db.execute(
        select(DataImport).where(DataImport.id == import_id)
    )
    data_import = result.scalar_one_or_none()
    if not data_import:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Import not found")

    if data_import.status != "mapped":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Import must have mapping configured before processing",
        )

    data_import.status = "processing"
    data_import.started_at = datetime.utcnow()

    # TODO: Dispatch Celery task

    return SuccessResponse(message="Import processing started")
