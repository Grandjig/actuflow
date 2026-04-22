"""
AI Query Log Model
==================

Log of AI queries for training and improvement.
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class AIQueryLog(Base):
    """AI query log model."""

    __tablename__ = "ai_query_logs"

    # Query
    query_text: Mapped[str] = mapped_column(Text, nullable=False)
    query_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="natural_language/narrative_generation/column_mapping/anomaly_detection",
    )

    # Response
    response: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    tokens_used: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    response_time_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Context
    context: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # User feedback
    was_helpful: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    feedback_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # User
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    # Relationships
    user: Mapped[Optional["User"]] = relationship("User")

    def __repr__(self) -> str:
        return f"<AIQueryLog(id={self.id}, type={self.query_type})>"
