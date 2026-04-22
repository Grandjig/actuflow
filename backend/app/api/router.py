"""API Router - Aggregates all route modules."""

from fastapi import APIRouter

from app.api import (
    auth,
    health,
    policies,
    policyholders,
    claims,
    assumptions,
    calculations,
    documents,
)

api_router = APIRouter()

# Health check (no auth required)
api_router.include_router(health.router, tags=["Health"])

# Auth routes
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Core business routes
api_router.include_router(policies.router, prefix="/policies", tags=["Policies"])
api_router.include_router(policyholders.router, prefix="/policyholders", tags=["Policyholders"])
api_router.include_router(claims.router, prefix="/claims", tags=["Claims"])
api_router.include_router(assumptions.router, prefix="/assumptions", tags=["Assumptions"])
api_router.include_router(calculations.router, prefix="/calculations", tags=["Calculations"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
