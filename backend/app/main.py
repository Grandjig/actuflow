"""ActuFlow Backend Application."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.api.router import api_router
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
 """Application lifespan handler."""
 # Startup
 print(f"Starting {settings.PROJECT_NAME}...")
 yield
 # Shutdown
 print(f"Shutting down {settings.PROJECT_NAME}...")


app = FastAPI(
 title=settings.PROJECT_NAME,
 description="AI-Powered Actuarial Data Management & Analysis Platform",
 version="1.0.0",
 openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
 docs_url=f"{settings.API_V1_PREFIX}/docs" if settings.DEBUG else None,
 redoc_url=f"{settings.API_V1_PREFIX}/redoc" if settings.DEBUG else None,
 lifespan=lifespan,
)

# CORS configuration for GitHub Pages deployment
allowed_origins = [
 "http://localhost:3000",
 "http://127.0.0.1:3000",
]

# Add production origins from environment
if settings.ALLOWED_ORIGINS:
 allowed_origins.extend(settings.ALLOWED_ORIGINS.split(","))

# Add GitHub Pages origin if configured
github_pages_url = os.getenv("GITHUB_PAGES_URL")
if github_pages_url:
 allowed_origins.append(github_pages_url)

app.add_middleware(
 CORSMiddleware,
 allow_origins=allowed_origins,
 allow_credentials=True,
 allow_methods=["*"],
 allow_headers=["*"],
 expose_headers=["X-Total-Count", "X-Page", "X-Page-Size"],
)

# Gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health")
async def health_check():
 """Health check endpoint."""
 return {"status": "healthy", "service": settings.PROJECT_NAME}


@app.get("/")
async def root():
 """Root endpoint."""
 return {
 "service": settings.PROJECT_NAME,
 "version": "1.0.0",
 "docs": f"{settings.API_V1_PREFIX}/docs",
 }
