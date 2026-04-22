"""SQLAlchemy Models.

Import all models here so Alembic can discover them.
"""

from app.models.base import Base

# Import models in dependency order
from app.models.role import Role, Permission
from app.models.user import User
from app.models.policyholder import Policyholder
from app.models.policy import Policy
from app.models.coverage import Coverage
from app.models.claim import Claim
from app.models.assumption_set import AssumptionSet
from app.models.assumption_table import AssumptionTable
from app.models.model_definition import ModelDefinition
from app.models.calculation_run import CalculationRun
from app.models.calculation_result import CalculationResult
from app.models.scenario import Scenario
from app.models.scenario_result import ScenarioResult
from app.models.report_template import ReportTemplate
from app.models.generated_report import GeneratedReport
from app.models.dashboard_config import DashboardConfig
from app.models.data_import import DataImport
from app.models.task import Task
from app.models.comment import Comment
from app.models.notification import Notification
from app.models.audit_log import AuditLog
from app.models.document import Document
from app.models.scheduled_job import ScheduledJob
from app.models.job_execution import JobExecution
from app.models.automation_rule import AutomationRule
from app.models.ai_query_log import AIQueryLog

__all__ = [
    "Base",
    "User",
    "Role",
    "Permission",
    "Policy",
    "Policyholder",
    "Coverage",
    "Claim",
    "AssumptionSet",
    "AssumptionTable",
    "ModelDefinition",
    "CalculationRun",
    "CalculationResult",
    "Scenario",
    "ScenarioResult",
    "ReportTemplate",
    "GeneratedReport",
    "DashboardConfig",
    "DataImport",
    "Task",
    "Comment",
    "Notification",
    "AuditLog",
    "Document",
    "ScheduledJob",
    "JobExecution",
    "AutomationRule",
    "AIQueryLog",
]
