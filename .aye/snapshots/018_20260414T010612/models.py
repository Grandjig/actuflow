"""
Model Definition API Routes
===========================

CRUD operations for actuarial model definitions.
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
from app.schemas.model import (
    ModelDefinitionCreate,
    ModelDefinitionListItem,
    ModelDefinitionResponse,
    ModelDefinitionUpdate,
    ModelValidationRequest,
    ModelValidationResponse,
)

router = APIRouter()


@router.get("", response_model=PaginatedResponse[ModelDefinitionListItem])
async def list_models(
    db: DBSession,
    user: CurrentUser,
    pagination: Pagination,
    sorting: Sorting,
    model_type: Optional[str] = None,
    line_of_business: Optional[str] = None,
    status_filter: Optional[str] = Query(default=None, alias="status"),
    search: Optional[str] = None,
    _: None = Depends(require_permission("model", "read")),
):
    """
    List model definitions with pagination.
    """
    from app.services.model_service import ModelService
    
    service = ModelService(db)
    
    models, total = await service.list_models(
        model_type=model_type,
        line_of_business=line_of_business,
        status=status_filter,
        search=search,
        offset=pagination.offset,
        limit=pagination.limit,
        sort_by=sorting.sort_by or "name",
        sort_order=sorting.sort_order,
    )
    
    return PaginatedResponse.create(
        items=models,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/templates", response_model=list[ModelDefinitionListItem])
async def list_model_templates(
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("model", "read")),
):
    """
    List available model templates.
    """
    from app.services.model_service import ModelService
    
    service = ModelService(db)
    templates = await service.list_templates()
    
    return templates


@router.get("/{model_id}", response_model=ModelDefinitionResponse)
async def get_model(
    model_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("model", "read")),
):
    """
    Get a model definition by ID.
    """
    from app.services.model_service import ModelService
    
    service = ModelService(db)
    model = await service.get_model(model_id)
    
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found",
        )
    
    return model


@router.post("", response_model=ModelDefinitionResponse, status_code=status.HTTP_201_CREATED)
async def create_model(
    data: ModelDefinitionCreate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("model", "create")),
):
    """
    Create a new model definition.
    """
    from app.services.model_service import ModelService
    
    service = ModelService(db)
    
    # Validate configuration
    validation = await service.validate_configuration(data.configuration)
    if not validation.valid:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": "Invalid model configuration", "errors": validation.errors},
        )
    
    model = await service.create_model(data, created_by=user)
    
    return model


@router.put("/{model_id}", response_model=ModelDefinitionResponse)
async def update_model(
    model_id: UUID,
    data: ModelDefinitionUpdate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("model", "update")),
):
    """
    Update a model definition.
    
    Can only update models in 'draft' status.
    """
    from app.services.model_service import ModelService
    
    service = ModelService(db)
    
    model = await service.get_model(model_id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found",
        )
    
    if model.status != "draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only update draft models",
        )
    
    # Validate configuration if provided
    if data.configuration:
        validation = await service.validate_configuration(data.configuration)
        if not validation.valid:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"message": "Invalid model configuration", "errors": validation.errors},
            )
    
    updated = await service.update_model(model, data, updated_by=user)
    
    return updated


@router.delete("/{model_id}", response_model=SuccessMessage)
async def delete_model(
    model_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("model", "delete")),
):
    """
    Soft delete a model definition.
    """
    from app.services.model_service import ModelService
    
    service = ModelService(db)
    
    model = await service.get_model(model_id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found",
        )
    
    if model.is_template:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete system templates",
        )
    
    await service.delete_model(model, deleted_by=user)
    
    return SuccessMessage(message="Model deleted")


@router.post("/{model_id}/clone", response_model=ModelDefinitionResponse)
async def clone_model(
    model_id: UUID,
    new_name: str = Query(max_length=255),
    db: DBSession = None,
    user: CurrentUser = None,
    _: None = Depends(require_permission("model", "create")),
):
    """
    Clone a model definition.
    """
    from app.services.model_service import ModelService
    
    service = ModelService(db)
    
    source_model = await service.get_model(model_id)
    if not source_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source model not found",
        )
    
    cloned = await service.clone_model(source_model, new_name=new_name, created_by=user)
    
    return cloned


@router.post("/validate", response_model=ModelValidationResponse)
async def validate_model_configuration(
    request: ModelValidationRequest,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("model", "read")),
):
    """
    Validate a model configuration without saving.
    """
    from app.services.model_service import ModelService
    
    service = ModelService(db)
    validation = await service.validate_configuration(request.configuration)
    
    return validation


@router.put("/{model_id}/activate", response_model=ModelDefinitionResponse)
async def activate_model(
    model_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("model", "update")),
):
    """
    Activate a model (change status from draft to active).
    """
    from app.services.model_service import ModelService
    
    service = ModelService(db)
    
    model = await service.get_model(model_id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found",
        )
    
    if model.status != "draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only activate draft models",
        )
    
    activated = await service.activate_model(model, activated_by=user)
    
    return activated
