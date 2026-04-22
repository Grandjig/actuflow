"""ActuFlow API Main Application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print("ActuFlow API starting up...")
    yield
    # Shutdown
    print("ActuFlow API shutting down...")


app = FastAPI(
    title="ActuFlow API",
    description="Actuarial Management Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS - allow all origins for demo (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "ActuFlow API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health",
    }
