"""Document Service."""

import base64
import logging
from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import NotFoundError
from app.models.document import Document
from app.models.user import User
from app.services.ai_service import AIService, AIServiceUnavailable

logger = logging.getLogger(__name__)


class DocumentService:
    """Service for document operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ai_service = AIService()
    
    async def get_document(self, document_id: UUID) -> Document | None:
        """Get a document by ID."""
        result = await self.db.execute(
            select(Document)
            .where(Document.id == document_id)
            .where(Document.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    async def list_documents(
        self,
        offset: int = 0,
        limit: int = 20,
        document_type: str | None = None,
        related_resource_type: str | None = None,
        related_resource_id: UUID | None = None,
    ) -> tuple[list[Document], int]:
        """List documents with filtering."""
        query = select(Document).where(Document.is_deleted == False)
        
        if document_type:
            query = query.where(Document.document_type == document_type)
        if related_resource_type:
            query = query.where(Document.related_resource_type == related_resource_type)
        if related_resource_id:
            query = query.where(Document.related_resource_id == related_resource_id)
        
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0
        
        query = query.order_by(Document.created_at.desc()).offset(offset).limit(limit)
        
        result = await self.db.execute(query)
        documents = list(result.scalars().all())
        
        return documents, total
    
    async def upload_document(
        self,
        file_name: str,
        file_path: str,
        file_size: int,
        content_type: str,
        uploaded_by: User,
        document_type: str | None = None,
        related_resource_type: str | None = None,
        related_resource_id: UUID | None = None,
    ) -> Document:
        """Upload a document."""
        document = Document(
            file_name=file_name,
            file_path=file_path,
            file_size=file_size,
            content_type=content_type,
            document_type=document_type,
            related_resource_type=related_resource_type,
            related_resource_id=related_resource_id,
            uploaded_by_id=uploaded_by.id,
        )
        
        self.db.add(document)
        await self.db.flush()
        await self.db.refresh(document)
        
        return document
    
    async def extract_document_data(
        self,
        document: Document,
        file_content: bytes,
    ) -> Document:
        """Extract data from document using AI."""
        try:
            content_base64 = base64.b64encode(file_content).decode("utf-8")
            
            result = await self.ai_service.extract_document_data(
                content_base64=content_base64,
                filename=document.file_name,
                document_type=document.document_type,
            )
            
            document.extracted_text = result.get("raw_text")
            document.extracted_data = result.get("structured_data")
            document.extraction_confidence = result.get("confidence_score")
            document.extraction_warnings = result.get("warnings")
            document.page_count = result.get("page_count")
            
            # Generate embedding for semantic search
            if document.extracted_text:
                try:
                    embedding = await self.ai_service.generate_embedding(
                        document.extracted_text[:5000]
                    )
                    if hasattr(document, 'embedding'):
                        document.embedding = embedding
                except Exception as e:
                    logger.warning(f"Failed to generate embedding: {e}")
            
            await self.db.flush()
            await self.db.refresh(document)
            
        except AIServiceUnavailable as e:
            logger.warning(f"AI extraction unavailable: {e}")
        
        return document
    
    async def search_documents(
        self,
        query: str,
        limit: int = 10,
    ) -> list[dict]:
        """Search documents using semantic search."""
        try:
            results = await self.ai_service.semantic_search(
                query=query,
                resource_type="document",
                limit=limit,
            )
            return results
        except AIServiceUnavailable:
            # Fallback to keyword search
            result = await self.db.execute(
                select(Document)
                .where(Document.is_deleted == False)
                .where(Document.file_name.ilike(f"%{query}%"))
                .limit(limit)
            )
            return [
                {
                    "id": str(d.id),
                    "resource_type": "document",
                    "title": d.file_name,
                    "score": 1.0,
                }
                for d in result.scalars()
            ]
    
    async def delete_document(self, document: Document) -> None:
        """Soft delete a document."""
        document.is_deleted = True
        document.deleted_at = datetime.utcnow()
        await self.db.flush()
