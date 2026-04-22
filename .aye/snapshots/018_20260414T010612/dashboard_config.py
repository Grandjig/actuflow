"""
Dashboard Config Model
======================

User-created dashboard configurations.
"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.user import User


class DashboardConfig(Base, TimestampMixin, SoftDeleteMixin):
    """
    Custom dashboard configuration.
    
    Users can create and share custom dashboards.
    """
    
    __tablename__ = "dashboard_config"
    
    # Owner
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Dashboard info
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Sharing
    is_shared: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    
    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        doc="Is this the user's default dashboard?",
    )
    
    # Layout configuration
    layout: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        doc="Grid layout configuration",
    )
    
    # Widgets
    widgets: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
        doc="List of widget configurations",
    )
    
    # Theme/styling
    theme: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )
    
    # Relationships
    owner: Mapped["User"] = relationship(
        "User",
        foreign_keys=[owner_id],
    )
    
    def __repr__(self) -> str:
        return f"<DashboardConfig(id={self.id}, name={self.name})>"
