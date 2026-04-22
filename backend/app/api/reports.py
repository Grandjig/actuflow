"""Reports API Routes."""

import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.dependencies import get_current_user, require_permission
from app.models.user import User
from app.models.report_template import ReportTemplate
from app.models.generated_report import GeneratedReport

router = APIRouter()


@router.get("/templates")
async def list_report_templates(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("report", "read"))],
):
    """List report templates."""
    result = await db.execute(
        select(ReportTemplate)
        .where(ReportTemplate.is_deleted == False)
        .order_by(ReportTemplate.name)
    )
    return list(result.scalars().all())


@router.get("/templates/{template_id}")
async def get_report_template(
    template_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("report", "read"))],
):
    """Get a report template."""
    result = await db.execute(
        select(ReportTemplate).where(
            ReportTemplate.id == template_id,
            ReportTemplate.is_deleted == False,
        )
    )
    template = result.scalar_one_or_none()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found",
        )
    
    return template


@router.get("")
async def list_generated_reports(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("report", "read"))],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    report_type: Optional[str] = None,
    status: Optional[str] = None,
):
    """List generated reports."""
    query = select(GeneratedReport).where(GeneratedReport.is_deleted == False)
    
    if report_type:
        query = query.where(GeneratedReport.report_type == report_type)
    
    if status:
        query = query.where(GeneratedReport.status == status)
    
    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Paginate
    query = query.order_by(GeneratedReport.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    reports = list(result.scalars().all())
    
    return {
        "items": reports,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size,
    }


@router.get("/{report_id}")
async def get_generated_report(
    report_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("report", "read"))],
):
    """Get a generated report."""
    result = await db.execute(
        select(GeneratedReport).where(
            GeneratedReport.id == report_id,
            GeneratedReport.is_deleted == False,
        )
    )
    report = result.scalar_one_or_none()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )
    
    return report


@router.post("")
async def generate_report(
    data: dict,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("report", "create"))],
):
    """Generate a new report."""
    template_id = data.get("template_id")
    
    # Get template
    template_result = await db.execute(
        select(ReportTemplate).where(ReportTemplate.id == uuid.UUID(template_id))
    )
    template = template_result.scalar_one_or_none()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found",
        )
    
    # Create report record
    report = GeneratedReport(
        report_template_id=template.id,
        name=data.get("name", f"{template.name} - Report"),
        report_type=template.report_type,
        status="generating",
        generated_by_id=current_user.id,
        parameters=data.get("parameters", {}),
    )
    db.add(report)
    await db.flush()
    await db.refresh(report)
    
    # TODO: Queue report generation task
    
    return report
