"""
Policyholders API Routes
========================

Policyholder management endpoints.
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
from app.models.policyholder import Policyholder
from app.models.policy import Policy
from app.schemas.policyholder import (
    PolicyholderCreate,
    PolicyholderUpdate,
    PolicyholderResponse,
    PolicyholderListItem,
)
from app.schemas.common import PaginatedResponse

router = APIRouter()


@router.get("", response_model=PaginatedResponse[PolicyholderListItem])
async def list_policyholders(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    search: Optional[str] = Query(None),
):
    """List policyholders with pagination and filtering."""
    # Build query
    query = select(Policyholder).where(Policyholder.is_deleted == False)

    if search:
        query = query.where(
            or_(
                Policyholder.first_name.ilike(f"%{search}%"),
                Policyholder.last_name.ilike(f"%{search}%"),
                Policyholder.email.ilike(f"%{search}%"),
                Policyholder.external_id.ilike(f"%{search}%"),
            )
        )

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Get paginated results with policy count
    query = (
        query
        .outerjoin(Policy, Policy.policyholder_id == Policyholder.id)
        .group_by(Policyholder.id)
        .add_columns(func.count(Policy.id).label("policy_count"))
        .offset(pagination.offset)
        .limit(pagination.page_size)
        .order_by(Policyholder.created_at.desc())
    )
    result = await db.execute(query)
    rows = result.all()

    items = [
        PolicyholderListItem(
            id=row.Policyholder.id,
            external_id=row.Policyholder.external_id,
            full_name=row.Policyholder.full_name,
            date_of_birth=row.Policyholder.date_of_birth,
            gender=row.Policyholder.gender,
            email=row.Policyholder.email,
            policy_count=row.policy_count,
        )
        for row in rows
    ]

    return PaginatedResponse.create(
        items=items,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{policyholder_id}", response_model=PolicyholderResponse)
async def get_policyholder(
    db: DBSession,
    policyholder_id: UUID,
    current_user: CurrentUser,
):
    """Get a specific policyholder by ID."""
    result = await db.execute(
        select(Policyholder)
        .where(Policyholder.id == policyholder_id)
        .where(Policyholder.is_deleted == False)
    )
    policyholder = result.scalar_one_or_none()

    if not policyholder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policyholder not found",
        )

    return policyholder


@router.post("", response_model=PolicyholderResponse, status_code=status.HTTP_201_CREATED)
async def create_policyholder(
    db: DBSession,
    ph_data: PolicyholderCreate,
    _: CurrentUser = Depends(require_permission("policyholder", "create")),
):
    """Create a new policyholder."""
    # Check if external_id already exists (if provided)
    if ph_data.external_id:
        result = await db.execute(
            select(Policyholder).where(Policyholder.external_id == ph_data.external_id)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Policyholder with this external_id already exists",
            )

    policyholder = Policyholder(**ph_data.model_dump())
    db.add(policyholder)
    await db.flush()
    await db.refresh(policyholder)

    return policyholder


@router.put("/{policyholder_id}", response_model=PolicyholderResponse)
async def update_policyholder(
    db: DBSession,
    policyholder_id: UUID,
    ph_data: PolicyholderUpdate,
    _: CurrentUser = Depends(require_permission("policyholder", "update")),
):
    """Update an existing policyholder."""
    result = await db.execute(
        select(Policyholder)
        .where(Policyholder.id == policyholder_id)
        .where(Policyholder.is_deleted == False)
    )
    policyholder = result.scalar_one_or_none()

    if not policyholder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policyholder not found",
        )

    update_data = ph_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(policyholder, field, value)

    await db.flush()
    await db.refresh(policyholder)

    return policyholder


@router.delete("/{policyholder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policyholder(
    db: DBSession,
    policyholder_id: UUID,
    _: CurrentUser = Depends(require_permission("policyholder", "delete")),
):
    """Soft delete a policyholder."""
    result = await db.execute(
        select(Policyholder)
        .where(Policyholder.id == policyholder_id)
        .where(Policyholder.is_deleted == False)
    )
    policyholder = result.scalar_one_or_none()

    if not policyholder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policyholder not found",
        )

    # Check for active policies
    result = await db.execute(
        select(func.count(Policy.id))
        .where(Policy.policyholder_id == policyholder_id)
        .where(Policy.status == "active")
    )
    active_count = result.scalar() or 0
    
    if active_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete policyholder with {active_count} active policies",
        )

    policyholder.is_deleted = True
