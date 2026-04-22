"""AI Service Configuration."""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """AI service settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )
    
    # Service
    SERVICE_NAME: str = "actuflow-ai-service"
    DEBUG: bool = False
    
    # Database (for vector storage)
    DATABASE_URL: str = "postgresql://actuflow:actuflow_secret@postgres:5432/actuflow"
    
    # Redis (for caching)
    REDIS_URL: str = "redis://redis:6379/3"
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    OPENAI_MAX_TOKENS: int = 4096
    OPENAI_TEMPERATURE: float = 0.1
    
    # LLM Provider: 'openai', 'azure', 'local'
    LLM_PROVIDER: Literal["openai", "azure", "local"] = "openai"
    
    # Azure OpenAI (if using Azure)
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_KEY: str = ""
    AZURE_OPENAI_DEPLOYMENT: str = ""
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"
    
    # Local LLM (Ollama)
    LOCAL_LLM_URL: str = "http://ollama:11434"
    LOCAL_LLM_MODEL: str = "llama2"
    
    # Embedding Model
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384
    USE_LOCAL_EMBEDDINGS: bool = True
    
    # OCR
    TESSERACT_CMD: str = "tesseract"
    OCR_LANGUAGE: str = "eng"
    
    # Anomaly Detection
    ANOMALY_CONTAMINATION: float = 0.1
    ANOMALY_THRESHOLD: float = 0.7
    
    # Feature Flags
    AI_ENABLED: bool = True
    AI_SMART_IMPORT: bool = True
    AI_NATURAL_LANGUAGE: bool = True
    AI_ANOMALY_DETECTION: bool = True
    AI_NARRATIVE_GENERATION: bool = True
    AI_SEMANTIC_SEARCH: bool = True
    AI_DOCUMENT_EXTRACTION: bool = True
    AI_EXPERIENCE_RECOMMENDATIONS: bool = True
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60
    
    # Cache TTL
    EMBEDDING_CACHE_TTL: int = 86400  # 24 hours
    QUERY_CACHE_TTL: int = 3600  # 1 hour


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
