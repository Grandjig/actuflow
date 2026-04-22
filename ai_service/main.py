"""AI Service entry point."""

import os
from fastapi import FastAPI

app = FastAPI(
    title="ActuFlow AI Service",
    description="AI/ML features for ActuFlow",
    version="0.1.0",
)

AI_ENABLED = os.getenv("AI_ENABLED", "true").lower() == "true"


@app.get("/")
async def root():
    """Root endpoint."""
    return {"service": "AI Service", "enabled": AI_ENABLED}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "ai_enabled": AI_ENABLED}
