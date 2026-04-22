"""Calculation Engine Configuration."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Calculation engine settings."""

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://actuflow:actuflow@localhost:5432/actuflow"

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Redis for progress tracking
    REDIS_URL: str = "redis://localhost:6379/1"

    # Calculation settings
    BATCH_SIZE: int = 1000
    MAX_PROJECTION_MONTHS: int = 1200  # 100 years

    # AI Service
    AI_SERVICE_URL: str = "http://localhost:8001"
    AI_ENABLED: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
