"""
Dashboard API Routes
====================

CRUD for dashboard configurations and widget data.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import CurrentUser, DBSession, require_permission
from app.schemas.common import PaginatedResponse, SuccessMessage
from app.schemas.dashboard import (
    DashboardConfigCreate,
    DashboardConfigListItem,
    DashboardConfigResponse,
    DashboardConfigUpdate,
    WidgetDataRequest,
    WidgetDataResponse,
)

router = APIRouter()


@router.get("", response_model=list[DashboardConfigListItem])
async def list_dashboards(
    db: DBSession,
    user: CurrentUser,
    include_shared: bool = Query(default=True),
):
    """
    List user's dashboards (and optionally shared ones).
    """
    from app.services.dashboard_service import DashboardService
    
    service = DashboardService(db)
    
    dashboards = await service.list_dashboards(
        user_id=user.id,
        include_shared=include_shared,
    )
    
    return dashboards


@router.get("/default", response_model=DashboardConfigResponse)
async def get_default_dashboard(
    db: DBSession,
    user: CurrentUser,
):
    """
    Get user's default dashboard.
    """
    from app.services.dashboard_service import DashboardService
    
    service = DashboardService(db)
    dashboard = await service.get_default(user.id)
    
    if not dashboard:
        # Return system default
        dashboard = await service.get_system_default()
    
    return dashboard


@router.get("/{dashboard_id}", response_model=DashboardConfigResponse)
async def get_dashboard(
    dashboard_id: UUID,
    db: DBSession,
    user: CurrentUser,
):
    """
    Get a dashboard by ID.
    """
    from app.services.dashboard_service import DashboardService
    
    service = DashboardService(db)
    dashboard = await service.get_dashboard(dashboard_id)
    
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found",
        )
    
    # Check access
    if dashboard.owner_id != user.id and not dashboard.is_shared:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    
    return dashboard


@router.post("", response_model=DashboardConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_dashboard(
    data: DashboardConfigCreate,
    db: DBSession,
    user: CurrentUser,
):
    """
    Create a new dashboard.
    """
    from app.services.dashboard_service import DashboardService
    
    service = DashboardService(db)
    dashboard = await service.create_dashboard(data, owner=user)
    
    return dashboard


@router.put("/{dashboard_id}", response_model=DashboardConfigResponse)
async def update_dashboard(
    dashboard_id: UUID,
    data: DashboardConfigUpdate,
    db: DBSession,
    user: CurrentUser,
):
    """
    Update a dashboard.
    """
    from app.services.dashboard_service import DashboardService
    
    service = DashboardService(db)
    
    dashboard = await service.get_dashboard(dashboard_id)
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found",
        )
    
    if dashboard.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only update your own dashboards",
        )
    
    updated = await service.update_dashboard(dashboard, data)
    
    return updated


@router.delete("/{dashboard_id}", response_model=SuccessMessage)
async def delete_dashboard(
    dashboard_id: UUID,
    db: DBSession,
    user: CurrentUser,
):
    """
    Delete a dashboard.
    """
    from app.services.dashboard_service import DashboardService
    
    service = DashboardService(db)
    
    dashboard = await service.get_dashboard(dashboard_id)
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found",
        )
    
    if dashboard.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only delete your own dashboards",
        )
    
    await service.delete_dashboard(dashboard)
    
    return SuccessMessage(message="Dashboard deleted")


@router.post("/{dashboard_id}/share", response_model=SuccessMessage)
async def share_dashboard(
    dashboard_id: UUID,
    db: DBSession,
    user: CurrentUser,
):
    """
    Share a dashboard with others.
    """
    from app.services.dashboard_service import DashboardService
    
    service = DashboardService(db)
    
    dashboard = await service.get_dashboard(dashboard_id)
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found",
        )
    
    if dashboard.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only share your own dashboards",
        )
    
    await service.share_dashboard(dashboard)
    
    return SuccessMessage(message="Dashboard shared")


@router.post("/widgets/data", response_model=WidgetDataResponse)
async def get_widget_data(
    request: WidgetDataRequest,
    db: DBSession,
    user: CurrentUser,
):
    """
    Fetch data for a dashboard widget.
    """
    from app.services.dashboard_service import DashboardService
    
    service = DashboardService(db)
    
    data = await service.get_widget_data(
        widget_type=request.widget_type,
        config=request.config,
        filters=request.filters,
        date_range=request.date_range,
        user=user,
    )
    
    return data
