"""
AI Query Log Model
==================

Logs of natural language queries for learning and auditing.
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class AIQueryLog(Base):
    """
    Log of natural language queries.
    
    Used for auditing, improving AI responses, and user query history.
    """
    
    __tablename__ = "ai_query_log"
    
    # User
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Query
    query_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    
    # AI interpretation
    interpreted_intent: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        doc="AI's understanding of user intent",
    )
    
    # What was executed
    executed_action: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        doc="search/filter/navigate/aggregate/etc.",
    )
    
    executed_params: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        doc="Parameters passed to the action",
    )
    
    # Result summary
    result_count: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    
    result_summary: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )
    
    # User feedback
    was_helpful: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
        doc="Did user mark result as helpful?",
    )
    
    feedback_text: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Performance
    latency_ms: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    
    # Error
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Timestamp
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )
    
    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id],
    )
    
    def __repr__(self) -> str:
        return f"<AIQueryLog(id={self.id}, query={self.query_text[:50]}...)>"
