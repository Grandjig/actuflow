"""
Claim Schemas
=============

Schemas for claims management endpoints.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ClaimBase(BaseModel):
    """Base claim fields."""
    
    policy_id: UUID
    claim_type: str = Field(max_length=100)
    claim_date: date
    incident_date: Optional[date] = None
    
    claim_amount: Decimal = Field(ge=0, decimal_places=2)
    currency: str = Field(default="USD", max_length=3)
    
    description: Optional[str] = None


class ClaimCreate(ClaimBase):
    """Schema for creating a claim."""
    
    claim_number: Optional[str] = Field(default=None, max_length=50)
    coverage_id: Optional[UUID] = None
    notification_date: Optional[date] = None
    claim_data: Optional[dict[str, Any]] = None


class ClaimUpdate(BaseModel):
    """Schema for updating a claim."""
    
    claim_type: Optional[str] = Field(default=None, max_length=100)
    incident_date: Optional[date] = None
    claim_amount: Optional[Decimal] = Field(default=None, ge=0)
    
    assessed_amount: Optional[Decimal] = Field(default=None, ge=0)
    adjuster_id: Optional[UUID] = None
    adjuster_notes: Optional[str] = None
    
    description: Optional[str] = None
    claim_data: Optional[dict[str, Any]] = None


class ClaimStatusUpdate(BaseModel):
    """Schema for updating claim status."""
    
    status: str = Field(pattern="^(open|under_review|approved|denied|paid|closed)$")
    settlement_amount: Optional[Decimal] = Field(default=None, ge=0)
    settlement_date: Optional[date] = None
    payment_date: Optional[date] = None
    denial_reason: Optional[str] = None
    denial_code: Optional[str] = Field(default=None, max_length=50)
    notes: Optional[str] = None


class ClaimResponse(ClaimBase):
    """Schema for claim response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    claim_number: str
    coverage_id: Optional[UUID] = None
    status: str
    
    notification_date: Optional[date] = None
    assessed_amount: Optional[Decimal] = None
    settlement_amount: Optional[Decimal] = None
    settlement_date: Optional[date] = None
    payment_date: Optional[date] = None
    
    adjuster_id: Optional[UUID] = None
    adjuster_notes: Optional[str] = None
    
    denial_reason: Optional[str] = None
    denial_code: Optional[str] = None
    
    anomaly_score: Optional[float] = None
    anomaly_reasons: Optional[list[str]] = None
    
    claim_data: Optional[dict[str, Any]] = None
    
    created_at: datetime
    updated_at: datetime
    
    # Computed
    is_suspicious: Optional[bool] = None
    days_to_settle: Optional[int] = None


class ClaimListItem(BaseModel):
    """Simplified claim for list views."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    claim_number: str
    policy_number: Optional[str] = None
    claim_type: str
    claim_date: date
    claim_amount: Decimal
    status: str
    anomaly_score: Optional[float] = None


class ClaimFilter(BaseModel):
    """Filter parameters for claim list."""
    
    claim_number: Optional[str] = None
    policy_id: Optional[UUID] = None
    policy_number: Optional[str] = None
    claim_type: Optional[str] = None
    status: Optional[str] = None
    status_in: Optional[list[str]] = None
    
    claim_date_from: Optional[date] = None
    claim_date_to: Optional[date] = None
    
    amount_min: Optional[Decimal] = None
    amount_max: Optional[Decimal] = None
    
    adjuster_id: Optional[UUID] = None
    
    # AI filters
    anomaly_flagged: Optional[bool] = Field(
        default=None,
        description="Filter for AI-flagged suspicious claims"
    )
    anomaly_score_min: Optional[float] = Field(default=None, ge=0, le=1)
    
    search: Optional[str] = None


class ClaimSummaryStats(BaseModel):
    """Summary statistics for claims."""
    
    total_count: int
    open_count: int
    paid_count: int
    denied_count: int
    total_claimed: Decimal
    total_paid: Decimal
    average_settlement_days: Optional[float] = None
    by_status: dict[str, int]
    by_type: dict[str, int]
    flagged_count: int = Field(description="AI-flagged suspicious claims")


class ClaimAnomalyAlert(BaseModel):
    """AI anomaly alert for a claim."""
    
    claim_id: UUID
    claim_number: str
    anomaly_score: float
    reasons: list[str]
    detected_at: datetime
    reviewed: bool = False
    reviewed_by: Optional[UUID] = None
    review_notes: Optional[str] = None
