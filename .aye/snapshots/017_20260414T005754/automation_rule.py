"""Automation Rule Model."""

import uuid
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.user import User


class TriggerType(str, Enum):
    """Automation trigger types."""
    POLICY_STATUS_CHANGE = "policy_status_change"
    CALCULATION_COMPLETE = "calculation_complete"
    THRESHOLD_BREACH = "threshold_breach"
    TIME_BASED = "time_based"
    CLAIM_STATUS_CHANGE = "claim_status_change"
    ASSUMPTION_APPROVED = "assumption_approved"
    IMPORT_COMPLETE = "import_complete"


class ActionType(str, Enum):
    """Automation action types."""
    SEND_NOTIFICATION = "send_notification"
    CREATE_TASK = "create_task"
    RUN_CALCULATION = "run_calculation"
    CALL_WEBHOOK = "call_webhook"
    SEND_EMAIL = "send_email"
    UPDATE_STATUS = "update_status"


class AutomationRule(BaseModel, SoftDeleteMixin):
    """Trigger-based automation rule."""
    
    __tablename__ = "automation_rules"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    trigger_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    trigger_config: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    
    action_type: Mapped[str] = mapped_column(String(50), nullable=False)
    action_config: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    execution_count: Mapped[int] = mapped_column(default=0, nullable=False)
    last_executed_at: Mapped[str | None] = mapped_column(nullable=True)
    
    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    
    def __repr__(self) -> str:
        return f"<AutomationRule({self.name}, {self.trigger_type} -> {self.action_type})>"
