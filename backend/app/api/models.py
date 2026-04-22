"""
Models API Routes
=================

Model definition management.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select

from app.dependencies import (
    DBSession,
    CurrentUser,
    Pagination,
    require_permission,
)
from app.models.model_definition import ModelDefinition
from app.schemas.calculation import (
    ModelDefinitionCreate,
    ModelDefinitionUpdate,
    ModelDefinitionResponse,
)
from app.schemas.common import PaginatedResponse

router = APIRouter()


@router.get("", response_model=PaginatedResponse[ModelDefinitionResponse])
async def list_models(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    search: Optional[str] = Query(None),
    model_type: Optional[str] = Query(None),
    line_of_business: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
):
    """List model definitions."""
    query = select(ModelDefinition).where(ModelDefinition.is_deleted == False)

    if search:
        query = query.where(ModelDefinition.name.ilike(f"%{search}%"))

    if model_type:
        query = query.where(ModelDefinition.model_type == model_type)

    if line_of_business:
        query = query.where(ModelDefinition.line_of_business == line_of_business)

    if status_filter:
        query = query.where(ModelDefinition.status == status_filter)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = (
        query
        .offset(pagination.offset)
        .limit(pagination.page_size)
        .order_by(ModelDefinition.name)
    )
    result = await db.execute(query)
    models = result.scalars().all()

    return PaginatedResponse.create(
        items=models,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/active", response_model=list[ModelDefinitionResponse])
async def list_active_models(
    db: DBSession,
    current_user: CurrentUser,
):
    """List active models for use in calculations."""
    result = await db.execute(
        select(ModelDefinition)
        .where(ModelDefinition.status == "active")
        .where(ModelDefinition.is_deleted == False)
        .order_by(ModelDefinition.name)
    )
    return result.scalars().all()


@router.get("/{model_id}", response_model=ModelDefinitionResponse)
async def get_model(
    db: DBSession,
    model_id: UUID,
    current_user: CurrentUser,
):
    """Get a model definition by ID."""
    result = await db.execute(
        select(ModelDefinition)
        .where(ModelDefinition.id == model_id)
        .where(ModelDefinition.is_deleted == False)
    )
    model = result.scalar_one_or_none()

    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found",
        )

    return model


@router.post("", response_model=ModelDefinitionResponse, status_code=status.HTTP_201_CREATED)
async def create_model(
    db: DBSession,
    data: ModelDefinitionCreate,
    current_user: CurrentUser = Depends(require_permission("model", "create")),
):
    """Create a new model definition."""
    model = ModelDefinition(
        **data.model_dump(),
        status="draft",
        is_system_model=False,
        created_by_id=current_user.id,
    )
    db.add(model)
    await db.flush()
    await db.refresh(model)

    return model


@router.put("/{model_id}", response_model=ModelDefinitionResponse)
async def update_model(
    db: DBSession,
    model_id: UUID,
    data: ModelDefinitionUpdate,
    _: CurrentUser = Depends(require_permission("model", "update")),
):
    """Update a model definition."""
    result = await db.execute(
        select(ModelDefinition)
        .where(ModelDefinition.id == model_id)
        .where(ModelDefinition.is_deleted == False)
    )
    model = result.scalar_one_or_none()

    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found",
        )

    if model.is_system_model:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify system models",
        )

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(model, field, value)

    await db.flush()
    await db.refresh(model)

    return model


@router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_model(
    db: DBSession,
    model_id: UUID,
    _: CurrentUser = Depends(require_permission("model", "delete")),
):
    """Soft delete a model definition."""
    result = await db.execute(
        select(ModelDefinition)
        .where(ModelDefinition.id == model_id)
        .where(ModelDefinition.is_deleted == False)
    )
    model = result.scalar_one_or_none()

    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found",
        )

    if model.is_system_model:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete system models",
        )

    model.is_deleted = True
