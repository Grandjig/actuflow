"""
Dashboards API Routes
=====================

Dashboard configuration management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from uuid import UUID
from typing import Optional
from pydantic import BaseModel

from app.dependencies import DBSession, CurrentUser, require_permission
from app.models.dashboard_config import DashboardConfig
from app.schemas.common import SuccessResponse

router = APIRouter()


class DashboardConfigResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    layout: dict
    widgets: list[dict]
    is_default: bool
    is_system: bool
    created_by_id: Optional[UUID]

    class Config:
        from_attributes = True


class DashboardConfigCreate(BaseModel):
    name: str
    description: Optional[str] = None
    layout: dict = {}
    widgets: list[dict] = []


@router.get("", response_model=list[DashboardConfigResponse])
async def list_dashboards(
    db: DBSession,
    current_user: CurrentUser,
):
    """List available dashboards."""
    result = await db.execute(
        select(DashboardConfig)
        .where(
            (DashboardConfig.is_system == True) |
            (DashboardConfig.created_by_id == current_user.id)
        )
        .order_by(DashboardConfig.name)
    )
    return result.scalars().all()


@router.get("/{dashboard_id}", response_model=DashboardConfigResponse)
async def get_dashboard(
    db: DBSession,
    dashboard_id: UUID,
    current_user: CurrentUser,
):
    """Get a dashboard configuration."""
    result = await db.execute(
        select(DashboardConfig).where(DashboardConfig.id == dashboard_id)
    )
    dashboard = result.scalar_one_or_none()
    if not dashboard:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dashboard not found")
    return dashboard


@router.post("", response_model=DashboardConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_dashboard(
    db: DBSession,
    data: DashboardConfigCreate,
    current_user: CurrentUser = Depends(require_permission("dashboard", "create")),
):
    """Create a custom dashboard."""
    dashboard = DashboardConfig(
        **data.model_dump(),
        is_default=False,
        is_system=False,
        created_by_id=current_user.id,
    )
    db.add(dashboard)
    await db.flush()
    await db.refresh(dashboard)
    return dashboard


@router.put("/{dashboard_id}", response_model=DashboardConfigResponse)
async def update_dashboard(
    db: DBSession,
    dashboard_id: UUID,
    data: DashboardConfigCreate,
    current_user: CurrentUser,
):
    """Update a dashboard configuration."""
    result = await db.execute(
        select(DashboardConfig).where(DashboardConfig.id == dashboard_id)
    )
    dashboard = result.scalar_one_or_none()
    if not dashboard:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dashboard not found")
    
    if dashboard.is_system and not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot modify system dashboards")

    for field, value in data.model_dump().items():
        setattr(dashboard, field, value)

    await db.flush()
    await db.refresh(dashboard)
    return dashboard
