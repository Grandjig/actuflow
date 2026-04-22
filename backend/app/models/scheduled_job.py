"""Scheduled Job Model."""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.models.base import Base


class ScheduledJob(Base):
    """Scheduled automation jobs."""

    __tablename__ = "scheduled_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    job_type = Column(String(100), nullable=False)  # calculation, report, import, data_check
    cron_expression = Column(String(100), nullable=False)
    config = Column(JSONB, default=dict)
    
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    
    last_run = Column(DateTime)
    next_run = Column(DateTime)
    
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by = relationship("User")
    executions = relationship("JobExecution", back_populates="scheduled_job", order_by="desc(JobExecution.started_at)")
