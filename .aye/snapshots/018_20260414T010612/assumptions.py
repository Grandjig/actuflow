"""
Assumption Management API Routes
================================

CRUD operations for assumption sets and tables.
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
from app.schemas.assumption import (
    AssumptionApprovalRequest,
    AssumptionComparison,
    AssumptionSetCreate,
    AssumptionSetListItem,
    AssumptionSetResponse,
    AssumptionSetUpdate,
    AssumptionSetWithTables,
    AssumptionSubmitRequest,
    AssumptionTableCreate,
    AssumptionTableResponse,
    AssumptionTableUpdate,
    ExperienceRecommendation,
)
from app.schemas.common import PaginatedResponse, SuccessMessage

router = APIRouter()


# =============================================================================
# Assumption Sets
# =============================================================================

@router.get("", response_model=PaginatedResponse[AssumptionSetListItem])
async def list_assumption_sets(
    db: DBSession,
    user: CurrentUser,
    pagination: Pagination,
    sorting: Sorting,
    status_filter: Optional[str] = Query(default=None, alias="status"),
    search: Optional[str] = None,
    _: None = Depends(require_permission("assumption", "read")),
):
    """
    List assumption sets with pagination.
    """
    from app.services.assumption_service import AssumptionService
    
    service = AssumptionService(db)
    
    sets, total = await service.list_sets(
        status=status_filter,
        search=search,
        offset=pagination.offset,
        limit=pagination.limit,
        sort_by=sorting.sort_by or "created_at",
        sort_order=sorting.sort_order,
    )
    
    return PaginatedResponse.create(
        items=sets,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{set_id}", response_model=AssumptionSetWithTables)
async def get_assumption_set(
    set_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("assumption", "read")),
):
    """
    Get assumption set with all tables.
    """
    from app.services.assumption_service import AssumptionService
    
    service = AssumptionService(db)
    assumption_set = await service.get_set_with_tables(set_id)
    
    if not assumption_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumption set not found",
        )
    
    return assumption_set


@router.post("", response_model=AssumptionSetResponse, status_code=status.HTTP_201_CREATED)
async def create_assumption_set(
    data: AssumptionSetCreate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("assumption", "create")),
):
    """
    Create a new assumption set.
    """
    from app.services.assumption_service import AssumptionService
    
    service = AssumptionService(db)
    assumption_set = await service.create_set(data, created_by=user)
    
    return assumption_set


@router.put("/{set_id}", response_model=AssumptionSetResponse)
async def update_assumption_set(
    set_id: UUID,
    data: AssumptionSetUpdate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("assumption", "update")),
):
    """
    Update an assumption set.
    
    Can only update sets in 'draft' status.
    """
    from app.services.assumption_service import AssumptionService
    
    service = AssumptionService(db)
    
    assumption_set = await service.get_set(set_id)
    if not assumption_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumption set not found",
        )
    
    if not assumption_set.is_editable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update assumption set in current status",
        )
    
    updated = await service.update_set(assumption_set, data, updated_by=user)
    
    return updated


@router.delete("/{set_id}", response_model=SuccessMessage)
async def delete_assumption_set(
    set_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("assumption", "delete")),
):
    """
    Soft delete an assumption set.
    
    Can only delete sets in 'draft' status.
    """
    from app.services.assumption_service import AssumptionService
    
    service = AssumptionService(db)
    
    assumption_set = await service.get_set(set_id)
    if not assumption_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumption set not found",
        )
    
    if assumption_set.status != "draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only delete draft assumption sets",
        )
    
    await service.delete_set(assumption_set, deleted_by=user)
    
    return SuccessMessage(message="Assumption set deleted")


@router.post("/{set_id}/clone", response_model=AssumptionSetResponse)
async def clone_assumption_set(
    set_id: UUID,
    new_name: str = Query(max_length=255),
    new_version: str = Query(max_length=50),
    db: DBSession = None,
    user: CurrentUser = None,
    _: None = Depends(require_permission("assumption", "create")),
):
    """
    Clone an assumption set with all its tables.
    """
    from app.services.assumption_service import AssumptionService
    
    service = AssumptionService(db)
    
    source_set = await service.get_set(set_id)
    if not source_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source assumption set not found",
        )
    
    cloned = await service.clone_set(
        source_set,
        new_name=new_name,
        new_version=new_version,
        created_by=user,
    )
    
    return cloned


# =============================================================================
# Workflow Actions
# =============================================================================

@router.post("/{set_id}/submit", response_model=AssumptionSetResponse)
async def submit_for_approval(
    set_id: UUID,
    request: AssumptionSubmitRequest,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("assumption", "update")),
):
    """
    Submit assumption set for approval.
    """
    from app.services.assumption_service import AssumptionService
    
    service = AssumptionService(db)
    
    assumption_set = await service.get_set(set_id)
    if not assumption_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumption set not found",
        )
    
    if assumption_set.status != "draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only submit draft assumption sets",
        )
    
    submitted = await service.submit_for_approval(
        assumption_set,
        notes=request.notes,
        submitted_by=user,
    )
    
    return submitted


@router.post("/{set_id}/approve", response_model=AssumptionSetResponse)
async def approve_or_reject(
    set_id: UUID,
    request: AssumptionApprovalRequest,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("assumption", "approve")),
):
    """
    Approve or reject an assumption set.
    """
    from app.services.assumption_service import AssumptionService
    
    service = AssumptionService(db)
    
    assumption_set = await service.get_set(set_id)
    if not assumption_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumption set not found",
        )
    
    if assumption_set.status != "pending_approval":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assumption set is not pending approval",
        )
    
    if request.action == "approve":
        result = await service.approve(
            assumption_set,
            notes=request.notes,
            approved_by=user,
        )
    else:
        result = await service.reject(
            assumption_set,
            notes=request.notes,
            rejected_by=user,
        )
    
    return result


# =============================================================================
# Comparison and AI Recommendations
# =============================================================================

@router.get("/{set_id}/compare/{other_id}", response_model=AssumptionComparison)
async def compare_assumption_sets(
    set_id: UUID,
    other_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("assumption", "read")),
):
    """
    Compare two assumption sets.
    """
    from app.services.assumption_service import AssumptionService
    
    service = AssumptionService(db)
    
    comparison = await service.compare_sets(set_id, other_id)
    
    if not comparison:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or both assumption sets not found",
        )
    
    return comparison


@router.get("/{set_id}/experience-recommendations", response_model=list[ExperienceRecommendation])
async def get_experience_recommendations(
    set_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("assumption", "read")),
):
    """
    Get AI-generated recommendations based on experience analysis.
    """
    from app.config import settings
    from app.services.assumption_service import AssumptionService
    
    if not settings.AI_EXPERIENCE_RECOMMENDATIONS:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI experience recommendations are not enabled",
        )
    
    service = AssumptionService(db)
    
    assumption_set = await service.get_set(set_id)
    if not assumption_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumption set not found",
        )
    
    recommendations = await service.get_experience_recommendations(assumption_set)
    
    return recommendations


# =============================================================================
# Assumption Tables
# =============================================================================

@router.get("/{set_id}/tables", response_model=list[AssumptionTableResponse])
async def list_assumption_tables(
    set_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("assumption", "read")),
):
    """
    List all tables in an assumption set.
    """
    from app.services.assumption_service import AssumptionService
    
    service = AssumptionService(db)
    tables = await service.list_tables(set_id)
    
    return tables


@router.get("/tables/{table_id}", response_model=AssumptionTableResponse)
async def get_assumption_table(
    table_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("assumption", "read")),
):
    """
    Get a specific assumption table.
    """
    from app.services.assumption_service import AssumptionService
    
    service = AssumptionService(db)
    table = await service.get_table(table_id)
    
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumption table not found",
        )
    
    return table


@router.post("/tables", response_model=AssumptionTableResponse, status_code=status.HTTP_201_CREATED)
async def create_assumption_table(
    data: AssumptionTableCreate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("assumption", "update")),
):
    """
    Add a table to an assumption set.
    """
    from app.services.assumption_service import AssumptionService
    
    service = AssumptionService(db)
    
    # Verify set exists and is editable
    assumption_set = await service.get_set(data.assumption_set_id)
    if not assumption_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumption set not found",
        )
    
    if not assumption_set.is_editable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot add tables to assumption set in current status",
        )
    
    table = await service.create_table(data)
    
    return table


@router.put("/tables/{table_id}", response_model=AssumptionTableResponse)
async def update_assumption_table(
    table_id: UUID,
    data: AssumptionTableUpdate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("assumption", "update")),
):
    """
    Update an assumption table.
    """
    from app.services.assumption_service import AssumptionService
    
    service = AssumptionService(db)
    
    table = await service.get_table(table_id)
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumption table not found",
        )
    
    # Check if parent set is editable
    assumption_set = await service.get_set(table.assumption_set_id)
    if not assumption_set.is_editable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update tables in assumption set with current status",
        )
    
    updated = await service.update_table(table, data)
    
    return updated


@router.delete("/tables/{table_id}", response_model=SuccessMessage)
async def delete_assumption_table(
    table_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("assumption", "update")),
):
    """
    Delete an assumption table.
    """
    from app.services.assumption_service import AssumptionService
    
    service = AssumptionService(db)
    
    table = await service.get_table(table_id)
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumption table not found",
        )
    
    # Check if parent set is editable
    assumption_set = await service.get_set(table.assumption_set_id)
    if not assumption_set.is_editable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete tables from assumption set with current status",
        )
    
    await service.delete_table(table)
    
    return SuccessMessage(message="Assumption table deleted")
