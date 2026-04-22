"""Experience Analysis API Routes."""

from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from app.dependencies import CurrentUser, DBSession, Pagination, require_permission
from app.exceptions import NotFoundError
from app.models.user import User
from app.schemas.common import PaginatedResponse
from app.services.experience_service import ExperienceService

router = APIRouter()


class ExperienceStudyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    analysis_type: str
    study_period_start: date
    study_period_end: date
    parameters: dict = {}
    assumption_set_id: UUID | None = None


class ExperienceStudyResponse(BaseModel):
    id: UUID
    name: str
    analysis_type: str
    study_period_start: date
    study_period_end: date
    total_actual: float | None
    total_expected: float | None
    ae_ratio: float | None
    ai_narrative: str | None
    
    class Config:
        from_attributes = True


class ExperienceStudyDetailResponse(ExperienceStudyResponse):
    parameters: dict
    results: dict | None
    ai_recommendations: list | None


class RecommendationResponse(BaseModel):
    type: str
    confidence: float
    description: str
    suggested_factor: float | None = None


@router.get("", response_model=PaginatedResponse[ExperienceStudyResponse])
async def list_experience_studies(
    db: DBSession,
    current_user: Annotated[User, Depends(require_permission("experience", "read"))],
    pagination: Pagination,
    analysis_type: str | None = Query(None),
):
    """List experience analyses."""
    service = ExperienceService(db)
    analyses, total = await service.list_analyses(
        offset=pagination.offset,
        limit=pagination.limit,
        analysis_type=analysis_type,
    )
    
    total_pages = (total + pagination.page_size - 1) // pagination.page_size
    
    return PaginatedResponse(
        items=[ExperienceStudyResponse.model_validate(a) for a in analyses],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        total_pages=total_pages,
        has_next=pagination.page < total_pages,
        has_prev=pagination.page > 1,
    )


@router.get("/{analysis_id}", response_model=ExperienceStudyDetailResponse)
async def get_experience_study(
    analysis_id: UUID,
    db: DBSession,
    current_user: Annotated[User, Depends(require_permission("experience", "read"))],
):
    """Get an experience analysis."""
    service = ExperienceService(db)
    analysis = await service.get_analysis(analysis_id)
    
    if not analysis:
        raise NotFoundError("Experience analysis", analysis_id)
    
    return ExperienceStudyDetailResponse.model_validate(analysis)


@router.post("", response_model=ExperienceStudyDetailResponse, status_code=201)
async def run_experience_study(
    data: ExperienceStudyCreate,
    db: DBSession,
    current_user: Annotated[User, Depends(require_permission("experience", "create"))],
):
    """Run a new experience study."""
    service = ExperienceService(db)
    analysis = await service.run_experience_study(
        name=data.name,
        analysis_type=data.analysis_type,
        study_period_start=data.study_period_start,
        study_period_end=data.study_period_end,
        parameters=data.parameters,
        created_by=current_user,
        assumption_set_id=data.assumption_set_id,
    )
    return ExperienceStudyDetailResponse.model_validate(analysis)


@router.get("/{analysis_id}/recommendations", response_model=list[RecommendationResponse])
async def get_recommendations(
    analysis_id: UUID,
    db: DBSession,
    current_user: Annotated[User, Depends(require_permission("experience", "read"))],
):
    """Get AI recommendations for an analysis."""
    service = ExperienceService(db)
    recommendations = await service.get_recommendations(analysis_id)
    return [RecommendationResponse(**r) for r in recommendations]
