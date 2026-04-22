"""Job Execution Model."""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.models.base import Base


class JobExecution(Base):
    """Records of scheduled job executions."""

    __tablename__ = "job_executions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scheduled_job_id = Column(UUID(as_uuid=True), ForeignKey("scheduled_jobs.id"), nullable=False)
    
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    status = Column(String(50), default="running")  # running, completed, failed
    
    result_summary = Column(JSONB)
    error_message = Column(Text)
    
    duration_seconds = Column(Integer)

    # Relationships
    scheduled_job = relationship("ScheduledJob", back_populates="executions")
