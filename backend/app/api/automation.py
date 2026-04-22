"""Automation API Routes."""

import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.dependencies import get_current_user, require_permission
from app.models.user import User
from app.models.scheduled_job import ScheduledJob
from app.models.job_execution import JobExecution
from app.models.automation_rule import AutomationRule
from app.services.audit_service import AuditService
from app.schemas.common import PaginatedResponse

router = APIRouter()


# === Scheduled Jobs ===

class ScheduledJobCreate(BaseModel):
    name: str
    description: Optional[str] = None
    job_type: str
    cron_expression: str
    config: dict = {}
    is_active: bool = True


class ScheduledJobResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    job_type: str
    cron_expression: str
    config: dict
    is_active: bool
    last_run: Optional[str]
    next_run: Optional[str]
    created_by_id: uuid.UUID
    created_at: str

    class Config:
        from_attributes = True


@router.get("/scheduled-jobs")
async def list_scheduled_jobs(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("automation", "read"))],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    is_active: Optional[bool] = None,
    job_type: Optional[str] = None,
):
    """List scheduled jobs."""
    query = select(ScheduledJob).where(ScheduledJob.is_deleted == False)
    
    if is_active is not None:
        query = query.where(ScheduledJob.is_active == is_active)
    if job_type:
        query = query.where(ScheduledJob.job_type == job_type)
    
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    query = query.order_by(ScheduledJob.name)
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    jobs = list(result.scalars().all())
    
    return {
        "items": jobs,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size,
    }


@router.post("/scheduled-jobs", status_code=status.HTTP_201_CREATED)
async def create_scheduled_job(
    data: ScheduledJobCreate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("automation", "create"))],
):
    """Create a scheduled job."""
    audit_service = AuditService(db)
    
    job = ScheduledJob(
        **data.model_dump(),
        created_by_id=current_user.id,
    )
    db.add(job)
    await db.flush()
    await db.refresh(job)
    
    await audit_service.log(
        user_id=current_user.id,
        action="create",
        resource_type="scheduled_job",
        resource_id=job.id,
        new_values=data.model_dump(),
    )
    
    return job


@router.get("/scheduled-jobs/{job_id}")
async def get_scheduled_job(
    job_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("automation", "read"))],
):
    """Get a scheduled job."""
    result = await db.execute(
        select(ScheduledJob).where(
            ScheduledJob.id == job_id,
            ScheduledJob.is_deleted == False,
        )
    )
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheduled job not found",
        )
    
    return job


@router.put("/scheduled-jobs/{job_id}")
async def update_scheduled_job(
    job_id: uuid.UUID,
    data: ScheduledJobCreate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("automation", "update"))],
):
    """Update a scheduled job."""
    result = await db.execute(
        select(ScheduledJob).where(
            ScheduledJob.id == job_id,
            ScheduledJob.is_deleted == False,
        )
    )
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheduled job not found",
        )
    
    for key, value in data.model_dump().items():
        setattr(job, key, value)
    
    await db.flush()
    await db.refresh(job)
    
    return job


@router.delete("/scheduled-jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scheduled_job(
    job_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("automation", "delete"))],
):
    """Delete a scheduled job."""
    result = await db.execute(
        select(ScheduledJob).where(
            ScheduledJob.id == job_id,
            ScheduledJob.is_deleted == False,
        )
    )
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheduled job not found",
        )
    
    job.is_deleted = True
    await db.flush()


@router.post("/scheduled-jobs/{job_id}/run-now")
async def run_job_now(
    job_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("automation", "update"))],
):
    """Trigger immediate execution of a scheduled job."""
    result = await db.execute(
        select(ScheduledJob).where(
            ScheduledJob.id == job_id,
            ScheduledJob.is_deleted == False,
        )
    )
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheduled job not found",
        )
    
    # TODO: Dispatch Celery task
    
    return {
        "message": "Job execution triggered",
        "job_id": str(job_id),
    }


@router.get("/scheduled-jobs/{job_id}/executions")
async def get_job_executions(
    job_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("automation", "read"))],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """Get execution history for a scheduled job."""
    query = select(JobExecution).where(JobExecution.scheduled_job_id == job_id)
    
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    query = query.order_by(JobExecution.started_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    executions = list(result.scalars().all())
    
    return {
        "items": executions,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


# === Automation Rules ===

class AutomationRuleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    trigger_type: str
    trigger_config: dict = {}
    action_type: str
    action_config: dict = {}
    is_active: bool = True


@router.get("/rules")
async def list_automation_rules(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("automation", "read"))],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    is_active: Optional[bool] = None,
):
    """List automation rules."""
    query = select(AutomationRule).where(AutomationRule.is_deleted == False)
    
    if is_active is not None:
        query = query.where(AutomationRule.is_active == is_active)
    
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    query = query.order_by(AutomationRule.name)
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    rules = list(result.scalars().all())
    
    return {
        "items": rules,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.post("/rules", status_code=status.HTTP_201_CREATED)
async def create_automation_rule(
    data: AutomationRuleCreate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("automation", "create"))],
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


@router.put("/rules/{rule_id}")
async def update_automation_rule(
    rule_id: uuid.UUID,
    data: AutomationRuleCreate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("automation", "update"))],
):
    """Update an automation rule."""
    result = await db.execute(
        select(AutomationRule).where(
            AutomationRule.id == rule_id,
            AutomationRule.is_deleted == False,
        )
    )
    rule = result.scalar_one_or_none()
    
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Automation rule not found",
        )
    
    for key, value in data.model_dump().items():
        setattr(rule, key, value)
    
    await db.flush()
    await db.refresh(rule)
    
    return rule


@router.delete("/rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_automation_rule(
    rule_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("automation", "delete"))],
):
    """Delete an automation rule."""
    result = await db.execute(
        select(AutomationRule).where(
            AutomationRule.id == rule_id,
            AutomationRule.is_deleted == False,
        )
    )
    rule = result.scalar_one_or_none()
    
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Automation rule not found",
        )
    
    rule.is_deleted = True
    await db.flush()
