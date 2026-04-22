"""
AI API Routes
=============

AI-powered features.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

from app.config import settings
from app.dependencies import DBSession, CurrentUser

router = APIRouter()


# Schemas
class NLQueryRequest(BaseModel):
    query: str
    context: Optional[dict] = None


class ParsedIntent(BaseModel):
    intent: str
    entity_type: Optional[str] = None
    filters: dict = {}
    clarification_needed: bool = False
    clarification_question: Optional[str] = None


class SuggestedAPICall(BaseModel):
    endpoint: str
    method: str
    params: dict


class NLQueryResponse(BaseModel):
    query: str
    parsed_intent: ParsedIntent
    explanation: str
    result_count: Optional[int] = None
    suggested_api_call: Optional[SuggestedAPICall] = None


class NarrativeRequest(BaseModel):
    template: str
    data: dict
    max_length: int = 500
    tone: str = "professional"


class NarrativeResponse(BaseModel):
    text: str
    tokens_used: Optional[int] = None


class FeedbackRequest(BaseModel):
    query_id: str
    helpful: bool
    comments: Optional[str] = None


@router.post("/query", response_model=NLQueryResponse)
async def natural_language_query(
    request: NLQueryRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """Process a natural language query."""
    if not settings.AI_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI features are not enabled",
        )

    # Simple keyword-based parsing for now
    query = request.query.lower()
    
    intent = "search"
    entity_type = None
    filters = {}
    
    # Detect entity type
    if "polic" in query:
        if "holder" in query:
            entity_type = "policyholder"
        else:
            entity_type = "policy"
    elif "claim" in query:
        entity_type = "claim"
    elif "assumption" in query:
        entity_type = "assumption_set"
    elif "calculation" in query or "run" in query:
        entity_type = "calculation"
    
    # Detect status filters
    if "active" in query:
        filters["status"] = "active"
    elif "lapsed" in query:
        filters["status"] = "lapsed"
    elif "pending" in query:
        filters["status"] = "pending_approval"
    elif "approved" in query:
        filters["status"] = "approved"
    
    # Build explanation
    explanation = f"Searching for {entity_type or 'all'} records"
    if filters:
        explanation += f" with filters: {filters}"
    
    # Build suggested API call
    endpoint_map = {
        "policy": "/api/v1/policies",
        "policyholder": "/api/v1/policyholders",
        "claim": "/api/v1/claims",
        "assumption_set": "/api/v1/assumption-sets",
        "calculation": "/api/v1/calculations",
    }
    
    suggested_api_call = None
    if entity_type and entity_type in endpoint_map:
        suggested_api_call = SuggestedAPICall(
            endpoint=endpoint_map[entity_type],
            method="GET",
            params=filters,
        )
    
    return NLQueryResponse(
        query=request.query,
        parsed_intent=ParsedIntent(
            intent=intent,
            entity_type=entity_type,
            filters=filters,
        ),
        explanation=explanation,
        suggested_api_call=suggested_api_call,
    )


@router.post("/narrative", response_model=NarrativeResponse)
async def generate_narrative(
    request: NarrativeRequest,
    current_user: CurrentUser,
):
    """Generate narrative text from structured data."""
    if not settings.AI_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI features are not enabled",
        )

    # TODO: Call AI service
    # For now, return a placeholder
    data = request.data
    
    if request.template == "calculation_summary":
        text = f"The calculation run processed {data.get('policy_count', 'N/A')} policies. "
        text += f"Total reserves calculated: ${data.get('total_reserves', 0):,.2f}."
    else:
        text = f"Summary for {request.template}: {data}"
    
    return NarrativeResponse(
        text=text,
        tokens_used=None,
    )


@router.post("/feedback")
async def submit_feedback(
    request: FeedbackRequest,
    current_user: CurrentUser,
):
    """Submit feedback on AI query results."""
    # TODO: Store feedback for model improvement
    return {"status": "received", "message": "Thank you for your feedback"}


@router.get("/status")
async def get_ai_status():
    """Get AI service status."""
    return {
        "enabled": settings.AI_ENABLED,
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
