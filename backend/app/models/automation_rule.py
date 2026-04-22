"""Automation Rule Model."""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.models.base import Base


class AutomationRule(Base):
    """Trigger-based automation rules."""

    __tablename__ = "automation_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    trigger_type = Column(String(100), nullable=False)
    trigger_config = Column(JSONB, default=dict)
    
    action_type = Column(String(100), nullable=False)
    action_config = Column(JSONB, default=dict)
    
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by = relationship("User")
