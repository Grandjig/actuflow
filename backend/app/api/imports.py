"""Data Import API Routes."""

import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.dependencies import get_current_user, require_permission
from app.models.user import User
from app.models.data_import import DataImport
from app.services.import_service import ImportService
from app.services.audit_service import AuditService

router = APIRouter()


@router.get("")
async def list_imports(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("import", "read"))],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    import_type: Optional[str] = None,
):
    """List data imports."""
    query = select(DataImport).where(DataImport.is_deleted == False)
    
    if status:
        query = query.where(DataImport.status == status)
    
    if import_type:
        query = query.where(DataImport.import_type == import_type)
    
    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Paginate
    query = query.order_by(DataImport.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    imports = list(result.scalars().all())
    
    return {
        "items": imports,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size,
    }


@router.get("/{import_id}")
async def get_import(
    import_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("import", "read"))],
):
    """Get an import by ID."""
    result = await db.execute(
        select(DataImport).where(
            DataImport.id == import_id,
            DataImport.is_deleted == False,
        )
    )
    data_import = result.scalar_one_or_none()
    
    if not data_import:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Import not found",
        )
    
    return data_import


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    import_type: str = Form(...),
    db: Annotated[AsyncSession, Depends(get_async_session)] = None,
    current_user: Annotated[User, Depends(require_permission("import", "create"))] = None,
):
    """Upload a file for import."""
    import_service = ImportService(db)
    
    # Validate file type
    if not file.filename.endswith((".csv", ".xlsx", ".xls")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Supported: CSV, Excel",
        )
    
    # Process upload
    result = await import_service.upload_file(
        file=file,
        import_type=import_type,
        uploaded_by=current_user.id,
    )
    
    return result


@router.post("/{import_id}/mapping")
async def set_column_mapping(
    import_id: uuid.UUID,
    mapping: dict,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("import", "create"))],
):
    """Set column mapping for an import."""
    import_service = ImportService(db)
    
    result = await db.execute(
        select(DataImport).where(
            DataImport.id == import_id,
            DataImport.is_deleted == False,
        )
    )
    data_import = result.scalar_one_or_none()
    
    if not data_import:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Import not found",
        )
    
    data_import.column_mapping = mapping.get("column_mapping", {})
    await db.flush()
    await db.refresh(data_import)
    
    return data_import


@router.post("/{import_id}/validate")
async def validate_import(
    import_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("import", "create"))],
):
    """Validate import data."""
    import_service = ImportService(db)
    
    result = await db.execute(
        select(DataImport).where(
            DataImport.id == import_id,
            DataImport.is_deleted == False,
        )
    )
    data_import = result.scalar_one_or_none()
    
    if not data_import:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Import not found",
        )
    
    validation_result = await import_service.validate(import_id)
    return validation_result


@router.post("/{import_id}/commit")
async def commit_import(
    import_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("import", "create"))],
):
    """Commit import (insert data)."""
    import_service = ImportService(db)
    audit_service = AuditService(db)
    
    result = await db.execute(
        select(DataImport).where(
            DataImport.id == import_id,
            DataImport.is_deleted == False,
        )
    )
    data_import = result.scalar_one_or_none()
    
    if not data_import:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Import not found",
        )
    
    if data_import.status not in ["validated", "uploaded"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Import must be validated before commit",
        )
    
    # Queue import task
    data_import.status = "processing"
    await db.flush()
    
    # TODO: Queue Celery task for actual import
    
    await audit_service.log(
        user_id=current_user.id,
        action="commit",
        resource_type="data_import",
        resource_id=import_id,
    )
    
    return data_import


@router.get("/{import_id}/ai-suggestions")
async def get_ai_suggestions(
    import_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("import", "read"))],
):
    """Get AI-generated column mapping suggestions."""
    import_service = ImportService(db)
    
    result = await db.execute(
        select(DataImport).where(
            DataImport.id == import_id,
            DataImport.is_deleted == False,
        )
    )
    data_import = result.scalar_one_or_none()
    
    if not data_import:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Import not found",
        )
    
    return {
        "column_mappings": data_import.ai_suggested_mapping or [],
        "data_issues": data_import.ai_data_issues or [],
    }
