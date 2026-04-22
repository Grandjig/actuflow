"""Document Extraction API Routes."""

import base64
import logging
import tempfile
from typing import Any

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from config import settings
from services.extraction_service import ExtractionService

logger = logging.getLogger(__name__)
router = APIRouter()


class ExtractedEntity(BaseModel):
    """Extracted entity from document."""
    entity_type: str  # policy_number, date, amount, name, address
    value: str
    confidence: float
    location: dict | None = None  # Page, bounding box


class DocumentExtractionResult(BaseModel):
    """Document extraction result."""
    raw_text: str
    entities: list[ExtractedEntity]
    structured_data: dict
    page_count: int
    confidence_score: float
    warnings: list[str] = []


class TableExtractionRequest(BaseModel):
    """Table extraction from image request."""
    image_base64: str
    expected_columns: list[str] | None = None


class ExtractedTable(BaseModel):
    """Extracted table data."""
    headers: list[str]
    rows: list[list[str]]
    confidence: float


class Base64DocumentRequest(BaseModel):
    """Document as base64 for extraction."""
    content_base64: str
    filename: str
    document_type: str | None = None  # application, policy_schedule, claim_form


@router.post("/document", response_model=DocumentExtractionResult)
async def extract_document(file: UploadFile = File(...)):
    """Extract text and entities from an uploaded document."""
    if not settings.AI_DOCUMENT_EXTRACTION:
        raise HTTPException(status_code=404, detail="Document extraction feature disabled")
    
    # Validate file type
    allowed_types = [
        "application/pdf",
        "image/png",
        "image/jpeg",
        "image/tiff",
    ]
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {allowed_types}",
        )
    
    try:
        service = ExtractionService()
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=_get_suffix(file.filename)) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        result = await service.extract_document(tmp_path, file.filename)
        
        return DocumentExtractionResult(**result)
        
    except Exception as e:
        logger.exception(f"Error extracting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/document-base64", response_model=DocumentExtractionResult)
async def extract_document_base64(request: Base64DocumentRequest):
    """Extract from base64-encoded document."""
    if not settings.AI_DOCUMENT_EXTRACTION:
        raise HTTPException(status_code=404, detail="Document extraction feature disabled")
    
    try:
        service = ExtractionService()
        
        # Decode and save to temp
        content = base64.b64decode(request.content_base64)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=_get_suffix(request.filename)) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        
        result = await service.extract_document(
            tmp_path,
            request.filename,
            request.document_type,
        )
        
        return DocumentExtractionResult(**result)
        
    except Exception as e:
        logger.exception(f"Error extracting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/table", response_model=ExtractedTable)
async def extract_table(request: TableExtractionRequest):
    """Extract tabular data from an image."""
    if not settings.AI_DOCUMENT_EXTRACTION:
        raise HTTPException(status_code=404, detail="Document extraction feature disabled")
    
    try:
        service = ExtractionService()
        
        # Decode image
        image_bytes = base64.b64decode(request.image_base64)
        
        result = await service.extract_table(
            image_bytes,
            request.expected_columns,
        )
        
        return ExtractedTable(**result)
        
    except Exception as e:
        logger.exception(f"Error extracting table: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _get_suffix(filename: str | None) -> str:
    """Get file suffix from filename."""
    if not filename:
        return ".pdf"
    if "." in filename:
        return "." + filename.rsplit(".", 1)[-1].lower()
    return ".pdf"
