"""
Tasks API Routes
================

Task management endpoints.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import func, select, or_
from sqlalchemy.orm import selectinload

from app.dependencies import (
    DBSession,
    CurrentUser,
    Pagination,
    require_permission,
)
from app.models.task import Task
from app.schemas.common import PaginatedResponse, SuccessResponse

router = APIRouter()


# Schemas
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    task_type: str = "general"
    priority: str = "medium"
    assigned_to_id: Optional[UUID] = None
    due_date: Optional[str] = None
    related_resource_type: Optional[str] = None
    related_resource_id: Optional[UUID] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to_id: Optional[UUID] = None
    due_date: Optional[str] = None
    completion_notes: Optional[str] = None


class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    task_type: str
    status: str
    priority: str
    assigned_to_id: Optional[UUID]
    assigned_by_id: Optional[UUID]
    due_date: Optional[str]
    completed_at: Optional[datetime]
    related_resource_type: Optional[str]
    related_resource_id: Optional[UUID]
    is_overdue: bool
    auto_generated: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


@router.get("", response_model=PaginatedResponse[TaskResponse])
async def list_tasks(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    status_filter: Optional[str] = Query(None, alias="status"),
    priority: Optional[str] = Query(None),
    assigned_to_me: bool = Query(False),
    overdue_only: bool = Query(False),
):
    """List tasks."""
    query = select(Task).where(Task.is_deleted == False)

    if status_filter:
        query = query.where(Task.status == status_filter)

    if priority:
        query = query.where(Task.priority == priority)

    if assigned_to_me:
        query = query.where(Task.assigned_to_id == current_user.id)

    if overdue_only:
        from datetime import date
        query = query.where(
            Task.due_date < date.today(),
            Task.status != "completed"
        )

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = (
        query
        .offset(pagination.offset)
        .limit(pagination.page_size)
        .order_by(Task.due_date.asc().nulls_last(), Task.priority.desc())
    )
    result = await db.execute(query)
    tasks = result.scalars().all()

    items = [
        TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            task_type=task.task_type,
            status=task.status,
            priority=task.priority,
            assigned_to_id=task.assigned_to_id,
            assigned_by_id=task.assigned_by_id,
            due_date=str(task.due_date) if task.due_date else None,
            completed_at=task.completed_at,
            related_resource_type=task.related_resource_type,
            related_resource_id=task.related_resource_id,
            is_overdue=task.is_overdue,
            auto_generated=task.auto_generated,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
        for task in tasks
    ]

    return PaginatedResponse.create(
        items=items,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/my", response_model=list[TaskResponse])
async def get_my_tasks(
    db: DBSession,
    current_user: CurrentUser,
    status_filter: Optional[str] = Query(None, alias="status"),
):
    """Get tasks assigned to the current user."""
    query = (
        select(Task)
        .where(Task.assigned_to_id == current_user.id)
        .where(Task.is_deleted == False)
    )

    if status_filter:
        query = query.where(Task.status == status_filter)
    else:
        query = query.where(Task.status != "completed")

    query = query.order_by(Task.due_date.asc().nulls_last())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    db: DBSession,
    task_id: UUID,
    current_user: CurrentUser,
):
    """Get a task by ID."""
    result = await db.execute(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.is_deleted == False)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    db: DBSession,
    data: TaskCreate,
    current_user: CurrentUser = Depends(require_permission("task", "create")),
):
    """Create a new task."""
    from datetime import date as d
    
    due_date = None
    if data.due_date:
        due_date = d.fromisoformat(data.due_date)

    task = Task(
        title=data.title,
        description=data.description,
        task_type=data.task_type,
        priority=data.priority,
        status="todo",
        assigned_to_id=data.assigned_to_id,
        assigned_by_id=current_user.id,
        due_date=due_date,
        related_resource_type=data.related_resource_type,
        related_resource_id=data.related_resource_id,
        auto_generated=False,
    )
    db.add(task)
    await db.flush()
    await db.refresh(task)

    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    db: DBSession,
    task_id: UUID,
    data: TaskUpdate,
    current_user: CurrentUser,
):
    """Update a task."""
    result = await db.execute(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.is_deleted == False)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    update_data = data.model_dump(exclude_unset=True)

    if "status" in update_data and update_data["status"] == "completed":
        update_data["completed_at"] = datetime.utcnow()

    if "due_date" in update_data and update_data["due_date"]:
        from datetime import date as d
        update_data["due_date"] = d.fromisoformat(update_data["due_date"])

    for field, value in update_data.items():
        setattr(task, field, value)

    await db.flush()
    await db.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    db: DBSession,
    task_id: UUID,
    current_user: CurrentUser = Depends(require_permission("task", "delete")),
):
    """Soft delete a task."""
    result = await db.execute(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.is_deleted == False)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    task.is_deleted = True
