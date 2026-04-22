"""Configuration for Calculation Engine"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    celery_broker_url: str = "redis://redis:6379/1"
    celery_result_backend: str = "redis://redis:6379/2"
    database_url: str = "postgresql://actuflow:actuflow@postgres:5432/actuflow"
    
    class Config:
        env_file = ".env"

settings = Settings()
