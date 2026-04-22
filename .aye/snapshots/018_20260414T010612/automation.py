"""Automation API Routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from app.dependencies import CurrentUser, DBSession, Pagination, require_permission
from app.exceptions import NotFoundError
from app.models.user import User
from app.schemas.common import PaginatedResponse, SuccessResponse
from app.services.automation_service import AutomationService

router = APIRouter()


# Schemas
class ScheduledJobCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    job_type: str
    cron_expression: str
    config: dict = {}


class ScheduledJobUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    cron_expression: str | None = None
    config: dict | None = None
    is_active: bool | None = None


class ScheduledJobResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    job_type: str
    cron_expression: str
    config: dict
    is_active: bool
    last_run: str | None
    last_run_status: str | None
    next_run: str | None
    
    class Config:
        from_attributes = True


class AutomationRuleCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    trigger_type: str
    trigger_config: dict = {}
    action_type: str
    action_config: dict = {}


class AutomationRuleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    trigger_config: dict | None = None
    action_config: dict | None = None
    is_active: bool | None = None


class AutomationRuleResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    trigger_type: str
    trigger_config: dict
    action_type: str
    action_config: dict
    is_active: bool
    execution_count: int
    
    class Config:
        from_attributes = True


class JobExecutionResponse(BaseModel):
    id: UUID
    scheduled_job_id: UUID
    started_at: str
    completed_at: str | None
    status: str
    duration_seconds: float | None
    error_message: str | None
    
    class Config:
        from_attributes = True


# Scheduled Jobs Routes

@router.get("/scheduled-jobs", response_model=PaginatedResponse[ScheduledJobResponse])
async def list_scheduled_jobs(
    db: DBSession,
    current_user: Annotated[User, Depends(require_permission("automation", "read"))],
    pagination: Pagination,
    is_active: bool | None = Query(None),
    job_type: str | None = Query(None),
):
    """List scheduled jobs."""
    service = AutomationService(db)
    jobs, total = await service.list_scheduled_jobs(
        offset=pagination.offset,
        limit=pagination.limit,
        is_active=is_active,
        job_type=job_type,
    )
    
    total_pages = (total + pagination.page_size - 1) // pagination.page_size
    
    return PaginatedResponse(
        items=[ScheduledJobResponse.model_validate(j) for j in jobs],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        total_pages=total_pages,
        has_next=pagination.page < total_pages,
        has_prev=pagination.page > 1,
    )


@router.get("/scheduled-jobs/{job_id}", response_model=ScheduledJobResponse)
async def get_scheduled_job(
    job_id: UUID,
    db: DBSession,
    current_user: Annotated[User, Depends(require_permission("automation", "read"))],
):
    """Get a scheduled job."""
    service = AutomationService(db)
    job = await service.get_scheduled_job(job_id)
    
    if not job:
        raise NotFoundError("Scheduled job", job_id)
    
    return ScheduledJobResponse.model_validate(job)


@router.post("/scheduled-jobs", response_model=ScheduledJobResponse, status_code=201)
async def create_scheduled_job(
    data: ScheduledJobCreate,
    db: DBSession,
    current_user: Annotated[User, Depends(require_permission("automation", "create"))],
):
    """Create a scheduled job."""
    service = AutomationService(db)
    job = await service.create_scheduled_job(
        name=data.name,
        description=data.description,
        job_type=data.job_type,
        cron_expression=data.cron_expression,
        config=data.config,
        created_by=current_user,
    )
    return ScheduledJobResponse.model_validate(job)


@router.put("/scheduled-jobs/{job_id}", response_model=ScheduledJobResponse)
async def update_scheduled_job(
    job_id: UUID,
    data: ScheduledJobUpdate,
    db: DBSession,
    current_user: Annotated[User, Depends(require_permission("automation", "update"))],
):
    """Update a scheduled job."""
    service = AutomationService(db)
    
    job = await service.get_scheduled_job(job_id)
    if not job:
        raise NotFoundError("Scheduled job", job_id)
    
    updated = await service.update_scheduled_job(
        job,
        name=data.name,
        description=data.description,
        cron_expression=data.cron_expression,
        config=data.config,
        is_active=data.is_active,
    )
    return ScheduledJobResponse.model_validate(updated)


@router.delete("/scheduled-jobs/{job_id}", response_model=SuccessResponse)
async def delete_scheduled_job(
    job_id: UUID,
    db: DBSession,
    current_user: Annotated[User, Depends(require_permission("automation", "delete"))],
):
    """Delete a scheduled job."""
    service = AutomationService(db)
    
    job = await service.get_scheduled_job(job_id)
    if not job:
        raise NotFoundError("Scheduled job", job_id)
    
    await service.delete_scheduled_job(job)
    return SuccessResponse(message="Scheduled job deleted")


@router.get("/scheduled-jobs/{job_id}/executions", response_model=list[JobExecutionResponse])
async def get_job_executions(
    job_id: UUID,
    db: DBSession,
    current_user: Annotated[User, Depends(require_permission("automation", "read"))],
    limit: int = Query(20, le=100),
):
    """Get execution history for a job."""
    service = AutomationService(db)
    
    job = await service.get_scheduled_job(job_id)
    if not job:
        raise NotFoundError("Scheduled job", job_id)
    
    executions = await service.get_job_executions(job_id, limit)
    return [JobExecutionResponse.model_validate(e) for e in executions]


@router.post("/scheduled-jobs/{job_id}/run-now", response_model=SuccessResponse)
async def run_job_now(
    job_id: UUID,
    db: DBSession,
    current_user: Annotated[User, Depends(require_permission("automation", "create"))],
):
    """Trigger a scheduled job to run immediately."""
    service = AutomationService(db)
    
    job = await service.get_scheduled_job(job_id)
    if not job:
        raise NotFoundError("Scheduled job", job_id)
    
    # TODO: Dispatch Celery task
    # from calculation_engine.tasks import execute_scheduled_job
    # execute_scheduled_job.delay(str(job_id))
    
    return SuccessResponse(message="Job triggered")


# Automation Rules Routes

@router.get("/rules", response_model=PaginatedResponse[AutomationRuleResponse])
async def list_automation_rules(
    db: DBSession,
    current_user: Annotated[User, Depends(require_permission("automation", "read"))],
    pagination: Pagination,
    trigger_type: str | None = Query(None),
    is_active: bool | None = Query(None),
):
    """List automation rules."""
    service = AutomationService(db)
    rules, total = await service.list_automation_rules(
        offset=pagination.offset,
        limit=pagination.limit,
        trigger_type=trigger_type,
        is_active=is_active,
    )
    
    total_pages = (total + pagination.page_size - 1) // pagination.page_size
    
    return PaginatedResponse(
        items=[AutomationRuleResponse.model_validate(r) for r in rules],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        total_pages=total_pages,
        has_next=pagination.page < total_pages,
        has_prev=pagination.page > 1,
    )


@router.get("/rules/{rule_id}", response_model=AutomationRuleResponse)
async def get_automation_rule(
    rule_id: UUID,
    db: DBSession,
    current_user: Annotated[User, Depends(require_permission("automation", "read"))],
):
    """Get an automation rule."""
    service = AutomationService(db)
    rule = await service.get_automation_rule(rule_id)
    
    if not rule:
        raise NotFoundError("Automation rule", rule_id)
    
    return AutomationRuleResponse.model_validate(rule)


@router.post("/rules", response_model=AutomationRuleResponse, status_code=201)
async def create_automation_rule(
    data: AutomationRuleCreate,
    db: DBSession,
    current_user: Annotated[User, Depends(require_permission("automation", "create"))],
):
    """Create an automation rule."""
    service = AutomationService(db)
    rule = await service.create_automation_rule(
        name=data.name,
        description=data.description,
        trigger_type=data.trigger_type,
        trigger_config=data.trigger_config,
        action_type=data.action_type,
        action_config=data.action_config,
        created_by=current_user,
    )
    return AutomationRuleResponse.model_validate(rule)


@router.put("/rules/{rule_id}", response_model=AutomationRuleResponse)
async def update_automation_rule(
    rule_id: UUID,
    data: AutomationRuleUpdate,
    db: DBSession,
    current_user: Annotated[User, Depends(require_permission("automation", "update"))],
):
    """Update an automation rule."""
    service = AutomationService(db)
    
    rule = await service.get_automation_rule(rule_id)
    if not rule:
        raise NotFoundError("Automation rule", rule_id)
    
    updated = await service.update_automation_rule(
        rule,
        name=data.name,
        description=data.description,
        trigger_config=data.trigger_config,
        action_config=data.action_config,
        is_active=data.is_active,
    )
    return AutomationRuleResponse.model_validate(updated)


@router.delete("/rules/{rule_id}", response_model=SuccessResponse)
async def delete_automation_rule(
    rule_id: UUID,
    db: DBSession,
    current_user: Annotated[User, Depends(require_permission("automation", "delete"))],
):
    """Delete an automation rule."""
    service = AutomationService(db)
    
    rule = await service.get_automation_rule(rule_id)
    if not rule:
        raise NotFoundError("Automation rule", rule_id)
    
    await service.delete_automation_rule(rule)
    return SuccessResponse(message="Automation rule deleted")
