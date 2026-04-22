"""Scheduled Job Tasks."""

import logging
from datetime import datetime, timedelta

from calculation_engine.celery_app import celery_app
from calculation_engine.config import settings

logger = logging.getLogger(__name__)


@celery_app.task
def check_scheduled_jobs():
    """Check and execute due scheduled jobs."""
    import asyncio
    from sqlalchemy import select
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker

    async def _check_jobs():
        engine = create_async_engine(settings.DATABASE_URL)
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with async_session() as session:
            from app.models.scheduled_job import ScheduledJob

            # Get jobs due for execution
            now = datetime.utcnow()
            result = await session.execute(
                select(ScheduledJob)
                .where(ScheduledJob.is_active == True)
                .where(ScheduledJob.is_deleted == False)
                .where(ScheduledJob.next_run_at <= now)
            )
            jobs = result.scalars().all()

            for job in jobs:
                logger.info(f"Executing scheduled job: {job.name}")
                try:
                    execute_scheduled_job.delay(str(job.id))
                except Exception as e:
                    logger.error(f"Failed to queue job {job.name}: {e}")

        await engine.dispose()

    asyncio.run(_check_jobs())


@celery_app.task(bind=True, max_retries=3)
def execute_scheduled_job(self, job_id: str):
    """Execute a specific scheduled job."""
    import asyncio
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    from croniter import croniter

    async def _execute():
        engine = create_async_engine(settings.DATABASE_URL)
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with async_session() as session:
            from app.models.scheduled_job import ScheduledJob
            from app.models.job_execution import JobExecution

            # Get job
            result = await session.execute(
                select(ScheduledJob).where(ScheduledJob.id == job_id)
            )
            job = result.scalar_one_or_none()

            if not job:
                logger.error(f"Job {job_id} not found")
                return

            # Create execution record
            execution = JobExecution(
                scheduled_job_id=job.id,
                started_at=datetime.utcnow(),
                status="running",
            )
            session.add(execution)
            await session.flush()

            try:
                # Execute based on job type
                if job.job_type == "calculation":
                    from calculation_engine.tasks.calculation_task import run_calculation
                    run_calculation.delay(job.config.get("calculation_run_id"))
                elif job.job_type == "report":
                    from calculation_engine.tasks.report_generation_task import generate_report
                    generate_report.delay(job.config.get("report_template_id"))
                elif job.job_type == "import":
                    from calculation_engine.tasks.import_task import process_import
                    process_import.delay(job.config.get("import_config"))
                elif job.job_type == "data_check":
                    logger.info(f"Running data check: {job.config}")
                else:
                    logger.warning(f"Unknown job type: {job.job_type}")

                execution.status = "completed"
                execution.completed_at = datetime.utcnow()
                job.last_run_status = "completed"

            except Exception as e:
                logger.exception(f"Job {job.name} failed")
                execution.status = "failed"
                execution.error_message = str(e)
                execution.completed_at = datetime.utcnow()
                job.last_run_status = "failed"
                raise

            finally:
                # Update next run time
                job.last_run_at = datetime.utcnow()
                cron = croniter(job.cron_expression, datetime.utcnow())
                job.next_run_at = cron.get_next(datetime)

                await session.commit()

        await engine.dispose()

    asyncio.run(_execute())
