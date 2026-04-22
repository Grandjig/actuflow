"""
Automation API Routes
=====================

Scheduled jobs and automation rules.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from app.dependencies import DBSession, CurrentUser, Pagination, require_permission
from app.models.scheduled_job import ScheduledJob
from app.models.job_execution import JobExecution
from app.models.automation_rule import AutomationRule
from app.schemas.common import PaginatedResponse, SuccessResponse

router = APIRouter()


# Schemas
class ScheduledJobCreate(BaseModel):
    name: str
    description: Optional[str] = None
    job_type: str
    cron_expression: str
    config: dict = {}
    is_active: bool = True


class ScheduledJobResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    job_type: str
    cron_expression: str
    config: dict
    is_active: bool
    last_run_at: Optional[datetime]
    last_run_status: Optional[str]
    next_run_at: Optional[datetime]
    created_by_id: Optional[UUID]
    created_at: datetime

    class Config:
        from_attributes = True


class JobExecutionResponse(BaseModel):
    id: UUID
    scheduled_job_id: UUID
    started_at: datetime
    completed_at: Optional[datetime]
    status: str
    result_summary: Optional[dict]
    error_message: Optional[str]

    class Config:
        from_attributes = True


class AutomationRuleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    trigger_type: str
    trigger_config: dict
    action_type: str
    action_config: dict
    is_active: bool = True


class AutomationRuleResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    trigger_type: str
    trigger_config: dict
    action_type: str
    action_config: dict
    is_active: bool
    created_by_id: Optional[UUID]
    created_at: datetime

    class Config:
        from_attributes = True


# Scheduled Jobs
@router.get("/scheduled-jobs", response_model=PaginatedResponse[ScheduledJobResponse])
async def list_scheduled_jobs(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    is_active: Optional[bool] = Query(None),
    job_type: Optional[str] = Query(None),
):
    """List scheduled jobs."""
    query = select(ScheduledJob).where(ScheduledJob.is_deleted == False)
    
    if is_active is not None:
        query = query.where(ScheduledJob.is_active == is_active)
    if job_type:
        query = query.where(ScheduledJob.job_type == job_type)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.offset(pagination.offset).limit(pagination.page_size).order_by(ScheduledJob.name)
    result = await db.execute(query)
    jobs = result.scalars().all()

    return PaginatedResponse.create(
        items=jobs,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.post("/scheduled-jobs", response_model=ScheduledJobResponse, status_code=status.HTTP_201_CREATED)
async def create_scheduled_job(
    db: DBSession,
    data: ScheduledJobCreate,
    current_user: CurrentUser = Depends(require_permission("automation", "create")),
):
    """Create a scheduled job."""
    job = ScheduledJob(
        **data.model_dump(),
        created_by_id=current_user.id,
    )
    db.add(job)
    await db.flush()
    await db.refresh(job)
    return job


@router.get("/scheduled-jobs/{job_id}", response_model=ScheduledJobResponse)
async def get_scheduled_job(
    db: DBSession,
    job_id: UUID,
    current_user: CurrentUser,
):
    """Get a scheduled job."""
    result = await db.execute(
        select(ScheduledJob).where(ScheduledJob.id == job_id).where(ScheduledJob.is_deleted == False)
    )
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job


@router.get("/scheduled-jobs/{job_id}/executions", response_model=list[JobExecutionResponse])
async def get_job_executions(
    db: DBSession,
    job_id: UUID,
    current_user: CurrentUser,
    limit: int = Query(20, le=100),
):
    """Get execution history for a job."""
    result = await db.execute(
        select(JobExecution)
        .where(JobExecution.scheduled_job_id == job_id)
        .order_by(JobExecution.started_at.desc())
        .limit(limit)
    )
    return result.scalars().all()


@router.post("/scheduled-jobs/{job_id}/run-now", response_model=SuccessResponse)
async def trigger_job_now(
    db: DBSession,
    job_id: UUID,
    current_user: CurrentUser = Depends(require_permission("automation", "update")),
):
    """Trigger immediate execution of a job."""
    result = await db.execute(
        select(ScheduledJob).where(ScheduledJob.id == job_id).where(ScheduledJob.is_deleted == False)
    )
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    # TODO: Dispatch Celery task

    return SuccessResponse(message="Job triggered")


@router.delete("/scheduled-jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scheduled_job(
    db: DBSession,
    job_id: UUID,
    _: CurrentUser = Depends(require_permission("automation", "delete")),
):
    """Delete a scheduled job."""
    result = await db.execute(
        select(ScheduledJob).where(ScheduledJob.id == job_id).where(ScheduledJob.is_deleted == False)
    )
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    job.is_deleted = True


# Automation Rules
@router.get("/rules", response_model=PaginatedResponse[AutomationRuleResponse])
async def list_automation_rules(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    is_active: Optional[bool] = Query(None),
):
    """List automation rules."""
    query = select(AutomationRule).where(AutomationRule.is_deleted == False)
    
    if is_active is not None:
        query = query.where(AutomationRule.is_active == is_active)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.offset(pagination.offset).limit(pagination.page_size).order_by(AutomationRule.name)
    result = await db.execute(query)
    rules = result.scalars().all()

    return PaginatedResponse.create(
        items=rules,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.post("/rules", response_model=AutomationRuleResponse, status_code=status.HTTP_201_CREATED)
async def create_automation_rule(
    db: DBSession,
    data: AutomationRuleCreate,
    current_user: CurrentUser = Depends(require_permission("automation", "create")),
):
    """Create an automation rule."""
    rule = AutomationRule(
        **data.model_dump(),
        created_by_id=current_user.id,
    )
    db.add(rule)
    await db.flush()
    await db.refresh(rule)
    return rule


@router.get("/rules/{rule_id}", response_model=AutomationRuleResponse)
async def get_automation_rule(
    db: DBSession,
    rule_id: UUID,
    current_user: CurrentUser,
):
    """Get an automation rule."""
    result = await db.execute(
        select(AutomationRule).where(AutomationRule.id == rule_id).where(AutomationRule.is_deleted == False)
    )
    rule = result.scalar_one_or_none()
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")
    return rule


@router.delete("/rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_automation_rule(
    db: DBSession,
    rule_id: UUID,
    _: CurrentUser = Depends(require_permission("automation", "delete")),
):
    """Delete an automation rule."""
    result = await db.execute(
        select(AutomationRule).where(AutomationRule.id == rule_id).where(AutomationRule.is_deleted == False)
    )
    rule = result.scalar_one_or_none()
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")
    rule.is_deleted = True
