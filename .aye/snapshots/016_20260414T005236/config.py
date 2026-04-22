"""Application Configuration - Complete."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )
    
    # Application
    APP_NAME: str = "ActuFlow"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    # Database
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "actuflow"
    POSTGRES_PASSWORD: str = "actuflow_secret"
    POSTGRES_DB: str = "actuflow"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0
    
    # JWT
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Keycloak
    KEYCLOAK_ENABLED: bool = False
    KEYCLOAK_SERVER_URL: str = "http://keycloak:8080"
    KEYCLOAK_REALM: str = "actuflow"
    KEYCLOAK_CLIENT_ID: str = "actuflow-backend"
    KEYCLOAK_CLIENT_SECRET: str = ""
    
    # S3 / MinIO
    S3_ENDPOINT: str = "http://minio:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET: str = "actuflow"
    S3_REGION: str = "us-east-1"
    S3_USE_SSL: bool = False
    
    # Elasticsearch
    ELASTICSEARCH_URL: str = "http://elasticsearch:9200"
    ELASTICSEARCH_INDEX_PREFIX: str = "actuflow"
    
    # Email
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "noreply@actuflow.com"
    SMTP_FROM_NAME: str = "ActuFlow"
    SMTP_USE_TLS: bool = True
    
    # File uploads
    MAX_UPLOAD_SIZE_MB: int = 100
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 1000
    
    # AI Service
    AI_ENABLED: bool = True
    AI_SERVICE_URL: str = "http://ai-service:8001"
    OPENAI_API_KEY: str = ""
    
    # Feature Flags
    AI_SMART_IMPORT: bool = True
    AI_NATURAL_LANGUAGE: bool = True
    AI_ANOMALY_DETECTION: bool = True
    AI_NARRATIVE_GENERATION: bool = True
    AI_SEMANTIC_SEARCH: bool = True
    AI_DOCUMENT_EXTRACTION: bool = True
    AI_EXPERIENCE_RECOMMENDATIONS: bool = True
    
    @computed_field
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    @computed_field
    @property
    def database_url_sync(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    @computed_field
    @property
    def redis_url(self) -> str:
        password_part = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{password_part}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    @computed_field
    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @computed_field
    @property
    def max_upload_size_bytes(self) -> int:
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
