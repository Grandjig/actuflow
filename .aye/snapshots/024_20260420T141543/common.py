"""
Common Schemas
==============

Shared Pydantic schemas used across the application.
"""

from datetime import datetime
from typing import Any, Generic, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# Generic type for paginated responses
T = TypeVar("T")


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=25, ge=1, le=1000)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper."""
    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int

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


class SuccessResponse(BaseModel):
    """Generic success response."""
    success: bool = True
    message: str = "Operation completed successfully"


class ErrorResponse(BaseModel):
    """Error response."""
    detail: str
    code: Optional[str] = None
    field: Optional[str] = None


class BulkActionRequest(BaseModel):
    """Bulk action request."""
    ids: list[UUID]
    action: str
    params: Optional[dict[str, Any]] = None


class BulkActionResponse(BaseModel):
    """Bulk action response."""
    success_count: int
    failure_count: int
    errors: list[dict[str, Any]] = []


class DateRangeFilter(BaseModel):
    """Date range filter."""
    start: Optional[datetime] = None
    end: Optional[datetime] = None


class SortParams(BaseModel):
    """Sort parameters."""
    sort_by: str = "created_at"
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields."""
    created_at: datetime
    updated_at: datetime


class IDMixin(BaseModel):
    """Mixin for ID field."""
    id: UUID
