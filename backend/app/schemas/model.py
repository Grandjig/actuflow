"""
Model Definition Schemas
========================

Schemas for actuarial model definitions.
"""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ModelDefinitionBase(BaseModel):
    """Base model definition fields."""
    
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    model_type: str = Field(
        pattern="^(reserving|pricing|cashflow|valuation|experience)$"
    )
    line_of_business: str = Field(max_length=100)
    regulatory_standard: Optional[str] = Field(
        default=None,
        pattern="^(IFRS17|SolvencyII|USGAAP|LDTI)$"
    )
    version: str = Field(default="1.0.0", max_length=50)


class ModelDefinitionCreate(ModelDefinitionBase):
    """Schema for creating a model definition."""
    
    configuration: dict[str, Any] = Field(
        description="Calculation graph configuration"
    )
    required_assumptions: Optional[list[str]] = None
    default_parameters: Optional[dict[str, Any]] = None
    parent_id: Optional[UUID] = Field(
        default=None,
        description="Parent model ID if cloning"
    )


class ModelDefinitionUpdate(BaseModel):
    """Schema for updating a model definition."""
    
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    version: Optional[str] = Field(default=None, max_length=50)
    status: Optional[str] = Field(
        default=None,
        pattern="^(draft|active|archived)$"
    )
    configuration: Optional[dict[str, Any]] = None
    required_assumptions: Optional[list[str]] = None
    default_parameters: Optional[dict[str, Any]] = None


class ModelDefinitionResponse(ModelDefinitionBase):
    """Schema for model definition response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    status: str
    configuration: dict[str, Any]
    required_assumptions: Optional[list[str]] = None
    default_parameters: Optional[dict[str, Any]] = None
    is_template: bool
    parent_id: Optional[UUID] = None
    
    created_at: datetime
    updated_at: datetime
    created_by_id: Optional[UUID] = None
    
    # Computed
    is_usable: Optional[bool] = None
    runs_count: int = 0


class ModelDefinitionListItem(BaseModel):
    """Simplified model definition for list views."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    model_type: str
    line_of_business: str
    regulatory_standard: Optional[str] = None
    version: str
    status: str
    is_template: bool
    runs_count: int = 0


class ModelValidationRequest(BaseModel):
    """Request to validate model configuration."""
    
    configuration: dict[str, Any]


class ModelValidationResponse(BaseModel):
    """Model validation result."""
    
    valid: bool
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    node_count: int = 0
    output_fields: list[str] = []
