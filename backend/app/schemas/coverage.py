"""
Coverage Schemas
================

Schemas for coverage/benefit management.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CoverageBase(BaseModel):
    """Base coverage fields."""
    
    coverage_code: str = Field(max_length=50)
    coverage_type: str = Field(max_length=100)
    coverage_name: str = Field(max_length=255)
    
    is_rider: bool = False
    
    start_date: date
    end_date: Optional[date] = None
    
    benefit_amount: Decimal = Field(ge=0, decimal_places=2)
    premium_amount: Decimal = Field(ge=0, decimal_places=2, default=0)
    
    waiting_period_days: Optional[int] = Field(default=None, ge=0)
    benefit_period_months: Optional[int] = Field(default=None, ge=0)


class CoverageCreate(CoverageBase):
    """Schema for creating a coverage."""
    
    policy_id: UUID
    status: str = Field(default="active")
    coverage_data: Optional[dict[str, Any]] = None


class CoverageUpdate(BaseModel):
    """Schema for updating a coverage."""
    
    coverage_name: Optional[str] = Field(default=None, max_length=255)
    status: Optional[str] = None
    end_date: Optional[date] = None
    benefit_amount: Optional[Decimal] = Field(default=None, ge=0)
    premium_amount: Optional[Decimal] = Field(default=None, ge=0)
    coverage_data: Optional[dict[str, Any]] = None


class CoverageResponse(CoverageBase):
    """Schema for coverage response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    policy_id: UUID
    status: str
    coverage_data: Optional[dict[str, Any]] = None
    
    created_at: datetime
    updated_at: datetime
    
    # Computed
    is_active: Optional[bool] = None
