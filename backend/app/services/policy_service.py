"""Policy Service."""

import uuid
from datetime import date
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.policy import Policy
from app.repositories.policy_repository import PolicyRepository
from app.schemas.policy import PolicyCreate, PolicyUpdate
from app.services.audit_service import AuditService


class PolicyService:
    """Service for policy operations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = PolicyRepository(session)
        self.audit = AuditService(session)

    async def get(self, id: uuid.UUID) -> Policy | None:
        """Get policy by ID."""
        return await self.repository.get_with_relations(id)

    async def get_by_policy_number(self, policy_number: str) -> Policy | None:
        """Get policy by policy number."""
        return await self.repository.get_by_policy_number(policy_number)

    async def list(
        self,
        *,
        search: str | None = None,
        status: str | list[str] | None = None,
        product_type: str | None = None,
        product_code: str | None = None,
        policyholder_id: uuid.UUID | None = None,
        issue_date_from: date | None = None,
        issue_date_to: date | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Policy], int]:
        """List policies with filters."""
        skip = (page - 1) * page_size
        return await self.repository.search(
            search=search,
            status=status,
            product_type=product_type,
            product_code=product_code,
            policyholder_id=policyholder_id,
            issue_date_from=issue_date_from,
            issue_date_to=issue_date_to,
            skip=skip,
            limit=page_size,
        )

    async def create(
        self,
        data: PolicyCreate,
        created_by: uuid.UUID,
    ) -> Policy:
        """Create new policy."""
        policy_data = data.model_dump()
        policy_data["created_by_id"] = created_by

        policy = await self.repository.create(policy_data)

        await self.audit.log(
            user_id=created_by,
            action="create",
            resource_type="policy",
            resource_id=policy.id,
            new_values=policy_data,
        )

        return policy

    async def update(
        self,
        id: uuid.UUID,
        data: PolicyUpdate,
        updated_by: uuid.UUID,
    ) -> Policy | None:
        """Update policy."""
        existing = await self.repository.get(id)
        if not existing:
            return None

        old_values = {
            k: getattr(existing, k)
            for k in data.model_dump(exclude_unset=True).keys()
        }

        update_data = data.model_dump(exclude_unset=True)
        policy = await self.repository.update(id, update_data)

        await self.audit.log(
            user_id=updated_by,
            action="update",
            resource_type="policy",
            resource_id=id,
            old_values=old_values,
            new_values=update_data,
        )

        return policy

    async def delete(self, id: uuid.UUID, deleted_by: uuid.UUID) -> bool:
        """Soft delete policy."""
        result = await self.repository.delete(id, soft=True)

        if result:
            await self.audit.log(
                user_id=deleted_by,
                action="delete",
                resource_type="policy",
                resource_id=id,
            )

        return result

    async def get_stats(self) -> dict[str, Any]:
        """Get policy statistics."""
        return await self.repository.get_stats()

    async def get_for_calculation(
        self,
        policy_filter: dict[str, Any] | None = None,
    ) -> list[Policy]:
        """Get policies for calculation."""
        return await self.repository.get_for_calculation(policy_filter)
