"""
Policyholder Management API Routes
==================================

CRUD operations for policyholders.
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
from app.schemas.policyholder import (
    PolicyholderCreate,
    PolicyholderFilter,
    PolicyholderListItem,
    PolicyholderResponse,
    PolicyholderUpdate,
    PolicyholderWithPolicies,
)

router = APIRouter()


@router.get("", response_model=PaginatedResponse[PolicyholderListItem])
async def list_policyholders(
    db: DBSession,
    user: CurrentUser,
    pagination: Pagination,
    sorting: Sorting,
    filters: PolicyholderFilter = Depends(),
    _: None = Depends(require_permission("policyholder", "read")),
):
    """
    List policyholders with pagination and filtering.
    """
    from app.services.policyholder_service import PolicyholderService
    
    service = PolicyholderService(db)
    
    policyholders, total = await service.list_policyholders(
        filters=filters,
        offset=pagination.offset,
        limit=pagination.limit,
        sort_by=sorting.sort_by or "created_at",
        sort_order=sorting.sort_order,
    )
    
    return PaginatedResponse.create(
        items=policyholders,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{policyholder_id}", response_model=PolicyholderWithPolicies)
async def get_policyholder(
    policyholder_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("policyholder", "read")),
):
    """
    Get a specific policyholder by ID with their policies.
    """
    from app.services.policyholder_service import PolicyholderService
    
    service = PolicyholderService(db)
    policyholder = await service.get_with_policies(policyholder_id)
    
    if not policyholder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policyholder not found",
        )
    
    return policyholder


@router.post("", response_model=PolicyholderResponse, status_code=status.HTTP_201_CREATED)
async def create_policyholder(
    data: PolicyholderCreate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("policyholder", "create")),
):
    """
    Create a new policyholder.
    """
    from app.services.policyholder_service import PolicyholderService
    
    service = PolicyholderService(db)
    
    # Check external_id uniqueness if provided
    if data.external_id:
        existing = await service.get_by_external_id(data.external_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Policyholder with this external ID already exists",
            )
    
    policyholder = await service.create_policyholder(data, created_by=user)
    
    return policyholder


@router.put("/{policyholder_id}", response_model=PolicyholderResponse)
async def update_policyholder(
    policyholder_id: UUID,
    data: PolicyholderUpdate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("policyholder", "update")),
):
    """
    Update a policyholder.
    """
    from app.services.policyholder_service import PolicyholderService
    
    service = PolicyholderService(db)
    
    policyholder = await service.get_policyholder(policyholder_id)
    if not policyholder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policyholder not found",
        )
    
    updated = await service.update_policyholder(
        policyholder,
        data,
        updated_by=user,
    )
    
    return updated


@router.delete("/{policyholder_id}", response_model=SuccessMessage)
async def delete_policyholder(
    policyholder_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("policyholder", "delete")),
):
    """
    Soft delete a policyholder.
    
    Cannot delete if policyholder has active policies.
    """
    from app.services.policyholder_service import PolicyholderService
    
    service = PolicyholderService(db)
    
    policyholder = await service.get_policyholder(policyholder_id)
    if not policyholder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policyholder not found",
        )
    
    # Check for active policies
    active_count = await service.get_active_policy_count(policyholder_id)
    if active_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete policyholder with {active_count} active policies",
        )
    
    await service.delete_policyholder(policyholder, deleted_by=user)
    
    return SuccessMessage(message="Policyholder deleted successfully")


@router.get("/{policyholder_id}/policies")
async def get_policyholder_policies(
    policyholder_id: UUID,
    db: DBSession,
    user: CurrentUser,
    pagination: Pagination,
    status_filter: Optional[str] = Query(default=None),
    _: None = Depends(require_permission("policyholder", "read")),
):
    """
    Get all policies for a policyholder.
    """
    from app.services.policyholder_service import PolicyholderService
    
    service = PolicyholderService(db)
    
    policies, total = await service.get_policies(
        policyholder_id=policyholder_id,
        status_filter=status_filter,
        offset=pagination.offset,
        limit=pagination.limit,
    )
    
    return PaginatedResponse.create(
        items=policies,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.post("/search")
async def search_policyholders(
    db: DBSession,
    user: CurrentUser,
    query: str = Query(min_length=2, max_length=100),
    limit: int = Query(default=10, ge=1, le=50),
    _: None = Depends(require_permission("policyholder", "read")),
):
    """
    Quick search for policyholders (for autocomplete).
    """
    from app.services.policyholder_service import PolicyholderService
    
    service = PolicyholderService(db)
    results = await service.quick_search(query, limit=limit)
    
    return results
