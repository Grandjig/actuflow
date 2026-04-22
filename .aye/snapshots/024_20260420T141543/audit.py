"""
Audit API Routes
================

Audit log viewing.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import func, select

from app.dependencies import (
    DBSession,
    CurrentUser,
    Pagination,
    require_permission,
)
from app.models.audit_log import AuditLog
from app.schemas.common import PaginatedResponse

router = APIRouter()


class AuditLogResponse(BaseModel):
    id: UUID
    timestamp: datetime
    user_id: Optional[UUID]
    user_email: Optional[str]
    action: str
    resource_type: str
    resource_id: Optional[UUID]
    resource_name: Optional[str]
    old_values: Optional[dict]
    new_values: Optional[dict]
    ip_address: Optional[str]

    class Config:
        from_attributes = True


@router.get("", response_model=PaginatedResponse[AuditLogResponse])
async def list_audit_logs(
    db: DBSession,
    pagination: Pagination,
    _: CurrentUser = Depends(require_permission("audit", "read")),
    user_id: Optional[UUID] = Query(None),
    action: Optional[str] = Query(None),
    resource_type: Optional[str] = Query(None),
    resource_id: Optional[UUID] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
):
    """List audit logs with filtering."""
    query = select(AuditLog)

    if user_id:
        query = query.where(AuditLog.user_id == user_id)

    if action:
        query = query.where(AuditLog.action == action)

    if resource_type:
        query = query.where(AuditLog.resource_type == resource_type)

    if resource_id:
        query = query.where(AuditLog.resource_id == resource_id)

    if date_from:
        query = query.where(AuditLog.timestamp >= date_from)

    if date_to:
        query = query.where(AuditLog.timestamp <= date_to)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = (
        query
        .offset(pagination.offset)
        .limit(pagination.page_size)
        .order_by(AuditLog.timestamp.desc())
    )
    result = await db.execute(query)
    logs = result.scalars().all()

    return PaginatedResponse.create(
        items=logs,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/resource/{resource_type}/{resource_id}", response_model=list[AuditLogResponse])
async def get_resource_history(
    db: DBSession,
    resource_type: str,
    resource_id: UUID,
    _: CurrentUser = Depends(require_permission("audit", "read")),
):
    """Get audit history for a specific resource."""
    result = await db.execute(
        select(AuditLog)
        .where(AuditLog.resource_type == resource_type)
        .where(AuditLog.resource_id == resource_id)
        .order_by(AuditLog.timestamp.desc())
        .limit(100)
    )
    return result.scalars().all()
