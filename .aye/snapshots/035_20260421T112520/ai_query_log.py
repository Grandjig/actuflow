"""AI Query Log Model."""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.models.base import Base


class AIQueryLog(Base):
    """Logs natural language queries for learning and auditing."""

    __tablename__ = "ai_query_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    query_text = Column(Text, nullable=False)
    interpreted_intent = Column(JSONB)
    executed_action = Column(JSONB)
    was_helpful = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="ai_queries")
