"""
Claim Schemas
=============

Pydantic schemas for claim-related operations.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class ClaimBase(BaseModel):
    """Base claim schema."""
    claim_type: str
    claim_date: date
    claimed_amount: Decimal = Field(..., gt=0)
    incident_date: Optional[date] = None
    notification_date: Optional[date] = None


class ClaimCreate(ClaimBase):
    """Schema for creating a claim."""
    policy_id: UUID
    claim_number: Optional[str] = None  # Auto-generated if not provided
    external_id: Optional[str] = None
    adjuster_notes: Optional[str] = None
    claim_data: Optional[dict[str, Any]] = None


class ClaimUpdate(BaseModel):
    """Schema for updating a claim."""
    status: Optional[str] = None
    settlement_date: Optional[date] = None
    settlement_amount: Optional[Decimal] = None
    adjuster_id: Optional[UUID] = None
    adjuster_notes: Optional[str] = None
    denial_reason: Optional[str] = None
    claim_data: Optional[dict[str, Any]] = None


class ClaimResponse(ClaimBase):
    """Schema for claim response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    claim_number: str
    policy_id: UUID
    external_id: Optional[str] = None
    status: str
    settlement_date: Optional[date] = None
    settlement_amount: Optional[Decimal] = None
    adjuster_id: Optional[UUID] = None
    adjuster_notes: Optional[str] = None
    denial_reason: Optional[str] = None
    anomaly_score: Optional[float] = None
    anomaly_reasons: Optional[list] = None
    created_at: datetime
    updated_at: datetime


class ClaimListItem(BaseModel):
    """Schema for claim list item."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    claim_number: str
    policy_id: UUID
    policy_number: Optional[str] = None
    claim_type: str
    claim_date: date
    claimed_amount: Decimal
    status: str
    anomaly_score: Optional[float] = None


class ClaimFilter(BaseModel):
    """Schema for claim filtering."""
    policy_id: Optional[UUID] = None
    status: Optional[str] = None
    claim_type: Optional[str] = None
    claim_date_from: Optional[date] = None
    claim_date_to: Optional[date] = None
    anomaly_only: bool = False
    search: Optional[str] = None


class ClaimStats(BaseModel):
    """Claim statistics."""
    total_claims: int
    open_claims: int
    total_claimed: Decimal
    total_settled: Decimal
    by_status: dict[str, int]
    by_type: dict[str, int]
