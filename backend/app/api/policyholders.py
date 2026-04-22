"""Policyholder API Routes."""

import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import func, select, or_
from pydantic import BaseModel
from datetime import date, datetime

from app.dependencies import DBSession, CurrentUser, Pagination
from app.models.policyholder import Policyholder
from app.schemas.common import PaginatedResponse

router = APIRouter()


class PolicyholderResponse(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    smoker_status: Optional[str] = None
    occupation_class: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("", response_model=PaginatedResponse[PolicyholderResponse])
async def list_policyholders(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    search: Optional[str] = Query(None),
):
    """List policyholders."""
    query = select(Policyholder).where(Policyholder.is_deleted == False)
    
    if search:
        search_filter = or_(
            Policyholder.first_name.ilike(f"%{search}%"),
            Policyholder.last_name.ilike(f"%{search}%"),
            Policyholder.email.ilike(f"%{search}%"),
        )
        query = query.where(search_filter)
    
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0
    
    query = query.offset(pagination.offset).limit(pagination.page_size)
    query = query.order_by(Policyholder.created_at.desc())
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    return PaginatedResponse.create(
        items=items,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{policyholder_id}", response_model=PolicyholderResponse)
async def get_policyholder(
    policyholder_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
):
    """Get policyholder by ID."""
    result = await db.execute(
        select(Policyholder)
        .where(Policyholder.id == policyholder_id)
        .where(Policyholder.is_deleted == False)
    )
    ph = result.scalar_one_or_none()
    
    if not ph:
        raise HTTPException(status_code=404, detail="Policyholder not found")
    
    return ph
