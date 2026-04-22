"""Import Service.

Handles data import operations.
"""

import uuid
import csv
import io
from datetime import datetime
from typing import Any, Optional

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.data_import import DataImport
from app.services.ai_service import AIService, AIServiceUnavailable
from app.config import settings


class ImportService:
    """Service for data import operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def upload_file(
        self,
        file: UploadFile,
        import_type: str,
        uploaded_by: uuid.UUID,
    ) -> dict[str, Any]:
        """Process an uploaded file."""
        # Read file content
        content = await file.read()
        
        # Parse file
        if file.filename.endswith('.csv'):
            columns, sample_data, total_rows = self._parse_csv(content)
        else:
            # TODO: Handle Excel files
            columns = []
            sample_data = []
            total_rows = 0
        
        # Create import record
        data_import = DataImport(
            file_name=file.filename,
            import_type=import_type,
            status="uploaded",
            total_rows=total_rows,
            uploaded_by_id=uploaded_by,
        )
        self.db.add(data_import)
        await self.db.flush()
        await self.db.refresh(data_import)
        
        # Get AI suggestions if enabled
        ai_suggestions = None
        if settings.AI_ENABLED:
            ai_suggestions = await self._get_ai_suggestions(
                import_type, columns, sample_data
            )
            data_import.ai_suggested_mapping = ai_suggestions.get("column_mappings")
            data_import.ai_data_issues = ai_suggestions.get("data_issues")
            await self.db.flush()
        
        return {
            "import_id": str(data_import.id),
            "file_name": file.filename,
            "total_rows": total_rows,
            "columns": columns,
            "sample_data": sample_data[:5],
            "ai_suggestions": ai_suggestions,
        }
    
    def _parse_csv(self, content: bytes) -> tuple[list[str], list[dict], int]:
        """Parse CSV content."""
        text = content.decode('utf-8')
        reader = csv.DictReader(io.StringIO(text))
        
        columns = reader.fieldnames or []
        rows = list(reader)
        sample_data = rows[:10]  # First 10 rows
        total_rows = len(rows)
        
        return columns, sample_data, total_rows
    
    async def _get_ai_suggestions(
        self,
        import_type: str,
        columns: list[str],
        sample_data: list[dict],
    ) -> dict[str, Any]:
        """Get AI-generated suggestions for column mapping."""
        try:
            ai_service = AIService()
            return await ai_service.get_import_suggestions(
                import_type=import_type,
                columns=columns,
                sample_data=sample_data[:5],
            )
        except AIServiceUnavailable:
            return {"column_mappings": [], "data_issues": []}
    
    async def validate(self, import_id: uuid.UUID) -> dict[str, Any]:
        """Validate import data."""
        result = await self.db.execute(
            select(DataImport).where(DataImport.id == import_id)
        )
        data_import = result.scalar_one_or_none()
        
        if not data_import:
            raise ValueError("Import not found")
        
        # TODO: Implement validation logic based on import type
        # For now, return mock validation result
        
        data_import.status = "validated"
        await self.db.flush()
        
        return {
            "is_valid": True,
            "total_rows": data_import.total_rows or 0,
            "valid_rows": (data_import.total_rows or 0) - 3,
            "error_rows": 3,
            "errors": [],
        }
