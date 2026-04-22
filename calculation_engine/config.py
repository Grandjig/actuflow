"""Calculation Engine Configuration."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Calculation engine settings."""
    
    # Database
    DATABASE_URL: str = "postgresql://actuflow:actuflow_secret@localhost:5432/actuflow"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Calculation settings
    MAX_POLICIES_PER_BATCH: int = 1000
    PROJECTION_MONTHS: int = 600  # 50 years
    
    class Config:
        env_file = ".env"


settings = Settings()
