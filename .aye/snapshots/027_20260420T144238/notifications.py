"""
Notifications API Routes
========================

User notification management.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import func, select, update

from app.dependencies import DBSession, CurrentUser, Pagination
from app.models.notification import Notification
from app.schemas.common import PaginatedResponse, SuccessResponse

router = APIRouter()


class NotificationResponse(BaseModel):
    id: UUID
    type: str
    title: str
    message: str
    is_read: bool
    resource_type: Optional[str]
    resource_id: Optional[UUID]
    action_url: Optional[str]
    created_at: str

    class Config:
        from_attributes = True


class UnreadCount(BaseModel):
    count: int


@router.get("", response_model=PaginatedResponse[NotificationResponse])
async def list_notifications(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    unread_only: bool = Query(False),
):
    """List notifications for the current user."""
    query = select(Notification).where(Notification.user_id == current_user.id)

    if unread_only:
        query = query.where(Notification.is_read == False)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = (
        query
        .offset(pagination.offset)
        .limit(pagination.page_size)
        .order_by(Notification.created_at.desc())
    )
    result = await db.execute(query)
    notifications = result.scalars().all()

    items = [
        NotificationResponse(
            id=n.id,
            type=n.type,
            title=n.title,
            message=n.message,
            is_read=n.is_read,
            resource_type=n.resource_type,
            resource_id=n.resource_id,
            action_url=n.action_url,
            created_at=n.created_at.isoformat(),
        )
        for n in notifications
    ]

    return PaginatedResponse.create(
        items=items,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/unread-count", response_model=UnreadCount)
async def get_unread_count(
    db: DBSession,
    current_user: CurrentUser,
):
    """Get count of unread notifications."""
    result = await db.execute(
        select(func.count(Notification.id))
        .where(Notification.user_id == current_user.id)
        .where(Notification.is_read == False)
    )
    count = result.scalar() or 0
    return UnreadCount(count=count)


@router.post("/{notification_id}/read", response_model=SuccessResponse)
async def mark_as_read(
    db: DBSession,
    notification_id: UUID,
    current_user: CurrentUser,
):
    """Mark a notification as read."""
    result = await db.execute(
        select(Notification)
        .where(Notification.id == notification_id)
        .where(Notification.user_id == current_user.id)
    )
    notification = result.scalar_one_or_none()

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    notification.is_read = True
    return SuccessResponse(message="Notification marked as read")


@router.post("/mark-all-read", response_model=SuccessResponse)
async def mark_all_as_read(
    db: DBSession,
    current_user: CurrentUser,
):
    """Mark all notifications as read."""
    await db.execute(
        update(Notification)
        .where(Notification.user_id == current_user.id)
        .where(Notification.is_read == False)
        .values(is_read=True)
    )
    return SuccessResponse(message="All notifications marked as read")


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    db: DBSession,
    notification_id: UUID,
    current_user: CurrentUser,
):
    """Delete a notification."""
    result = await db.execute(
        select(Notification)
        .where(Notification.id == notification_id)
        .where(Notification.user_id == current_user.id)
    )
    notification = result.scalar_one_or_none()

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    await db.delete(notification)
