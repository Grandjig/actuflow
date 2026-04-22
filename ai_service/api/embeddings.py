"""Embeddings API Routes."""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from config import settings
from services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)
router = APIRouter()


class GenerateEmbeddingRequest(BaseModel):
    """Embedding generation request."""
    text: str = Field(min_length=1, max_length=10000)


class BatchEmbeddingRequest(BaseModel):
    """Batch embedding generation request."""
    texts: list[str] = Field(min_items=1, max_items=100)


class EmbeddingResponse(BaseModel):
    """Embedding response."""
    embedding: list[float]
    dimension: int
    model: str


class BatchEmbeddingResponse(BaseModel):
    """Batch embedding response."""
    embeddings: list[list[float]]
    dimension: int
    model: str
    count: int


class SimilaritySearchRequest(BaseModel):
    """Similarity search request."""
    query: str = Field(min_length=1)
    resource_type: str | None = None  # policy, document, etc.
    limit: int = Field(default=10, le=100)
    threshold: float = Field(default=0.7, ge=0, le=1)


class SimilarityResult(BaseModel):
    """Similarity search result."""
    id: str
    resource_type: str
    title: str
    score: float
    metadata: dict | None = None


@router.post("/generate", response_model=EmbeddingResponse)
async def generate_embedding(request: GenerateEmbeddingRequest):
    """Generate embedding for text."""
    if not settings.AI_SEMANTIC_SEARCH:
        raise HTTPException(status_code=404, detail="Semantic search feature disabled")
    
    try:
        service = EmbeddingService()
        embedding = await service.generate_embedding(request.text)
        
        return EmbeddingResponse(
            embedding=embedding,
            dimension=len(embedding),
            model=settings.EMBEDDING_MODEL,
        )
    except Exception as e:
        logger.exception(f"Error generating embedding: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch", response_model=BatchEmbeddingResponse)
async def batch_generate_embeddings(request: BatchEmbeddingRequest):
    """Generate embeddings for multiple texts."""
    if not settings.AI_SEMANTIC_SEARCH:
        raise HTTPException(status_code=404, detail="Semantic search feature disabled")
    
    try:
        service = EmbeddingService()
        embeddings = await service.batch_generate(request.texts)
        
        return BatchEmbeddingResponse(
            embeddings=embeddings,
            dimension=len(embeddings[0]) if embeddings else 0,
            model=settings.EMBEDDING_MODEL,
            count=len(embeddings),
        )
    except Exception as e:
        logger.exception(f"Error generating embeddings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=list[SimilarityResult])
async def similarity_search(request: SimilaritySearchRequest):
    """Search for similar content using embeddings."""
    if not settings.AI_SEMANTIC_SEARCH:
        raise HTTPException(status_code=404, detail="Semantic search feature disabled")
    
    try:
        service = EmbeddingService()
        results = await service.find_similar(
            query=request.query,
            resource_type=request.resource_type,
            limit=request.limit,
            threshold=request.threshold,
        )
        
        return [SimilarityResult(**r) for r in results]
    except Exception as e:
        logger.exception(f"Error in similarity search: {e}")
        raise HTTPException(status_code=500, detail=str(e))
