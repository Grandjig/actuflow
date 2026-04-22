"""AI API Routes."""

import uuid
from typing import Annotated, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.dependencies import get_current_user
from app.models.user import User
from app.models.ai_query_log import AIQueryLog
from app.services.ai_service import AIService, AIServiceUnavailable
from app.config import settings

router = APIRouter()


class NLQueryRequest(BaseModel):
    query: str
    context: Optional[dict] = None


class NLQueryResponse(BaseModel):
    query: str
    parsed_intent: dict
    explanation: str
    result_count: Optional[int] = None
    suggested_api_call: Optional[dict] = None


class NarrativeRequest(BaseModel):
    template: str
    data: dict
    max_length: int = 500
    tone: str = "professional"


class NarrativeResponse(BaseModel):
    text: str
    generated_at: Optional[str] = None


class SemanticSearchRequest(BaseModel):
    query: str
    resource_type: Optional[str] = None
    limit: int = 10


@router.get("/status")
async def get_ai_status():
    """Get AI service status."""
    if not settings.AI_ENABLED:
        return {
            "enabled": False,
            "healthy": False,
            "features": {},
        }
    
    ai_service = AIService()
    healthy = await ai_service.health_check()
    
    return {
        "enabled": True,
        "healthy": healthy,
        "features": {
            "natural_language": True,
            "anomaly_detection": True,
            "narrative_generation": True,
            "semantic_search": True,
            "document_extraction": True,
        },
    }


@router.post("/query", response_model=NLQueryResponse)
async def process_natural_language_query(
    request: NLQueryRequest,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Process a natural language query."""
    if not settings.AI_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI features are disabled",
        )
    
    ai_service = AIService()
    
    try:
        result = await ai_service.parse_natural_language_query(
            query=request.query,
            context=request.context,
        )
        
        # Log the query
        query_log = AIQueryLog(
            user_id=current_user.id,
            query_text=request.query,
            interpreted_intent=result.get("parsed_intent"),
            executed_action=result.get("suggested_api_call"),
        )
        db.add(query_log)
        
        return NLQueryResponse(
            query=request.query,
            parsed_intent=result.get("parsed_intent", {}),
            explanation=result.get("explanation", ""),
            result_count=result.get("result_count"),
            suggested_api_call=result.get("suggested_api_call"),
        )
    except AIServiceUnavailable as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )


@router.post("/narrative", response_model=NarrativeResponse)
async def generate_narrative(
    request: NarrativeRequest,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Generate narrative text from data."""
    if not settings.AI_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI features are disabled",
        )
    
    ai_service = AIService()
    
    try:
        result = await ai_service.generate_narrative(
            template=request.template,
            data=request.data,
            max_length=request.max_length,
            tone=request.tone,
        )
        
        return NarrativeResponse(
            text=result.get("text", ""),
            generated_at=datetime.utcnow().isoformat(),
        )
    except AIServiceUnavailable as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )


@router.post("/search")
async def semantic_search(
    request: SemanticSearchRequest,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Perform semantic search."""
    if not settings.AI_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI features are disabled",
        )
    
    ai_service = AIService()
    
    try:
        results = await ai_service.semantic_search(
            query=request.query,
            resource_type=request.resource_type,
            limit=request.limit,
        )
        
        return {
            "results": results,
            "total": len(results),
        }
    except AIServiceUnavailable as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )


@router.get("/query-history")
async def get_query_history(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(get_current_user)],
    limit: int = 10,
):
    """Get user's AI query history."""
    result = await db.execute(
        select(AIQueryLog)
        .where(AIQueryLog.user_id == current_user.id)
        .order_by(AIQueryLog.timestamp.desc())
        .limit(limit)
    )
    queries = result.scalars().all()
    
    return [
        {
            "id": str(q.id),
            "query": q.query_text,
            "timestamp": q.timestamp.isoformat(),
        }
        for q in queries
    ]


@router.post("/query/{query_id}/feedback")
async def submit_query_feedback(
    query_id: uuid.UUID,
    was_helpful: bool,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Submit feedback on an AI query result."""
    result = await db.execute(
        select(AIQueryLog).where(
            AIQueryLog.id == query_id,
            AIQueryLog.user_id == current_user.id,
        )
    )
    query_log = result.scalar_one_or_none()
    
    if not query_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Query not found",
        )
    
    query_log.was_helpful = was_helpful
    await db.flush()
    
    return {"success": True}
