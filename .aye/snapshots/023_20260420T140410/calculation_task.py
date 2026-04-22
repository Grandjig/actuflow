"""Calculation tasks."""

from celery_app import celery_app


@celery_app.task(bind=True)
def run_calculation(self, run_id: str):
    """Run actuarial calculation."""
    print(f"Starting calculation run: {run_id}")
    # Placeholder - actual implementation would go here
    return {"run_id": run_id, "status": "completed"}
