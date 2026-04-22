"""Document Extraction Service."""

import io
import logging
import os
import re
from typing import Any

from PIL import Image
import pytesseract

from config import settings
from models.entity_extractor import EntityExtractor

logger = logging.getLogger(__name__)


class ExtractionService:
    """Service for document extraction (OCR + entity extraction)."""
    
    def __init__(self):
        self.entity_extractor = EntityExtractor()
        pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
    
    async def extract_document(
        self,
        file_path: str,
        filename: str,
        document_type: str | None = None,
    ) -> dict:
        """Extract text and entities from a document."""
        # Determine file type
        ext = os.path.splitext(filename)[1].lower()
        
        if ext == ".pdf":
            raw_text, page_count = await self._extract_pdf(file_path)
        elif ext in [".png", ".jpg", ".jpeg", ".tiff", ".tif"]:
            raw_text = await self._extract_image(file_path)
            page_count = 1
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        
        # Extract entities
        entities = self.entity_extractor.extract(raw_text)
        
        # Convert to list of entity objects
        entity_list = []
        for entity_type, value in entities.items():
            if isinstance(value, list):
                for v in value:
                    entity_list.append({
                        "entity_type": entity_type,
                        "value": str(v),
                        "confidence": 0.8,
                        "location": None,
                    })
            else:
                entity_list.append({
                    "entity_type": entity_type,
                    "value": str(value),
                    "confidence": 0.8,
                    "location": None,
                })
        
        # Generate structured data
        structured_data = await self._generate_structured_data(
            raw_text, entities, document_type
        )
        
        # Calculate confidence
        confidence = self._calculate_confidence(raw_text, entity_list)
        
        # Generate warnings
        warnings = self._generate_warnings(raw_text, entity_list)
        
        return {
            "raw_text": raw_text,
            "entities": entity_list,
            "structured_data": structured_data,
            "page_count": page_count,
            "confidence_score": confidence,
            "warnings": warnings,
        }
    
    async def _extract_pdf(self, file_path: str) -> tuple[str, int]:
        """Extract text from PDF."""
        try:
            from pdf2image import convert_from_path
            
            # Convert PDF pages to images
            pages = convert_from_path(file_path, dpi=300)
            
            texts = []
            for page in pages:
                text = pytesseract.image_to_string(
                    page,
                    lang=settings.OCR_LANGUAGE,
                )
                texts.append(text)
            
            return "\n\n".join(texts), len(pages)
            
        except Exception as e:
            logger.exception(f"PDF extraction failed: {e}")
            raise
    
    async def _extract_image(self, file_path: str) -> str:
        """Extract text from image."""
        try:
            image = Image.open(file_path)
            
            text = pytesseract.image_to_string(
                image,
                lang=settings.OCR_LANGUAGE,
            )
            
            return text
            
        except Exception as e:
            logger.exception(f"Image extraction failed: {e}")
            raise
    
    async def _generate_structured_data(
        self,
        raw_text: str,
        entities: dict,
        document_type: str | None,
    ) -> dict:
        """Generate structured data from extracted content."""
        structured = {}
        
        # Map entities to structured fields based on document type
        if document_type == "application":
            structured = {
                "applicant_name": entities.get("person_name"),
                "date_of_birth": entities.get("date"),
                "sum_assured": entities.get("amount"),
                "policy_type": None,  # Would need more sophisticated extraction
            }
        elif document_type == "policy_schedule":
            structured = {
                "policy_number": entities.get("policy_number"),
                "policyholder_name": entities.get("person_name"),
                "effective_date": entities.get("date"),
                "sum_assured": entities.get("amount"),
                "premium_amount": None,
            }
        elif document_type == "claim_form":
            structured = {
                "claim_number": entities.get("claim_number"),
                "policy_number": entities.get("policy_number"),
                "claim_date": entities.get("date"),
                "claim_amount": entities.get("amount"),
                "claimant_name": entities.get("person_name"),
            }
        else:
            # Generic extraction
            structured = {k: v for k, v in entities.items()}
        
        return structured
    
    def _calculate_confidence(self, text: str, entities: list) -> float:
        """Calculate overall extraction confidence."""
        if not text.strip():
            return 0.0
        
        # Factors affecting confidence
        factors = []
        
        # Text length factor
        if len(text) > 100:
            factors.append(0.9)
        elif len(text) > 50:
            factors.append(0.7)
        else:
            factors.append(0.4)
        
        # Entity extraction factor
        if len(entities) > 3:
            factors.append(0.9)
        elif len(entities) > 1:
            factors.append(0.7)
        else:
            factors.append(0.5)
        
        # Character quality factor (OCR noise indicator)
        weird_chars = len(re.findall(r'[^\w\s.,;:!?@#$%&*()-+=]', text))
        char_ratio = weird_chars / max(len(text), 1)
        if char_ratio < 0.05:
            factors.append(0.9)
        elif char_ratio < 0.1:
            factors.append(0.7)
        else:
            factors.append(0.4)
        
        return sum(factors) / len(factors)
    
    def _generate_warnings(self, text: str, entities: list) -> list[str]:
        """Generate warnings about extraction quality."""
        warnings = []
        
        if len(text) < 50:
            warnings.append("Extracted text is very short. Document may not have been processed correctly.")
        
        if not entities:
            warnings.append("No entities were extracted. Manual review recommended.")
        
        # Check for common OCR issues
        if re.search(r'[Il1|]{5,}', text):
            warnings.append("Possible OCR confusion between similar characters (I, l, 1, |).")
        
        if re.search(r'[O0]{5,}', text):
            warnings.append("Possible OCR confusion between O and 0.")
        
        return warnings
    
    async def extract_table(
        self,
        image_bytes: bytes,
        expected_columns: list[str] | None = None,
    ) -> dict:
        """Extract tabular data from an image."""
        try:
            image = Image.open(io.BytesIO(image_bytes))
            
            # Use pytesseract to get data with bounding boxes
            data = pytesseract.image_to_data(
                image,
                output_type=pytesseract.Output.DICT,
                lang=settings.OCR_LANGUAGE,
            )
            
            # Simple table reconstruction
            # Group text by line (similar top coordinate)
            lines = {}
            for i, text in enumerate(data['text']):
                if text.strip():
                    top = data['top'][i]
                    # Round to group nearby texts
                    line_key = top // 20 * 20
                    if line_key not in lines:
                        lines[line_key] = []
                    lines[line_key].append({
                        'text': text,
                        'left': data['left'][i],
                    })
            
            # Sort lines by position
            sorted_lines = sorted(lines.items())
            
            rows = []
            for _, line_items in sorted_lines:
                # Sort items in line by horizontal position
                sorted_items = sorted(line_items, key=lambda x: x['left'])
                row = [item['text'] for item in sorted_items]
                rows.append(row)
            
            # First row as headers (or use expected columns)
            if rows:
                if expected_columns:
                    headers = expected_columns
                else:
                    headers = rows[0] if rows else []
                    rows = rows[1:] if len(rows) > 1 else []
            else:
                headers = expected_columns or []
            
            # Normalize row lengths
            max_cols = len(headers) if headers else max(len(r) for r in rows) if rows else 0
            normalized_rows = []
            for row in rows:
                if len(row) < max_cols:
                    row = row + [''] * (max_cols - len(row))
                elif len(row) > max_cols:
                    row = row[:max_cols]
                normalized_rows.append(row)
            
            return {
                "headers": headers,
                "rows": normalized_rows,
                "confidence": 0.7,  # Table extraction is tricky
            }
            
        except Exception as e:
            logger.exception(f"Table extraction failed: {e}")
            raise
