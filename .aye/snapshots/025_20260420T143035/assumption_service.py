"""Assumption Service."""

import uuid
from datetime import datetime
from typing import Any

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
    AssumptionTableUpdate,
)
from app.services.audit_service import AuditService


class AssumptionService:
    """Service for assumption operations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.set_repo = AssumptionSetRepository(session)
        self.table_repo = AssumptionTableRepository(session)
        self.audit = AuditService(session)

    # Assumption Sets

    async def get_set(self, id: uuid.UUID) -> AssumptionSet | None:
        """Get assumption set by ID."""
        return await self.set_repo.get_with_tables(id)

    async def list_sets(
        self,
        *,
        search: str | None = None,
        status: str | list[str] | None = None,
        line_of_business: str | None = None,
        page: int = 1,
        page_size: int = 20,
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
        data: AssumptionSetCreate,
        created_by: uuid.UUID,
    ) -> AssumptionSet:
        """Create new assumption set."""
        set_data = data.model_dump()
        set_data["created_by_id"] = created_by
        set_data["status"] = "draft"

        assumption_set = await self.set_repo.create(set_data)

        await self.audit.log(
            user_id=created_by,
            action="create",
            resource_type="assumption_set",
            resource_id=assumption_set.id,
            new_values=set_data,
        )

        return assumption_set

    async def update_set(
        self,
        id: uuid.UUID,
        data: AssumptionSetUpdate,
        updated_by: uuid.UUID,
    ) -> AssumptionSet | None:
        """Update assumption set."""
        existing = await self.set_repo.get(id)
        if not existing:
            return None

        # Can only update draft sets
        if existing.status != "draft":
            raise ValueError("Can only update draft assumption sets")

        update_data = data.model_dump(exclude_unset=True)
        assumption_set = await self.set_repo.update(id, update_data)

        await self.audit.log(
            user_id=updated_by,
            action="update",
            resource_type="assumption_set",
            resource_id=id,
            new_values=update_data,
        )

        return assumption_set

    async def delete_set(self, id: uuid.UUID, deleted_by: uuid.UUID) -> bool:
        """Delete assumption set."""
        existing = await self.set_repo.get(id)
        if not existing:
            return False

        if existing.status == "approved":
            raise ValueError("Cannot delete approved assumption sets")

        result = await self.set_repo.delete(id, soft=True)

        if result:
            await self.audit.log(
                user_id=deleted_by,
                action="delete",
                resource_type="assumption_set",
                resource_id=id,
            )

        return result

    async def submit_for_approval(
        self,
        id: uuid.UUID,
        submitted_by: uuid.UUID,
    ) -> AssumptionSet | None:
        """Submit assumption set for approval."""
        existing = await self.set_repo.get(id)
        if not existing:
            return None

        if existing.status != "draft":
            raise ValueError("Can only submit draft assumption sets")

        assumption_set = await self.set_repo.update(
            id, {"status": "pending_approval"}
        )

        await self.audit.log(
            user_id=submitted_by,
            action="submit_for_approval",
            resource_type="assumption_set",
            resource_id=id,
        )

        return assumption_set

    async def approve(
        self,
        id: uuid.UUID,
        approved_by: uuid.UUID,
        notes: str | None = None,
    ) -> AssumptionSet | None:
        """Approve assumption set."""
        existing = await self.set_repo.get(id)
        if not existing:
            return None

        if existing.status != "pending_approval":
            raise ValueError("Can only approve pending assumption sets")

        assumption_set = await self.set_repo.update(
            id,
            {
                "status": "approved",
                "approved_by_id": approved_by,
                "approval_date": datetime.utcnow(),
                "approval_notes": notes,
            },
        )

        await self.audit.log(
            user_id=approved_by,
            action="approve",
            resource_type="assumption_set",
            resource_id=id,
            new_values={"approval_notes": notes},
        )

        return assumption_set

    async def reject(
        self,
        id: uuid.UUID,
        rejected_by: uuid.UUID,
        reason: str,
    ) -> AssumptionSet | None:
        """Reject assumption set."""
        existing = await self.set_repo.get(id)
        if not existing:
            return None

        if existing.status != "pending_approval":
            raise ValueError("Can only reject pending assumption sets")

        assumption_set = await self.set_repo.update(
            id,
            {
                "status": "rejected",
                "rejection_reason": reason,
            },
        )

        await self.audit.log(
            user_id=rejected_by,
            action="reject",
            resource_type="assumption_set",
            resource_id=id,
            new_values={"rejection_reason": reason},
        )

        return assumption_set

    # Assumption Tables

    async def get_tables(self, set_id: uuid.UUID) -> list[AssumptionTable]:
        """Get all tables for an assumption set."""
        return await self.table_repo.get_by_set(set_id)

    async def get_table(self, id: uuid.UUID) -> AssumptionTable | None:
        """Get assumption table by ID."""
        return await self.table_repo.get(id)

    async def create_table(
        self,
        set_id: uuid.UUID,
        data: AssumptionTableCreate,
        created_by: uuid.UUID,
    ) -> AssumptionTable:
        """Create new assumption table."""
        # Verify set exists and is draft
        assumption_set = await self.set_repo.get(set_id)
        if not assumption_set:
            raise ValueError("Assumption set not found")
        if assumption_set.status != "draft":
            raise ValueError("Can only add tables to draft assumption sets")

        table_data = data.model_dump()
        table_data["assumption_set_id"] = set_id

        table = await self.table_repo.create(table_data)

        await self.audit.log(
            user_id=created_by,
            action="create",
            resource_type="assumption_table",
            resource_id=table.id,
            new_values={"assumption_set_id": str(set_id), **table_data},
        )

        return table

    async def update_table(
        self,
        id: uuid.UUID,
        data: AssumptionTableUpdate,
        updated_by: uuid.UUID,
    ) -> AssumptionTable | None:
        """Update assumption table."""
        existing = await self.table_repo.get(id)
        if not existing:
            return None

        # Verify set is draft
        assumption_set = await self.set_repo.get(existing.assumption_set_id)
        if assumption_set and assumption_set.status != "draft":
            raise ValueError("Can only update tables in draft assumption sets")

        update_data = data.model_dump(exclude_unset=True)
        table = await self.table_repo.update(id, update_data)

        await self.audit.log(
            user_id=updated_by,
            action="update",
            resource_type="assumption_table",
            resource_id=id,
            new_values=update_data,
        )

        return table

    async def delete_table(self, id: uuid.UUID, deleted_by: uuid.UUID) -> bool:
        """Delete assumption table."""
        existing = await self.table_repo.get(id)
        if not existing:
            return False

        # Verify set is draft
        assumption_set = await self.set_repo.get(existing.assumption_set_id)
        if assumption_set and assumption_set.status != "draft":
            raise ValueError("Can only delete tables from draft assumption sets")

        result = await self.table_repo.delete(id, soft=False)

        if result:
            await self.audit.log(
                user_id=deleted_by,
                action="delete",
                resource_type="assumption_table",
                resource_id=id,
            )

        return result
