"""
API Router
==========

Main API router that includes all sub-routers.
"""

from fastapi import APIRouter

from app.api import (
    auth,
    users,
    roles,
    policies,
    policyholders,
    claims,
    assumptions,
    models,
    calculations,
    scenarios,
    reports,
    dashboards,
    imports,
    tasks,
    notifications,
    audit,
    search,
    ai,
    automation,
    experience,
    documents,
)

api_router = APIRouter()

# Authentication
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
)

# User Management
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
)

api_router.include_router(
    roles.router,
    prefix="/roles",
    tags=["Roles"],
)

# Policy Data
api_router.include_router(
    policies.router,
    prefix="/policies",
    tags=["Policies"],
)

api_router.include_router(
    policyholders.router,
    prefix="/policyholders",
    tags=["Policyholders"],
)

api_router.include_router(
    claims.router,
    prefix="/claims",
    tags=["Claims"],
)

# Actuarial
api_router.include_router(
    assumptions.router,
    prefix="/assumption-sets",
    tags=["Assumptions"],
)

api_router.include_router(
    models.router,
    prefix="/models",
    tags=["Models"],
)

api_router.include_router(
    calculations.router,
    prefix="/calculations",
    tags=["Calculations"],
)

api_router.include_router(
    scenarios.router,
    prefix="/scenarios",
    tags=["Scenarios"],
)

api_router.include_router(
    experience.router,
    prefix="/experience-analysis",
    tags=["Experience Analysis"],
)

# Reporting
api_router.include_router(
    reports.router,
    prefix="/reports",
    tags=["Reports"],
)

api_router.include_router(
    dashboards.router,
    prefix="/dashboards",
    tags=["Dashboards"],
)

# Data Management
api_router.include_router(
    imports.router,
    prefix="/imports",
    tags=["Data Imports"],
)

api_router.include_router(
    documents.router,
    prefix="/documents",
    tags=["Documents"],
)

# Workflow
api_router.include_router(
    tasks.router,
    prefix="/tasks",
    tags=["Tasks"],
)

api_router.include_router(
    notifications.router,
    prefix="/notifications",
    tags=["Notifications"],
)

# Automation
api_router.include_router(
    automation.router,
    prefix="/automation",
    tags=["Automation"],
)

# Audit & Search
api_router.include_router(
    audit.router,
    prefix="/audit-logs",
    tags=["Audit"],
)

api_router.include_router(
    search.router,
    prefix="/search",
    tags=["Search"],
)

# AI Features
api_router.include_router(
    ai.router,
    prefix="/ai",
    tags=["AI"],
)
