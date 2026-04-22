"""Celery application configuration."""

import os
from celery import Celery

# Get Redis URL from environment
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Create Celery app
celery_app = Celery(
    "actuflow",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[
        "app.tasks.calculation_tasks",
        "app.tasks.report_tasks",
        "app.tasks.import_tasks",
    ],
)

# Celery configuration
celery_app.conf.update(
    # Task settings
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Result backend settings
    result_expires=3600,  # Results expire after 1 hour
    
    # Worker settings
    worker_prefetch_multiplier=1,  # Prevent worker from grabbing too many tasks
    worker_concurrency=2,  # Limit concurrent tasks (for free tier)
    
    # Task routing
    task_routes={
        "app.tasks.calculation_tasks.*": {"queue": "calculations"},
        "app.tasks.report_tasks.*": {"queue": "reports"},
        "app.tasks.import_tasks.*": {"queue": "imports"},
    },
    
    # Task defaults
    task_default_queue="default",
    task_default_exchange="default",
    task_default_routing_key="default",
    
    # Retry settings
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    
    # Beat schedule (for scheduled jobs)
    beat_schedule={},
)


@celery_app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery connection."""
    print(f"Request: {self.request!r}")
    return "Celery is working!"
