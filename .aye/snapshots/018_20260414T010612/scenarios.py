"""
Scenario Management API Routes
==============================

CRUD and execution for scenarios and stress testing.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import (
    CurrentUser,
    DBSession,
    Pagination,
    Sorting,
    require_permission,
)
from app.schemas.common import PaginatedResponse, SuccessMessage
from app.schemas.scenario import (
    ScenarioComparison,
    ScenarioCreate,
    ScenarioListItem,
    ScenarioResponse,
    ScenarioResultResponse,
    ScenarioRunRequest,
    ScenarioUpdate,
)

router = APIRouter()


@router.get("", response_model=PaginatedResponse[ScenarioListItem])
async def list_scenarios(
    db: DBSession,
    user: CurrentUser,
    pagination: Pagination,
    sorting: Sorting,
    category: Optional[str] = None,
    status_filter: Optional[str] = Query(default=None, alias="status"),
    is_regulatory: Optional[bool] = None,
    _: None = Depends(require_permission("scenario", "read")),
):
    """
    List scenarios with pagination.
    """
    from app.services.scenario_service import ScenarioService
    
    service = ScenarioService(db)
    
    scenarios, total = await service.list_scenarios(
        category=category,
        status=status_filter,
        is_regulatory=is_regulatory,
        offset=pagination.offset,
        limit=pagination.limit,
        sort_by=sorting.sort_by or "name",
        sort_order=sorting.sort_order,
    )
    
    return PaginatedResponse.create(
        items=scenarios,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{scenario_id}", response_model=ScenarioResponse)
async def get_scenario(
    scenario_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("scenario", "read")),
):
    """
    Get a scenario by ID.
    """
    from app.services.scenario_service import ScenarioService
    
    service = ScenarioService(db)
    scenario = await service.get_scenario(scenario_id)
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found",
        )
    
    return scenario


@router.post("", response_model=ScenarioResponse, status_code=status.HTTP_201_CREATED)
async def create_scenario(
    data: ScenarioCreate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("scenario", "create")),
):
    """
    Create a new scenario.
    """
    from app.services.scenario_service import ScenarioService
    
    service = ScenarioService(db)
    scenario = await service.create_scenario(data, created_by=user)
    
    return scenario


@router.put("/{scenario_id}", response_model=ScenarioResponse)
async def update_scenario(
    scenario_id: UUID,
    data: ScenarioUpdate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("scenario", "update")),
):
    """
    Update a scenario.
    """
    from app.services.scenario_service import ScenarioService
    
    service = ScenarioService(db)
    
    scenario = await service.get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found",
        )
    
    if scenario.is_regulatory:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify regulatory scenarios",
        )
    
    updated = await service.update_scenario(scenario, data, updated_by=user)
    
    return updated


@router.delete("/{scenario_id}", response_model=SuccessMessage)
async def delete_scenario(
    scenario_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("scenario", "delete")),
):
    """
    Soft delete a scenario.
    """
    from app.services.scenario_service import ScenarioService
    
    service = ScenarioService(db)
    
    scenario = await service.get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found",
        )
    
    if scenario.is_regulatory:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete regulatory scenarios",
        )
    
    await service.delete_scenario(scenario, deleted_by=user)
    
    return SuccessMessage(message="Scenario deleted")


@router.post("/{scenario_id}/run", response_model=ScenarioResultResponse)
async def run_scenario(
    scenario_id: UUID,
    request: ScenarioRunRequest,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("scenario", "run")),
):
    """
    Run a scenario (triggers a calculation with scenario adjustments).
    """
    from app.services.scenario_service import ScenarioService
    
    service = ScenarioService(db)
    
    scenario = await service.get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found",
        )
    
    if scenario.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scenario is not active",
        )
    
    result = await service.run_scenario(
        scenario=scenario,
        base_run_id=request.base_calculation_run_id,
        policy_filter=request.policy_filter,
        parameters=request.parameters,
        triggered_by=user,
    )
    
    return result


@router.get("/{scenario_id}/results", response_model=PaginatedResponse[ScenarioResultResponse])
async def get_scenario_results(
    scenario_id: UUID,
    db: DBSession,
    user: CurrentUser,
    pagination: Pagination,
    _: None = Depends(require_permission("scenario", "read")),
):
    """
    Get all results for a scenario.
    """
    from app.services.scenario_service import ScenarioService
    
    service = ScenarioService(db)
    
    results, total = await service.get_results(
        scenario_id=scenario_id,
        offset=pagination.offset,
        limit=pagination.limit,
    )
    
    return PaginatedResponse.create(
        items=results,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.post("/compare", response_model=ScenarioComparison)
async def compare_scenarios(
    scenario_ids: list[UUID],
    base_run_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("scenario", "read")),
):
    """
    Compare multiple scenarios against a base calculation.
    """
    from app.services.scenario_service import ScenarioService
    
    if len(scenario_ids) < 1 or len(scenario_ids) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must compare 1-10 scenarios",
        )
    
    service = ScenarioService(db)
    
    comparison = await service.compare_scenarios(
        scenario_ids=scenario_ids,
        base_run_id=base_run_id,
    )
    
    return comparison
