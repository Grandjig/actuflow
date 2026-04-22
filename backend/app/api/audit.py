"""Audit Log API Routes."""

import uuid
from typing import Annotated, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_async_session
from app.dependencies import get_current_user, require_permission
from app.models.user import User
from app.models.audit_log import AuditLog

router = APIRouter()


@router.get("")
async def list_audit_logs(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("audit", "read"))],
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    user_id: Optional[uuid.UUID] = None,
    action: Optional[str] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[uuid.UUID] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
):
    """List audit logs."""
    query = select(AuditLog).options(selectinload(AuditLog.user))
    
    if user_id:
        query = query.where(AuditLog.user_id == user_id)
    
    if action:
        query = query.where(AuditLog.action == action)
    
    if resource_type:
        query = query.where(AuditLog.resource_type == resource_type)
    
    if resource_id:
        query = query.where(AuditLog.resource_id == resource_id)
    
    if date_from:
        query = query.where(AuditLog.created_at >= date_from)
    
    if date_to:
        query = query.where(AuditLog.created_at <= date_to)
    
    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Paginate
    query = query.order_by(AuditLog.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    logs = list(result.unique().scalars().all())
    
    return {
        "items": [{
            "id": str(log.id),
            "user_id": str(log.user_id) if log.user_id else None,
            "user_email": log.user.email if log.user else None,
            "action": log.action,
            "resource_type": log.resource_type,
            "resource_id": str(log.resource_id) if log.resource_id else None,
            "old_values": log.old_values,
            "new_values": log.new_values,
            "ip_address": log.ip_address,
            "created_at": log.created_at.isoformat(),
        } for log in logs],
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size,
    }


@router.get("/actions")
async def list_action_types(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("audit", "read"))],
):
    """List distinct action types."""
    result = await db.execute(
        select(AuditLog.action).distinct()
    )
    return [row[0] for row in result.all()]


@router.get("/resource-types")
async def list_resource_types(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("audit", "read"))],
):
    """List distinct resource types."""
    result = await db.execute(
        select(AuditLog.resource_type).distinct()
    )
    return [row[0] for row in result.all()]
