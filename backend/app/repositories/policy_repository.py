"""Policy Repository."""

import uuid
from datetime import date
from typing import Any

from sqlalchemy import select, func, and_, or_, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.policy import Policy
from app.models.policyholder import Policyholder
from app.repositories.base import BaseRepository


class PolicyRepository(BaseRepository[Policy]):
    """Repository for Policy operations."""

    def __init__(self, session: AsyncSession):
        super().__init__(Policy, session)

    async def get_with_relations(self, id: uuid.UUID) -> Policy | None:
        """Get policy with related data."""
        result = await self.session.execute(
            select(Policy)
            .options(
                selectinload(Policy.policyholder),
                selectinload(Policy.coverages),
                selectinload(Policy.claims),
            )
            .where(Policy.id == id)
            .where(Policy.is_deleted == False)
        )
        return result.scalar_one_or_none()

    async def get_by_policy_number(self, policy_number: str) -> Policy | None:
        """Get policy by policy number."""
        result = await self.session.execute(
            select(Policy)
            .where(Policy.policy_number == policy_number)
            .where(Policy.is_deleted == False)
        )
        return result.scalar_one_or_none()

    async def search(
        self,
        *,
        search: str | None = None,
        status: str | list[str] | None = None,
        product_type: str | None = None,
        product_code: str | None = None,
        policyholder_id: uuid.UUID | None = None,
        issue_date_from: date | None = None,
        issue_date_to: date | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Policy], int]:
        """Search policies with filters."""
        query = (
            select(Policy)
            .options(selectinload(Policy.policyholder))
            .where(Policy.is_deleted == False)
        )
        count_query = select(func.count(Policy.id)).where(Policy.is_deleted == False)

        # Build filter conditions
        conditions = []

        if search:
            search_term = f"%{search}%"
            conditions.append(
                or_(
                    Policy.policy_number.ilike(search_term),
                    Policy.product_name.ilike(search_term),
                )
            )

        if status:
            if isinstance(status, list):
                conditions.append(Policy.status.in_(status))
            else:
                conditions.append(Policy.status == status)

        if product_type:
            conditions.append(Policy.product_type == product_type)

        if product_code:
            conditions.append(Policy.product_code == product_code)

        if policyholder_id:
            conditions.append(Policy.policyholder_id == policyholder_id)

        if issue_date_from:
            conditions.append(Policy.issue_date >= issue_date_from)

        if issue_date_to:
            conditions.append(Policy.issue_date <= issue_date_to)

        # Apply conditions
        if conditions:
            query = query.where(and_(*conditions))
            count_query = count_query.where(and_(*conditions))

        # Get total count
        count_result = await self.session.execute(count_query)
        total = count_result.scalar_one()

        # Apply pagination and ordering
        query = query.order_by(Policy.created_at.desc()).offset(skip).limit(limit)

        result = await self.session.execute(query)
        policies = list(result.scalars().all())

        return policies, total

    async def get_stats(self) -> dict[str, Any]:
        """Get policy statistics."""
        # Total policies
        total_result = await self.session.execute(
            select(func.count(Policy.id)).where(Policy.is_deleted == False)
        )
        total = total_result.scalar_one()

        # Active policies
        active_result = await self.session.execute(
            select(func.count(Policy.id))
            .where(Policy.is_deleted == False)
            .where(Policy.status == "active")
        )
        active = active_result.scalar_one()

        # Total premium
        premium_result = await self.session.execute(
            select(func.sum(Policy.premium_amount))
            .where(Policy.is_deleted == False)
            .where(Policy.status == "active")
        )
        total_premium = premium_result.scalar_one() or 0

        # By status
        status_result = await self.session.execute(
            select(Policy.status, func.count(Policy.id))
            .where(Policy.is_deleted == False)
            .group_by(Policy.status)
        )
        by_status = {row[0]: row[1] for row in status_result.all()}

        # By product type
        product_result = await self.session.execute(
            select(Policy.product_type, func.count(Policy.id))
            .where(Policy.is_deleted == False)
            .group_by(Policy.product_type)
        )
        by_product_type = {row[0]: row[1] for row in product_result.all()}

        return {
            "total_policies": total,
            "active_policies": active,
            "total_premium": float(total_premium),
            "by_status": by_status,
            "by_product_type": by_product_type,
        }

    async def get_for_calculation(
        self,
        policy_filter: dict[str, Any] | None = None,
    ) -> list[Policy]:
        """Get policies for calculation run."""
        query = (
            select(Policy)
            .options(selectinload(Policy.coverages))
            .where(Policy.is_deleted == False)
            .where(Policy.status == "active")
        )

        if policy_filter:
            if "product_type" in policy_filter:
                query = query.where(Policy.product_type == policy_filter["product_type"])
            if "product_code" in policy_filter:
                query = query.where(Policy.product_code == policy_filter["product_code"])
            if "policy_ids" in policy_filter:
                query = query.where(Policy.id.in_(policy_filter["policy_ids"]))

        result = await self.session.execute(query)
        return list(result.scalars().all())
