"""
Coverage Management API Routes
==============================

CRUD operations for policy coverages.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import CurrentUser, DBSession, require_permission
from app.schemas.common import SuccessMessage
from app.schemas.coverage import (
    CoverageCreate,
    CoverageResponse,
    CoverageUpdate,
)

router = APIRouter()


@router.get("/policy/{policy_id}", response_model=list[CoverageResponse])
async def list_policy_coverages(
    policy_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("policy", "read")),
):
    """
    List all coverages for a policy.
    """
    from app.services.coverage_service import CoverageService
    
    service = CoverageService(db)
    coverages = await service.list_by_policy(policy_id)
    
    return coverages


@router.get("/{coverage_id}", response_model=CoverageResponse)
async def get_coverage(
    coverage_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("policy", "read")),
):
    """
    Get a specific coverage by ID.
    """
    from app.services.coverage_service import CoverageService
    
    service = CoverageService(db)
    coverage = await service.get_coverage(coverage_id)
    
    if not coverage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coverage not found",
        )
    
    return coverage


@router.post("", response_model=CoverageResponse, status_code=status.HTTP_201_CREATED)
async def create_coverage(
    data: CoverageCreate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("policy", "update")),
):
    """
    Add a coverage to a policy.
    """
    from app.services.coverage_service import CoverageService
    from app.services.policy_service import PolicyService
    
    # Verify policy exists
    policy_service = PolicyService(db)
    policy = await policy_service.get_policy(data.policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found",
        )
    
    service = CoverageService(db)
    coverage = await service.create_coverage(data)
    
    return coverage


@router.put("/{coverage_id}", response_model=CoverageResponse)
async def update_coverage(
    coverage_id: UUID,
    data: CoverageUpdate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("policy", "update")),
):
    """
    Update a coverage.
    """
    from app.services.coverage_service import CoverageService
    
    service = CoverageService(db)
    
    coverage = await service.get_coverage(coverage_id)
    if not coverage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coverage not found",
        )
    
    updated = await service.update_coverage(coverage, data)
    
    return updated


@router.delete("/{coverage_id}", response_model=SuccessMessage)
async def delete_coverage(
    coverage_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("policy", "update")),
):
    """
    Delete a coverage.
    """
    from app.services.coverage_service import CoverageService
    
    service = CoverageService(db)
    
    coverage = await service.get_coverage(coverage_id)
    if not coverage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coverage not found",
        )
    
    await service.delete_coverage(coverage)
    
    return SuccessMessage(message="Coverage deleted successfully")
