"""Claim Schemas."""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class ClaimCreate(BaseModel):
    """Schema for creating a claim."""
    policy_id: UUID
    claim_type: str
    claim_date: date
    incident_date: Optional[date] = None
    notification_date: Optional[date] = None
    claimed_amount: Decimal = Field(..., ge=0)
    adjuster_notes: Optional[str] = None


class ClaimUpdate(BaseModel):
    """Schema for updating a claim."""
    status: Optional[str] = None
    settlement_date: Optional[date] = None
    settlement_amount: Optional[Decimal] = None
    adjuster_id: Optional[UUID] = None
    adjuster_notes: Optional[str] = None
    denial_reason: Optional[str] = None


class ClaimResponse(BaseModel):
    """Schema for claim response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    claim_number: str
    policy_id: UUID
    claim_type: str
    claim_date: date
    incident_date: Optional[date] = None
    notification_date: Optional[date] = None
    claimed_amount: Decimal
    status: str
    settlement_date: Optional[date] = None
    settlement_amount: Optional[Decimal] = None
    adjuster_id: Optional[UUID] = None
    adjuster_notes: Optional[str] = None
    denial_reason: Optional[str] = None
    anomaly_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime


class ClaimListResponse(BaseModel):
    """Paginated claim list response."""
    items: list[ClaimResponse]
    total: int
    page: int
    page_size: int
    pages: int


class ClaimStats(BaseModel):
    """Claim statistics."""
    total_claims: int
    open_claims: int
    total_claimed: float
    total_settled: float
    by_status: dict[str, int]
    by_type: dict[str, int]
