"""Assumption Service.

Business logic for assumption sets and tables.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.assumption_set import AssumptionSet
from app.models.assumption_table import AssumptionTable
from app.repositories.assumption_repository import (
    AssumptionSetRepository,
    AssumptionTableRepository,
)
from app.schemas.assumption import (
    AssumptionSetCreate,
    AssumptionSetUpdate,
    AssumptionTableCreate,
)
from app.services.ai_service import AIService, AIServiceUnavailable
from app.config import settings


class AssumptionService:
    """Service for assumption operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.set_repo = AssumptionSetRepository(db)
        self.table_repo = AssumptionTableRepository(db)
    
    async def get_by_id(self, set_id: uuid.UUID) -> Optional[AssumptionSet]:
        """Get assumption set by ID."""
        return await self.set_repo.get_with_tables(set_id)
    
    async def list_sets(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        status: Optional[str] = None,
        line_of_business: Optional[str] = None,
    ) -> tuple[list[AssumptionSet], int]:
        """List assumption sets."""
        skip = (page - 1) * page_size
        return await self.set_repo.search(
            search=search,
            status=status,
            line_of_business=line_of_business,
            skip=skip,
            limit=page_size,
        )
    
    async def get_approved_sets(self) -> list[AssumptionSet]:
        """Get all approved assumption sets."""
        return await self.set_repo.get_approved()
    
    async def create_set(
        self,
        set_data: AssumptionSetCreate,
        created_by: uuid.UUID,
    ) -> AssumptionSet:
        """Create a new assumption set."""
        data = set_data.model_dump()
        data["created_by_id"] = created_by
        data["status"] = "draft"
        
        return await self.set_repo.create(data)
    
    async def update_set(
        self,
        set_id: uuid.UUID,
        set_data: AssumptionSetUpdate,
    ) -> Optional[AssumptionSet]:
        """Update an assumption set."""
        data = set_data.model_dump(exclude_unset=True)
        return await self.set_repo.update(set_id, data)
    
    async def soft_delete(self, set_id: uuid.UUID) -> bool:
        """Soft delete an assumption set."""
        return await self.set_repo.soft_delete(set_id)
    
    async def submit_for_approval(self, set_id: uuid.UUID) -> Optional[AssumptionSet]:
        """Submit assumption set for approval."""
        return await self.set_repo.update(set_id, {"status": "pending_approval"})
    
    async def approve(
        self,
        set_id: uuid.UUID,
        approved_by: uuid.UUID,
        notes: Optional[str] = None,
    ) -> Optional[AssumptionSet]:
        """Approve an assumption set."""
        return await self.set_repo.update(set_id, {
            "status": "approved",
            "approved_by_id": approved_by,
            "approval_date": datetime.utcnow(),
            "approval_notes": notes,
        })
    
    async def reject(
        self,
        set_id: uuid.UUID,
        reason: str,
    ) -> Optional[AssumptionSet]:
        """Reject an assumption set."""
        return await self.set_repo.update(set_id, {
            "status": "rejected",
            "rejection_reason": reason,
        })
    
    # Table operations
    async def get_tables(self, set_id: uuid.UUID) -> list[AssumptionTable]:
        """Get tables for an assumption set."""
        return await self.table_repo.get_for_set(set_id)
    
    async def create_table(
        self,
        set_id: uuid.UUID,
        table_data: AssumptionTableCreate,
    ) -> AssumptionTable:
        """Create a table in an assumption set."""
        data = table_data.model_dump()
        data["assumption_set_id"] = set_id
        return await self.table_repo.create(data)
    
    async def get_recommendations(self, set_id: uuid.UUID) -> list[dict]:
        """Get AI-generated experience recommendations."""
        if not settings.AI_ENABLED:
            return []
        
        try:
            ai_service = AIService()
            tables = await self.get_tables(set_id)
            
            return await ai_service.get_experience_recommendations(
                tables=[{"type": t.table_type, "data": t.data} for t in tables]
            )
        except AIServiceUnavailable:
            return []
