"""
SQLAlchemy Models
=================

All database models for ActuFlow.
Imported here so Alembic can discover them for migrations.
"""

from app.models.base import Base, TimestampMixin, SoftDeleteMixin, AuditMixin

# Auth & Users
from app.models.user import User
from app.models.role import Role, Permission, role_permissions

# Policy Management
from app.models.policyholder import Policyholder
from app.models.policy import Policy
from app.models.coverage import Coverage
from app.models.claim import Claim

# Actuarial
from app.models.assumption_set import AssumptionSet
from app.models.assumption_table import AssumptionTable
from app.models.model_definition import ModelDefinition
from app.models.calculation_run import CalculationRun
from app.models.calculation_result import CalculationResult
from app.models.scenario import Scenario
from app.models.scenario_result import ScenarioResult

# Reporting
from app.models.report_template import ReportTemplate
from app.models.generated_report import GeneratedReport
from app.models.dashboard_config import DashboardConfig

# Data Management
from app.models.data_import import DataImport
from app.models.document import Document

# Workflow
from app.models.task import Task
from app.models.comment import Comment
from app.models.notification import Notification

# Automation
from app.models.scheduled_job import ScheduledJob
from app.models.job_execution import JobExecution
from app.models.automation_rule import AutomationRule

# Audit & AI
from app.models.audit_log import AuditLog
from app.models.ai_query_log import AIQueryLog
from app.models.experience_analysis import ExperienceAnalysis

__all__ = [
    # Base
    "Base",
    "TimestampMixin",
    "SoftDeleteMixin",
    "AuditMixin",
    # Auth
    "User",
    "Role",
    "Permission",
    "role_permissions",
    # Policy
    "Policyholder",
    "Policy",
    "Coverage",
    "Claim",
    # Actuarial
    "AssumptionSet",
    "AssumptionTable",
    "ModelDefinition",
    "CalculationRun",
    "CalculationResult",
    "Scenario",
    "ScenarioResult",
    # Reporting
    "ReportTemplate",
    "GeneratedReport",
    "DashboardConfig",
    # Data
    "DataImport",
    "Document",
    # Workflow
    "Task",
    "Comment",
    "Notification",
    # Automation
    "ScheduledJob",
    "JobExecution",
    "AutomationRule",
    # Audit
    "AuditLog",
    "AIQueryLog",
    "ExperienceAnalysis",
]
