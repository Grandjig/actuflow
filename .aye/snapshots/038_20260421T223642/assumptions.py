"""
Assumptions API Routes
======================

Assumption set and table management.
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
from app.models.assumption_set import AssumptionSet
from app.models.assumption_table import AssumptionTable
from app.schemas.assumption import (
    AssumptionSetCreate,
    AssumptionSetUpdate,
    AssumptionSetResponse,
    AssumptionSetListItem,
    AssumptionTableCreate,
    AssumptionTableUpdate,
    AssumptionTableResponse,
    AssumptionApprovalRequest,
    AssumptionRejectionRequest,
)
from app.schemas.common import PaginatedResponse, SuccessResponse

router = APIRouter()


@router.get("", response_model=PaginatedResponse[AssumptionSetListItem])
async def list_assumption_sets(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    """List assumption sets."""
    query = select(AssumptionSet).where(AssumptionSet.is_deleted == False)

    if search:
        query = query.where(AssumptionSet.name.ilike(f"%{search}%"))

    if status:
        query = query.where(AssumptionSet.status == status)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = (
        query
        .options(selectinload(AssumptionSet.tables))
        .offset(pagination.offset)
        .limit(pagination.page_size)
        .order_by(AssumptionSet.created_at.desc())
    )
    result = await db.execute(query)
    assumption_sets = result.scalars().all()

    items = [
        AssumptionSetListItem(
            id=aset.id,
            name=aset.name,
            version=aset.version,
            status=aset.status,
            effective_date=aset.effective_date,
            table_count=len(aset.tables) if aset.tables else 0,
            created_at=aset.created_at,
        )
        for aset in assumption_sets
    ]

    return PaginatedResponse.create(
        items=items,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/approved", response_model=list[AssumptionSetResponse])
async def list_approved_assumption_sets(
    db: DBSession,
    current_user: CurrentUser,
):
    """List approved assumption sets for use in calculations."""
    result = await db.execute(
        select(AssumptionSet)
        .where(AssumptionSet.status == "approved")
        .where(AssumptionSet.is_deleted == False)
        .options(selectinload(AssumptionSet.tables))
        .order_by(AssumptionSet.effective_date.desc())
    )
    return result.scalars().all()


@router.get("/{set_id}", response_model=AssumptionSetResponse)
async def get_assumption_set(
    db: DBSession,
    set_id: UUID,
    current_user: CurrentUser,
):
    """Get assumption set by ID."""
    result = await db.execute(
        select(AssumptionSet)
        .where(AssumptionSet.id == set_id)
        .where(AssumptionSet.is_deleted == False)
        .options(selectinload(AssumptionSet.tables))
    )
    assumption_set = result.scalar_one_or_none()

    if not assumption_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumption set not found",
        )

    return assumption_set


@router.post("", response_model=AssumptionSetResponse, status_code=status.HTTP_201_CREATED)
async def create_assumption_set(
    db: DBSession,
    data: AssumptionSetCreate,
    current_user: CurrentUser = Depends(require_permission("assumption", "create")),
):
    """Create a new assumption set."""
    assumption_set = AssumptionSet(
        **data.model_dump(),
        status="draft",
        created_by_id=current_user.id,
    )
    db.add(assumption_set)
    await db.flush()
    await db.refresh(assumption_set)

    return assumption_set


@router.put("/{set_id}", response_model=AssumptionSetResponse)
async def update_assumption_set(
    db: DBSession,
    set_id: UUID,
    data: AssumptionSetUpdate,
    _: CurrentUser = Depends(require_permission("assumption", "update")),
):
    """Update an assumption set."""
    result = await db.execute(
        select(AssumptionSet)
        .where(AssumptionSet.id == set_id)
        .where(AssumptionSet.is_deleted == False)
    )
    assumption_set = result.scalar_one_or_none()

    if not assumption_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumption set not found",
        )

    if assumption_set.status == "approved":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify approved assumption set",
        )

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(assumption_set, field, value)

    await db.flush()
    await db.refresh(assumption_set, ["tables"])

    return assumption_set


@router.post("/{set_id}/submit", response_model=AssumptionSetResponse)
async def submit_for_approval(
    db: DBSession,
    set_id: UUID,
    _: CurrentUser = Depends(require_permission("assumption", "update")),
):
    """Submit assumption set for approval."""
    result = await db.execute(
        select(AssumptionSet)
        .where(AssumptionSet.id == set_id)
        .where(AssumptionSet.is_deleted == False)
    )
    assumption_set = result.scalar_one_or_none()

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

    assumption_set.status = "pending_approval"
    await db.flush()
    await db.refresh(assumption_set)

    return assumption_set


@router.post("/{set_id}/approve", response_model=AssumptionSetResponse)
async def approve_assumption_set(
    db: DBSession,
    set_id: UUID,
    data: AssumptionApprovalRequest,
    current_user: CurrentUser = Depends(require_permission("assumption", "approve")),
):
    """Approve an assumption set."""
    result = await db.execute(
        select(AssumptionSet)
        .where(AssumptionSet.id == set_id)
        .where(AssumptionSet.is_deleted == False)
    )
    assumption_set = result.scalar_one_or_none()

    if not assumption_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumption set not found",
        )

    if assumption_set.status != "pending_approval":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only approve pending assumption sets",
        )

    assumption_set.status = "approved"
    assumption_set.approved_by_id = current_user.id
    assumption_set.approval_date = datetime.utcnow()
    assumption_set.approval_notes = data.approval_notes

    await db.flush()
    await db.refresh(assumption_set)

    return assumption_set


@router.post("/{set_id}/reject", response_model=AssumptionSetResponse)
async def reject_assumption_set(
    db: DBSession,
    set_id: UUID,
    data: AssumptionRejectionRequest,
    current_user: CurrentUser = Depends(require_permission("assumption", "approve")),
):
    """Reject an assumption set."""
    result = await db.execute(
        select(AssumptionSet)
        .where(AssumptionSet.id == set_id)
        .where(AssumptionSet.is_deleted == False)
    )
    assumption_set = result.scalar_one_or_none()

    if not assumption_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumption set not found",
        )

    if assumption_set.status != "pending_approval":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only reject pending assumption sets",
        )

    assumption_set.status = "rejected"
    assumption_set.rejection_reason = data.rejection_reason

    await db.flush()
    await db.refresh(assumption_set)

    return assumption_set


@router.delete("/{set_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_assumption_set(
    db: DBSession,
    set_id: UUID,
    _: CurrentUser = Depends(require_permission("assumption", "delete")),
):
    """Soft delete an assumption set."""
    result = await db.execute(
        select(AssumptionSet)
        .where(AssumptionSet.id == set_id)
        .where(AssumptionSet.is_deleted == False)
    )
    assumption_set = result.scalar_one_or_none()

    if not assumption_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumption set not found",
        )

    assumption_set.is_deleted = True


# =============================================================================
# Assumption Tables
# =============================================================================

@router.get("/{set_id}/tables", response_model=list[AssumptionTableResponse])
async def list_tables(
    db: DBSession,
    set_id: UUID,
    current_user: CurrentUser,
):
    """List tables in an assumption set."""
    result = await db.execute(
        select(AssumptionTable)
        .where(AssumptionTable.assumption_set_id == set_id)
        .order_by(AssumptionTable.table_type, AssumptionTable.name)
    )
    return result.scalars().all()


@router.post("/{set_id}/tables", response_model=AssumptionTableResponse, status_code=status.HTTP_201_CREATED)
async def create_table(
    db: DBSession,
    set_id: UUID,
    data: AssumptionTableCreate,
    _: CurrentUser = Depends(require_permission("assumption", "update")),
):
    """Add a table to an assumption set."""
    # Verify set exists and is editable
    result = await db.execute(
        select(AssumptionSet)
        .where(AssumptionSet.id == set_id)
        .where(AssumptionSet.is_deleted == False)
    )
    assumption_set = result.scalar_one_or_none()

    if not assumption_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumption set not found",
        )

    if assumption_set.status == "approved":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot add tables to approved assumption set",
        )

    table = AssumptionTable(
        assumption_set_id=set_id,
        **data.model_dump(),
    )
    db.add(table)
    await db.flush()
    await db.refresh(table)

    return table


@router.put("/{set_id}/tables/{table_id}", response_model=AssumptionTableResponse)
async def update_table(
    db: DBSession,
    set_id: UUID,
    table_id: UUID,
    data: AssumptionTableUpdate,
    _: CurrentUser = Depends(require_permission("assumption", "update")),
):
    """Update a table in an assumption set."""
    result = await db.execute(
        select(AssumptionTable)
        .where(AssumptionTable.id == table_id)
        .where(AssumptionTable.assumption_set_id == set_id)
    )
    table = result.scalar_one_or_none()

    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found",
        )

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(table, field, value)

    await db.flush()
    await db.refresh(table)

    return table


@router.delete("/{set_id}/tables/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(
    db: DBSession,
    set_id: UUID,
    table_id: UUID,
    _: CurrentUser = Depends(require_permission("assumption", "update")),
):
    """Delete a table from an assumption set."""
    result = await db.execute(
        select(AssumptionTable)
        .where(AssumptionTable.id == table_id)
        .where(AssumptionTable.assumption_set_id == set_id)
    )
    table = result.scalar_one_or_none()

    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found",
        )

    await db.delete(table)
