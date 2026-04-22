"""
Dashboard Schemas
=================

Schemas for dashboard configuration.
"""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class WidgetConfig(BaseModel):
    """Individual dashboard widget configuration."""
    
    id: str = Field(description="Widget instance ID")
    widget_type: str = Field(
        description="Widget type: chart/table/metric/list/etc."
    )
    title: str = Field(max_length=100)
    
    # Grid position
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    width: int = Field(ge=1, le=12)
    height: int = Field(ge=1, le=12)
    
    # Widget-specific configuration
    config: dict[str, Any] = Field(
        description="Widget-specific configuration"
    )
    
    # Refresh settings
    refresh_interval_seconds: Optional[int] = Field(default=None, ge=30)


class DashboardConfigBase(BaseModel):
    """Base dashboard configuration fields."""
    
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None


class DashboardConfigCreate(DashboardConfigBase):
    """Schema for creating a dashboard."""
    
    layout: dict[str, Any] = Field(
        default_factory=dict,
        description="Grid layout configuration"
    )
    widgets: list[WidgetConfig] = Field(default_factory=list)
    theme: Optional[dict[str, Any]] = None
    is_shared: bool = False


class DashboardConfigUpdate(BaseModel):
    """Schema for updating a dashboard."""
    
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    layout: Optional[dict[str, Any]] = None
    widgets: Optional[list[WidgetConfig]] = None
    theme: Optional[dict[str, Any]] = None
    is_shared: Optional[bool] = None
    is_default: Optional[bool] = None


class DashboardConfigResponse(DashboardConfigBase):
    """Schema for dashboard configuration response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    owner_id: UUID
    is_shared: bool
    is_default: bool
    
    layout: dict[str, Any]
    widgets: list[WidgetConfig]
    theme: Optional[dict[str, Any]] = None
    
    created_at: datetime
    updated_at: datetime


class DashboardConfigListItem(BaseModel):
    """Simplified dashboard config for list views."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    description: Optional[str] = None
    owner_id: UUID
    owner_name: Optional[str] = None
    is_shared: bool
    is_default: bool
    widget_count: int = 0


class WidgetDataRequest(BaseModel):
    """Request to fetch widget data."""
    
    widget_type: str
    config: dict[str, Any]
    filters: Optional[dict[str, Any]] = None
    date_range: Optional[dict[str, str]] = None


class WidgetDataResponse(BaseModel):
    """Response with widget data."""
    
    widget_type: str
    data: Any
    metadata: Optional[dict[str, Any]] = None
    generated_at: datetime
    cache_ttl_seconds: int = 60
