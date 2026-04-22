"""Celery application configuration."""

import os
from celery import Celery

# Redis URL from environment
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Create Celery app
celery_app = Celery(
    "actuflow",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[
        "tasks.calculation_task",
        "tasks.report_task",
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max
    worker_prefetch_multiplier=1,
    worker_concurrency=4,
)


@celery_app.task(bind=True)
def debug_task(self):
    """Debug task for testing."""
    print(f"Request: {self.request!r}")
    return "pong"
