"""
Calculation API Routes
======================

Endpoints for running and managing actuarial calculations.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse

from app.dependencies import (
    CurrentUser,
    DBSession,
    Pagination,
    Sorting,
    require_permission,
)
from app.schemas.calculation import (
    CalculationComparisonRequest,
    CalculationComparisonResponse,
    CalculationNarrative,
    CalculationResultFilter,
    CalculationResultResponse,
    CalculationRunCreate,
    CalculationRunFilter,
    CalculationRunListItem,
    CalculationRunProgress,
    CalculationRunResponse,
)
from app.schemas.common import PaginatedResponse, SuccessMessage

router = APIRouter()


@router.get("", response_model=PaginatedResponse[CalculationRunListItem])
async def list_calculation_runs(
    db: DBSession,
    user: CurrentUser,
    pagination: Pagination,
    sorting: Sorting,
    filters: CalculationRunFilter = Depends(),
    _: None = Depends(require_permission("calculation", "read")),
):
    """
    List calculation runs with pagination.
    """
    from app.services.calculation_service import CalculationService
    
    service = CalculationService(db)
    
    runs, total = await service.list_runs(
        filters=filters,
        offset=pagination.offset,
        limit=pagination.limit,
        sort_by=sorting.sort_by or "created_at",
        sort_order=sorting.sort_order or "desc",
    )
    
    return PaginatedResponse.create(
        items=runs,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{run_id}", response_model=CalculationRunResponse)
async def get_calculation_run(
    run_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("calculation", "read")),
):
    """
    Get a calculation run by ID.
    """
    from app.services.calculation_service import CalculationService
    
    service = CalculationService(db)
    run = await service.get_run(run_id)
    
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation run not found",
        )
    
    return run


@router.post("", response_model=CalculationRunResponse, status_code=status.HTTP_201_CREATED)
async def create_calculation_run(
    data: CalculationRunCreate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("calculation", "run")),
):
    """
    Create and start a new calculation run.
    """
    from app.services.calculation_service import CalculationService
    from app.services.model_service import ModelService
    from app.services.assumption_service import AssumptionService
    
    # Verify model exists and is active
    model_service = ModelService(db)
    model = await model_service.get_model(data.model_definition_id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model definition not found",
        )
    if not model.is_usable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Model is not active",
        )
    
    # Verify assumption set exists and is approved
    assumption_service = AssumptionService(db)
    assumption_set = await assumption_service.get_set(data.assumption_set_id)
    if not assumption_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumption set not found",
        )
    if not assumption_set.is_usable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assumption set is not approved",
        )
    
    service = CalculationService(db)
    run = await service.create_run(data, triggered_by=user)
    
    return run


@router.delete("/{run_id}/cancel", response_model=SuccessMessage)
async def cancel_calculation_run(
    run_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("calculation", "run")),
):
    """
    Cancel a running calculation.
    """
    from app.services.calculation_service import CalculationService
    
    service = CalculationService(db)
    
    run = await service.get_run(run_id)
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation run not found",
        )
    
    if not run.is_running:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Calculation is not running",
        )
    
    await service.cancel_run(run, cancelled_by=user)
    
    return SuccessMessage(message="Calculation cancelled")


@router.get("/{run_id}/progress", response_model=CalculationRunProgress)
async def get_calculation_progress(
    run_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("calculation", "read")),
):
    """
    Get real-time progress of a calculation run.
    """
    from app.services.calculation_service import CalculationService
    
    service = CalculationService(db)
    progress = await service.get_progress(run_id)
    
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation run not found",
        )
    
    return progress


@router.get("/{run_id}/results", response_model=PaginatedResponse[CalculationResultResponse])
async def get_calculation_results(
    run_id: UUID,
    db: DBSession,
    user: CurrentUser,
    pagination: Pagination,
    filters: CalculationResultFilter = Depends(),
    _: None = Depends(require_permission("calculation", "read")),
):
    """
    Get detailed results for a calculation run.
    """
    from app.services.calculation_service import CalculationService
    
    service = CalculationService(db)
    
    results, total = await service.get_results(
        run_id=run_id,
        filters=filters,
        offset=pagination.offset,
        limit=pagination.limit,
    )
    
    return PaginatedResponse.create(
        items=results,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{run_id}/results/export")
async def export_calculation_results(
    run_id: UUID,
    db: DBSession,
    user: CurrentUser,
    format: str = Query(default="csv", pattern="^(csv|xlsx)$"),
    result_type: Optional[str] = None,
    _: None = Depends(require_permission("calculation", "export")),
):
    """
    Export calculation results to CSV or Excel.
    """
    from app.services.calculation_service import CalculationService
    
    service = CalculationService(db)
    
    run = await service.get_run(run_id)
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation run not found",
        )
    
    if run.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only export completed calculations",
        )
    
    file_content, filename, media_type = await service.export_results(
        run_id=run_id,
        format=format,
        result_type=result_type,
    )
    
    return StreamingResponse(
        iter([file_content]),
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/{run_id}/summary")
async def get_calculation_summary(
    run_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("calculation", "read")),
):
    """
    Get aggregated summary for a calculation run.
    """
    from app.services.calculation_service import CalculationService
    
    service = CalculationService(db)
    
    run = await service.get_run(run_id)
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation run not found",
        )
    
    summary = await service.get_summary(run_id)
    
    return summary


@router.get("/{run_id}/narrative", response_model=CalculationNarrative)
async def get_calculation_narrative(
    run_id: UUID,
    db: DBSession,
    user: CurrentUser,
    regenerate: bool = Query(default=False),
    _: None = Depends(require_permission("calculation", "read")),
):
    """
    Get AI-generated narrative for a calculation run.
    """
    from app.config import settings
    from app.services.calculation_service import CalculationService
    
    if not settings.AI_NARRATIVE_GENERATION:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI narrative generation is not enabled",
        )
    
    service = CalculationService(db)
    
    run = await service.get_run(run_id)
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation run not found",
        )
    
    if run.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only generate narrative for completed calculations",
        )
    
    narrative = await service.get_narrative(run_id, regenerate=regenerate)
    
    return narrative


@router.get("/{run_id}/anomalies")
async def get_calculation_anomalies(
    run_id: UUID,
    db: DBSession,
    user: CurrentUser,
    pagination: Pagination,
    min_score: float = Query(default=0.7, ge=0, le=1),
    _: None = Depends(require_permission("calculation", "read")),
):
    """
    Get AI-flagged anomalous results from a calculation.
    """
    from app.config import settings
    from app.services.calculation_service import CalculationService
    
    if not settings.AI_ANOMALY_DETECTION:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI anomaly detection is not enabled",
        )
    
    service = CalculationService(db)
    
    anomalies, total = await service.get_anomalies(
        run_id=run_id,
        min_score=min_score,
        offset=pagination.offset,
        limit=pagination.limit,
    )
    
    return PaginatedResponse.create(
        items=anomalies,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.post("/{run_id}/rerun", response_model=CalculationRunResponse)
async def rerun_calculation(
    run_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("calculation", "run")),
):
    """
    Rerun a calculation with the same parameters.
    """
    from app.services.calculation_service import CalculationService
    
    service = CalculationService(db)
    
    original_run = await service.get_run(run_id)
    if not original_run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation run not found",
        )
    
    new_run = await service.rerun(original_run, triggered_by=user)
    
    return new_run


@router.post("/compare", response_model=CalculationComparisonResponse)
async def compare_calculations(
    request: CalculationComparisonRequest,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("calculation", "read")),
):
    """
    Compare two calculation runs.
    """
    from app.services.calculation_service import CalculationService
    
    service = CalculationService(db)
    
    comparison = await service.compare_runs(
        base_run_id=request.base_run_id,
        comparison_run_id=request.comparison_run_id,
        result_types=request.result_types,
    )
    
    if not comparison:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or both calculation runs not found",
        )
    
    return comparison
