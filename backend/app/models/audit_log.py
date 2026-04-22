"""Audit Log Model."""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.models.base import Base


class AuditLog(Base):
    """Immutable audit trail for all changes."""

    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Who performed the action
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user_email = Column(String(255))  # Denormalized for historical record
    
    # What action was performed
    action = Column(String(50), nullable=False, index=True)  # create, update, delete, approve, etc.
    
    # What resource was affected
    resource_type = Column(String(100), nullable=False, index=True)
    resource_id = Column(UUID(as_uuid=True), index=True)
    resource_name = Column(String(255))  # Denormalized for readability
    
    # Change details
    old_values = Column(JSONB)  # Previous state
    new_values = Column(JSONB)  # New state
    
    # Additional context - RENAMED from 'metadata' to avoid SQLAlchemy conflict
    extra_data = Column(JSONB)  # Any additional context
    description = Column(Text)  # Human-readable description
    
    # Request info
    ip_address = Column(String(45))
    user_agent = Column(Text)
    request_id = Column(UUID(as_uuid=True))  # For correlating related actions

    # Relationships
    user = relationship("User", foreign_keys=[user_id])
