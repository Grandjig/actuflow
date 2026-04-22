"""
ActuFlow Configuration
======================

Centralized configuration management using Pydantic Settings.
All configuration is loaded from environment variables with sensible defaults.
"""

from functools import lru_cache
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings have sensible defaults for development.
    Production deployments should set appropriate values via environment.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )
    
    # -------------------------------------------------------------------------
    # Application
    # -------------------------------------------------------------------------
    APP_NAME: str = "ActuFlow"
    APP_ENV: str = Field(default="development", pattern="^(development|staging|production)$")
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production-min-32-chars"
    API_V1_PREFIX: str = "/api/v1"
    
    # -------------------------------------------------------------------------
    # Database
    # -------------------------------------------------------------------------
    DATABASE_URL: str = "postgresql+asyncpg://actuflow:actuflow@localhost:5432/actuflow"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_ECHO: bool = False  # Set to True to log SQL queries
    
    @property
    def database_url_sync(self) -> str:
        """Synchronous database URL for Alembic migrations."""
        return self.DATABASE_URL.replace("+asyncpg", "")
    
    # -------------------------------------------------------------------------
    # Redis
    # -------------------------------------------------------------------------
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # -------------------------------------------------------------------------
    # Object Storage (S3/MinIO)
    # -------------------------------------------------------------------------
    S3_ENDPOINT_URL: Optional[str] = "http://localhost:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET_NAME: str = "actuflow"
    S3_REGION: str = "us-east-1"
    
    # -------------------------------------------------------------------------
    # Elasticsearch
    # -------------------------------------------------------------------------
    ELASTICSEARCH_URL: Optional[str] = "http://localhost:9200"
    ELASTICSEARCH_INDEX_PREFIX: str = "actuflow"
    
    # -------------------------------------------------------------------------
    # Authentication - Keycloak
    # -------------------------------------------------------------------------
    KEYCLOAK_URL: Optional[str] = None
    KEYCLOAK_REALM: str = "actuflow"
    KEYCLOAK_CLIENT_ID: str = "actuflow-backend"
    KEYCLOAK_CLIENT_SECRET: Optional[str] = None
    
    # -------------------------------------------------------------------------
    # Authentication - JWT (for local development without Keycloak)
    # -------------------------------------------------------------------------
    JWT_SECRET_KEY: str = "your-jwt-secret-key-min-32-characters-long"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    @property
    def use_keycloak(self) -> bool:
        """Check if Keycloak is configured."""
        return bool(self.KEYCLOAK_URL and self.KEYCLOAK_CLIENT_SECRET)
    
    # -------------------------------------------------------------------------
    # CORS
    # -------------------------------------------------------------------------
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    CORS_ALLOW_CREDENTIALS: bool = True
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    # -------------------------------------------------------------------------
    # Email (SMTP)
    # -------------------------------------------------------------------------
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: str = "noreply@actuflow.com"
    SMTP_FROM_NAME: str = "ActuFlow"
    SMTP_USE_TLS: bool = True
    
    @property
    def email_enabled(self) -> bool:
        """Check if email is configured."""
        return bool(self.SMTP_HOST and self.SMTP_USER)
    
    # -------------------------------------------------------------------------
    # AI Features
    # -------------------------------------------------------------------------
    AI_ENABLED: bool = True
    AI_SERVICE_URL: Optional[str] = "http://localhost:8001"
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Azure OpenAI (alternative)
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_DEPLOYMENT: Optional[str] = None
    
    # Local LLM (alternative)
    OLLAMA_URL: Optional[str] = None
    OLLAMA_MODEL: str = "llama2"
    
    # Individual AI feature flags
    AI_SMART_IMPORT: bool = True
    AI_NATURAL_LANGUAGE: bool = True
    AI_ANOMALY_DETECTION: bool = True
    AI_NARRATIVE_GENERATION: bool = True
    AI_SEMANTIC_SEARCH: bool = True
    AI_DOCUMENT_EXTRACTION: bool = True
    AI_EXPERIENCE_RECOMMENDATIONS: bool = True
    
    @property
    def llm_provider(self) -> str:
        """Determine which LLM provider to use."""
        if self.AZURE_OPENAI_ENDPOINT and self.AZURE_OPENAI_API_KEY:
            return "azure"
        elif self.OLLAMA_URL:
            return "ollama"
        elif self.OPENAI_API_KEY:
            return "openai"
        else:
            return "none"
    
    # -------------------------------------------------------------------------
    # File Uploads
    # -------------------------------------------------------------------------
    MAX_UPLOAD_SIZE_MB: int = 100
    ALLOWED_UPLOAD_EXTENSIONS: str = ".csv,.xlsx,.xls,.pdf,.png,.jpg,.jpeg"
    
    @property
    def max_upload_size_bytes(self) -> int:
        """Convert max upload size to bytes."""
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    
    @property
    def allowed_extensions_list(self) -> list[str]:
        """Parse allowed extensions into a list."""
        return [ext.strip().lower() for ext in self.ALLOWED_UPLOAD_EXTENSIONS.split(",")]
    
    # -------------------------------------------------------------------------
    # Pagination
    # -------------------------------------------------------------------------
    DEFAULT_PAGE_SIZE: int = 25
    MAX_PAGE_SIZE: int = 1000
    
    # -------------------------------------------------------------------------
    # Calculation Engine
    # -------------------------------------------------------------------------
    CALCULATION_WORKER_CONCURRENCY: int = 4
    CALCULATION_TASK_TIME_LIMIT: int = 3600  # 1 hour
    CALCULATION_SOFT_TIME_LIMIT: int = 3300  # 55 minutes
    CALCULATION_BATCH_SIZE: int = 1000
    
    # -------------------------------------------------------------------------
    # Logging
    # -------------------------------------------------------------------------
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = Field(default="console", pattern="^(json|console)$")
    
    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_levels}")
        return v.upper()
    
    # -------------------------------------------------------------------------
    # Monitoring
    # -------------------------------------------------------------------------
    SENTRY_DSN: Optional[str] = None
    PROMETHEUS_ENABLED: bool = True
    
    # -------------------------------------------------------------------------
    # Feature Flags
    # -------------------------------------------------------------------------
    FEATURE_SCENARIOS: bool = True
    FEATURE_EXPERIENCE_ANALYSIS: bool = True
    FEATURE_DOCUMENT_EXTRACTION: bool = True
    FEATURE_AUTOMATION: bool = True


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Settings are loaded once and cached for performance.
    Use dependency injection in FastAPI endpoints.
    """
    return Settings()


# Global settings instance for convenience
settings = get_settings()
