"""
Report Schemas
==============

Schemas for report templates and generation.
"""

from datetime import date, datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# =============================================================================
# Report Template Schemas
# =============================================================================

class ReportTemplateBase(BaseModel):
    """Base report template fields."""
    
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    report_type: str = Field(pattern="^(regulatory|internal|adhoc)$")
    regulatory_standard: Optional[str] = Field(
        default=None,
        pattern="^(IFRS17|SolvencyII|USGAAP|LDTI)$"
    )
    output_format: str = Field(default="PDF", pattern="^(PDF|Excel|CSV)$")


class ReportTemplateCreate(ReportTemplateBase):
    """Schema for creating a report template."""
    
    template_config: dict[str, Any] = Field(
        description="Report structure configuration"
    )
    include_ai_narrative: bool = False
    ai_narrative_config: Optional[dict[str, Any]] = None


class ReportTemplateUpdate(BaseModel):
    """Schema for updating a report template."""
    
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    template_config: Optional[dict[str, Any]] = None
    output_format: Optional[str] = Field(
        default=None,
        pattern="^(PDF|Excel|CSV)$"
    )
    include_ai_narrative: Optional[bool] = None
    ai_narrative_config: Optional[dict[str, Any]] = None


class ReportTemplateResponse(ReportTemplateBase):
    """Schema for report template response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    template_config: dict[str, Any]
    include_ai_narrative: bool
    ai_narrative_config: Optional[dict[str, Any]] = None
    is_system_template: bool
    
    created_at: datetime
    updated_at: datetime
    created_by_id: Optional[UUID] = None


class ReportTemplateListItem(BaseModel):
    """Simplified report template for list views."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    report_type: str
    regulatory_standard: Optional[str] = None
    output_format: str
    is_system_template: bool


# =============================================================================
# Generated Report Schemas
# =============================================================================

class GenerateReportRequest(BaseModel):
    """Request to generate a report."""
    
    report_template_id: UUID
    name: Optional[str] = Field(default=None, max_length=255)
    reporting_period_start: Optional[date] = None
    reporting_period_end: Optional[date] = None
    parameters: Optional[dict[str, Any]] = None
    output_format: Optional[str] = Field(
        default=None,
        pattern="^(PDF|Excel|CSV)$"
    )


class GeneratedReportResponse(BaseModel):
    """Schema for generated report response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    report_template_id: Optional[UUID] = None
    name: str
    
    reporting_period_start: Optional[date] = None
    reporting_period_end: Optional[date] = None
    
    status: str
    generated_by_id: Optional[UUID] = None
    generated_at: Optional[datetime] = None
    
    file_path: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    output_format: str
    
    parameters: Optional[dict[str, Any]] = None
    ai_summary: Optional[str] = None
    error_message: Optional[str] = None
    
    created_at: datetime


class GeneratedReportListItem(BaseModel):
    """Simplified generated report for list views."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    template_name: Optional[str] = None
    status: str
    output_format: str
    generated_at: Optional[datetime] = None
    file_size: Optional[int] = None


class ReportScheduleCreate(BaseModel):
    """Schema for scheduling report generation."""
    
    report_template_id: UUID
    name: str = Field(max_length=255)
    cron_expression: str = Field(max_length=100)
    parameters: Optional[dict[str, Any]] = None
    email_recipients: Optional[list[str]] = None
    is_active: bool = True
