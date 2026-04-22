"""
Search Schemas
==============

Schemas for search functionality.
"""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """Global search request."""
    
    query: str = Field(min_length=1, max_length=500)
    resource_types: Optional[list[str]] = Field(
        default=None,
        description="Limit search to specific resource types"
    )
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class SearchResultItem(BaseModel):
    """Individual search result."""
    
    resource_type: str
    resource_id: UUID
    title: str
    subtitle: Optional[str] = None
    snippet: Optional[str] = None
    score: float
    url: str
    metadata: Optional[dict[str, Any]] = None
    highlights: list[str] = []


class SearchResponse(BaseModel):
    """Search response."""
    
    query: str
    results: list[SearchResultItem]
    total: int
    took_ms: int
    
    facets: Optional[dict[str, list[dict[str, Any]]]] = Field(
        default=None,
        description="Faceted counts by resource type"
    )


class SearchSuggestion(BaseModel):
    """Search autocomplete suggestion."""
    
    text: str
    type: str = Field(description="suggestion type: query/resource/recent")
    resource_type: Optional[str] = None
    resource_id: Optional[UUID] = None
