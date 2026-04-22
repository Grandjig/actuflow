"""AI Query Log Model."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class AIQueryLog(BaseModel):
    """Log of AI natural language queries."""
    
    __tablename__ = "ai_query_logs"
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    
    query_text: Mapped[str] = mapped_column(Text, nullable=False)
    
    interpreted_intent: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    executed_action: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    
    was_successful: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    was_helpful: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    feedback_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    response_time_ms: Mapped[int | None] = mapped_column(nullable=True)
    
    def __repr__(self) -> str:
        return f"<AIQueryLog({self.query_text[:50]}...)>"
