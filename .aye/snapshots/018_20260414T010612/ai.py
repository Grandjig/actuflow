"""AI API Routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from app.dependencies import CurrentUser, DBSession
from app.models.user import User
from app.models.ai_query_log import AIQueryLog
from app.services.ai_service import AIService, AIServiceUnavailable
from app.schemas.common import PaginatedResponse

router = APIRouter()


class NaturalLanguageQueryRequest(BaseModel):
    """Natural language query request."""
    query: str = Field(min_length=1, max_length=1000)
    context: dict | None = None


class NaturalLanguageQueryResponse(BaseModel):
    """Natural language query response."""
    intent: str
    entities: dict
    confidence: float
    suggested_action: dict | None
    raw_interpretation: str
    query_id: UUID | None = None


class QueryFeedbackRequest(BaseModel):
    """Feedback on query result."""
    was_helpful: bool
    feedback_text: str | None = None


class GenerateNarrativeRequest(BaseModel):
    """Narrative generation request."""
    template: str
    data: dict
    max_length: int = 500
    tone: str = "professional"


class NarrativeResponse(BaseModel):
    """Generated narrative response."""
    text: str
    template: str
    ai_generated: bool = True


class SemanticSearchRequest(BaseModel):
    """Semantic search request."""
    query: str
    resource_type: str | None = None
    limit: int = 10


class SemanticSearchResult(BaseModel):
    """Semantic search result."""
    id: str
    resource_type: str
    title: str
    score: float


@router.get("/features")
async def get_ai_features(
    current_user: CurrentUser,
):
    """Get enabled AI features."""
    ai_service = AIService()
    return await ai_service.get_features()


@router.get("/health")
async def check_ai_health(
    current_user: CurrentUser,
):
    """Check AI service health."""
    ai_service = AIService()
    is_healthy = await ai_service.health_check()
    return {"healthy": is_healthy}


@router.post("/query", response_model=NaturalLanguageQueryResponse)
async def natural_language_query(
    request: NaturalLanguageQueryRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """Process a natural language query."""
    import time
    start_time = time.time()
    
    ai_service = AIService()
    
    try:
        result = await ai_service.parse_natural_language_query(
            request.query,
            request.context,
        )
        
        response_time = int((time.time() - start_time) * 1000)
        
        # Log the query
        query_log = AIQueryLog(
            user_id=current_user.id,
            query_text=request.query,
            interpreted_intent=result,
            executed_action=result.get("suggested_action"),
            was_successful=True,
            response_time_ms=response_time,
        )
        db.add(query_log)
        await db.flush()
        
        return NaturalLanguageQueryResponse(
            intent=result["intent"],
            entities=result["entities"],
            confidence=result["confidence"],
            suggested_action=result.get("suggested_action"),
            raw_interpretation=result["raw_interpretation"],
            query_id=query_log.id,
        )
        
    except AIServiceUnavailable as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.post("/query/{query_id}/feedback")
async def submit_query_feedback(
    query_id: UUID,
    request: QueryFeedbackRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """Submit feedback on a query result."""
    from sqlalchemy import select
    
    result = await db.execute(
        select(AIQueryLog).where(AIQueryLog.id == query_id)
    )
    query_log = result.scalar_one_or_none()
    
    if not query_log:
        raise HTTPException(status_code=404, detail="Query not found")
    
    if query_log.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot provide feedback on another user's query")
    
    query_log.was_helpful = request.was_helpful
    query_log.feedback_text = request.feedback_text
    
    await db.flush()
    
    return {"message": "Feedback recorded"}


@router.get("/query-history")
async def get_query_history(
    db: DBSession,
    current_user: CurrentUser,
    limit: int = Query(20, le=100),
):
    """Get user's query history."""
    from sqlalchemy import select
    
    result = await db.execute(
        select(AIQueryLog)
        .where(AIQueryLog.user_id == current_user.id)
        .order_by(AIQueryLog.created_at.desc())
        .limit(limit)
    )
    
    queries = result.scalars().all()
    
    return [
        {
            "id": str(q.id),
            "query": q.query_text,
            "intent": q.interpreted_intent.get("intent") if q.interpreted_intent else None,
            "was_helpful": q.was_helpful,
            "created_at": q.created_at,
        }
        for q in queries
    ]


@router.post("/generate-narrative", response_model=NarrativeResponse)
async def generate_narrative(
    request: GenerateNarrativeRequest,
    current_user: CurrentUser,
):
    """Generate narrative text from structured data."""
    ai_service = AIService()
    
    try:
        result = await ai_service.generate_narrative(
            template=request.template,
            data=request.data,
            max_length=request.max_length,
            tone=request.tone,
        )
        
        return NarrativeResponse(
            text=result["text"],
            template=request.template,
        )
        
    except AIServiceUnavailable as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.post("/search", response_model=list[SemanticSearchResult])
async def semantic_search(
    request: SemanticSearchRequest,
    current_user: CurrentUser,
):
    """Search using semantic similarity."""
    ai_service = AIService()
    
    try:
        results = await ai_service.semantic_search(
            query=request.query,
            resource_type=request.resource_type,
            limit=request.limit,
        )
        
        return [SemanticSearchResult(**r) for r in results]
        
    except AIServiceUnavailable as e:
        raise HTTPException(status_code=503, detail=str(e))
