"""
Task Schemas
============

Schemas for workflow tasks.
"""

from datetime import date, datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    """Base task fields."""
    
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    task_type: str = Field(
        pattern="^(approval|review|data_entry|follow_up|other)$"
    )
    priority: str = Field(
        default="medium",
        pattern="^(low|medium|high|urgent)$"
    )
    due_date: Optional[date] = None


class TaskCreate(TaskBase):
    """Schema for creating a task."""
    
    assigned_to_id: Optional[UUID] = None
    related_resource_type: Optional[str] = Field(default=None, max_length=100)
    related_resource_id: Optional[UUID] = None
    task_data: Optional[dict[str, Any]] = None


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    priority: Optional[str] = Field(
        default=None,
        pattern="^(low|medium|high|urgent)$"
    )
    due_date: Optional[date] = None
    task_data: Optional[dict[str, Any]] = None


class TaskStatusUpdate(BaseModel):
    """Schema for updating task status."""
    
    status: str = Field(pattern="^(open|in_progress|completed|cancelled)$")
    completion_notes: Optional[str] = None


class TaskAssignment(BaseModel):
    """Schema for task assignment."""
    
    assigned_to_id: UUID


class TaskResponse(TaskBase):
    """Schema for task response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    status: str
    
    assigned_to_id: Optional[UUID] = None
    assigned_to_name: Optional[str] = None
    assigned_by_id: Optional[UUID] = None
    assigned_at: Optional[datetime] = None
    
    completed_at: Optional[datetime] = None
    completed_by_id: Optional[UUID] = None
    completion_notes: Optional[str] = None
    
    related_resource_type: Optional[str] = None
    related_resource_id: Optional[UUID] = None
    
    auto_generated: bool
    automation_rule_id: Optional[UUID] = None
    
    task_data: Optional[dict[str, Any]] = None
    
    created_at: datetime
    updated_at: datetime
    
    # Computed
    is_overdue: Optional[bool] = None


class TaskListItem(BaseModel):
    """Simplified task for list views."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    title: str
    task_type: str
    status: str
    priority: str
    due_date: Optional[date] = None
    assigned_to_name: Optional[str] = None
    is_overdue: bool = False


class TaskFilter(BaseModel):
    """Filter parameters for task list."""
    
    task_type: Optional[str] = None
    status: Optional[str] = None
    status_in: Optional[list[str]] = None
    priority: Optional[str] = None
    assigned_to_id: Optional[UUID] = None
    assigned_by_id: Optional[UUID] = None
    
    due_date_from: Optional[date] = None
    due_date_to: Optional[date] = None
    overdue_only: Optional[bool] = None
    
    related_resource_type: Optional[str] = None
    related_resource_id: Optional[UUID] = None
    
    search: Optional[str] = None
