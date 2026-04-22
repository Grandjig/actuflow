"""Calculation Repository."""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import select, func, and_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.calculation_run import CalculationRun
from app.models.calculation_result import CalculationResult
from app.repositories.base import BaseRepository


class CalculationRunRepository(BaseRepository[CalculationRun]):
    """Repository for CalculationRun operations."""

    def __init__(self, session: AsyncSession):
        super().__init__(CalculationRun, session)

    async def get_with_relations(self, id: uuid.UUID) -> CalculationRun | None:
        """Get calculation run with related data."""
        result = await self.session.execute(
            select(CalculationRun)
            .options(
                selectinload(CalculationRun.model_definition),
                selectinload(CalculationRun.assumption_set),
                selectinload(CalculationRun.triggered_by),
            )
            .where(CalculationRun.id == id)
        )
        return result.scalar_one_or_none()

    async def search(
        self,
        *,
        search: str | None = None,
        status: str | list[str] | None = None,
        trigger_type: str | None = None,
        model_id: uuid.UUID | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[CalculationRun], int]:
        """Search calculation runs."""
        query = select(CalculationRun).options(
            selectinload(CalculationRun.model_definition),
            selectinload(CalculationRun.assumption_set),
        )
        count_query = select(func.count(CalculationRun.id))

        conditions = []

        if search:
            search_term = f"%{search}%"
            conditions.append(CalculationRun.run_name.ilike(search_term))

        if status:
            if isinstance(status, list):
                conditions.append(CalculationRun.status.in_(status))
            else:
                conditions.append(CalculationRun.status == status)

        if trigger_type:
            conditions.append(CalculationRun.trigger_type == trigger_type)

        if model_id:
            conditions.append(CalculationRun.model_definition_id == model_id)

        if conditions:
            query = query.where(and_(*conditions))
            count_query = count_query.where(and_(*conditions))

        count_result = await self.session.execute(count_query)
        total = count_result.scalar_one()

        query = query.order_by(CalculationRun.created_at.desc()).offset(skip).limit(limit)

        result = await self.session.execute(query)
        runs = list(result.scalars().all())

        return runs, total

    async def get_running(self) -> list[CalculationRun]:
        """Get all currently running calculations."""
        result = await self.session.execute(
            select(CalculationRun)
            .where(CalculationRun.status.in_(["queued", "running"]))
            .order_by(CalculationRun.created_at)
        )
        return list(result.scalars().all())

    async def update_progress(
        self,
        id: uuid.UUID,
        *,
        status: str | None = None,
        policies_processed: int | None = None,
        error_message: str | None = None,
    ) -> None:
        """Update calculation progress."""
        data = {}
        if status:
            data["status"] = status
            if status == "running":
                data["started_at"] = datetime.utcnow()
            elif status in ["completed", "failed", "cancelled"]:
                data["completed_at"] = datetime.utcnow()
        if policies_processed is not None:
            data["policies_processed"] = policies_processed
        if error_message:
            data["error_message"] = error_message

        if data:
            await self.session.execute(
                update(CalculationRun).where(CalculationRun.id == id).values(**data)
            )
            await self.session.flush()


class CalculationResultRepository(BaseRepository[CalculationResult]):
    """Repository for CalculationResult operations."""

    def __init__(self, session: AsyncSession):
        super().__init__(CalculationResult, session)

    async def get_by_run(
        self,
        run_id: uuid.UUID,
        *,
        result_type: str | None = None,
        policy_id: uuid.UUID | None = None,
        skip: int = 0,
        limit: int = 1000,
    ) -> list[CalculationResult]:
        """Get results for a calculation run."""
        query = select(CalculationResult).where(
            CalculationResult.calculation_run_id == run_id
        )

        if result_type:
            query = query.where(CalculationResult.result_type == result_type)

        if policy_id:
            query = query.where(CalculationResult.policy_id == policy_id)

        query = query.offset(skip).limit(limit)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_summary(self, run_id: uuid.UUID) -> dict[str, Any]:
        """Get summary statistics for a calculation run."""
        # Get total policies
        policy_count = await self.session.execute(
            select(func.count(func.distinct(CalculationResult.policy_id))).where(
                CalculationResult.calculation_run_id == run_id
            )
        )
        total_policies = policy_count.scalar_one()

        # Get anomaly count
        anomaly_count = await self.session.execute(
            select(func.count(CalculationResult.id))
            .where(CalculationResult.calculation_run_id == run_id)
            .where(CalculationResult.anomaly_flag == True)
        )
        anomalies = anomaly_count.scalar_one()

        return {
            "total_policies": total_policies,
            "anomaly_count": anomalies,
            "total_reserves": 0,  # Would aggregate from JSONB values
            "total_premiums": 0,
        }

    async def bulk_create(self, results: list[dict[str, Any]]) -> None:
        """Bulk insert calculation results."""
        instances = [CalculationResult(**r) for r in results]
        self.session.add_all(instances)
        await self.session.flush()

    async def get_anomalies(self, run_id: uuid.UUID) -> list[CalculationResult]:
        """Get anomaly-flagged results."""
        result = await self.session.execute(
            select(CalculationResult)
            .where(CalculationResult.calculation_run_id == run_id)
            .where(CalculationResult.anomaly_flag == True)
        )
        return list(result.scalars().all())
