"""Application configuration."""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
 """Application settings loaded from environment variables."""

 model_config = SettingsConfigDict(
 env_file=".env",
 env_file_encoding="utf-8",
 case_sensitive=True,
 extra="ignore",
 )

 # Project
 PROJECT_NAME: str = "ActuFlow"
 DEBUG: bool = False
 API_V1_PREFIX: str = "/api/v1"

 # Security
 SECRET_KEY: str = "change-me-in-production-use-openssl-rand-hex-32"
 ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
 REFRESH_TOKEN_EXPIRE_DAYS: int = 7

 # Database
 DATABASE_URL: str = "postgresql://actuflow:actuflow_secret@localhost:5432/actuflow"

 # Redis
 REDIS_URL: str = "redis://localhost:6379/0"

 # CORS - comma-separated list of allowed origins
 # For GitHub Pages: https://username.github.io
 ALLOWED_ORIGINS: str = ""

 # GitHub Pages URL (optional)
 GITHUB_PAGES_URL: Optional[str] = None

 # File Storage
 S3_ENDPOINT: str = "http://localhost:9000"
 S3_ACCESS_KEY: str = "minioadmin"
 S3_SECRET_KEY: str = "minioadmin"
 S3_BUCKET: str = "actuflow"

 # AI Service
 AI_SERVICE_URL: str = "http://localhost:8001"
 AI_ENABLED: bool = True

 # Email (optional)
 SMTP_HOST: Optional[str] = None
 SMTP_PORT: int = 587
 SMTP_USER: Optional[str] = None
 SMTP_PASSWORD: Optional[str] = None


@lru_cache
def get_settings() -> Settings:
 """Get cached settings instance."""
 return Settings()


settings = get_settings()
