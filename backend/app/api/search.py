"""
Search API Routes
=================

Unified search across resources.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Query
from pydantic import BaseModel
from sqlalchemy import select, or_

from app.dependencies import DBSession, CurrentUser
from app.models.policy import Policy
from app.models.policyholder import Policyholder
from app.models.claim import Claim
from app.models.assumption_set import AssumptionSet
from app.models.calculation_run import CalculationRun

router = APIRouter()


class SearchResult(BaseModel):
    id: UUID
    resource_type: str
    title: str
    subtitle: Optional[str] = None
    status: Optional[str] = None
    url: str
    score: float = 1.0


class SearchResponse(BaseModel):
    query: str
    total: int
    results: list[SearchResult]


@router.get("", response_model=SearchResponse)
async def search(
    db: DBSession,
    current_user: CurrentUser,
    q: str = Query(..., min_length=2),
    resource_types: Optional[str] = Query(None, description="Comma-separated list"),
    limit: int = Query(20, le=100),
):
    """Search across all resources."""
    results: list[SearchResult] = []
    types = resource_types.split(",") if resource_types else None

    # Search policies
    if not types or "policy" in types:
        policy_results = await db.execute(
            select(Policy)
            .where(Policy.is_deleted == False)
            .where(
                or_(
                    Policy.policy_number.ilike(f"%{q}%"),
                    Policy.product_name.ilike(f"%{q}%"),
                )
            )
            .limit(limit)
        )
        for policy in policy_results.scalars():
            results.append(
                SearchResult(
                    id=policy.id,
                    resource_type="policy",
                    title=policy.policy_number,
                    subtitle=policy.product_name,
                    status=policy.status,
                    url=f"/policies/{policy.id}",
                )
            )

    # Search policyholders
    if not types or "policyholder" in types:
        holder_results = await db.execute(
            select(Policyholder)
            .where(Policyholder.is_deleted == False)
            .where(
                or_(
                    Policyholder.first_name.ilike(f"%{q}%"),
                    Policyholder.last_name.ilike(f"%{q}%"),
                    Policyholder.email.ilike(f"%{q}%"),
                )
            )
            .limit(limit)
        )
        for holder in holder_results.scalars():
            results.append(
                SearchResult(
                    id=holder.id,
                    resource_type="policyholder",
                    title=holder.full_name,
                    subtitle=holder.email,
                    url=f"/policyholders/{holder.id}",
                )
            )

    # Search claims
    if not types or "claim" in types:
        claim_results = await db.execute(
            select(Claim)
            .where(Claim.is_deleted == False)
            .where(Claim.claim_number.ilike(f"%{q}%"))
            .limit(limit)
        )
        for claim in claim_results.scalars():
            results.append(
                SearchResult(
                    id=claim.id,
                    resource_type="claim",
                    title=claim.claim_number,
                    subtitle=claim.claim_type,
                    status=claim.status,
                    url=f"/claims/{claim.id}",
                )
            )

    # Search assumption sets
    if not types or "assumption_set" in types:
        assumption_results = await db.execute(
            select(AssumptionSet)
            .where(AssumptionSet.is_deleted == False)
            .where(AssumptionSet.name.ilike(f"%{q}%"))
            .limit(limit)
        )
        for aset in assumption_results.scalars():
            results.append(
                SearchResult(
                    id=aset.id,
                    resource_type="assumption_set",
                    title=aset.name,
                    subtitle=f"v{aset.version}",
                    status=aset.status,
                    url=f"/assumptions/{aset.id}",
                )
            )

    # Search calculations
    if not types or "calculation" in types:
        calc_results = await db.execute(
            select(CalculationRun)
            .where(CalculationRun.run_name.ilike(f"%{q}%"))
            .limit(limit)
        )
        for calc in calc_results.scalars():
            results.append(
                SearchResult(
                    id=calc.id,
                    resource_type="calculation",
                    title=calc.run_name,
                    status=calc.status,
                    url=f"/calculations/{calc.id}",
                )
            )

    # Sort by relevance (simple: exact matches first)
    results.sort(key=lambda r: (0 if q.lower() in r.title.lower() else 1, r.title))

    return SearchResponse(
        query=q,
        total=len(results),
        results=results[:limit],
    )
