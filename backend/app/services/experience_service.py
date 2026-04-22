"""Experience Analysis Service."""

import logging
from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.experience_analysis import ExperienceAnalysis, AnalysisType
from app.models.user import User
from app.services.ai_service import AIService, AIServiceUnavailable

logger = logging.getLogger(__name__)


class ExperienceService:
    """Service for experience analysis operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ai_service = AIService()
    
    async def get_analysis(self, analysis_id: UUID) -> ExperienceAnalysis | None:
        """Get an experience analysis by ID."""
        result = await self.db.execute(
            select(ExperienceAnalysis).where(ExperienceAnalysis.id == analysis_id)
        )
        return result.scalar_one_or_none()
    
    async def list_analyses(
        self,
        offset: int = 0,
        limit: int = 20,
        analysis_type: str | None = None,
    ) -> tuple[list[ExperienceAnalysis], int]:
        """List experience analyses."""
        query = select(ExperienceAnalysis)
        
        if analysis_type:
            query = query.where(ExperienceAnalysis.analysis_type == analysis_type)
        
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0
        
        query = query.order_by(ExperienceAnalysis.created_at.desc())
        query = query.offset(offset).limit(limit)
        
        result = await self.db.execute(query)
        analyses = list(result.scalars().all())
        
        return analyses, total
    
    async def run_experience_study(
        self,
        name: str,
        analysis_type: str,
        study_period_start: date,
        study_period_end: date,
        parameters: dict,
        created_by: User,
        assumption_set_id: UUID | None = None,
    ) -> ExperienceAnalysis:
        """Run an experience study."""
        # Create analysis record
        analysis = ExperienceAnalysis(
            name=name,
            analysis_type=analysis_type,
            study_period_start=study_period_start,
            study_period_end=study_period_end,
            parameters=parameters,
            created_by_id=created_by.id,
            assumption_set_id=assumption_set_id,
        )
        
        self.db.add(analysis)
        await self.db.flush()
        
        # Run the study
        results = await self._calculate_experience(
            analysis_type,
            study_period_start,
            study_period_end,
            parameters,
        )
        
        analysis.results = results
        analysis.total_actual = results.get("total_actual", 0)
        analysis.total_expected = results.get("total_expected", 0)
        
        if analysis.total_expected > 0:
            analysis.ae_ratio = analysis.total_actual / analysis.total_expected
        
        # Generate AI recommendations
        try:
            recommendations = await self._generate_recommendations(analysis)
            analysis.ai_recommendations = recommendations
            
            # Generate narrative
            narrative_result = await self.ai_service.generate_narrative(
                template="executive_summary",
                data={
                    "type": "Experience Analysis",
                    "analysis_type": analysis_type,
                    "period": f"{study_period_start} to {study_period_end}",
                    "ae_ratio": analysis.ae_ratio,
                    "results": results,
                },
            )
            analysis.ai_narrative = narrative_result.get("text")
            
        except AIServiceUnavailable:
            logger.warning("AI service unavailable for recommendations")
        
        await self.db.flush()
        await self.db.refresh(analysis)
        
        return analysis
    
    async def _calculate_experience(
        self,
        analysis_type: str,
        start_date: date,
        end_date: date,
        parameters: dict,
    ) -> dict:
        """Calculate actual vs expected experience."""
        # This is a simplified placeholder
        # Real implementation would query policies/claims and calculate A/E
        
        if analysis_type == AnalysisType.MORTALITY.value:
            return await self._calculate_mortality_experience(
                start_date, end_date, parameters
            )
        elif analysis_type == AnalysisType.LAPSE.value:
            return await self._calculate_lapse_experience(
                start_date, end_date, parameters
            )
        else:
            return {
                "total_actual": 0,
                "total_expected": 0,
                "by_segment": [],
            }
    
    async def _calculate_mortality_experience(
        self,
        start_date: date,
        end_date: date,
        parameters: dict,
    ) -> dict:
        """Calculate mortality experience."""
        # Placeholder - would query death claims vs expected deaths
        from sqlalchemy import text
        
        # Get death claims in period
        claims_result = await self.db.execute(
            text("""
                SELECT COUNT(*) as count, COALESCE(SUM(settlement_amount), 0) as amount
                FROM claims
                WHERE claim_type = 'death'
                  AND claim_date BETWEEN :start AND :end
                  AND is_deleted = false
            """),
            {"start": start_date, "end": end_date},
        )
        claims_row = claims_result.fetchone()
        actual_count = claims_row.count if claims_row else 0
        actual_amount = float(claims_row.amount) if claims_row else 0
        
        # Expected would come from applying mortality rates to exposure
        # This is a simplified placeholder
        expected_amount = actual_amount * 0.95  # Placeholder
        
        return {
            "total_actual": actual_amount,
            "total_expected": expected_amount,
            "actual_count": actual_count,
            "by_age_band": [],  # Would be populated with detailed breakdown
            "by_gender": [],
        }
    
    async def _calculate_lapse_experience(
        self,
        start_date: date,
        end_date: date,
        parameters: dict,
    ) -> dict:
        """Calculate lapse experience."""
        from sqlalchemy import text
        
        # Get lapsed policies in period
        lapse_result = await self.db.execute(
            text("""
                SELECT COUNT(*) as count
                FROM policies
                WHERE status = 'lapsed'
                  AND updated_at BETWEEN :start AND :end
                  AND is_deleted = false
            """),
            {"start": start_date, "end": end_date},
        )
        lapse_row = lapse_result.fetchone()
        actual_lapses = lapse_row.count if lapse_row else 0
        
        # Expected lapses (placeholder)
        expected_lapses = actual_lapses * 0.9
        
        return {
            "total_actual": actual_lapses,
            "total_expected": expected_lapses,
            "by_duration": [],
            "by_product": [],
        }
    
    async def _generate_recommendations(
        self,
        analysis: ExperienceAnalysis,
    ) -> list[dict]:
        """Generate AI recommendations based on experience results."""
        recommendations = []
        
        if analysis.ae_ratio and analysis.ae_ratio > 1.1:
            recommendations.append({
                "type": "increase_assumption",
                "confidence": 0.8,
                "description": f"Actual experience is {(analysis.ae_ratio - 1) * 100:.1f}% higher than expected. Consider increasing the {analysis.analysis_type} assumption.",
                "suggested_factor": analysis.ae_ratio,
            })
        elif analysis.ae_ratio and analysis.ae_ratio < 0.9:
            recommendations.append({
                "type": "decrease_assumption",
                "confidence": 0.8,
                "description": f"Actual experience is {(1 - analysis.ae_ratio) * 100:.1f}% lower than expected. Consider decreasing the {analysis.analysis_type} assumption.",
                "suggested_factor": analysis.ae_ratio,
            })
        
        return recommendations
    
    async def get_recommendations(
        self,
        analysis_id: UUID,
    ) -> list[dict]:
        """Get recommendations for an analysis."""
        analysis = await self.get_analysis(analysis_id)
        if not analysis:
            return []
        
        return analysis.ai_recommendations or []
