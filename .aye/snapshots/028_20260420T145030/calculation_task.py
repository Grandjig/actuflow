"""Calculation Celery Task."""

import logging
import uuid
from datetime import datetime

import redis
from celery import Task

from calculation_engine.celery_app import celery_app
from calculation_engine.config import settings
from calculation_engine.engine.executor import CalculationExecutor

logger = logging.getLogger(__name__)


class CalculationTask(Task):
    """Base calculation task with error handling."""

    autoretry_for = (Exception,)
    retry_kwargs = {"max_retries": 3}
    retry_backoff = True
    retry_backoff_max = 600

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Handle task failure."""
        run_id = args[0] if args else kwargs.get("run_id")
        if run_id:
            logger.error(f"Calculation {run_id} failed: {exc}")
            # Update status in Redis for immediate UI feedback
            r = redis.from_url(settings.REDIS_URL)
            r.hset(f"calc:{run_id}", mapping={
                "status": "failed",
                "error": str(exc),
                "completed_at": datetime.utcnow().isoformat(),
            })


@celery_app.task(base=CalculationTask, bind=True)
def run_calculation(self, run_id: str):
    """Execute a calculation run."""
    logger.info(f"Starting calculation run: {run_id}")

    # Update progress in Redis
    r = redis.from_url(settings.REDIS_URL)
    r.hset(f"calc:{run_id}", mapping={
        "status": "running",
        "started_at": datetime.utcnow().isoformat(),
        "progress": 0,
        "message": "Initializing...",
    })

    try:
        executor = CalculationExecutor(run_id=uuid.UUID(run_id))

        # Progress callback
        def on_progress(processed: int, total: int, message: str):
            progress = int((processed / total) * 100) if total > 0 else 0
            r.hset(f"calc:{run_id}", mapping={
                "progress": progress,
                "processed": processed,
                "total": total,
                "message": message,
            })

        executor.on_progress = on_progress

        # Execute
        result = executor.execute()

        # Mark complete
        r.hset(f"calc:{run_id}", mapping={
            "status": "completed",
            "progress": 100,
            "completed_at": datetime.utcnow().isoformat(),
            "message": "Calculation completed",
        })

        logger.info(f"Calculation {run_id} completed successfully")
        return result

    except Exception as e:
        logger.exception(f"Calculation {run_id} failed")
        r.hset(f"calc:{run_id}", mapping={
            "status": "failed",
            "error": str(e),
            "completed_at": datetime.utcnow().isoformat(),
        })
        raise


@celery_app.task
def cancel_calculation(run_id: str):
    """Cancel a running calculation."""
    logger.info(f"Cancelling calculation: {run_id}")

    r = redis.from_url(settings.REDIS_URL)
    r.hset(f"calc:{run_id}", mapping={
        "status": "cancelled",
        "completed_at": datetime.utcnow().isoformat(),
        "message": "Calculation cancelled by user",
    })

    # The executor checks for cancellation flag periodically
    r.set(f"calc:{run_id}:cancel", "1", ex=3600)
