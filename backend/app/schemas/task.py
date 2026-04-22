"""Task Schemas."""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class TaskCreate(BaseModel):
    """Schema for creating a task."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    task_type: str = "general"
    priority: str = "medium"
    assigned_to_id: Optional[UUID] = None
    due_date: Optional[date] = None
    related_resource_type: Optional[str] = None
    related_resource_id: Optional[UUID] = None


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to_id: Optional[UUID] = None
    due_date: Optional[date] = None


class TaskResponse(BaseModel):
    """Schema for task response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    title: str
    description: Optional[str] = None
    task_type: str
    status: str
    priority: str
    assigned_to_id: Optional[UUID] = None
    assigned_by_id: Optional[UUID] = None
    due_date: Optional[date] = None
    completed_at: Optional[datetime] = None
    related_resource_type: Optional[str] = None
    related_resource_id: Optional[UUID] = None
    auto_generated: bool = False
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    """Paginated task list response."""
    items: list[TaskResponse]
    total: int
    page: int
    page_size: int
    pages: int
