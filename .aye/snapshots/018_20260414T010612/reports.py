"""
Report Management API Routes
============================

CRUD for report templates and report generation.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse

from app.dependencies import (
    CurrentUser,
    DBSession,
    Pagination,
    Sorting,
    require_permission,
)
from app.schemas.common import PaginatedResponse, SuccessMessage
from app.schemas.report import (
    GeneratedReportListItem,
    GeneratedReportResponse,
    GenerateReportRequest,
    ReportScheduleCreate,
    ReportTemplateCreate,
    ReportTemplateListItem,
    ReportTemplateResponse,
    ReportTemplateUpdate,
)

router = APIRouter()


# =============================================================================
# Report Templates
# =============================================================================

@router.get("/templates", response_model=PaginatedResponse[ReportTemplateListItem])
async def list_report_templates(
    db: DBSession,
    user: CurrentUser,
    pagination: Pagination,
    report_type: Optional[str] = None,
    regulatory_standard: Optional[str] = None,
    _: None = Depends(require_permission("report", "read")),
):
    """
    List report templates.
    """
    from app.services.report_service import ReportService
    
    service = ReportService(db)
    
    templates, total = await service.list_templates(
        report_type=report_type,
        regulatory_standard=regulatory_standard,
        offset=pagination.offset,
        limit=pagination.limit,
    )
    
    return PaginatedResponse.create(
        items=templates,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/templates/{template_id}", response_model=ReportTemplateResponse)
async def get_report_template(
    template_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("report", "read")),
):
    """
    Get a report template by ID.
    """
    from app.services.report_service import ReportService
    
    service = ReportService(db)
    template = await service.get_template(template_id)
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report template not found",
        )
    
    return template


@router.post("/templates", response_model=ReportTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_report_template(
    data: ReportTemplateCreate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("report", "create")),
):
    """
    Create a new report template.
    """
    from app.services.report_service import ReportService
    
    service = ReportService(db)
    template = await service.create_template(data, created_by=user)
    
    return template


@router.put("/templates/{template_id}", response_model=ReportTemplateResponse)
async def update_report_template(
    template_id: UUID,
    data: ReportTemplateUpdate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("report", "update")),
):
    """
    Update a report template.
    """
    from app.services.report_service import ReportService
    
    service = ReportService(db)
    
    template = await service.get_template(template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report template not found",
        )
    
    if template.is_system_template:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify system templates",
        )
    
    updated = await service.update_template(template, data, updated_by=user)
    
    return updated


@router.delete("/templates/{template_id}", response_model=SuccessMessage)
async def delete_report_template(
    template_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("report", "delete")),
):
    """
    Delete a report template.
    """
    from app.services.report_service import ReportService
    
    service = ReportService(db)
    
    template = await service.get_template(template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report template not found",
        )
    
    if template.is_system_template:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete system templates",
        )
    
    await service.delete_template(template, deleted_by=user)
    
    return SuccessMessage(message="Report template deleted")


# =============================================================================
# Generated Reports
# =============================================================================

@router.get("", response_model=PaginatedResponse[GeneratedReportListItem])
async def list_generated_reports(
    db: DBSession,
    user: CurrentUser,
    pagination: Pagination,
    sorting: Sorting,
    template_id: Optional[UUID] = None,
    status_filter: Optional[str] = Query(default=None, alias="status"),
    _: None = Depends(require_permission("report", "read")),
):
    """
    List generated reports.
    """
    from app.services.report_service import ReportService
    
    service = ReportService(db)
    
    reports, total = await service.list_reports(
        template_id=template_id,
        status=status_filter,
        offset=pagination.offset,
        limit=pagination.limit,
        sort_by=sorting.sort_by or "created_at",
        sort_order=sorting.sort_order or "desc",
    )
    
    return PaginatedResponse.create(
        items=reports,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{report_id}", response_model=GeneratedReportResponse)
async def get_generated_report(
    report_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("report", "read")),
):
    """
    Get a generated report by ID.
    """
    from app.services.report_service import ReportService
    
    service = ReportService(db)
    report = await service.get_report(report_id)
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )
    
    return report


@router.post("/generate", response_model=GeneratedReportResponse, status_code=status.HTTP_201_CREATED)
async def generate_report(
    request: GenerateReportRequest,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("report", "generate")),
):
    """
    Generate a new report.
    """
    from app.services.report_service import ReportService
    
    service = ReportService(db)
    
    # Verify template exists
    template = await service.get_template(request.report_template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report template not found",
        )
    
    report = await service.generate_report(request, generated_by=user)
    
    return report


@router.get("/{report_id}/download")
async def download_report(
    report_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("report", "read")),
):
    """
    Download a generated report file.
    """
    from app.services.report_service import ReportService
    
    service = ReportService(db)
    
    report = await service.get_report(report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )
    
    if report.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Report is not ready for download",
        )
    
    file_content, filename, media_type = await service.download_report(report)
    
    return StreamingResponse(
        iter([file_content]),
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


# =============================================================================
# Report Schedules
# =============================================================================

@router.post("/schedules", response_model=SuccessMessage, status_code=status.HTTP_201_CREATED)
async def create_report_schedule(
    data: ReportScheduleCreate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("report", "create")),
):
    """
    Create a scheduled report generation job.
    """
    from app.services.report_service import ReportService
    
    service = ReportService(db)
    
    # Verify template exists
    template = await service.get_template(data.report_template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report template not found",
        )
    
    await service.create_schedule(data, created_by=user)
    
    return SuccessMessage(message="Report schedule created")
