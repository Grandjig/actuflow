"""Audit Service."""

import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog


class AuditService:
    """Service for audit logging."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def log(
        self,
        *,
        user_id: uuid.UUID | None,
        action: str,
        resource_type: str,
        resource_id: uuid.UUID | None = None,
        old_values: dict[str, Any] | None = None,
        new_values: dict[str, Any] | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        request_id: uuid.UUID | None = None,
    ) -> AuditLog:
        """Create audit log entry."""
        # Serialize UUIDs in values
        if old_values:
            old_values = self._serialize_values(old_values)
        if new_values:
            new_values = self._serialize_values(new_values)

        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
        )

        self.session.add(audit_log)
        await self.session.flush()

        return audit_log

    def _serialize_values(self, values: dict[str, Any]) -> dict[str, Any]:
        """Serialize values for JSON storage."""
        result = {}
        for key, value in values.items():
            if isinstance(value, uuid.UUID):
                result[key] = str(value)
            elif hasattr(value, "isoformat"):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result
