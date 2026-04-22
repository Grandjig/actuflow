"""Celery app factory"""

from celery import Celery
from config import settings

app = Celery("actuflow_calc")

app.conf.update(
    broker_url=settings.celery_broker_url,
    result_backend=settings.celery_result_backend,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
)
