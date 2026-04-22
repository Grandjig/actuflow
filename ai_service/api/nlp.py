"""NLP API Routes."""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from config import settings
from services.nlp_service import NLPService

logger = logging.getLogger(__name__)
router = APIRouter()


class ParseQueryRequest(BaseModel):
    """Natural language query request."""
    query: str = Field(min_length=1, max_length=1000)
    context: dict | None = None


class ParsedIntent(BaseModel):
    """Parsed intent from query."""
    intent: str  # search, filter, navigate, aggregate, report, explain
    entities: dict[str, Any]
    confidence: float
    suggested_action: dict | None = None
    raw_interpretation: str


class GenerateTextRequest(BaseModel):
    """Text generation request."""
    template: str  # calculation_summary, reserve_movement, variance_commentary
    data: dict
    max_length: int = 500
    tone: str = "professional"


class GeneratedText(BaseModel):
    """Generated text response."""
    text: str
    template: str
    tokens_used: int | None = None


class SuggestMappingRequest(BaseModel):
    """Column mapping suggestion request."""
    source_columns: list[str]
    sample_values: dict[str, list[Any]]
    target_type: str  # policy, policyholder, claim


class ColumnMapping(BaseModel):
    """Suggested column mapping."""
    source_column: str
    suggested_field: str
    confidence: float
    reason: str | None = None


class DataQualityIssue(BaseModel):
    """Detected data quality issue."""
    column: str
    issue_type: str  # missing, outlier, format, inconsistent
    description: str
    affected_rows: int
    suggestion: str | None = None


@router.post("/parse-query", response_model=ParsedIntent)
async def parse_query(request: ParseQueryRequest):
    """Parse a natural language query into structured intent."""
    if not settings.AI_NATURAL_LANGUAGE:
        raise HTTPException(status_code=404, detail="Natural language feature disabled")
    
    try:
        nlp_service = NLPService()
        result = await nlp_service.parse_user_query(request.query, request.context)
        return ParsedIntent(**result)
    except Exception as e:
        logger.exception(f"Error parsing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-text", response_model=GeneratedText)
async def generate_text(request: GenerateTextRequest):
    """Generate narrative text from structured data."""
    if not settings.AI_NARRATIVE_GENERATION:
        raise HTTPException(status_code=404, detail="Narrative generation feature disabled")
    
    try:
        nlp_service = NLPService()
        text, tokens = await nlp_service.generate_narrative(
            template=request.template,
            data=request.data,
            max_length=request.max_length,
            tone=request.tone,
        )
        return GeneratedText(
            text=text,
            template=request.template,
            tokens_used=tokens,
        )
    except Exception as e:
        logger.exception(f"Error generating text: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/suggest-mapping", response_model=list[ColumnMapping])
async def suggest_column_mapping(request: SuggestMappingRequest):
    """Suggest column mappings for data import."""
    if not settings.AI_SMART_IMPORT:
        raise HTTPException(status_code=404, detail="Smart import feature disabled")
    
    try:
        nlp_service = NLPService()
        mappings = await nlp_service.suggest_column_mapping(
            source_columns=request.source_columns,
            sample_values=request.sample_values,
            target_type=request.target_type,
        )
        return [ColumnMapping(**m) for m in mappings]
    except Exception as e:
        logger.exception(f"Error suggesting mappings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-data-quality", response_model=list[DataQualityIssue])
async def analyze_data_quality(data: dict):
    """Analyze data quality issues in import data."""
    if not settings.AI_SMART_IMPORT:
        raise HTTPException(status_code=404, detail="Smart import feature disabled")
    
    try:
        nlp_service = NLPService()
        issues = await nlp_service.analyze_data_quality(data)
        return [DataQualityIssue(**i) for i in issues]
    except Exception as e:
        logger.exception(f"Error analyzing data quality: {e}")
        raise HTTPException(status_code=500, detail=str(e))
