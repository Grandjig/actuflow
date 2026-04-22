"""
Calculations API Routes
=======================

Calculation run management and results.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.dependencies import (
    DBSession,
    CurrentUser,
    Pagination,
    require_permission,
)
from app.models.calculation_run import CalculationRun
from app.models.calculation_result import CalculationResult
from app.models.model_definition import ModelDefinition
from app.models.assumption_set import AssumptionSet
from app.schemas.calculation import (
    CalculationRunCreate,
    CalculationRunResponse,
    CalculationRunListItem,
    CalculationProgress,
    CalculationResultResponse,
    CalculationSummary,
    CalculationNarrative,
)
from app.schemas.common import PaginatedResponse, SuccessResponse

router = APIRouter()


@router.get("", response_model=PaginatedResponse[CalculationRunListItem])
async def list_calculations(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    search: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    trigger_type: Optional[str] = Query(None),
):
    """List calculation runs."""
    query = select(CalculationRun)

    if search:
        query = query.where(CalculationRun.run_name.ilike(f"%{search}%"))

    if status_filter:
        query = query.where(CalculationRun.status == status_filter)

    if trigger_type:
        query = query.where(CalculationRun.trigger_type == trigger_type)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = (
        query
        .options(
            selectinload(CalculationRun.model_definition),
            selectinload(CalculationRun.assumption_set),
        )
        .offset(pagination.offset)
        .limit(pagination.page_size)
        .order_by(CalculationRun.created_at.desc())
    )
    result = await db.execute(query)
    runs = result.scalars().all()

    items = [
        CalculationRunListItem(
            id=run.id,
            run_name=run.run_name,
            model_name=run.model_definition.name if run.model_definition else None,
            status=run.status,
            started_at=run.started_at,
            completed_at=run.completed_at,
            duration_seconds=run.duration_seconds,
            policies_count=run.policies_count,
            trigger_type=run.trigger_type,
        )
        for run in runs
    ]

    return PaginatedResponse.create(
        items=items,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{run_id}", response_model=CalculationRunResponse)
async def get_calculation(
    db: DBSession,
    run_id: UUID,
    current_user: CurrentUser,
):
    """Get a calculation run by ID."""
    result = await db.execute(
        select(CalculationRun)
        .where(CalculationRun.id == run_id)
        .options(
            selectinload(CalculationRun.model_definition),
            selectinload(CalculationRun.assumption_set),
            selectinload(CalculationRun.triggered_by),
        )
    )
    run = result.scalar_one_or_none()

    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation run not found",
        )

    return run


@router.post("", response_model=CalculationRunResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_calculation(
    db: DBSession,
    data: CalculationRunCreate,
    current_user: CurrentUser = Depends(require_permission("calculation", "create")),
):
    """Create and queue a new calculation run."""
    # Validate model exists and is active
    result = await db.execute(
        select(ModelDefinition)
        .where(ModelDefinition.id == data.model_definition_id)
        .where(ModelDefinition.status == "active")
        .where(ModelDefinition.is_deleted == False)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Model not found or not active",
        )

    # Validate assumption set exists and is approved
    result = await db.execute(
        select(AssumptionSet)
        .where(AssumptionSet.id == data.assumption_set_id)
        .where(AssumptionSet.status == "approved")
        .where(AssumptionSet.is_deleted == False)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assumption set not found or not approved",
        )

    run = CalculationRun(
        run_name=data.run_name,
        model_definition_id=data.model_definition_id,
        assumption_set_id=data.assumption_set_id,
        policy_filter=data.policy_filter,
        parameters=data.parameters,
        status="queued",
        trigger_type="manual",
        triggered_by_id=current_user.id,
    )
    db.add(run)
    await db.flush()
    await db.refresh(run, ["model_definition", "assumption_set"])

    # TODO: Dispatch Celery task
    # from calculation_engine.tasks import run_calculation_task
    # run_calculation_task.delay(str(run.id))

    return run


@router.get("/{run_id}/progress", response_model=CalculationProgress)
async def get_calculation_progress(
    run_id: UUID,
    current_user: CurrentUser,
):
    """Get real-time progress of a running calculation."""
    # In production, this would read from Redis
    # For now, return mock data
    return CalculationProgress(
        status="running",
        progress_percent=45,
        progress_message="Processing batch 45 of 100",
        policies_processed=4500,
        policies_total=10000,
        started_at=datetime.utcnow(),
        estimated_completion=None,
    )


@router.post("/{run_id}/cancel", response_model=SuccessResponse)
async def cancel_calculation(
    db: DBSession,
    run_id: UUID,
    current_user: CurrentUser = Depends(require_permission("calculation", "update")),
):
    """Cancel a running or queued calculation."""
    result = await db.execute(
        select(CalculationRun).where(CalculationRun.id == run_id)
    )
    run = result.scalar_one_or_none()

    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation run not found",
        )

    if run.status not in ["queued", "running"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel calculation with status '{run.status}'",
        )

    run.status = "cancelled"
    run.completed_at = datetime.utcnow()

    # TODO: Revoke Celery task

    return SuccessResponse(message="Calculation cancelled")


@router.get("/{run_id}/results", response_model=PaginatedResponse[CalculationResultResponse])
async def get_calculation_results(
    db: DBSession,
    run_id: UUID,
    pagination: Pagination,
    current_user: CurrentUser,
    policy_id: Optional[UUID] = Query(None),
    result_type: Optional[str] = Query(None),
    anomaly_only: bool = Query(False),
):
    """Get calculation results."""
    query = select(CalculationResult).where(CalculationResult.calculation_run_id == run_id)

    if policy_id:
        query = query.where(CalculationResult.policy_id == policy_id)

    if result_type:
        query = query.where(CalculationResult.result_type == result_type)

    if anomaly_only:
        query = query.where(CalculationResult.anomaly_flag == True)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = (
        query
        .offset(pagination.offset)
        .limit(pagination.page_size)
        .order_by(CalculationResult.policy_id, CalculationResult.projection_month)
    )
    result = await db.execute(query)
    results = result.scalars().all()

    return PaginatedResponse.create(
        items=results,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{run_id}/summary", response_model=CalculationSummary)
async def get_calculation_summary(
    db: DBSession,
    run_id: UUID,
    current_user: CurrentUser,
):
    """Get summary statistics for a calculation run."""
    result = await db.execute(
        select(CalculationRun).where(CalculationRun.id == run_id)
    )
    run = result.scalar_one_or_none()

    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation run not found",
        )

    # Get anomaly count
    anomaly_result = await db.execute(
        select(func.count(CalculationResult.id))
        .where(CalculationResult.calculation_run_id == run_id)
        .where(CalculationResult.anomaly_flag == True)
    )
    anomaly_count = anomaly_result.scalar() or 0

    summary = run.result_summary or {}

    return CalculationSummary(
        total_policies=run.policies_count or 0,
        total_reserves=summary.get("total_reserves", 0),
        total_premiums=summary.get("total_premiums", 0),
        by_product_type=summary.get("by_product_type", {}),
        by_status=summary.get("by_status", {}),
        anomaly_count=anomaly_count,
    )


@router.get("/{run_id}/narrative", response_model=CalculationNarrative)
async def get_calculation_narrative(
    db: DBSession,
    run_id: UUID,
    current_user: CurrentUser,
):
    """Get AI-generated narrative for a calculation run."""
    result = await db.execute(
        select(CalculationRun).where(CalculationRun.id == run_id)
    )
    run = result.scalar_one_or_none()

    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation run not found",
        )

    narrative = run.ai_narrative or "Narrative not yet generated."

    return CalculationNarrative(
        narrative=narrative,
        generated_at=run.completed_at or datetime.utcnow(),
        key_points=[],
        confidence=0.9,
    )


@router.get("/{run_id}/anomalies", response_model=list[CalculationResultResponse])
async def get_calculation_anomalies(
    db: DBSession,
    run_id: UUID,
    current_user: CurrentUser,
    limit: int = Query(20, le=100),
):
    """Get anomalous results from a calculation run."""
    result = await db.execute(
        select(CalculationResult)
        .where(CalculationResult.calculation_run_id == run_id)
        .where(CalculationResult.anomaly_flag == True)
        .order_by(CalculationResult.created_at.desc())
        .limit(limit)
    )
    return result.scalars().all()
