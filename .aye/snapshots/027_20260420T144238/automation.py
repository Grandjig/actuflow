"""Automation API Routes."""

import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.dependencies import get_current_user, require_permission
from app.models.user import User
from app.models.scheduled_job import ScheduledJob
from app.models.job_execution import JobExecution
from app.models.automation_rule import AutomationRule
from calculation_engine.scheduler.scheduler_service import SchedulerService

router = APIRouter()


# ============================================================================
# Scheduled Jobs
# ============================================================================

@router.get("/jobs")
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
    
    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Paginate
    query = query.order_by(ScheduledJob.created_at.desc())
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


@router.get("/jobs/{job_id}")
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
            detail="Job not found",
        )
    
    return job


@router.post("/jobs")
async def create_scheduled_job(
    data: dict,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("automation", "create"))],
):
    """Create a scheduled job."""
    scheduler = SchedulerService(db)
    
    job = await scheduler.create_job(
        name=data["name"],
        job_type=data["job_type"],
        cron_expression=data["cron_expression"],
        config=data.get("config", {}),
        created_by_id=current_user.id,
    )
    
    return job


@router.put("/jobs/{job_id}")
async def update_scheduled_job(
    job_id: uuid.UUID,
    data: dict,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("automation", "update"))],
):
    """Update a scheduled job."""
    scheduler = SchedulerService(db)
    
    try:
        job = await scheduler.update_job(job_id, **data)
        return job
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
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
            detail="Job not found",
        )
    
    job.is_deleted = True
    await db.flush()


@router.post("/jobs/{job_id}/run")
async def trigger_job_now(
    job_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("automation", "update"))],
):
    """Trigger a job to run immediately."""
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
            detail="Job not found",
        )
    
    # Queue task
    from calculation_engine.tasks.scheduled_job_task import execute_scheduled_job
    
    # Create execution record
    from datetime import datetime
    execution = JobExecution(
        scheduled_job_id=job.id,
        status="queued",
    )
    db.add(execution)
    await db.flush()
    
    execute_scheduled_job.delay(str(job.id), str(execution.id))
    
    return {"execution_id": str(execution.id), "status": "queued"}


@router.get("/jobs/{job_id}/executions")
async def get_job_executions(
    job_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("automation", "read"))],
    limit: int = Query(20, ge=1, le=100),
):
    """Get executions for a job."""
    result = await db.execute(
        select(JobExecution)
        .where(JobExecution.scheduled_job_id == job_id)
        .order_by(JobExecution.started_at.desc())
        .limit(limit)
    )
    return list(result.scalars().all())


# ============================================================================
# Automation Rules
# ============================================================================

@router.get("/rules")
async def list_automation_rules(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("automation", "read"))],
    is_active: Optional[bool] = None,
):
    """List automation rules."""
    query = select(AutomationRule).where(AutomationRule.is_deleted == False)
    
    if is_active is not None:
        query = query.where(AutomationRule.is_active == is_active)
    
    query = query.order_by(AutomationRule.name)
    
    result = await db.execute(query)
    return list(result.scalars().all())


@router.get("/rules/{rule_id}")
async def get_automation_rule(
    rule_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("automation", "read"))],
):
    """Get an automation rule."""
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
            detail="Rule not found",
        )
    
    return rule


@router.post("/rules")
async def create_automation_rule(
    data: dict,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("automation", "create"))],
):
    """Create an automation rule."""
    rule = AutomationRule(
        name=data["name"],
        description=data.get("description"),
        trigger_type=data["trigger_type"],
        trigger_config=data.get("trigger_config", {}),
        action_type=data["action_type"],
        action_config=data.get("action_config", {}),
        is_active=data.get("is_active", True),
        created_by_id=current_user.id,
    )
    db.add(rule)
    await db.flush()
    await db.refresh(rule)
    
    return rule


@router.put("/rules/{rule_id}")
async def update_automation_rule(
    rule_id: uuid.UUID,
    data: dict,
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
            detail="Rule not found",
        )
    
    for key, value in data.items():
        if hasattr(rule, key) and value is not None:
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
            detail="Rule not found",
        )
    
    rule.is_deleted = True
    await db.flush()
