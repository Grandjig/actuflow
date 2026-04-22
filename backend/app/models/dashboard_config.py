"""
Dashboard Config Model
======================

User dashboard configurations.
"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class DashboardConfig(Base, TimestampMixin):
    """Dashboard configuration model."""

    __tablename__ = "dashboard_configs"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    layout: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        doc="Grid layout configuration",
    )

    widgets: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
        doc="List of widget configurations",
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        doc="System dashboards cannot be deleted",
    )

    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    created_by: Mapped[Optional["User"]] = relationship("User")

    def __repr__(self) -> str:
        return f"<DashboardConfig(id={self.id}, name={self.name})>"
