"""Embedding Service."""

import hashlib
import json
import logging
from typing import Any

import numpy as np

from config import settings

logger = logging.getLogger(__name__)

# Global model instance (loaded once)
_embedding_model = None


class EmbeddingService:
    """Service for text embeddings and semantic search."""
    
    def __init__(self):
        self._model = None
    
    def _load_model(self):
        """Load the embedding model."""
        global _embedding_model
        
        if _embedding_model is not None:
            self._model = _embedding_model
            return
        
        if settings.USE_LOCAL_EMBEDDINGS:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
            _embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
            self._model = _embedding_model
        else:
            # Will use OpenAI API
            self._model = None
    
    async def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        if settings.USE_LOCAL_EMBEDDINGS:
            return await self._local_embedding(text)
        else:
            return await self._openai_embedding(text)
    
    async def batch_generate(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        if settings.USE_LOCAL_EMBEDDINGS:
            return await self._local_batch_embedding(texts)
        else:
            return await self._openai_batch_embedding(texts)
    
    async def _local_embedding(self, text: str) -> list[float]:
        """Generate embedding using local model."""
        if self._model is None:
            self._load_model()
        
        embedding = self._model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    async def _local_batch_embedding(self, texts: list[str]) -> list[list[float]]:
        """Generate batch embeddings using local model."""
        if self._model is None:
            self._load_model()
        
        embeddings = self._model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
    
    async def _openai_embedding(self, text: str) -> list[float]:
        """Generate embedding using OpenAI API."""
        import openai
        
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        response = client.embeddings.create(
            input=text,
            model=settings.OPENAI_EMBEDDING_MODEL,
        )
        
        return response.data[0].embedding
    
    async def _openai_batch_embedding(self, texts: list[str]) -> list[list[float]]:
        """Generate batch embeddings using OpenAI API."""
        import openai
        
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        response = client.embeddings.create(
            input=texts,
            model=settings.OPENAI_EMBEDDING_MODEL,
        )
        
        return [item.embedding for item in response.data]
    
    async def find_similar(
        self,
        query: str,
        resource_type: str | None = None,
        limit: int = 10,
        threshold: float = 0.7,
    ) -> list[dict]:
        """Find similar content using vector similarity."""
        # Generate query embedding
        query_embedding = await self.generate_embedding(query)
        
        # Search in database using pgvector
        results = await self._vector_search(
            query_embedding,
            resource_type,
            limit,
            threshold,
        )
        
        return results
    
    async def _vector_search(
        self,
        embedding: list[float],
        resource_type: str | None,
        limit: int,
        threshold: float,
    ) -> list[dict]:
        """Search using pgvector in database."""
        from sqlalchemy import create_engine, text
        
        engine = create_engine(settings.DATABASE_URL)
        
        # Build query based on resource type
        if resource_type == "policy":
            query = text("""
                SELECT id::text, 'policy' as resource_type, policy_number as title,
                       1 - (embedding <=> :embedding) as score
                FROM policies
                WHERE embedding IS NOT NULL
                  AND 1 - (embedding <=> :embedding) > :threshold
                ORDER BY embedding <=> :embedding
                LIMIT :limit
            """)
        elif resource_type == "document":
            query = text("""
                SELECT id::text, 'document' as resource_type, file_name as title,
                       1 - (embedding <=> :embedding) as score
                FROM documents
                WHERE embedding IS NOT NULL
                  AND 1 - (embedding <=> :embedding) > :threshold
                ORDER BY embedding <=> :embedding
                LIMIT :limit
            """)
        else:
            # Search across multiple tables
            query = text("""
                SELECT * FROM (
                    SELECT id::text, 'policy' as resource_type, policy_number as title,
                           1 - (embedding <=> :embedding) as score
                    FROM policies
                    WHERE embedding IS NOT NULL
                    UNION ALL
                    SELECT id::text, 'document' as resource_type, file_name as title,
                           1 - (embedding <=> :embedding) as score
                    FROM documents
                    WHERE embedding IS NOT NULL
                ) combined
                WHERE score > :threshold
                ORDER BY score DESC
                LIMIT :limit
            """)
        
        try:
            with engine.connect() as conn:
                # Convert embedding to pgvector format
                embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"
                
                result = conn.execute(
                    query,
                    {
                        "embedding": embedding_str,
                        "threshold": threshold,
                        "limit": limit,
                    }
                )
                
                results = []
                for row in result:
                    results.append({
                        "id": row.id,
                        "resource_type": row.resource_type,
                        "title": row.title,
                        "score": float(row.score),
                        "metadata": None,
                    })
                
                return results
                
        except Exception as e:
            logger.warning(f"Vector search failed (might not have embeddings): {e}")
            return []
    
    def cosine_similarity(self, a: list[float], b: list[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        a_np = np.array(a)
        b_np = np.array(b)
        return float(np.dot(a_np, b_np) / (np.linalg.norm(a_np) * np.linalg.norm(b_np)))
