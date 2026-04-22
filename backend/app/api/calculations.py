"""Calculations API Routes."""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from datetime import datetime

from app.dependencies import DBSession, CurrentUser, Pagination, require_permission
from app.models.calculation_run import CalculationRun
from app.schemas.common import PaginatedResponse

router = APIRouter()


class CalculationRunResponse(BaseModel):
    id: uuid.UUID
    run_name: str
    status: str
    trigger_type: str
    model_definition_id: Optional[uuid.UUID] = None
    assumption_set_id: Optional[uuid.UUID] = None
    policies_count: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    result_summary: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CalculationRunCreate(BaseModel):
    run_name: str
    model_definition_id: uuid.UUID
    assumption_set_id: uuid.UUID
    policy_filter: Optional[dict] = None
    parameters: Optional[dict] = None


@router.get("", response_model=PaginatedResponse[CalculationRunResponse])
async def list_calculations(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
):
    """List calculation runs."""
    query = select(CalculationRun)
    
    if status:
        query = query.where(CalculationRun.status == status)
    if search:
        query = query.where(CalculationRun.run_name.ilike(f"%{search}%"))
    
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0
    
    query = query.offset(pagination.offset).limit(pagination.page_size)
    query = query.order_by(CalculationRun.created_at.desc())
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    return PaginatedResponse.create(
        items=items,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{calculation_id}", response_model=CalculationRunResponse)
async def get_calculation(
    calculation_id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
):
    """Get calculation run by ID."""
    result = await db.execute(
        select(CalculationRun).where(CalculationRun.id == calculation_id)
    )
    calc = result.scalar_one_or_none()
    
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation run not found")
    
    return calc


@router.post("", response_model=CalculationRunResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_calculation(
    data: CalculationRunCreate,
    db: DBSession,
    current_user: CurrentUser = Depends(require_permission("calculation", "create")),
):
    """Start a new calculation run."""
    calc = CalculationRun(
        run_name=data.run_name,
        model_definition_id=data.model_definition_id,
        assumption_set_id=data.assumption_set_id,
        policy_filter=data.policy_filter,
        parameters=data.parameters,
        status="queued",
        trigger_type="manual",
        triggered_by_id=current_user.id,
    )
    db.add(calc)
    await db.flush()
    await db.refresh(calc)
    
    # TODO: Dispatch Celery task
    # from calculation_engine.tasks import run_calculation
    # run_calculation.delay(str(calc.id))
    
    return calc
