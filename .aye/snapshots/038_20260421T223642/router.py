"""API Router.

Combines all API route modules.
"""

from fastapi import APIRouter

from app.api import (
    auth,
    users,
    policies,
    policyholders,
    claims,
    assumptions,
    calculations,
    scenarios,
    reports,
    dashboards,
    imports,
    documents,
    notifications,
    audit,
    ai,
    automation,
)

api_router = APIRouter()

# Auth routes
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# User management
api_router.include_router(users.router, prefix="/users", tags=["Users"])

# Policy management
api_router.include_router(policies.router, prefix="/policies", tags=["Policies"])
api_router.include_router(policyholders.router, prefix="/policyholders", tags=["Policyholders"])
api_router.include_router(claims.router, prefix="/claims", tags=["Claims"])

# Actuarial
api_router.include_router(assumptions.router, prefix="/assumption-sets", tags=["Assumptions"])
api_router.include_router(calculations.router, prefix="/calculations", tags=["Calculations"])
api_router.include_router(scenarios.router, prefix="/scenarios", tags=["Scenarios"])

# Reporting
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(dashboards.router, prefix="/dashboards", tags=["Dashboards"])

# Data management
api_router.include_router(imports.router, prefix="/imports", tags=["Imports"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])

# Notifications
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])

# Audit
api_router.include_router(audit.router, prefix="/audit-logs", tags=["Audit"])

# AI features
api_router.include_router(ai.router, prefix="/ai", tags=["AI"])

# Automation
api_router.include_router(automation.router, prefix="/automation", tags=["Automation"])
