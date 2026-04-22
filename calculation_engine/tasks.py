"""Celery tasks"""

from celery_app import app

@app.task
def test_task():
    return "Task completed"
