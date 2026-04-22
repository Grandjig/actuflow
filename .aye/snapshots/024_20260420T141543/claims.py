"""
Claims API Routes
=================

Claim management endpoints.
"""

import uuid
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select, or_
from sqlalchemy.orm import selectinload

from app.dependencies import (
    DBSession,
    CurrentUser,
    Pagination,
    require_permission,
)
from app.models.claim import Claim
from app.models.policy import Policy
from app.schemas.claim import (
    ClaimCreate,
    ClaimUpdate,
    ClaimResponse,
    ClaimListItem,
    ClaimStats,
)
from app.schemas.common import PaginatedResponse

router = APIRouter()


def generate_claim_number() -> str:
    """Generate a unique claim number."""
    return f"CLM-{uuid.uuid4().hex[:8].upper()}"


@router.get("", response_model=PaginatedResponse[ClaimListItem])
async def list_claims(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    claim_type: Optional[str] = Query(None),
    policy_id: Optional[UUID] = Query(None),
    anomaly_only: bool = Query(False),
):
    """List claims with pagination and filtering."""
    query = (
        select(Claim)
        .where(Claim.is_deleted == False)
        .options(selectinload(Claim.policy))
    )

    if search:
        query = query.where(
            or_(
                Claim.claim_number.ilike(f"%{search}%"),
                Claim.policy.has(Policy.policy_number.ilike(f"%{search}%")),
            )
        )

    if status:
        query = query.where(Claim.status == status)

    if claim_type:
        query = query.where(Claim.claim_type == claim_type)

    if policy_id:
        query = query.where(Claim.policy_id == policy_id)

    if anomaly_only:
        query = query.where(Claim.anomaly_score > 0.5)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Get paginated results
    query = (
        query
        .offset(pagination.offset)
        .limit(pagination.page_size)
        .order_by(Claim.created_at.desc())
    )
    result = await db.execute(query)
    claims = result.scalars().all()

    items = [
        ClaimListItem(
            id=claim.id,
            claim_number=claim.claim_number,
            policy_id=claim.policy_id,
            policy_number=claim.policy.policy_number if claim.policy else None,
            claim_type=claim.claim_type,
            claim_date=claim.claim_date,
            claimed_amount=claim.claimed_amount,
            status=claim.status,
            anomaly_score=claim.anomaly_score,
        )
        for claim in claims
    ]

    return PaginatedResponse.create(
        items=items,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/stats", response_model=ClaimStats)
async def get_claim_stats(
    db: DBSession,
    current_user: CurrentUser,
):
    """Get claim statistics."""
    # Total claims
    total_result = await db.execute(
        select(func.count(Claim.id)).where(Claim.is_deleted == False)
    )
    total_claims = total_result.scalar() or 0

    # Open claims
    open_result = await db.execute(
        select(func.count(Claim.id))
        .where(Claim.is_deleted == False)
        .where(Claim.status.in_(["submitted", "under_review"]))
    )
    open_claims = open_result.scalar() or 0

    # Total claimed
    claimed_result = await db.execute(
        select(func.sum(Claim.claimed_amount))
        .where(Claim.is_deleted == False)
    )
    total_claimed = claimed_result.scalar() or 0

    # Total settled
    settled_result = await db.execute(
        select(func.sum(Claim.settlement_amount))
        .where(Claim.is_deleted == False)
        .where(Claim.status == "paid")
    )
    total_settled = settled_result.scalar() or 0

    # By status
    status_result = await db.execute(
        select(Claim.status, func.count(Claim.id))
        .where(Claim.is_deleted == False)
        .group_by(Claim.status)
    )
    by_status = {row[0]: row[1] for row in status_result.all()}

    # By type
    type_result = await db.execute(
        select(Claim.claim_type, func.count(Claim.id))
        .where(Claim.is_deleted == False)
        .group_by(Claim.claim_type)
    )
    by_type = {row[0]: row[1] for row in type_result.all()}

    return ClaimStats(
        total_claims=total_claims,
        open_claims=open_claims,
        total_claimed=total_claimed,
        total_settled=total_settled,
        by_status=by_status,
        by_type=by_type,
    )


@router.get("/anomalies", response_model=list[ClaimResponse])
async def get_anomalous_claims(
    db: DBSession,
    current_user: CurrentUser,
    limit: int = Query(10, ge=1, le=100),
):
    """Get claims flagged as anomalous by AI."""
    result = await db.execute(
        select(Claim)
        .where(Claim.is_deleted == False)
        .where(Claim.anomaly_score > 0.5)
        .order_by(Claim.anomaly_score.desc())
        .limit(limit)
    )
    return result.scalars().all()


@router.get("/{claim_id}", response_model=ClaimResponse)
async def get_claim(
    db: DBSession,
    claim_id: UUID,
    current_user: CurrentUser,
):
    """Get a specific claim by ID."""
    result = await db.execute(
        select(Claim)
        .where(Claim.id == claim_id)
        .where(Claim.is_deleted == False)
        .options(selectinload(Claim.policy))
    )
    claim = result.scalar_one_or_none()

    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found",
        )

    return claim


@router.post("", response_model=ClaimResponse, status_code=status.HTTP_201_CREATED)
async def create_claim(
    db: DBSession,
    claim_data: ClaimCreate,
    _: CurrentUser = Depends(require_permission("claim", "create")),
):
    """Create a new claim."""
    # Validate policy exists and is active
    result = await db.execute(
        select(Policy)
        .where(Policy.id == claim_data.policy_id)
        .where(Policy.is_deleted == False)
    )
    policy = result.scalar_one_or_none()

    if not policy:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid policy_id",
        )

    if policy.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot create claim for policy with status '{policy.status}'",
        )

    # Generate claim number if not provided
    claim_number = claim_data.claim_number or generate_claim_number()

    claim = Claim(
        **claim_data.model_dump(exclude={"claim_number"}),
        claim_number=claim_number,
        status="submitted",
    )
    db.add(claim)
    await db.flush()
    await db.refresh(claim)

    return claim


@router.put("/{claim_id}", response_model=ClaimResponse)
async def update_claim(
    db: DBSession,
    claim_id: UUID,
    claim_data: ClaimUpdate,
    _: CurrentUser = Depends(require_permission("claim", "update")),
):
    """Update an existing claim."""
    result = await db.execute(
        select(Claim)
        .where(Claim.id == claim_id)
        .where(Claim.is_deleted == False)
    )
    claim = result.scalar_one_or_none()

    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found",
        )

    update_data = claim_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(claim, field, value)

    await db.flush()
    await db.refresh(claim)

    return claim


@router.delete("/{claim_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_claim(
    db: DBSession,
    claim_id: UUID,
    _: CurrentUser = Depends(require_permission("claim", "delete")),
):
    """Soft delete a claim."""
    result = await db.execute(
        select(Claim)
        .where(Claim.id == claim_id)
        .where(Claim.is_deleted == False)
    )
    claim = result.scalar_one_or_none()

    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found",
        )

    if claim.status in ["approved", "paid"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete approved or paid claims",
        )

    claim.is_deleted = True
