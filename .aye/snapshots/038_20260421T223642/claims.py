"""Claims API Routes."""

import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_async_session
from app.dependencies import get_current_user, require_permission
from app.models.user import User
from app.models.claim import Claim
from app.schemas.claim import (
    ClaimCreate,
    ClaimUpdate,
    ClaimResponse,
    ClaimListResponse,
    ClaimStats,
)
from app.services.audit_service import AuditService

router = APIRouter()


@router.get("", response_model=ClaimListResponse)
async def list_claims(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("claim", "read"))],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    claim_type: Optional[str] = None,
    policy_id: Optional[uuid.UUID] = None,
    anomaly_only: bool = False,
):
    """List claims."""
    query = (
        select(Claim)
        .options(selectinload(Claim.policy))
        .where(Claim.is_deleted == False)
    )
    
    if search:
        search_term = f"%{search}%"
        query = query.where(Claim.claim_number.ilike(search_term))
    
    if status:
        query = query.where(Claim.status == status)
    
    if claim_type:
        query = query.where(Claim.claim_type == claim_type)
    
    if policy_id:
        query = query.where(Claim.policy_id == policy_id)
    
    if anomaly_only:
        query = query.where(Claim.anomaly_score > 0.5)
    
    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Paginate
    query = query.order_by(Claim.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    claims = list(result.unique().scalars().all())
    
    return ClaimListResponse(
        items=claims,
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size,
    )


@router.get("/stats", response_model=ClaimStats)
async def get_claim_stats(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("claim", "read"))],
):
    """Get claim statistics."""
    # Total claims
    total_result = await db.execute(
        select(func.count()).where(Claim.is_deleted == False)
    )
    total_claims = total_result.scalar() or 0
    
    # Open claims
    open_result = await db.execute(
        select(func.count()).where(
            Claim.is_deleted == False,
            Claim.status.in_(["submitted", "under_review"]),
        )
    )
    open_claims = open_result.scalar() or 0
    
    # Total claimed
    claimed_result = await db.execute(
        select(func.sum(Claim.claimed_amount)).where(Claim.is_deleted == False)
    )
    total_claimed = float(claimed_result.scalar() or 0)
    
    # Total settled
    settled_result = await db.execute(
        select(func.sum(Claim.settlement_amount)).where(
            Claim.is_deleted == False,
            Claim.status == "paid",
        )
    )
    total_settled = float(settled_result.scalar() or 0)
    
    # By status
    status_result = await db.execute(
        select(Claim.status, func.count())
        .where(Claim.is_deleted == False)
        .group_by(Claim.status)
    )
    by_status = {row[0]: row[1] for row in status_result.all()}
    
    # By type
    type_result = await db.execute(
        select(Claim.claim_type, func.count())
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


@router.get("/anomalies")
async def get_anomaly_claims(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("claim", "read"))],
    limit: int = Query(10, ge=1, le=100),
):
    """Get claims flagged with anomalies."""
    result = await db.execute(
        select(Claim)
        .options(selectinload(Claim.policy))
        .where(
            Claim.is_deleted == False,
            Claim.anomaly_score.isnot(None),
            Claim.anomaly_score > 0.5,
        )
        .order_by(Claim.anomaly_score.desc())
        .limit(limit)
    )
    return list(result.unique().scalars().all())


@router.get("/{claim_id}", response_model=ClaimResponse)
async def get_claim(
    claim_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("claim", "read"))],
):
    """Get a claim by ID."""
    result = await db.execute(
        select(Claim)
        .options(selectinload(Claim.policy))
        .where(Claim.id == claim_id, Claim.is_deleted == False)
    )
    claim = result.unique().scalar_one_or_none()
    
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found",
        )
    
    return claim


@router.post("", response_model=ClaimResponse, status_code=status.HTTP_201_CREATED)
async def create_claim(
    data: ClaimCreate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("claim", "create"))],
):
    """Create a new claim."""
    audit_service = AuditService(db)
    
    # Generate claim number
    import datetime
    claim_number = f"CLM-{datetime.datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
    
    claim = Claim(
        claim_number=claim_number,
        **data.model_dump(),
        status="submitted",
    )
    db.add(claim)
    await db.flush()
    await db.refresh(claim)
    
    # TODO: Run anomaly detection asynchronously
    
    await audit_service.log(
        user_id=current_user.id,
        action="create",
        resource_type="claim",
        resource_id=claim.id,
        new_values=data.model_dump(),
    )
    
    return claim


@router.put("/{claim_id}", response_model=ClaimResponse)
async def update_claim(
    claim_id: uuid.UUID,
    data: ClaimUpdate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("claim", "update"))],
):
    """Update a claim."""
    audit_service = AuditService(db)
    
    result = await db.execute(
        select(Claim).where(Claim.id == claim_id, Claim.is_deleted == False)
    )
    claim = result.scalar_one_or_none()
    
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found",
        )
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(claim, key, value)
    
    await db.flush()
    await db.refresh(claim)
    
    await audit_service.log(
        user_id=current_user.id,
        action="update",
        resource_type="claim",
        resource_id=claim_id,
        new_values=update_data,
    )
    
    return claim


@router.delete("/{claim_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_claim(
    claim_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("claim", "delete"))],
):
    """Delete a claim."""
    audit_service = AuditService(db)
    
    result = await db.execute(
        select(Claim).where(Claim.id == claim_id, Claim.is_deleted == False)
    )
    claim = result.scalar_one_or_none()
    
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found",
        )
    
    if claim.status == "paid":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a paid claim",
        )
    
    claim.is_deleted = True
    await db.flush()
    
    await audit_service.log(
        user_id=current_user.id,
        action="delete",
        resource_type="claim",
        resource_id=claim_id,
    )
