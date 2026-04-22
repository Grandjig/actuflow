"""
Policy Management API Routes
============================

CRUD operations for insurance policies.
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
from app.schemas.common import BulkActionResponse, PaginatedResponse, SuccessMessage
from app.schemas.policy import (
    PolicyBulkUpdate,
    PolicyCreate,
    PolicyFilter,
    PolicyListItem,
    PolicyResponse,
    PolicyStatusUpdate,
    PolicySummaryStats,
    PolicyUpdate,
    PolicyWithDetails,
)

router = APIRouter()


@router.get("", response_model=PaginatedResponse[PolicyListItem])
async def list_policies(
    db: DBSession,
    user: CurrentUser,
    pagination: Pagination,
    sorting: Sorting,
    filters: PolicyFilter = Depends(),
    _: None = Depends(require_permission("policy", "read")),
):
    """
    List policies with pagination, sorting, and filtering.
    """
    from app.services.policy_service import PolicyService
    
    service = PolicyService(db)
    
    policies, total = await service.list_policies(
        filters=filters,
        offset=pagination.offset,
        limit=pagination.limit,
        sort_by=sorting.sort_by or "created_at",
        sort_order=sorting.sort_order,
    )
    
    return PaginatedResponse.create(
        items=policies,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/stats", response_model=PolicySummaryStats)
async def get_policy_stats(
    db: DBSession,
    user: CurrentUser,
    filters: PolicyFilter = Depends(),
    _: None = Depends(require_permission("policy", "read")),
):
    """
    Get summary statistics for policies.
    """
    from app.services.policy_service import PolicyService
    
    service = PolicyService(db)
    stats = await service.get_summary_stats(filters=filters)
    
    return stats


@router.get("/export")
async def export_policies(
    db: DBSession,
    user: CurrentUser,
    filters: PolicyFilter = Depends(),
    format: str = Query(default="csv", pattern="^(csv|xlsx)$"),
    _: None = Depends(require_permission("policy", "export")),
):
    """
    Export policies to CSV or Excel.
    """
    from app.services.policy_service import PolicyService
    
    service = PolicyService(db)
    file_content, filename, media_type = await service.export_policies(
        filters=filters,
        format=format,
    )
    
    return StreamingResponse(
        iter([file_content]),
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/{policy_id}", response_model=PolicyWithDetails)
async def get_policy(
    policy_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("policy", "read")),
):
    """
    Get a specific policy by ID with related data.
    """
    from app.services.policy_service import PolicyService
    
    service = PolicyService(db)
    policy = await service.get_policy_with_details(policy_id)
    
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found",
        )
    
    return policy


@router.post("", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED)
async def create_policy(
    policy_data: PolicyCreate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("policy", "create")),
):
    """
    Create a new policy.
    """
    from app.services.policy_service import PolicyService
    
    service = PolicyService(db)
    
    # Check policy number uniqueness
    existing = await service.get_by_policy_number(policy_data.policy_number)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Policy with this number already exists",
        )
    
    policy = await service.create_policy(policy_data, created_by=user)
    
    return policy


@router.put("/{policy_id}", response_model=PolicyResponse)
async def update_policy(
    policy_id: UUID,
    policy_data: PolicyUpdate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("policy", "update")),
):
    """
    Update a policy.
    """
    from app.services.policy_service import PolicyService
    
    service = PolicyService(db)
    
    policy = await service.get_policy(policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found",
        )
    
    updated_policy = await service.update_policy(
        policy,
        policy_data,
        updated_by=user,
    )
    
    return updated_policy


@router.put("/{policy_id}/status", response_model=PolicyResponse)
async def update_policy_status(
    policy_id: UUID,
    status_data: PolicyStatusUpdate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("policy", "update")),
):
    """
    Update a policy's status.
    """
    from app.services.policy_service import PolicyService
    
    service = PolicyService(db)
    
    policy = await service.get_policy(policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found",
        )
    
    updated_policy = await service.update_status(
        policy,
        status_data,
        updated_by=user,
    )
    
    return updated_policy


@router.delete("/{policy_id}", response_model=SuccessMessage)
async def delete_policy(
    policy_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("policy", "delete")),
):
    """
    Soft delete a policy.
    """
    from app.services.policy_service import PolicyService
    
    service = PolicyService(db)
    
    policy = await service.get_policy(policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found",
        )
    
    await service.delete_policy(policy, deleted_by=user)
    
    return SuccessMessage(message="Policy deleted successfully")


@router.post("/bulk", response_model=BulkActionResponse)
async def bulk_create_policies(
    policies: list[PolicyCreate],
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("policy", "create")),
):
    """
    Bulk create policies.
    """
    from app.services.policy_service import PolicyService
    
    service = PolicyService(db)
    result = await service.bulk_create(policies, created_by=user)
    
    return result


@router.put("/bulk", response_model=BulkActionResponse)
async def bulk_update_policies(
    bulk_data: PolicyBulkUpdate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("policy", "update")),
):
    """
    Bulk update policies.
    """
    from app.services.policy_service import PolicyService
    
    service = PolicyService(db)
    result = await service.bulk_update(
        bulk_data.ids,
        bulk_data.update,
        updated_by=user,
    )
    
    return result


@router.get("/{policy_id}/history")
async def get_policy_history(
    policy_id: UUID,
    db: DBSession,
    user: CurrentUser,
    pagination: Pagination,
    _: None = Depends(require_permission("policy", "read")),
):
    """
    Get audit history for a policy.
    """
    from app.services.audit_service import AuditService
    
    service = AuditService(db)
    
    history, total = await service.get_resource_history(
        resource_type="policy",
        resource_id=policy_id,
        offset=pagination.offset,
        limit=pagination.limit,
    )
    
    return PaginatedResponse.create(
        items=history,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{policy_id}/similar")
async def find_similar_policies(
    policy_id: UUID,
    db: DBSession,
    user: CurrentUser,
    limit: int = Query(default=5, ge=1, le=20),
    _: None = Depends(require_permission("policy", "read")),
):
    """
    Find policies similar to this one (AI-powered).
    """
    from app.config import settings
    from app.services.policy_service import PolicyService
    
    if not settings.AI_SEMANTIC_SEARCH:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI search is not enabled",
        )
    
    service = PolicyService(db)
    
    policy = await service.get_policy(policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found",
        )
    
    similar = await service.find_similar(policy, limit=limit)
    
    return similar
