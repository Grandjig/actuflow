"""Assumption Repository."""

import uuid
from typing import Any

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.assumption_set import AssumptionSet
from app.models.assumption_table import AssumptionTable
from app.repositories.base import BaseRepository


class AssumptionSetRepository(BaseRepository[AssumptionSet]):
    """Repository for AssumptionSet operations."""

    def __init__(self, session: AsyncSession):
        super().__init__(AssumptionSet, session)

    async def get_with_tables(self, id: uuid.UUID) -> AssumptionSet | None:
        """Get assumption set with its tables."""
        result = await self.session.execute(
            select(AssumptionSet)
            .options(selectinload(AssumptionSet.tables))
            .where(AssumptionSet.id == id)
            .where(AssumptionSet.is_deleted == False)
        )
        return result.scalar_one_or_none()

    async def get_approved(self) -> list[AssumptionSet]:
        """Get all approved assumption sets."""
        result = await self.session.execute(
            select(AssumptionSet)
            .where(AssumptionSet.is_deleted == False)
            .where(AssumptionSet.status == "approved")
            .order_by(AssumptionSet.effective_date.desc())
        )
        return list(result.scalars().all())

    async def get_latest_approved(
        self, line_of_business: str | None = None
    ) -> AssumptionSet | None:
        """Get latest approved assumption set."""
        query = (
            select(AssumptionSet)
            .options(selectinload(AssumptionSet.tables))
            .where(AssumptionSet.is_deleted == False)
            .where(AssumptionSet.status == "approved")
        )

        if line_of_business:
            query = query.where(AssumptionSet.line_of_business == line_of_business)

        query = query.order_by(AssumptionSet.effective_date.desc()).limit(1)

        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def search(
        self,
        *,
        search: str | None = None,
        status: str | list[str] | None = None,
        line_of_business: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[AssumptionSet], int]:
        """Search assumption sets with filters."""
        query = select(AssumptionSet).where(AssumptionSet.is_deleted == False)
        count_query = select(func.count(AssumptionSet.id)).where(
            AssumptionSet.is_deleted == False
        )

        conditions = []

        if search:
            search_term = f"%{search}%"
            conditions.append(AssumptionSet.name.ilike(search_term))

        if status:
            if isinstance(status, list):
                conditions.append(AssumptionSet.status.in_(status))
            else:
                conditions.append(AssumptionSet.status == status)

        if line_of_business:
            conditions.append(AssumptionSet.line_of_business == line_of_business)

        if conditions:
            query = query.where(and_(*conditions))
            count_query = count_query.where(and_(*conditions))

        count_result = await self.session.execute(count_query)
        total = count_result.scalar_one()

        query = query.order_by(AssumptionSet.created_at.desc()).offset(skip).limit(limit)

        result = await self.session.execute(query)
        sets = list(result.scalars().all())

        return sets, total


class AssumptionTableRepository(BaseRepository[AssumptionTable]):
    """Repository for AssumptionTable operations."""

    def __init__(self, session: AsyncSession):
        super().__init__(AssumptionTable, session)

    async def get_by_set(self, set_id: uuid.UUID) -> list[AssumptionTable]:
        """Get all tables for an assumption set."""
        result = await self.session.execute(
            select(AssumptionTable)
            .where(AssumptionTable.assumption_set_id == set_id)
            .order_by(AssumptionTable.table_type)
        )
        return list(result.scalars().all())

    async def get_by_type(
        self, set_id: uuid.UUID, table_type: str
    ) -> AssumptionTable | None:
        """Get table by type within a set."""
        result = await self.session.execute(
            select(AssumptionTable)
            .where(AssumptionTable.assumption_set_id == set_id)
            .where(AssumptionTable.table_type == table_type)
        )
        return result.scalar_one_or_none()
