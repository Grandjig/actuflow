"""
Scenarios API Routes
====================

Scenario management for what-if analysis.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from uuid import UUID
from typing import Optional
from pydantic import BaseModel

from app.dependencies import DBSession, CurrentUser, Pagination, require_permission
from app.models.scenario import Scenario
from app.schemas.common import PaginatedResponse, SuccessResponse

router = APIRouter()


class ScenarioCreate(BaseModel):
    name: str
    description: Optional[str] = None
    scenario_type: str
    base_assumption_set_id: UUID
    adjustments: dict


class ScenarioResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    scenario_type: str
    base_assumption_set_id: UUID
    adjustments: dict
    status: str
    created_by_id: UUID

    class Config:
        from_attributes = True


@router.get("", response_model=PaginatedResponse[ScenarioResponse])
async def list_scenarios(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    scenario_type: Optional[str] = Query(None),
):
    """List scenarios."""
    query = select(Scenario).where(Scenario.is_deleted == False)

    if scenario_type:
        query = query.where(Scenario.scenario_type == scenario_type)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.offset(pagination.offset).limit(pagination.page_size).order_by(Scenario.created_at.desc())
    result = await db.execute(query)
    scenarios = result.scalars().all()

    return PaginatedResponse.create(
        items=scenarios,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.post("", response_model=ScenarioResponse, status_code=status.HTTP_201_CREATED)
async def create_scenario(
    db: DBSession,
    data: ScenarioCreate,
    current_user: CurrentUser = Depends(require_permission("scenario", "create")),
):
    """Create a scenario."""
    scenario = Scenario(
        **data.model_dump(),
        status="draft",
        created_by_id=current_user.id,
    )
    db.add(scenario)
    await db.flush()
    await db.refresh(scenario)
    return scenario


@router.get("/{scenario_id}", response_model=ScenarioResponse)
async def get_scenario(
    db: DBSession,
    scenario_id: UUID,
    current_user: CurrentUser,
):
    """Get a scenario by ID."""
    result = await db.execute(
        select(Scenario).where(Scenario.id == scenario_id).where(Scenario.is_deleted == False)
    )
    scenario = result.scalar_one_or_none()
    if not scenario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")
    return scenario


@router.delete("/{scenario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scenario(
    db: DBSession,
    scenario_id: UUID,
    _: CurrentUser = Depends(require_permission("scenario", "delete")),
):
    """Delete a scenario."""
    result = await db.execute(
        select(Scenario).where(Scenario.id == scenario_id).where(Scenario.is_deleted == False)
    )
    scenario = result.scalar_one_or_none()
    if not scenario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")
    scenario.is_deleted = True
