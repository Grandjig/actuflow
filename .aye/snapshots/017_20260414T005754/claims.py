"""
Claims Management API Routes
============================

CRUD operations for insurance claims.
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
from app.schemas.claim import (
    ClaimAnomalyAlert,
    ClaimCreate,
    ClaimFilter,
    ClaimListItem,
    ClaimResponse,
    ClaimStatusUpdate,
    ClaimSummaryStats,
    ClaimUpdate,
)
from app.schemas.common import PaginatedResponse, SuccessMessage

router = APIRouter()


@router.get("", response_model=PaginatedResponse[ClaimListItem])
async def list_claims(
    db: DBSession,
    user: CurrentUser,
    pagination: Pagination,
    sorting: Sorting,
    filters: ClaimFilter = Depends(),
    _: None = Depends(require_permission("claim", "read")),
):
    """
    List claims with pagination and filtering.
    """
    from app.services.claim_service import ClaimService
    
    service = ClaimService(db)
    
    claims, total = await service.list_claims(
        filters=filters,
        offset=pagination.offset,
        limit=pagination.limit,
        sort_by=sorting.sort_by or "claim_date",
        sort_order=sorting.sort_order,
    )
    
    return PaginatedResponse.create(
        items=claims,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/stats", response_model=ClaimSummaryStats)
async def get_claim_stats(
    db: DBSession,
    user: CurrentUser,
    filters: ClaimFilter = Depends(),
    _: None = Depends(require_permission("claim", "read")),
):
    """
    Get summary statistics for claims.
    """
    from app.services.claim_service import ClaimService
    
    service = ClaimService(db)
    stats = await service.get_summary_stats(filters=filters)
    
    return stats


@router.get("/anomalies", response_model=PaginatedResponse[ClaimAnomalyAlert])
async def get_anomaly_alerts(
    db: DBSession,
    user: CurrentUser,
    pagination: Pagination,
    min_score: float = Query(default=0.7, ge=0, le=1),
    reviewed: Optional[bool] = None,
    _: None = Depends(require_permission("claim", "read")),
):
    """
    Get AI-flagged suspicious claims.
    """
    from app.config import settings
    from app.services.claim_service import ClaimService
    
    if not settings.AI_ANOMALY_DETECTION:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI anomaly detection is not enabled",
        )
    
    service = ClaimService(db)
    
    alerts, total = await service.get_anomaly_alerts(
        min_score=min_score,
        reviewed=reviewed,
        offset=pagination.offset,
        limit=pagination.limit,
    )
    
    return PaginatedResponse.create(
        items=alerts,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{claim_id}", response_model=ClaimResponse)
async def get_claim(
    claim_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("claim", "read")),
):
    """
    Get a specific claim by ID.
    """
    from app.services.claim_service import ClaimService
    
    service = ClaimService(db)
    claim = await service.get_claim(claim_id)
    
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found",
        )
    
    return claim


@router.post("", response_model=ClaimResponse, status_code=status.HTTP_201_CREATED)
async def create_claim(
    data: ClaimCreate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("claim", "create")),
):
    """
    Create a new claim.
    """
    from app.services.claim_service import ClaimService
    from app.services.policy_service import PolicyService
    
    # Verify policy exists
    policy_service = PolicyService(db)
    policy = await policy_service.get_policy(data.policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found",
        )
    
    service = ClaimService(db)
    claim = await service.create_claim(data, created_by=user)
    
    return claim


@router.put("/{claim_id}", response_model=ClaimResponse)
async def update_claim(
    claim_id: UUID,
    data: ClaimUpdate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("claim", "update")),
):
    """
    Update a claim.
    """
    from app.services.claim_service import ClaimService
    
    service = ClaimService(db)
    
    claim = await service.get_claim(claim_id)
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found",
        )
    
    updated = await service.update_claim(claim, data, updated_by=user)
    
    return updated


@router.put("/{claim_id}/status", response_model=ClaimResponse)
async def update_claim_status(
    claim_id: UUID,
    status_data: ClaimStatusUpdate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("claim", "update")),
):
    """
    Update a claim's status.
    """
    from app.services.claim_service import ClaimService
    
    service = ClaimService(db)
    
    claim = await service.get_claim(claim_id)
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found",
        )
    
    updated = await service.update_status(claim, status_data, updated_by=user)
    
    return updated


@router.delete("/{claim_id}", response_model=SuccessMessage)
async def delete_claim(
    claim_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("claim", "delete")),
):
    """
    Soft delete a claim.
    """
    from app.services.claim_service import ClaimService
    
    service = ClaimService(db)
    
    claim = await service.get_claim(claim_id)
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found",
        )
    
    await service.delete_claim(claim, deleted_by=user)
    
    return SuccessMessage(message="Claim deleted successfully")


@router.put("/{claim_id}/anomaly-review")
async def review_claim_anomaly(
    claim_id: UUID,
    false_positive: bool,
    notes: Optional[str] = None,
    db: DBSession = None,
    user: CurrentUser = None,
    _: None = Depends(require_permission("claim", "update")),
):
    """
    Review an AI-flagged anomaly for a claim.
    """
    from app.services.claim_service import ClaimService
    
    service = ClaimService(db)
    
    claim = await service.get_claim(claim_id)
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found",
        )
    
    await service.review_anomaly(
        claim,
        false_positive=false_positive,
        notes=notes,
        reviewed_by=user,
    )
    
    return SuccessMessage(message="Anomaly review recorded")
