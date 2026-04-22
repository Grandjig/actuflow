"""
Reports API Routes
==================

Report generation and management.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from app.dependencies import DBSession, CurrentUser, Pagination, require_permission
from app.models.report_template import ReportTemplate
from app.models.generated_report import GeneratedReport
from app.schemas.common import PaginatedResponse, SuccessResponse

router = APIRouter()


class ReportTemplateResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    report_type: str
    regulatory_standard: Optional[str]
    output_format: str
    is_system_template: bool
    include_ai_narrative: bool

    class Config:
        from_attributes = True


class GeneratedReportResponse(BaseModel):
    id: UUID
    report_template_id: UUID
    name: str
    reporting_period_start: str
    reporting_period_end: str
    status: str
    generated_by_id: UUID
    generated_at: Optional[datetime]
    file_path: Optional[str]
    file_size: Optional[int]
    ai_summary: Optional[str]

    class Config:
        from_attributes = True


class GenerateReportRequest(BaseModel):
    report_template_id: UUID
    name: str
    reporting_period_start: str
    reporting_period_end: str
    parameters: Optional[dict] = None


@router.get("/templates", response_model=list[ReportTemplateResponse])
async def list_report_templates(
    db: DBSession,
    current_user: CurrentUser,
    report_type: Optional[str] = Query(None),
):
    """List available report templates."""
    query = select(ReportTemplate)
    if report_type:
        query = query.where(ReportTemplate.report_type == report_type)
    query = query.order_by(ReportTemplate.name)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("", response_model=PaginatedResponse[GeneratedReportResponse])
async def list_generated_reports(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    status_filter: Optional[str] = Query(None, alias="status"),
):
    """List generated reports."""
    query = select(GeneratedReport)
    if status_filter:
        query = query.where(GeneratedReport.status == status_filter)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.offset(pagination.offset).limit(pagination.page_size).order_by(GeneratedReport.created_at.desc())
    result = await db.execute(query)
    reports = result.scalars().all()

    return PaginatedResponse.create(
        items=reports,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.post("/generate", response_model=GeneratedReportResponse, status_code=status.HTTP_202_ACCEPTED)
async def generate_report(
    db: DBSession,
    data: GenerateReportRequest,
    current_user: CurrentUser = Depends(require_permission("report", "create")),
):
    """Generate a new report."""
    # Validate template exists
    result = await db.execute(
        select(ReportTemplate).where(ReportTemplate.id == data.report_template_id)
    )
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Template not found")

    from datetime import date
    report = GeneratedReport(
        report_template_id=data.report_template_id,
        name=data.name,
        reporting_period_start=date.fromisoformat(data.reporting_period_start),
        reporting_period_end=date.fromisoformat(data.reporting_period_end),
        status="queued",
        generated_by_id=current_user.id,
        parameters=data.parameters,
    )
    db.add(report)
    await db.flush()
    await db.refresh(report)

    # TODO: Dispatch Celery task for report generation

    return report


@router.get("/{report_id}", response_model=GeneratedReportResponse)
async def get_report(
    db: DBSession,
    report_id: UUID,
    current_user: CurrentUser,
):
    """Get a generated report by ID."""
    result = await db.execute(
        select(GeneratedReport).where(GeneratedReport.id == report_id)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return report
