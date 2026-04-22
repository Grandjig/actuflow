"""Policy API Routes."""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select, or_
from sqlalchemy.orm import selectinload

from app.dependencies import DBSession, CurrentUser, Pagination, require_permission
from app.models.policy import Policy
from app.models.policyholder import Policyholder
from app.schemas.policy import (
    PolicyCreate,
    PolicyUpdate,
    PolicyResponse,
    PolicyListItem,
    PolicySummaryStats,
)
from app.schemas.common import PaginatedResponse

router = APIRouter()


@router.get("", response_model=PaginatedResponse[PolicyListItem])
async def list_policies(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    status: Optional[str] = Query(None),
    product_type: Optional[str] = Query(None),
    product_code: Optional[str] = Query(None),
    policyholder_id: Optional[uuid.UUID] = Query(None),
    search: Optional[str] = Query(None),
):
    """List policies with filtering and pagination."""
    query = select(Policy).where(Policy.is_deleted == False)
    
    # Apply filters
    if status:
        query = query.where(Policy.status == status)
    if product_type:
        query = query.where(Policy.product_type == product_type)
    if product_code:
        query = query.where(Policy.product_code == product_code)
    if policyholder_id:
        query = query.where(Policy.policyholder_id == policyholder_id)
    if search:
        search_filter = or_(
            Policy.policy_number.ilike(f"%{search}%"),
            Policy.product_name.ilike(f"%{search}%"),
        )
        query = query.where(search_filter)
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0
    
    # Apply pagination and ordering
    query = query.offset(pagination.offset).limit(pagination.page_size)
    query = query.order_by(Policy.created_at.desc())
    query = query.options(selectinload(Policy.policyholder))
    
    result = await db.execute(query)
    policies = result.scalars().all()
    
    # Map to list items
    items = []
    for p in policies:
        item = PolicyListItem(
            id=p.id,
            policy_number=p.policy_number,
            product_type=p.product_type,
            product_code=p.product_code,
            product_name=p.product_name,
            status=p.status,
            policyholder_id=p.policyholder_id,
            policyholder_name=f"{p.policyholder.first_name} {p.policyholder.last_name}" if p.policyholder else None,
            issue_date=p.issue_date,
            maturity_date=p.maturity_date,
            sum_assured=p.sum_assured,
            premium_amount=p.premium_amount,
            premium_frequency=p.premium_frequency,
            currency=p.currency,
            created_at=p.created_at,
        )
        items.append(item)
    
    return PaginatedResponse.create(
        items=items,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/stats", response_model=PolicySummaryStats)
async def get_policy_stats(
    db: DBSession,
    current_user: CurrentUser,
):
    """Get policy summary statistics."""
    # Total and active count
    total_result = await db.execute(
        select(func.count()).select_from(Policy).where(Policy.is_deleted == False)
    )
    total = total_result.scalar() or 0
    
    active_result = await db.execute(
        select(func.count()).select_from(Policy)
        .where(Policy.is_deleted == False)
        .where(Policy.status == "active")
    )
    active = active_result.scalar() or 0
    
    # Sums
    sums_result = await db.execute(
        select(
            func.coalesce(func.sum(Policy.sum_assured), 0),
            func.coalesce(func.sum(Policy.premium_amount), 0),
        ).where(Policy.is_deleted == False)
    )
    sums = sums_result.one()
    
    # By product type
    product_result = await db.execute(
        select(Policy.product_type, func.count())
        .where(Policy.is_deleted == False)
        .group_by(Policy.product_type)
    )
    by_product = {row[0]: row[1] for row in product_result.all()}
    
    # By status
    status_result = await db.execute(
        select(Policy.status, func.count())
        .where(Policy.is_deleted == False)
        .group_by(Policy.status)
    )
    by_status = {row[0]: row[1] for row in status_result.all()}
    
    return PolicySummaryStats(
        total_policies=total,
        active_policies=active,
        total_sum_assured=sums[0],
        total_premium=sums[1],
        by_product_type=by_product,
        by_status=by_status,
    )


@router.get("/{policy_id}", response_model=PolicyResponse)
async def get_policy(
    policy_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
):
    """Get a specific policy by ID."""
    result = await db.execute(
        select(Policy)
        .options(selectinload(Policy.policyholder))
        .where(Policy.id == policy_id)
        .where(Policy.is_deleted == False)
    )
    policy = result.scalar_one_or_none()
    
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    return policy


@router.post("", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED)
async def create_policy(
    data: PolicyCreate,
    db: DBSession,
    current_user: CurrentUser = Depends(require_permission("policy", "create")),
):
    """Create a new policy."""
    # Verify policyholder exists
    ph_result = await db.execute(
        select(Policyholder).where(Policyholder.id == data.policyholder_id)
    )
    if not ph_result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Policyholder not found")
    
    # Check for duplicate policy number
    existing = await db.execute(
        select(Policy).where(Policy.policy_number == data.policy_number)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Policy number already exists")
    
    policy = Policy(
        **data.model_dump(),
        created_by_id=current_user.id,
    )
    db.add(policy)
    await db.flush()
    await db.refresh(policy)
    
    return policy


@router.put("/{policy_id}", response_model=PolicyResponse)
async def update_policy(
    policy_id: uuid.UUID,
    data: PolicyUpdate,
    db: DBSession,
    current_user: CurrentUser = Depends(require_permission("policy", "update")),
):
    """Update a policy."""
    result = await db.execute(
        select(Policy)
        .where(Policy.id == policy_id)
        .where(Policy.is_deleted == False)
    )
    policy = result.scalar_one_or_none()
    
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(policy, field, value)
    
    await db.flush()
    await db.refresh(policy)
    
    return policy


@router.delete("/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policy(
    policy_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser = Depends(require_permission("policy", "delete")),
):
    """Soft delete a policy."""
    result = await db.execute(
        select(Policy)
        .where(Policy.id == policy_id)
        .where(Policy.is_deleted == False)
    )
    policy = result.scalar_one_or_none()
    
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    policy.is_deleted = True
    await db.flush()
