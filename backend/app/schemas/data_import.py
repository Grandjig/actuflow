"""
Data Import Schemas
===================

Schemas for data import operations.
"""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DataImportCreate(BaseModel):
    """Schema for initiating a data import."""
    
    import_type: str = Field(
        pattern="^(policy|policyholder|claim|assumption|coverage)$"
    )
    file_name: str = Field(max_length=255)
    import_options: Optional[dict[str, Any]] = Field(
        default=None,
        description="Options like on_duplicate, skip_errors, etc."
    )


class DataImportResponse(BaseModel):
    """Schema for data import response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    file_name: str
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    file_type: str
    import_type: str
    
    status: str
    total_rows: Optional[int] = None
    processed_rows: int
    success_rows: int
    error_rows: int
    
    column_mapping: Optional[dict[str, Any]] = None
    ai_suggested_mapping: Optional[dict[str, Any]] = None
    ai_data_issues: Optional[list[dict[str, Any]]] = None
    validation_errors: Optional[list[dict[str, Any]]] = None
    
    import_options: Optional[dict[str, Any]] = None
    
    uploaded_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    uploaded_by_id: Optional[UUID] = None
    error_message: Optional[str] = None


class DataImportListItem(BaseModel):
    """Simplified data import for list views."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    file_name: str
    import_type: str
    status: str
    total_rows: Optional[int] = None
    success_rows: int
    error_rows: int
    uploaded_at: datetime
    completed_at: Optional[datetime] = None


class DataImportProgress(BaseModel):
    """Real-time import progress."""
    
    import_id: UUID
    status: str
    total_rows: Optional[int] = None
    processed_rows: int
    success_rows: int
    error_rows: int
    current_step: str
    estimated_completion: Optional[datetime] = None


class ColumnMappingRequest(BaseModel):
    """Request to set column mapping."""
    
    mapping: dict[str, str] = Field(
        description="Source column -> target field mapping"
    )
    skip_columns: Optional[list[str]] = Field(
        default=None,
        description="Columns to skip during import"
    )


class ValidationResultResponse(BaseModel):
    """Validation result for import."""
    
    valid: bool
    total_rows: int
    valid_rows: int
    invalid_rows: int
    errors: list[dict[str, Any]] = Field(
        description="List of validation errors with row numbers"
    )
    warnings: list[dict[str, Any]] = []


# =============================================================================
# AI Suggestion Schemas
# =============================================================================

class AISuggestedMapping(BaseModel):
    """AI-suggested column mapping."""
    
    source_column: str
    target_field: str
    confidence: float = Field(ge=0, le=1)
    reason: str
    alternative_fields: Optional[list[str]] = None


class AIDataIssue(BaseModel):
    """AI-detected data issue."""
    
    column: str
    issue_type: str
    severity: str = Field(pattern="^(error|warning|info)$")
    count: int
    sample_rows: list[int]
    description: str
    suggestion: Optional[str] = None


class AISuggestionResponse(BaseModel):
    """Combined AI suggestions for import."""
    
    column_mappings: list[AISuggestedMapping]
    data_issues: list[AIDataIssue]
    overall_confidence: float = Field(ge=0, le=1)
    recommendations: list[str]
