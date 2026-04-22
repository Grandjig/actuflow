"""AI Service Main Application."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import settings
from api import nlp, embeddings, extraction, anomaly
from services.embedding_service import EmbeddingService

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("Starting AI Service...")
    
    # Initialize embedding model on startup
    if settings.USE_LOCAL_EMBEDDINGS:
        logger.info("Loading local embedding model...")
        embedding_service = EmbeddingService()
        embedding_service._load_model()
        logger.info("Embedding model loaded")
    
    logger.info(f"AI Service started. Features enabled:")
    logger.info(f"  - Smart Import: {settings.AI_SMART_IMPORT}")
    logger.info(f"  - Natural Language: {settings.AI_NATURAL_LANGUAGE}")
    logger.info(f"  - Anomaly Detection: {settings.AI_ANOMALY_DETECTION}")
    logger.info(f"  - Narrative Generation: {settings.AI_NARRATIVE_GENERATION}")
    logger.info(f"  - Semantic Search: {settings.AI_SEMANTIC_SEARCH}")
    logger.info(f"  - Document Extraction: {settings.AI_DOCUMENT_EXTRACTION}")
    
    yield
    
    logger.info("Shutting down AI Service...")


app = FastAPI(
    title="ActuFlow AI Service",
    description="AI/ML features for ActuFlow platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS - only allow internal services
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to backend service
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
    )


# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "ai_enabled": settings.AI_ENABLED,
    }


@app.get("/features")
async def get_features():
    """Get enabled AI features."""
    return {
        "ai_enabled": settings.AI_ENABLED,
        "features": {
            "smart_import": settings.AI_SMART_IMPORT,
            "natural_language": settings.AI_NATURAL_LANGUAGE,
            "anomaly_detection": settings.AI_ANOMALY_DETECTION,
            "narrative_generation": settings.AI_NARRATIVE_GENERATION,
            "semantic_search": settings.AI_SEMANTIC_SEARCH,
            "document_extraction": settings.AI_DOCUMENT_EXTRACTION,
            "experience_recommendations": settings.AI_EXPERIENCE_RECOMMENDATIONS,
        },
    }


# Include routers
if settings.AI_ENABLED:
    app.include_router(nlp.router, prefix="/nlp", tags=["NLP"])
    app.include_router(embeddings.router, prefix="/embeddings", tags=["Embeddings"])
    app.include_router(extraction.router, prefix="/extract", tags=["Extraction"])
    app.include_router(anomaly.router, prefix="/anomaly", tags=["Anomaly Detection"])
