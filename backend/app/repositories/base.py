"""Base Repository Pattern."""

import uuid
from typing import Any, Generic, TypeVar, Type

from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations."""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: uuid.UUID) -> ModelType | None:
        """Get by ID."""
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_ids(self, ids: list[uuid.UUID]) -> list[ModelType]:
        """Get multiple by IDs."""
        result = await self.session.execute(
            select(self.model).where(self.model.id.in_(ids))
        )
        return list(result.scalars().all())

    async def list(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: dict[str, Any] | None = None,
        order_by: str | None = None,
        order_desc: bool = False,
    ) -> list[ModelType]:
        """List with pagination and filtering."""
        query = select(self.model)

        # Apply soft delete filter if model has it
        if hasattr(self.model, "is_deleted"):
            query = query.where(self.model.is_deleted == False)

        # Apply filters
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    column = getattr(self.model, key)
                    if isinstance(value, list):
                        query = query.where(column.in_(value))
                    else:
                        query = query.where(column == value)

        # Apply ordering
        if order_by and hasattr(self.model, order_by):
            column = getattr(self.model, order_by)
            query = query.order_by(column.desc() if order_desc else column)
        elif hasattr(self.model, "created_at"):
            query = query.order_by(self.model.created_at.desc())

        # Apply pagination
        query = query.offset(skip).limit(limit)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        """Count records."""
        query = select(func.count(self.model.id))

        if hasattr(self.model, "is_deleted"):
            query = query.where(self.model.is_deleted == False)

        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    column = getattr(self.model, key)
                    if isinstance(value, list):
                        query = query.where(column.in_(value))
                    else:
                        query = query.where(column == value)

        result = await self.session.execute(query)
        return result.scalar_one()

    async def create(self, data: dict[str, Any]) -> ModelType:
        """Create new record."""
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def update(
        self, id: uuid.UUID, data: dict[str, Any]
    ) -> ModelType | None:
        """Update record."""
        instance = await self.get(id)
        if not instance:
            return None

        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def delete(self, id: uuid.UUID, soft: bool = True) -> bool:
        """Delete record (soft delete by default)."""
        instance = await self.get(id)
        if not instance:
            return False

        if soft and hasattr(instance, "is_deleted"):
            instance.is_deleted = True
        else:
            await self.session.delete(instance)

        await self.session.flush()
        return True

    async def exists(self, id: uuid.UUID) -> bool:
        """Check if record exists."""
        query = select(func.count(self.model.id)).where(self.model.id == id)
        if hasattr(self.model, "is_deleted"):
            query = query.where(self.model.is_deleted == False)
        result = await self.session.execute(query)
        return result.scalar_one() > 0
