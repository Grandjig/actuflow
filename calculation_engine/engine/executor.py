"""Calculation Executor."""

import logging
import uuid
from typing import Any, Callable

import numpy as np
import redis

from calculation_engine.config import settings

logger = logging.getLogger(__name__)


class CalculationExecutor:
    """Executes actuarial calculations."""

    def __init__(self, run_id: uuid.UUID):
        self.run_id = run_id
        self.redis = redis.from_url(settings.REDIS_URL)
        self.on_progress: Callable[[int, int, str], None] | None = None
        self.batch_size = settings.BATCH_SIZE

    def execute(self) -> dict[str, Any]:
        """Execute the calculation run."""
        import asyncio
        return asyncio.run(self._execute_async())

    async def _execute_async(self) -> dict[str, Any]:
        """Async execution logic."""
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker, selectinload
        from sqlalchemy import select

        engine = create_async_engine(settings.DATABASE_URL)
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with async_session() as session:
            # Load run configuration
            from app.models.calculation_run import CalculationRun
            from app.models.model_definition import ModelDefinition
            from app.models.assumption_set import AssumptionSet

            result = await session.execute(
                select(CalculationRun)
                .options(
                    selectinload(CalculationRun.model_definition),
                    selectinload(CalculationRun.assumption_set)
                    .selectinload(AssumptionSet.tables),
                )
                .where(CalculationRun.id == self.run_id)
            )
            run = result.scalar_one_or_none()

            if not run:
                raise ValueError(f"Calculation run {self.run_id} not found")

            # Update status
            run.status = "running"
            run.started_at = self._now()
            await session.commit()

            try:
                # Load policies
                from app.repositories.policy_repository import PolicyRepository
                policy_repo = PolicyRepository(session)
                policies = await policy_repo.get_for_calculation(run.policy_filter)

                total_policies = len(policies)
                run.policies_count = total_policies

                if self.on_progress:
                    self.on_progress(0, total_policies, "Loading assumptions...")

                # Load assumption tables
                assumptions = self._load_assumptions(run.assumption_set)

                # Process in batches
                all_results = []
                processed = 0

                for i in range(0, len(policies), self.batch_size):
                    # Check for cancellation
                    if self._is_cancelled():
                        run.status = "cancelled"
                        await session.commit()
                        return {"status": "cancelled"}

                    batch = policies[i:i + self.batch_size]
                    batch_results = self._process_batch(
                        batch,
                        run.model_definition.configuration,
                        assumptions,
                        run.parameters or {},
                    )
                    all_results.extend(batch_results)

                    processed += len(batch)
                    if self.on_progress:
                        self.on_progress(
                            processed,
                            total_policies,
                            f"Processing policies ({processed}/{total_policies})...",
                        )

                # Save results
                if self.on_progress:
                    self.on_progress(processed, total_policies, "Saving results...")

                from app.repositories.calculation_repository import CalculationResultRepository
                result_repo = CalculationResultRepository(session)
                await result_repo.bulk_create(all_results)

                # Generate summary
                summary = self._generate_summary(all_results)
                run.result_summary = summary

                # Complete
                run.status = "completed"
                run.completed_at = self._now()
                run.duration_seconds = int(
                    (run.completed_at - run.started_at).total_seconds()
                )

                await session.commit()

                logger.info(
                    f"Calculation {self.run_id} completed: "
                    f"{total_policies} policies in {run.duration_seconds}s"
                )

                return {
                    "status": "completed",
                    "policies_processed": total_policies,
                    "duration_seconds": run.duration_seconds,
                    "summary": summary,
                }

            except Exception as e:
                run.status = "failed"
                run.error_message = str(e)
                run.completed_at = self._now()
                await session.commit()
                raise

        await engine.dispose()

    def _load_assumptions(self, assumption_set) -> dict[str, Any]:
        """Load assumption tables into usable format."""
        assumptions = {}
        for table in assumption_set.tables:
            assumptions[table.table_type] = table.data
        return assumptions

    def _process_batch(
        self,
        policies: list,
        model_config: dict,
        assumptions: dict,
        parameters: dict,
    ) -> list[dict]:
        """Process a batch of policies."""
        results = []

        for policy in policies:
            policy_results = self._calculate_policy(
                policy,
                model_config,
                assumptions,
                parameters,
            )
            results.extend(policy_results)

        return results

    def _calculate_policy(
        self,
        policy,
        model_config: dict,
        assumptions: dict,
        parameters: dict,
    ) -> list[dict]:
        """Calculate results for a single policy."""
        results = []

        projection_months = model_config.get("projection_months", 360)
        valuation_date = parameters.get("valuation_date")

        # Get policy data
        issue_age = self._calculate_age(policy.date_of_birth_insured, policy.issue_date) \
            if hasattr(policy, 'date_of_birth_insured') else 35
        sum_assured = float(policy.sum_assured or 0)
        premium = float(policy.premium_amount or 0)

        # Get mortality rates
        mortality_table = assumptions.get("mortality", {})
        lapse_table = assumptions.get("lapse", {})
        discount_table = assumptions.get("discount_rate", {})

        # Simple projection (simplified for demonstration)
        inforce = 1.0
        total_reserve = 0.0

        for month in range(projection_months):
            # Get rates (simplified lookup)
            qx = self._lookup_mortality(mortality_table, issue_age, month)
            lapse = self._lookup_lapse(lapse_table, month)
            discount = self._lookup_discount(discount_table, month)

            # Calculate survival
            px = (1 - qx) * (1 - lapse)
            inforce *= px

            # Calculate cashflows
            claims = inforce * qx * sum_assured
            premiums = inforce * premium
            net_cashflow = premiums - claims

            # Discount
            discount_factor = 1 / (1 + discount) ** (month / 12)
            pv_cashflow = net_cashflow * discount_factor
            total_reserve += pv_cashflow

        # Store summary result
        results.append({
            "calculation_run_id": self.run_id,
            "policy_id": policy.id,
            "projection_month": 0,
            "result_type": "reserve",
            "values": {
                "best_estimate_liability": total_reserve,
                "sum_assured": sum_assured,
                "premium": premium,
            },
            "anomaly_flag": abs(total_reserve) > sum_assured * 2,  # Simple anomaly check
        })

        return results

    def _lookup_mortality(self, table: dict, age: int, duration: int) -> float:
        """Lookup mortality rate."""
        rates = table.get("rates", [])
        for rate in rates:
            if rate.get("age") == age + duration // 12:
                return rate.get("male", 0.001)
        return 0.001  # Default

    def _lookup_lapse(self, table: dict, duration: int) -> float:
        """Lookup lapse rate."""
        rates = table.get("rates", [])
        year = duration // 12
        for rate in rates:
            if rate.get("duration") == year:
                return rate.get("rate", 0.05)
        return 0.02  # Default

    def _lookup_discount(self, table: dict, month: int) -> float:
        """Lookup discount rate."""
        rates = table.get("rates", [])
        for rate in rates:
            if rate.get("term_months", 0) >= month:
                return rate.get("rate", 0.04)
        return 0.04  # Default

    def _calculate_age(self, dob, as_of_date) -> int:
        """Calculate age in years."""
        if not dob or not as_of_date:
            return 35
        return (as_of_date - dob).days // 365

    def _generate_summary(self, results: list[dict]) -> dict:
        """Generate summary statistics."""
        reserves = [r["values"].get("best_estimate_liability", 0) for r in results]
        premiums = [r["values"].get("premium", 0) for r in results]
        anomalies = sum(1 for r in results if r.get("anomaly_flag"))

        return {
            "total_policies": len(results),
            "total_reserves": sum(reserves),
            "total_premiums": sum(premiums),
            "average_reserve": np.mean(reserves) if reserves else 0,
            "anomaly_count": anomalies,
        }

    def _is_cancelled(self) -> bool:
        """Check if calculation was cancelled."""
        return self.redis.exists(f"calc:{self.run_id}:cancel")

    def _now(self):
        """Get current datetime."""
        from datetime import datetime
        return datetime.utcnow()
