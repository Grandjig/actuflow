"""
Audit Log Schemas
=================

Schemas for audit trail.
"""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AuditLogResponse(BaseModel):
    """Schema for audit log entry."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    timestamp: datetime
    
    user_id: Optional[UUID] = None
    user_email: Optional[str] = None
    
    action: str
    resource_type: str
    resource_id: Optional[UUID] = None
    resource_name: Optional[str] = None
    
    old_values: Optional[dict[str, Any]] = None
    new_values: Optional[dict[str, Any]] = None
    
    description: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    request_id: Optional[UUID] = None


class AuditLogListItem(BaseModel):
    """Simplified audit log for list views."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    timestamp: datetime
    user_email: Optional[str] = None
    action: str
    resource_type: str
    resource_name: Optional[str] = None
    description: Optional[str] = None


class AuditLogFilter(BaseModel):
    """Filter parameters for audit log."""
    
    user_id: Optional[UUID] = None
    action: Optional[str] = None
    action_in: Optional[list[str]] = None
    resource_type: Optional[str] = None
    resource_id: Optional[UUID] = None
    
    timestamp_from: Optional[datetime] = None
    timestamp_to: Optional[datetime] = None
    
    ip_address: Optional[str] = None
    
    search: Optional[str] = None
