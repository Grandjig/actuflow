"""Celery Application Configuration."""

from celery import Celery

from calculation_engine.config import settings

celery_app = Celery(
    "actuflow",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "calculation_engine.tasks.calculation_task",
        "calculation_engine.tasks.report_task",
        "calculation_engine.tasks.import_task",
        "calculation_engine.tasks.scheduled_job_task",
    ],
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
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)

# Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    "check-scheduled-jobs": {
        "task": "calculation_engine.tasks.scheduled_job_task.check_scheduled_jobs",
        "schedule": 60.0,  # Every minute
    },
}
