"""
Automation Rule Model
=====================

Trigger-based automation rules.
"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.user import User


class AutomationRule(Base, TimestampMixin, SoftDeleteMixin):
    """Automation rule model."""

    __tablename__ = "automation_rules"

    # Rule info
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Trigger
    trigger_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="policy_status_change/calculation_complete/threshold_breach/claim_filed/etc.",
    )

    trigger_config: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        doc="Conditions that must be met for trigger to fire",
    )

    # Action
    action_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        doc="send_notification/create_task/run_calculation/call_webhook/send_email",
    )

    action_config: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        doc="Configuration for the action to perform",
    )

    # Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
    )

    # Statistics
    times_triggered: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )

    # Creator
    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    created_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[created_by_id],
    )

    def __repr__(self) -> str:
        return f"<AutomationRule(id={self.id}, name={self.name}, trigger={self.trigger_type})>"
