"""User Repository."""

import uuid
from typing import Any

from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.models.role import Role
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User operations."""

    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_with_role(self, id: uuid.UUID) -> User | None:
        """Get user with role and permissions."""
        result = await self.session.execute(
            select(User)
            .options(
                selectinload(User.role).selectinload(Role.permissions)
            )
            .where(User.id == id)
            .where(User.is_deleted == False)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email."""
        result = await self.session.execute(
            select(User)
            .options(
                selectinload(User.role).selectinload(Role.permissions)
            )
            .where(User.email == email)
            .where(User.is_deleted == False)
        )
        return result.scalar_one_or_none()

    async def get_by_keycloak_id(self, keycloak_id: str) -> User | None:
        """Get user by Keycloak ID."""
        result = await self.session.execute(
            select(User)
            .options(
                selectinload(User.role).selectinload(Role.permissions)
            )
            .where(User.keycloak_id == keycloak_id)
            .where(User.is_deleted == False)
        )
        return result.scalar_one_or_none()

    async def search(
        self,
        *,
        search: str | None = None,
        role_id: uuid.UUID | None = None,
        is_active: bool | None = None,
        department: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[User], int]:
        """Search users with filters."""
        query = (
            select(User)
            .options(selectinload(User.role))
            .where(User.is_deleted == False)
        )
        count_query = select(func.count(User.id)).where(User.is_deleted == False)

        conditions = []

        if search:
            search_term = f"%{search}%"
            conditions.append(
                or_(
                    User.email.ilike(search_term),
                    User.full_name.ilike(search_term),
                )
            )

        if role_id:
            conditions.append(User.role_id == role_id)

        if is_active is not None:
            conditions.append(User.is_active == is_active)

        if department:
            conditions.append(User.department == department)

        if conditions:
            query = query.where(and_(*conditions))
            count_query = count_query.where(and_(*conditions))

        count_result = await self.session.execute(count_query)
        total = count_result.scalar_one()

        query = query.order_by(User.full_name).offset(skip).limit(limit)

        result = await self.session.execute(query)
        users = list(result.scalars().all())

        return users, total

    async def update_last_login(self, id: uuid.UUID) -> None:
        """Update last login timestamp."""
        from datetime import datetime
        await self.update(id, {"last_login": datetime.utcnow()})
