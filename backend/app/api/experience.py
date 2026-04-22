"""
Experience Analysis API Routes
==============================

Experience studies and A/E analysis.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime

from app.dependencies import DBSession, CurrentUser, Pagination, require_permission
from app.models.experience_analysis import ExperienceAnalysis
from app.schemas.common import PaginatedResponse

router = APIRouter()


class ExperienceStudyCreate(BaseModel):
    name: str
    analysis_type: str  # mortality, lapse, morbidity
    study_period_start: str
    study_period_end: str
    parameters: dict = {}
    assumption_set_id: Optional[UUID] = None


class ExperienceAnalysisResponse(BaseModel):
    id: UUID
    name: str
    analysis_type: str
    study_period_start: date
    study_period_end: date
    parameters: dict
    results: Optional[dict]
    total_actual: Optional[float]
    total_expected: Optional[float]
    ae_ratio: Optional[float]
    ai_recommendations: Optional[list]
    ai_narrative: Optional[str]
    created_by_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("", response_model=PaginatedResponse[ExperienceAnalysisResponse])
async def list_experience_analyses(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    analysis_type: Optional[str] = Query(None),
):
    """List experience analyses."""
    query = select(ExperienceAnalysis)
    
    if analysis_type:
        query = query.where(ExperienceAnalysis.analysis_type == analysis_type)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.offset(pagination.offset).limit(pagination.page_size).order_by(ExperienceAnalysis.created_at.desc())
    result = await db.execute(query)
    analyses = result.scalars().all()

    return PaginatedResponse.create(
        items=analyses,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.post("", response_model=ExperienceAnalysisResponse, status_code=status.HTTP_201_CREATED)
async def create_experience_study(
    db: DBSession,
    data: ExperienceStudyCreate,
    current_user: CurrentUser = Depends(require_permission("calculation", "create")),
):
    """Create and run an experience study."""
    analysis = ExperienceAnalysis(
        name=data.name,
        analysis_type=data.analysis_type,
        study_period_start=date.fromisoformat(data.study_period_start),
        study_period_end=date.fromisoformat(data.study_period_end),
        parameters=data.parameters,
        assumption_set_id=data.assumption_set_id,
        created_by_id=current_user.id,
    )
    db.add(analysis)
    await db.flush()

    # TODO: Run actual experience analysis
    # For now, set mock results
    analysis.total_actual = 150
    analysis.total_expected = 145
    analysis.ae_ratio = 150 / 145
    analysis.results = {
        "by_age_band": [],
        "by_gender": [],
        "by_duration": [],
    }

    await db.flush()
    await db.refresh(analysis)
    return analysis


@router.get("/{analysis_id}", response_model=ExperienceAnalysisResponse)
async def get_experience_analysis(
    db: DBSession,
    analysis_id: UUID,
    current_user: CurrentUser,
):
    """Get an experience analysis."""
    result = await db.execute(
        select(ExperienceAnalysis).where(ExperienceAnalysis.id == analysis_id)
    )
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    return analysis


@router.get("/{analysis_id}/recommendations")
async def get_experience_recommendations(
    db: DBSession,
    analysis_id: UUID,
    current_user: CurrentUser,
):
    """Get AI recommendations from experience analysis."""
    result = await db.execute(
        select(ExperienceAnalysis).where(ExperienceAnalysis.id == analysis_id)
    )
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")

    return {
        "analysis_id": str(analysis.id),
        "recommendations": analysis.ai_recommendations or [],
        "narrative": analysis.ai_narrative,
    }
