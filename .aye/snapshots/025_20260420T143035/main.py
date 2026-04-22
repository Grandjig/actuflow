"""
FastAPI Application Entry Point
===============================

Main application factory and configuration.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.exceptions import (
    ActuFlowException,
    NotFoundError,
    ForbiddenError,
    ValidationError,
)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"AI Enabled: {settings.AI_ENABLED}")
    yield
    # Shutdown
    logger.info("Shutting down...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Insurance Data Management & Actuarial Platform",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# =============================================================================
# Middleware
# =============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# Exception Handlers
# =============================================================================

@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message, "error": exc.details},
    )


@app.exception_handler(ForbiddenError)
async def forbidden_handler(request: Request, exc: ForbiddenError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": exc.message},
    )


@app.exception_handler(ValidationError)
async def validation_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.message, "errors": exc.errors},
    )


@app.exception_handler(ActuFlowException)
async def actuflow_exception_handler(request: Request, exc: ActuFlowException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": exc.message, "error": exc.details},
    )


# =============================================================================
# Health & Root Endpoints
# =============================================================================

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
    }


@app.get("/ready")
async def readiness_check():
    """Readiness check - verifies dependencies."""
    from app.database import engine
    
    checks = {"database": False, "redis": False}
    
    # Check database
    try:
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
            checks["database"] = True
    except Exception as e:
        logger.warning(f"Database check failed: {e}")
    
    # Check Redis
    try:
        import redis.asyncio as redis
        r = redis.from_url(settings.REDIS_URL)
        await r.ping()
        checks["redis"] = True
    except Exception as e:
        logger.warning(f"Redis check failed: {e}")
    
    all_healthy = all(checks.values())
    return JSONResponse(
        status_code=status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"status": "ready" if all_healthy else "not_ready", "checks": checks},
    )


# =============================================================================
# Include Routers
# =============================================================================

from app.api.router import api_router

app.include_router(api_router, prefix=settings.API_V1_PREFIX)
