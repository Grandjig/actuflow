"""AI Query Log Model."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class AIQueryLog(Base):
    """Log of AI natural language queries."""

    __tablename__ = "ai_query_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    query_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    
    interpreted_intent: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )
    
    executed_action: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    
    result_summary: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )
    
    was_helpful: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
    )
    
    feedback_text: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="ai_queries",
        foreign_keys=[user_id],
    )

    def __repr__(self) -> str:
        return f"<AIQueryLog(id={self.id}, user_id={self.user_id})>"
