"""
Automation Schemas
==================

Schemas for scheduled jobs and automation rules.
"""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# =============================================================================
# Scheduled Job Schemas
# =============================================================================

class ScheduledJobBase(BaseModel):
    """Base scheduled job fields."""
    
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    job_type: str = Field(
        pattern="^(calculation|report|import|data_check|cleanup)$"
    )
    cron_expression: str = Field(max_length=100)
    timezone: str = Field(default="UTC", max_length=50)


class ScheduledJobCreate(ScheduledJobBase):
    """Schema for creating a scheduled job."""
    
    config: dict[str, Any] = Field(description="Job configuration")
    is_active: bool = True
    max_retries: int = Field(default=3, ge=0, le=10)
    retry_delay_minutes: int = Field(default=5, ge=1, le=60)
    notify_on_success: bool = False
    notify_on_failure: bool = True
    notification_emails: Optional[list[str]] = None


class ScheduledJobUpdate(BaseModel):
    """Schema for updating a scheduled job."""
    
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    cron_expression: Optional[str] = Field(default=None, max_length=100)
    timezone: Optional[str] = Field(default=None, max_length=50)
    config: Optional[dict[str, Any]] = None
    is_active: Optional[bool] = None
    max_retries: Optional[int] = Field(default=None, ge=0, le=10)
    retry_delay_minutes: Optional[int] = Field(default=None, ge=1, le=60)
    notify_on_success: Optional[bool] = None
    notify_on_failure: Optional[bool] = None
    notification_emails: Optional[list[str]] = None


class ScheduledJobResponse(ScheduledJobBase):
    """Schema for scheduled job response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    config: dict[str, Any]
    is_active: bool
    
    last_run_at: Optional[datetime] = None
    last_run_status: Optional[str] = None
    next_run_at: Optional[datetime] = None
    
    max_retries: int
    retry_delay_minutes: int
    notify_on_success: bool
    notify_on_failure: bool
    notification_emails: Optional[list[str]] = None
    
    created_at: datetime
    updated_at: datetime
    created_by_id: Optional[UUID] = None


class ScheduledJobListItem(BaseModel):
    """Simplified scheduled job for list views."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    job_type: str
    cron_expression: str
    is_active: bool
    last_run_at: Optional[datetime] = None
    last_run_status: Optional[str] = None
    next_run_at: Optional[datetime] = None


# =============================================================================
# Job Execution Schemas
# =============================================================================

class JobExecutionResponse(BaseModel):
    """Schema for job execution response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    scheduled_job_id: UUID
    
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    
    status: str
    attempt_number: int
    
    result_summary: Optional[dict[str, Any]] = None
    created_resources: Optional[dict[str, Any]] = None
    
    error_message: Optional[str] = None
    error_details: Optional[dict[str, Any]] = None


class JobExecutionListItem(BaseModel):
    """Simplified job execution for list views."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    status: str
    attempt_number: int


# =============================================================================
# Automation Rule Schemas
# =============================================================================

class AutomationRuleBase(BaseModel):
    """Base automation rule fields."""
    
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    trigger_type: str = Field(max_length=50)
    action_type: str = Field(max_length=50)


class AutomationRuleCreate(AutomationRuleBase):
    """Schema for creating an automation rule."""
    
    trigger_config: dict[str, Any] = Field(description="Trigger conditions")
    action_config: dict[str, Any] = Field(description="Action configuration")
    is_active: bool = True
    priority: int = Field(default=100, ge=1)
    cooldown_minutes: Optional[int] = Field(default=None, ge=1)
    max_executions_per_day: Optional[int] = Field(default=None, ge=1)


class AutomationRuleUpdate(BaseModel):
    """Schema for updating an automation rule."""
    
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    trigger_config: Optional[dict[str, Any]] = None
    action_config: Optional[dict[str, Any]] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = Field(default=None, ge=1)
    cooldown_minutes: Optional[int] = Field(default=None, ge=1)
    max_executions_per_day: Optional[int] = Field(default=None, ge=1)


class AutomationRuleResponse(AutomationRuleBase):
    """Schema for automation rule response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    trigger_config: dict[str, Any]
    action_config: dict[str, Any]
    is_active: bool
    priority: int
    cooldown_minutes: Optional[int] = None
    max_executions_per_day: Optional[int] = None
    
    execution_count: int
    last_executed_at: Optional[str] = None
    
    created_at: datetime
    updated_at: datetime
    created_by_id: Optional[UUID] = None


class AutomationRuleListItem(BaseModel):
    """Simplified automation rule for list views."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    trigger_type: str
    action_type: str
    is_active: bool
    execution_count: int
    last_executed_at: Optional[str] = None


class AutomationRuleTestRequest(BaseModel):
    """Request to test an automation rule."""
    
    test_data: dict[str, Any] = Field(
        description="Sample event data to test against"
    )


class AutomationRuleTestResponse(BaseModel):
    """Result of automation rule test."""
    
    would_trigger: bool
    matched_conditions: list[str]
    unmatched_conditions: list[str]
    action_preview: Optional[dict[str, Any]] = None
