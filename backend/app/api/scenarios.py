"""Scenario API Routes."""

import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.dependencies import get_current_user, require_permission
from app.models.user import User
from app.models.scenario import Scenario
from app.models.scenario_result import ScenarioResult
from app.services.audit_service import AuditService

router = APIRouter()


@router.get("")
async def list_scenarios(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("scenario", "read"))],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    scenario_type: Optional[str] = None,
    status: Optional[str] = None,
):
    """List scenarios."""
    query = select(Scenario).where(Scenario.is_deleted == False)
    
    if scenario_type:
        query = query.where(Scenario.scenario_type == scenario_type)
    
    if status:
        query = query.where(Scenario.status == status)
    
    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Paginate
    query = query.order_by(Scenario.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    scenarios = list(result.scalars().all())
    
    return {
        "items": scenarios,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size,
    }


@router.get("/{scenario_id}")
async def get_scenario(
    scenario_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("scenario", "read"))],
):
    """Get a scenario by ID."""
    result = await db.execute(
        select(Scenario).where(
            Scenario.id == scenario_id,
            Scenario.is_deleted == False,
        )
    )
    scenario = result.scalar_one_or_none()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found",
        )
    
    return scenario


@router.post("")
async def create_scenario(
    data: dict,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("scenario", "create"))],
):
    """Create a new scenario."""
    audit_service = AuditService(db)
    
    scenario = Scenario(
        name=data["name"],
        description=data.get("description"),
        scenario_type=data.get("scenario_type", "deterministic"),
        base_assumption_set_id=data.get("base_assumption_set_id"),
        adjustments=data.get("adjustments", {}),
        status="draft",
        created_by_id=current_user.id,
    )
    db.add(scenario)
    await db.flush()
    await db.refresh(scenario)
    
    await audit_service.log(
        user_id=current_user.id,
        action="create",
        resource_type="scenario",
        resource_id=scenario.id,
        new_values=data,
    )
    
    return scenario


@router.put("/{scenario_id}")
async def update_scenario(
    scenario_id: uuid.UUID,
    data: dict,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("scenario", "update"))],
):
    """Update a scenario."""
    result = await db.execute(
        select(Scenario).where(
            Scenario.id == scenario_id,
            Scenario.is_deleted == False,
        )
    )
    scenario = result.scalar_one_or_none()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found",
        )
    
    for key, value in data.items():
        if hasattr(scenario, key) and value is not None:
            setattr(scenario, key, value)
    
    await db.flush()
    await db.refresh(scenario)
    
    return scenario


@router.delete("/{scenario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scenario(
    scenario_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("scenario", "delete"))],
):
    """Delete a scenario."""
    result = await db.execute(
        select(Scenario).where(
            Scenario.id == scenario_id,
            Scenario.is_deleted == False,
        )
    )
    scenario = result.scalar_one_or_none()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found",
        )
    
    scenario.is_deleted = True
    await db.flush()


@router.post("/{scenario_id}/run")
async def run_scenario(
    scenario_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("scenario", "update"))],
):
    """Run a scenario calculation."""
    result = await db.execute(
        select(Scenario).where(
            Scenario.id == scenario_id,
            Scenario.is_deleted == False,
        )
    )
    scenario = result.scalar_one_or_none()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found",
        )
    
    # TODO: Queue scenario calculation
    scenario.status = "running"
    await db.flush()
    
    return {"message": "Scenario run started", "scenario_id": str(scenario_id)}


@router.get("/{scenario_id}/results")
async def get_scenario_results(
    scenario_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("scenario", "read"))],
):
    """Get scenario results."""
    result = await db.execute(
        select(ScenarioResult).where(ScenarioResult.scenario_id == scenario_id)
    )
    return list(result.scalars().all())
