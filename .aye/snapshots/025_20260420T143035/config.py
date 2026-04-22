"""
Application Configuration
=========================

Centralized settings using Pydantic Settings.
"""

from functools import lru_cache
from typing import Any, Optional

from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ==========================================================================
    # Application
    # ==========================================================================
    APP_NAME: str = "ActuFlow"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # ==========================================================================
    # API
    # ==========================================================================
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # ==========================================================================
    # Database
    # ==========================================================================
    DATABASE_URL: str = "postgresql+asyncpg://actuflow:actuflow_dev@postgres:5432/actuflow"
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10

    # ==========================================================================
    # Redis
    # ==========================================================================
    REDIS_URL: str = "redis://redis:6379/0"

    # ==========================================================================
    # Authentication
    # ==========================================================================
    JWT_SECRET: str = "dev-secret-change-in-production-immediately"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ==========================================================================
    # Keycloak (Optional)
    # ==========================================================================
    KEYCLOAK_ENABLED: bool = False
    KEYCLOAK_SERVER_URL: str = "http://keycloak:8080"
    KEYCLOAK_REALM: str = "actuflow"
    KEYCLOAK_CLIENT_ID: str = "actuflow-api"
    KEYCLOAK_CLIENT_SECRET: str = ""

    # ==========================================================================
    # Storage (S3/MinIO)
    # ==========================================================================
    S3_ENDPOINT_URL: str = "http://minio:9000"
    S3_ACCESS_KEY: str = "actuflow"
    S3_SECRET_KEY: str = "actuflow_dev"
    S3_BUCKET_NAME: str = "actuflow"
    S3_REGION: str = "us-east-1"

    # ==========================================================================
    # AI Service
    # ==========================================================================
    AI_ENABLED: bool = False
    AI_SERVICE_URL: str = "http://ai-service:8001"
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4-turbo-preview"

    # AI Feature Flags
    AI_SMART_IMPORT: bool = True
    AI_NATURAL_LANGUAGE: bool = True
    AI_ANOMALY_DETECTION: bool = True
    AI_NARRATIVE_GENERATION: bool = True
    AI_SEMANTIC_SEARCH: bool = True
    AI_DOCUMENT_EXTRACTION: bool = True
    AI_EXPERIENCE_RECOMMENDATIONS: bool = True

    # ==========================================================================
    # Celery
    # ==========================================================================
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"

    # ==========================================================================
    # Email
    # ==========================================================================
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "noreply@actuflow.com"
    SMTP_TLS: bool = True

    # ==========================================================================
    # Pagination
    # ==========================================================================
    DEFAULT_PAGE_SIZE: int = 25
    MAX_PAGE_SIZE: int = 1000


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
