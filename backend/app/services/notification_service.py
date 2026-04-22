"""Notification Service."""

import uuid
from typing import Optional

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification
from app.models.user import User


class NotificationService:
    """Service for notification operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(
        self,
        user_id: uuid.UUID,
        type: str,
        title: str,
        message: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[uuid.UUID] = None,
    ) -> Notification:
        """Create a notification."""
        notification = Notification(
            user_id=user_id,
            type=type,
            title=title,
            message=message,
            resource_type=resource_type,
            resource_id=resource_id,
        )
        self.db.add(notification)
        await self.db.flush()
        await self.db.refresh(notification)
        return notification
    
    async def create_for_users(
        self,
        user_ids: list[uuid.UUID],
        type: str,
        title: str,
        message: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[uuid.UUID] = None,
    ) -> list[Notification]:
        """Create notifications for multiple users."""
        notifications = []
        for user_id in user_ids:
            notification = await self.create(
                user_id=user_id,
                type=type,
                title=title,
                message=message,
                resource_type=resource_type,
                resource_id=resource_id,
            )
            notifications.append(notification)
        return notifications
    
    async def get_for_user(
        self,
        user_id: uuid.UUID,
        is_read: Optional[bool] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[list[Notification], int]:
        """Get notifications for a user."""
        query = select(Notification).where(Notification.user_id == user_id)
        
        if is_read is not None:
            query = query.where(Notification.is_read == is_read)
        
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0
        
        query = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        notifications = list(result.scalars().all())
        
        return notifications, total
    
    async def get_unread_count(self, user_id: uuid.UUID) -> int:
        """Get unread notification count for a user."""
        result = await self.db.execute(
            select(func.count())
            .select_from(Notification)
            .where(
                Notification.user_id == user_id,
                Notification.is_read == False,
            )
        )
        return result.scalar() or 0
    
    async def mark_as_read(self, notification_id: uuid.UUID) -> Optional[Notification]:
        """Mark a notification as read."""
        result = await self.db.execute(
            select(Notification).where(Notification.id == notification_id)
        )
        notification = result.scalar_one_or_none()
        
        if notification:
            notification.is_read = True
            await self.db.flush()
            await self.db.refresh(notification)
        
        return notification
    
    async def mark_all_as_read(self, user_id: uuid.UUID) -> int:
        """Mark all notifications as read for a user."""
        result = await self.db.execute(
            update(Notification)
            .where(
                Notification.user_id == user_id,
                Notification.is_read == False,
            )
            .values(is_read=True)
        )
        return result.rowcount
