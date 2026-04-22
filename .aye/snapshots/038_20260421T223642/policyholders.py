"""Policyholder API Routes."""

import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.dependencies import get_current_user, require_permission
from app.models.user import User
from app.models.policyholder import Policyholder
from app.models.policy import Policy
from app.schemas.policyholder import (
    PolicyholderCreate,
    PolicyholderUpdate,
    PolicyholderResponse,
    PolicyholderListResponse,
)
from app.services.audit_service import AuditService

router = APIRouter()


@router.get("", response_model=PolicyholderListResponse)
async def list_policyholders(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("policyholder", "read"))],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
):
    """List policyholders."""
    query = select(Policyholder).where(Policyholder.is_deleted == False)
    
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Policyholder.first_name.ilike(search_term),
                Policyholder.last_name.ilike(search_term),
                Policyholder.email.ilike(search_term),
                Policyholder.external_id.ilike(search_term),
            )
        )
    
    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Paginate
    query = query.order_by(Policyholder.last_name, Policyholder.first_name)
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    policyholders = list(result.scalars().all())
    
    return PolicyholderListResponse(
        items=policyholders,
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size,
    )


@router.get("/{policyholder_id}", response_model=PolicyholderResponse)
async def get_policyholder(
    policyholder_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("policyholder", "read"))],
):
    """Get a policyholder by ID."""
    result = await db.execute(
        select(Policyholder).where(
            Policyholder.id == policyholder_id,
            Policyholder.is_deleted == False,
        )
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
    data: PolicyholderCreate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("policyholder", "create"))],
):
    """Create a new policyholder."""
    audit_service = AuditService(db)
    
    policyholder = Policyholder(
        **data.model_dump(),
        created_by_id=current_user.id,
    )
    db.add(policyholder)
    await db.flush()
    await db.refresh(policyholder)
    
    await audit_service.log(
        user_id=current_user.id,
        action="create",
        resource_type="policyholder",
        resource_id=policyholder.id,
        new_values=data.model_dump(),
    )
    
    return policyholder


@router.put("/{policyholder_id}", response_model=PolicyholderResponse)
async def update_policyholder(
    policyholder_id: uuid.UUID,
    data: PolicyholderUpdate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("policyholder", "update"))],
):
    """Update a policyholder."""
    audit_service = AuditService(db)
    
    result = await db.execute(
        select(Policyholder).where(
            Policyholder.id == policyholder_id,
            Policyholder.is_deleted == False,
        )
    )
    policyholder = result.scalar_one_or_none()
    
    if not policyholder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policyholder not found",
        )
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(policyholder, key, value)
    
    await db.flush()
    await db.refresh(policyholder)
    
    await audit_service.log(
        user_id=current_user.id,
        action="update",
        resource_type="policyholder",
        resource_id=policyholder_id,
        new_values=update_data,
    )
    
    return policyholder


@router.delete("/{policyholder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policyholder(
    policyholder_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("policyholder", "delete"))],
):
    """Delete a policyholder."""
    audit_service = AuditService(db)
    
    result = await db.execute(
        select(Policyholder).where(
            Policyholder.id == policyholder_id,
            Policyholder.is_deleted == False,
        )
    )
    policyholder = result.scalar_one_or_none()
    
    if not policyholder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policyholder not found",
        )
    
    # Check for active policies
    policy_result = await db.execute(
        select(Policy).where(
            Policy.policyholder_id == policyholder_id,
            Policy.status == "active",
            Policy.is_deleted == False,
        ).limit(1)
    )
    if policy_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete policyholder with active policies",
        )
    
    policyholder.is_deleted = True
    await db.flush()
    
    await audit_service.log(
        user_id=current_user.id,
        action="delete",
        resource_type="policyholder",
        resource_id=policyholder_id,
    )


@router.get("/{policyholder_id}/policies")
async def get_policyholder_policies(
    policyholder_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("policyholder", "read"))],
):
    """Get policies for a policyholder."""
    # Verify policyholder exists
    ph_result = await db.execute(
        select(Policyholder).where(
            Policyholder.id == policyholder_id,
            Policyholder.is_deleted == False,
        )
    )
    if not ph_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policyholder not found",
        )
    
    result = await db.execute(
        select(Policy).where(
            Policy.policyholder_id == policyholder_id,
            Policy.is_deleted == False,
        ).order_by(Policy.issue_date.desc())
    )
    
    return list(result.scalars().all())
