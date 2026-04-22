"""
Policies API Routes
===================

Policy management endpoints.
"""

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
from app.models.policy import Policy
from app.models.policyholder import Policyholder
from app.models.coverage import Coverage
from app.schemas.policy import (
    PolicyCreate,
    PolicyUpdate,
    PolicyResponse,
    PolicyListItem,
    PolicyStats,
)
from app.schemas.common import PaginatedResponse

router = APIRouter()


@router.get("", response_model=PaginatedResponse[PolicyListItem])
async def list_policies(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    product_type: Optional[str] = Query(None),
    product_code: Optional[str] = Query(None),
    policyholder_id: Optional[UUID] = Query(None),
):
    """List policies with pagination and filtering."""
    # Build query
    query = (
        select(Policy)
        .where(Policy.is_deleted == False)
        .options(selectinload(Policy.policyholder))
    )

    if search:
        query = query.where(
            or_(
                Policy.policy_number.ilike(f"%{search}%"),
                Policy.policyholder.has(
                    Policyholder.first_name.ilike(f"%{search}%")
                ),
                Policy.policyholder.has(
                    Policyholder.last_name.ilike(f"%{search}%")
                ),
            )
        )

    if status:
        query = query.where(Policy.status == status)

    if product_type:
        query = query.where(Policy.product_type == product_type)

    if product_code:
        query = query.where(Policy.product_code == product_code)

    if policyholder_id:
        query = query.where(Policy.policyholder_id == policyholder_id)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Get paginated results
    query = (
        query
        .offset(pagination.offset)
        .limit(pagination.page_size)
        .order_by(Policy.created_at.desc())
    )
    result = await db.execute(query)
    policies = result.scalars().all()

    items = [
        PolicyListItem(
            id=policy.id,
            policy_number=policy.policy_number,
            product_type=policy.product_type,
            product_code=policy.product_code,
            product_name=policy.product_name,
            status=policy.status,
            policyholder_id=policy.policyholder_id,
            policyholder_name=policy.policyholder.full_name if policy.policyholder else None,
            issue_date=policy.issue_date,
            sum_assured=policy.sum_assured,
            premium_amount=policy.premium_amount,
            premium_frequency=policy.premium_frequency,
            currency=policy.currency,
        )
        for policy in policies
    ]

    return PaginatedResponse.create(
        items=items,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/stats", response_model=PolicyStats)
async def get_policy_stats(
    db: DBSession,
    current_user: CurrentUser,
):
    """Get policy statistics."""
    # Total policies
    total_result = await db.execute(
        select(func.count(Policy.id)).where(Policy.is_deleted == False)
    )
    total_policies = total_result.scalar() or 0

    # Active policies
    active_result = await db.execute(
        select(func.count(Policy.id))
        .where(Policy.is_deleted == False)
        .where(Policy.status == "active")
    )
    active_policies = active_result.scalar() or 0

    # Sum assured
    sum_assured_result = await db.execute(
        select(func.sum(Policy.sum_assured))
        .where(Policy.is_deleted == False)
        .where(Policy.status == "active")
    )
    total_sum_assured = sum_assured_result.scalar() or 0

    # Premium
    premium_result = await db.execute(
        select(func.sum(Policy.premium_amount))
        .where(Policy.is_deleted == False)
        .where(Policy.status == "active")
    )
    total_premium = premium_result.scalar() or 0

    # By status
    status_result = await db.execute(
        select(Policy.status, func.count(Policy.id))
        .where(Policy.is_deleted == False)
        .group_by(Policy.status)
    )
    by_status = {row[0]: row[1] for row in status_result.all()}

    # By product type
    product_result = await db.execute(
        select(Policy.product_type, func.count(Policy.id))
        .where(Policy.is_deleted == False)
        .group_by(Policy.product_type)
    )
    by_product_type = {row[0]: row[1] for row in product_result.all()}

    return PolicyStats(
        total_policies=total_policies,
        active_policies=active_policies,
        total_sum_assured=total_sum_assured,
        total_premium=total_premium,
        by_status=by_status,
        by_product_type=by_product_type,
    )


@router.get("/{policy_id}", response_model=PolicyResponse)
async def get_policy(
    db: DBSession,
    policy_id: UUID,
    current_user: CurrentUser,
):
    """Get a specific policy by ID."""
    result = await db.execute(
        select(Policy)
        .where(Policy.id == policy_id)
        .where(Policy.is_deleted == False)
        .options(
            selectinload(Policy.policyholder),
            selectinload(Policy.coverages),
        )
    )
    policy = result.scalar_one_or_none()

    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found",
        )

    return policy


@router.post("", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED)
async def create_policy(
    db: DBSession,
    policy_data: PolicyCreate,
    current_user: CurrentUser = Depends(require_permission("policy", "create")),
):
    """Create a new policy."""
    # Check if policy number already exists
    result = await db.execute(
        select(Policy).where(Policy.policy_number == policy_data.policy_number)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Policy with this number already exists",
        )

    # Validate policyholder exists
    result = await db.execute(
        select(Policyholder).where(Policyholder.id == policy_data.policyholder_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid policyholder_id",
        )

    # Create policy
    coverages_data = policy_data.coverages
    policy_dict = policy_data.model_dump(exclude={"coverages"})
    
    policy = Policy(**policy_dict)
    db.add(policy)
    await db.flush()

    # Create coverages
    for coverage_data in coverages_data:
        coverage = Coverage(
            policy_id=policy.id,
            **coverage_data.model_dump(),
        )
        db.add(coverage)

    await db.flush()
    await db.refresh(policy, ["policyholder", "coverages"])

    return policy


@router.put("/{policy_id}", response_model=PolicyResponse)
async def update_policy(
    db: DBSession,
    policy_id: UUID,
    policy_data: PolicyUpdate,
    _: CurrentUser = Depends(require_permission("policy", "update")),
):
    """Update an existing policy."""
    result = await db.execute(
        select(Policy)
        .where(Policy.id == policy_id)
        .where(Policy.is_deleted == False)
    )
    policy = result.scalar_one_or_none()

    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found",
        )

    # Update fields
    update_data = policy_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(policy, field, value)

    await db.flush()
    await db.refresh(policy, ["policyholder", "coverages"])

    return policy


@router.delete("/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policy(
    db: DBSession,
    policy_id: UUID,
    _: CurrentUser = Depends(require_permission("policy", "delete")),
):
    """Soft delete a policy."""
    result = await db.execute(
        select(Policy)
        .where(Policy.id == policy_id)
        .where(Policy.is_deleted == False)
    )
    policy = result.scalar_one_or_none()

    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found",
        )

    policy.is_deleted = True
