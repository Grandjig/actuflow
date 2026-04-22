"""Automation Service."""

import logging
from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import NotFoundError, ValidationError
from app.models.automation_rule import AutomationRule, ActionType, TriggerType
from app.models.scheduled_job import ScheduledJob, JobType
from app.models.job_execution import JobExecution
from app.models.user import User
from app.utils.validators import validate_cron_expression

logger = logging.getLogger(__name__)


class AutomationService:
    """Service for automation operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # ==========================================
    # Scheduled Jobs
    # ==========================================
    
    async def get_scheduled_job(self, job_id: UUID) -> ScheduledJob | None:
        """Get a scheduled job by ID."""
        result = await self.db.execute(
            select(ScheduledJob)
            .where(ScheduledJob.id == job_id)
            .where(ScheduledJob.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    async def list_scheduled_jobs(
        self,
        offset: int = 0,
        limit: int = 20,
        is_active: bool | None = None,
        job_type: str | None = None,
    ) -> tuple[list[ScheduledJob], int]:
        """List scheduled jobs."""
        query = select(ScheduledJob).where(ScheduledJob.is_deleted == False)
        
        if is_active is not None:
            query = query.where(ScheduledJob.is_active == is_active)
        if job_type:
            query = query.where(ScheduledJob.job_type == job_type)
        
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0
        
        query = query.order_by(ScheduledJob.name).offset(offset).limit(limit)
        
        result = await self.db.execute(query)
        jobs = list(result.scalars().all())
        
        return jobs, total
    
    async def create_scheduled_job(
        self,
        name: str,
        job_type: str,
        cron_expression: str,
        config: dict,
        created_by: User,
        description: str | None = None,
    ) -> ScheduledJob:
        """Create a scheduled job."""
        # Validate cron expression
        is_valid, error = validate_cron_expression(cron_expression)
        if not is_valid:
            raise ValidationError(f"Invalid cron expression: {error}")
        
        # Validate job type
        valid_types = [t.value for t in JobType]
        if job_type not in valid_types:
            raise ValidationError(f"Invalid job type. Must be one of: {valid_types}")
        
        job = ScheduledJob(
            name=name,
            description=description,
            job_type=job_type,
            cron_expression=cron_expression,
            config=config,
            is_active=True,
            created_by_id=created_by.id,
        )
        
        self.db.add(job)
        await self.db.flush()
        await self.db.refresh(job)
        
        # TODO: Notify scheduler to add job
        
        return job
    
    async def update_scheduled_job(
        self,
        job: ScheduledJob,
        name: str | None = None,
        description: str | None = None,
        cron_expression: str | None = None,
        config: dict | None = None,
        is_active: bool | None = None,
    ) -> ScheduledJob:
        """Update a scheduled job."""
        if cron_expression:
            is_valid, error = validate_cron_expression(cron_expression)
            if not is_valid:
                raise ValidationError(f"Invalid cron expression: {error}")
            job.cron_expression = cron_expression
        
        if name:
            job.name = name
        if description is not None:
            job.description = description
        if config is not None:
            job.config = config
        if is_active is not None:
            job.is_active = is_active
        
        await self.db.flush()
        await self.db.refresh(job)
        
        # TODO: Notify scheduler to update job
        
        return job
    
    async def delete_scheduled_job(self, job: ScheduledJob) -> None:
        """Soft delete a scheduled job."""
        job.is_deleted = True
        job.deleted_at = datetime.utcnow()
        job.is_active = False
        await self.db.flush()
        
        # TODO: Notify scheduler to remove job
    
    async def get_job_executions(
        self,
        job_id: UUID,
        limit: int = 20,
    ) -> list[JobExecution]:
        """Get execution history for a job."""
        result = await self.db.execute(
            select(JobExecution)
            .where(JobExecution.scheduled_job_id == job_id)
            .order_by(JobExecution.started_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    # ==========================================
    # Automation Rules
    # ==========================================
    
    async def get_automation_rule(self, rule_id: UUID) -> AutomationRule | None:
        """Get an automation rule by ID."""
        result = await self.db.execute(
            select(AutomationRule)
            .where(AutomationRule.id == rule_id)
            .where(AutomationRule.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    async def list_automation_rules(
        self,
        offset: int = 0,
        limit: int = 20,
        trigger_type: str | None = None,
        is_active: bool | None = None,
    ) -> tuple[list[AutomationRule], int]:
        """List automation rules."""
        query = select(AutomationRule).where(AutomationRule.is_deleted == False)
        
        if trigger_type:
            query = query.where(AutomationRule.trigger_type == trigger_type)
        if is_active is not None:
            query = query.where(AutomationRule.is_active == is_active)
        
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0
        
        query = query.order_by(AutomationRule.name).offset(offset).limit(limit)
        
        result = await self.db.execute(query)
        rules = list(result.scalars().all())
        
        return rules, total
    
    async def create_automation_rule(
        self,
        name: str,
        trigger_type: str,
        trigger_config: dict,
        action_type: str,
        action_config: dict,
        created_by: User,
        description: str | None = None,
    ) -> AutomationRule:
        """Create an automation rule."""
        # Validate trigger type
        valid_triggers = [t.value for t in TriggerType]
        if trigger_type not in valid_triggers:
            raise ValidationError(f"Invalid trigger type. Must be one of: {valid_triggers}")
        
        # Validate action type
        valid_actions = [a.value for a in ActionType]
        if action_type not in valid_actions:
            raise ValidationError(f"Invalid action type. Must be one of: {valid_actions}")
        
        rule = AutomationRule(
            name=name,
            description=description,
            trigger_type=trigger_type,
            trigger_config=trigger_config,
            action_type=action_type,
            action_config=action_config,
            is_active=True,
            created_by_id=created_by.id,
        )
        
        self.db.add(rule)
        await self.db.flush()
        await self.db.refresh(rule)
        
        return rule
    
    async def update_automation_rule(
        self,
        rule: AutomationRule,
        name: str | None = None,
        description: str | None = None,
        trigger_config: dict | None = None,
        action_config: dict | None = None,
        is_active: bool | None = None,
    ) -> AutomationRule:
        """Update an automation rule."""
        if name:
            rule.name = name
        if description is not None:
            rule.description = description
        if trigger_config is not None:
            rule.trigger_config = trigger_config
        if action_config is not None:
            rule.action_config = action_config
        if is_active is not None:
            rule.is_active = is_active
        
        await self.db.flush()
        await self.db.refresh(rule)
        
        return rule
    
    async def delete_automation_rule(self, rule: AutomationRule) -> None:
        """Soft delete an automation rule."""
        rule.is_deleted = True
        rule.deleted_at = datetime.utcnow()
        await self.db.flush()
    
    async def get_rules_for_trigger(
        self,
        trigger_type: str,
    ) -> list[AutomationRule]:
        """Get active rules for a trigger type."""
        result = await self.db.execute(
            select(AutomationRule)
            .where(AutomationRule.trigger_type == trigger_type)
            .where(AutomationRule.is_active == True)
            .where(AutomationRule.is_deleted == False)
        )
        return list(result.scalars().all())
    
    async def evaluate_and_execute_rules(
        self,
        trigger_type: str,
        event_data: dict,
    ) -> list[dict]:
        """Evaluate rules for a trigger and execute matching ones."""
        rules = await self.get_rules_for_trigger(trigger_type)
        results = []
        
        for rule in rules:
            if self._evaluate_condition(rule.trigger_config, event_data):
                try:
                    await self._execute_action(rule, event_data)
                    rule.execution_count += 1
                    rule.last_executed_at = datetime.utcnow()
                    results.append({
                        "rule_id": str(rule.id),
                        "rule_name": rule.name,
                        "success": True,
                    })
                except Exception as e:
                    logger.exception(f"Failed to execute rule {rule.id}: {e}")
                    results.append({
                        "rule_id": str(rule.id),
                        "rule_name": rule.name,
                        "success": False,
                        "error": str(e),
                    })
        
        await self.db.flush()
        return results
    
    def _evaluate_condition(self, trigger_config: dict, event_data: dict) -> bool:
        """Evaluate if trigger condition is met."""
        conditions = trigger_config.get("conditions", [])
        
        if not conditions:
            return True
        
        for condition in conditions:
            field = condition.get("field")
            operator = condition.get("operator")
            value = condition.get("value")
            
            actual_value = event_data.get(field)
            
            if operator == "equals":
                if actual_value != value:
                    return False
            elif operator == "not_equals":
                if actual_value == value:
                    return False
            elif operator == "contains":
                if value not in str(actual_value):
                    return False
            elif operator == "greater_than":
                if not (actual_value and actual_value > value):
                    return False
            elif operator == "less_than":
                if not (actual_value and actual_value < value):
                    return False
            elif operator == "in":
                if actual_value not in value:
                    return False
        
        return True
    
    async def _execute_action(self, rule: AutomationRule, event_data: dict) -> None:
        """Execute the rule action."""
        action_type = rule.action_type
        action_config = rule.action_config
        
        if action_type == ActionType.SEND_NOTIFICATION.value:
            await self._send_notification_action(action_config, event_data)
        elif action_type == ActionType.CREATE_TASK.value:
            await self._create_task_action(action_config, event_data)
        elif action_type == ActionType.CALL_WEBHOOK.value:
            await self._call_webhook_action(action_config, event_data)
        elif action_type == ActionType.RUN_CALCULATION.value:
            await self._run_calculation_action(action_config, event_data)
        else:
            logger.warning(f"Unknown action type: {action_type}")
    
    async def _send_notification_action(self, config: dict, event_data: dict) -> None:
        """Send notification action."""
        from app.services.notification_service import NotificationService
        
        user_ids = config.get("user_ids", [])
        title = config.get("title", "Automation Notification")
        message = config.get("message", "")
        
        # Template replacement
        for key, value in event_data.items():
            message = message.replace(f"{{{key}}}", str(value))
        
        notification_service = NotificationService(self.db)
        
        for user_id in user_ids:
            await notification_service.create_notification(
                user_id=user_id,
                title=title,
                message=message,
                notification_type="automation",
            )
    
    async def _create_task_action(self, config: dict, event_data: dict) -> None:
        """Create task action."""
        # TODO: Implement task creation
        pass
    
    async def _call_webhook_action(self, config: dict, event_data: dict) -> None:
        """Call webhook action."""
        import httpx
        
        url = config.get("url")
        method = config.get("method", "POST")
        headers = config.get("headers", {})
        
        async with httpx.AsyncClient() as client:
            await client.request(
                method,
                url,
                json=event_data,
                headers=headers,
                timeout=30.0,
            )
    
    async def _run_calculation_action(self, config: dict, event_data: dict) -> None:
        """Run calculation action."""
        # TODO: Dispatch calculation task
        pass
