"""
Common Schemas
==============

Shared schemas used across multiple endpoints.
"""

from datetime import date, datetime
from typing import Any, Generic, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

# Generic type for paginated responses
T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class PaginationParams(BaseModel):
    """Pagination query parameters."""
    
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=25, ge=1, le=1000, description="Items per page")
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        return self.page_size


class SortParams(BaseModel):
    """Sorting query parameters."""
    
    sort_by: Optional[str] = Field(default=None, description="Field to sort by")
    sort_order: str = Field(default="asc", pattern="^(asc|desc)$", description="Sort order")


class FilterParams(BaseModel):
    """Generic filter parameters."""
    
    filters: Optional[dict[str, Any]] = Field(default=None, description="Filter conditions")


class DateRange(BaseModel):
    """Date range filter."""
    
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class PaginatedResponse(BaseSchema, Generic[T]):
    """Paginated response wrapper."""
    
    items: list[T]
    total: int = Field(description="Total number of items")
    page: int = Field(description="Current page number")
    page_size: int = Field(description="Items per page")
    pages: int = Field(description="Total number of pages")
    
    @classmethod
    def create(
        cls,
        items: list[T],
        total: int,
        page: int,
        page_size: int,
    ) -> "PaginatedResponse[T]":
        pages = (total + page_size - 1) // page_size if page_size > 0 else 0
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=pages,
        )


class BulkActionRequest(BaseModel):
    """Request for bulk operations."""
    
    ids: list[UUID] = Field(min_length=1, max_length=1000, description="Resource IDs")


class BulkActionResponse(BaseModel):
    """Response for bulk operations."""
    
    success_count: int = Field(description="Number of successful operations")
    failure_count: int = Field(description="Number of failed operations")
    errors: Optional[list[dict[str, Any]]] = Field(default=None, description="Error details")


class ErrorResponse(BaseModel):
    """Standard error response."""
    
    error: dict[str, Any] = Field(description="Error details")


class SuccessMessage(BaseModel):
    """Simple success message response."""
    
    message: str = Field(description="Success message")
    data: Optional[dict[str, Any]] = Field(default=None, description="Additional data")


class FileUploadResponse(BaseModel):
    """Response for file upload operations."""
    
    file_id: UUID
    file_name: str
    file_size: int
    file_type: str
    upload_url: Optional[str] = None


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields."""
    
    created_at: datetime
    updated_at: datetime


class AuditMixin(BaseModel):
    """Mixin for audit fields."""
    
    created_by_id: Optional[UUID] = None
    updated_by_id: Optional[UUID] = None
