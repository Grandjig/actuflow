"""Claims API Routes."""

import uuid
from typing import Optional
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select, or_
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from datetime import date, datetime

from app.dependencies import DBSession, CurrentUser, Pagination, require_permission
from app.models.claim import Claim
from app.schemas.common import PaginatedResponse

router = APIRouter()


class ClaimResponse(BaseModel):
    id: uuid.UUID
    claim_number: str
    policy_id: uuid.UUID
    claim_type: str
    status: str
    claim_date: date
    incident_date: Optional[date] = None
    claimed_amount: Decimal
    settlement_amount: Optional[Decimal] = None
    settlement_date: Optional[date] = None
    anomaly_score: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ClaimCreate(BaseModel):
    policy_id: uuid.UUID
    claim_type: str
    claim_date: date
    incident_date: Optional[date] = None
    claimed_amount: Decimal
    adjuster_notes: Optional[str] = None


@router.get("", response_model=PaginatedResponse[ClaimResponse])
async def list_claims(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    status: Optional[str] = Query(None),
    claim_type: Optional[str] = Query(None),
    policy_id: Optional[uuid.UUID] = Query(None),
    search: Optional[str] = Query(None),
):
    """List claims."""
    query = select(Claim).where(Claim.is_deleted == False)
    
    if status:
        query = query.where(Claim.status == status)
    if claim_type:
        query = query.where(Claim.claim_type == claim_type)
    if policy_id:
        query = query.where(Claim.policy_id == policy_id)
    if search:
        query = query.where(Claim.claim_number.ilike(f"%{search}%"))
    
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0
    
    query = query.offset(pagination.offset).limit(pagination.page_size)
    query = query.order_by(Claim.created_at.desc())
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    return PaginatedResponse.create(
        items=items,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{claim_id}", response_model=ClaimResponse)
async def get_claim(
    claim_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
):
    """Get claim by ID."""
    result = await db.execute(
        select(Claim)
        .where(Claim.id == claim_id)
        .where(Claim.is_deleted == False)
    )
    claim = result.scalar_one_or_none()
    
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    return claim


@router.post("", response_model=ClaimResponse, status_code=status.HTTP_201_CREATED)
async def create_claim(
    data: ClaimCreate,
    db: DBSession,
    current_user: CurrentUser = Depends(require_permission("claim", "create")),
):
    """Create a new claim."""
    # Generate claim number
    count_result = await db.execute(select(func.count()).select_from(Claim))
    count = (count_result.scalar() or 0) + 1
    claim_number = f"CLM-{datetime.utcnow().year}-{str(count).zfill(6)}"
    
    claim = Claim(
        claim_number=claim_number,
        policy_id=data.policy_id,
        claim_type=data.claim_type,
        claim_date=data.claim_date,
        incident_date=data.incident_date,
        claimed_amount=data.claimed_amount,
        adjuster_notes=data.adjuster_notes,
        status="filed",
        created_by_id=current_user.id,
    )
    db.add(claim)
    await db.flush()
    await db.refresh(claim)
    
    return claim
