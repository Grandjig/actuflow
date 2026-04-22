"""Assumptions API Routes."""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from datetime import date, datetime

from app.dependencies import DBSession, CurrentUser, Pagination, require_permission
from app.models.assumption_set import AssumptionSet
from app.models.assumption_table import AssumptionTable
from app.schemas.common import PaginatedResponse

router = APIRouter()


class AssumptionSetResponse(BaseModel):
    id: uuid.UUID
    name: str
    version: str
    description: Optional[str] = None
    status: str
    effective_date: Optional[date] = None
    line_of_business: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AssumptionSetCreate(BaseModel):
    name: str
    version: str
    description: Optional[str] = None
    effective_date: Optional[date] = None
    line_of_business: Optional[str] = None


@router.get("", response_model=PaginatedResponse[AssumptionSetResponse])
async def list_assumption_sets(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
):
    """List assumption sets."""
    query = select(AssumptionSet).where(AssumptionSet.is_deleted == False)
    
    if status:
        query = query.where(AssumptionSet.status == status)
    if search:
        query = query.where(AssumptionSet.name.ilike(f"%{search}%"))
    
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0
    
    query = query.offset(pagination.offset).limit(pagination.page_size)
    query = query.order_by(AssumptionSet.created_at.desc())
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    return PaginatedResponse.create(
        items=items,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{assumption_set_id}", response_model=AssumptionSetResponse)
async def get_assumption_set(
    assumption_set_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
):
    """Get assumption set by ID."""
    result = await db.execute(
        select(AssumptionSet)
        .where(AssumptionSet.id == assumption_set_id)
        .where(AssumptionSet.is_deleted == False)
    )
    assumption_set = result.scalar_one_or_none()
    
    if not assumption_set:
        raise HTTPException(status_code=404, detail="Assumption set not found")
    
    return assumption_set


@router.post("", response_model=AssumptionSetResponse, status_code=status.HTTP_201_CREATED)
async def create_assumption_set(
    data: AssumptionSetCreate,
    db: DBSession,
    current_user: CurrentUser = Depends(require_permission("assumption", "create")),
):
    """Create a new assumption set."""
    assumption_set = AssumptionSet(
        name=data.name,
        version=data.version,
        description=data.description,
        effective_date=data.effective_date,
        line_of_business=data.line_of_business,
        status="draft",
        created_by_id=current_user.id,
    )
    db.add(assumption_set)
    await db.flush()
    await db.refresh(assumption_set)
    
    return assumption_set
