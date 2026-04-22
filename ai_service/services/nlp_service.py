"""NLP Service."""

import json
import logging
import re
from typing import Any

from config import settings
from services.llm_client import LLMClient
from models.intent_classifier import IntentClassifier
from models.entity_extractor import EntityExtractor

logger = logging.getLogger(__name__)


class NLPService:
    """Service for natural language processing."""
    
    def __init__(self):
        self.llm_client = LLMClient()
        self.intent_classifier = IntentClassifier()
        self.entity_extractor = EntityExtractor()
    
    async def parse_user_query(
        self,
        query: str,
        context: dict | None = None,
    ) -> dict:
        """Parse a natural language query into structured intent."""
        # First, classify intent using rules/ML
        intent = self.intent_classifier.classify(query)
        
        # Extract entities
        entities = self.entity_extractor.extract(query)
        
        # Use LLM to refine understanding
        suggested_action = await self._generate_suggested_action(query, intent, entities, context)
        
        # Raw interpretation
        raw_interpretation = self._format_interpretation(query, intent, entities)
        
        return {
            "intent": intent["type"],
            "entities": entities,
            "confidence": intent["confidence"],
            "suggested_action": suggested_action,
            "raw_interpretation": raw_interpretation,
        }
    
    async def _generate_suggested_action(
        self,
        query: str,
        intent: dict,
        entities: dict,
        context: dict | None,
    ) -> dict | None:
        """Use LLM to generate a specific action from the query."""
        prompt = f"""You are an assistant for an actuarial insurance platform. 
Convert the following user query into an API action.

User Query: {query}
Detected Intent: {intent['type']}
Extracted Entities: {json.dumps(entities)}
Context: {json.dumps(context) if context else 'None'}

Available actions:
1. search_policies: Search for policies with filters
2. search_policyholders: Search for policyholders
3. search_claims: Search for claims
4. get_calculation_results: Get calculation run results
5. navigate_to: Navigate to a specific page
6. generate_report: Generate a report
7. filter_data: Apply filters to current view

Respond with a JSON object containing:
- action: The action type
- parameters: The parameters for the action
- explanation: Brief explanation

If the query is unclear, set action to "clarify" and include a question in the explanation.

JSON Response:"""
        
        try:
            response = await self.llm_client.complete(
                prompt,
                max_tokens=500,
                temperature=0.1,
            )
            
            # Parse JSON from response
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            logger.warning(f"LLM action generation failed: {e}")
        
        # Fallback to rule-based action
        return self._rule_based_action(intent, entities)
    
    def _rule_based_action(self, intent: dict, entities: dict) -> dict:
        """Generate action from rules when LLM unavailable."""
        intent_type = intent["type"]
        
        if intent_type == "search":
            if "policy_number" in entities:
                return {
                    "action": "search_policies",
                    "parameters": {"policy_number": entities["policy_number"]},
                    "explanation": f"Search for policy {entities['policy_number']}",
                }
            elif "person_name" in entities:
                return {
                    "action": "search_policyholders",
                    "parameters": {"name": entities["person_name"]},
                    "explanation": f"Search for policyholder {entities['person_name']}",
                }
        elif intent_type == "filter":
            return {
                "action": "filter_data",
                "parameters": {k: v for k, v in entities.items()},
                "explanation": "Apply filters to current view",
            }
        elif intent_type == "navigate":
            return {
                "action": "navigate_to",
                "parameters": {"page": entities.get("resource_type", "dashboard")},
                "explanation": f"Navigate to {entities.get('resource_type', 'dashboard')}",
            }
        
        return {
            "action": "clarify",
            "parameters": {},
            "explanation": "I'm not sure what you're looking for. Could you be more specific?",
        }
    
    def _format_interpretation(self, query: str, intent: dict, entities: dict) -> str:
        """Format a human-readable interpretation."""
        parts = [f"Intent: {intent['type']} (confidence: {intent['confidence']:.0%})"]
        
        if entities:
            entity_strs = [f"{k}: {v}" for k, v in entities.items()]
            parts.append(f"Entities: {', '.join(entity_strs)}")
        
        return "; ".join(parts)
    
    async def generate_narrative(
        self,
        template: str,
        data: dict,
        max_length: int = 500,
        tone: str = "professional",
    ) -> tuple[str, int | None]:
        """Generate narrative text from structured data."""
        templates = {
            "calculation_summary": self._calculation_summary_prompt,
            "reserve_movement": self._reserve_movement_prompt,
            "variance_commentary": self._variance_commentary_prompt,
            "executive_summary": self._executive_summary_prompt,
            "scenario_comparison": self._scenario_comparison_prompt,
        }
        
        prompt_generator = templates.get(template, self._generic_summary_prompt)
        prompt = prompt_generator(data, tone)
        
        try:
            response = await self.llm_client.complete(
                prompt,
                max_tokens=max_length,
                temperature=0.3,
            )
            
            # Clean up response
            text = response.strip()
            
            # Estimate tokens (rough)
            tokens = len(response.split()) + len(prompt.split())
            
            return text, tokens
        except Exception as e:
            logger.exception(f"Narrative generation failed: {e}")
            return self._fallback_narrative(template, data), None
    
    def _calculation_summary_prompt(self, data: dict, tone: str) -> str:
        return f"""Generate a {tone} summary of the following actuarial calculation results.
The summary should be suitable for inclusion in an executive report.

Calculation Data:
- Model: {data.get('model_name', 'Unknown')}
- Run Date: {data.get('run_date', 'Unknown')}
- Total Policies: {data.get('policy_count', 'Unknown')}
- Results Summary: {json.dumps(data.get('result_summary', {}), indent=2)}

Write 2-3 paragraphs summarizing:
1. What was calculated and key assumptions
2. Key findings and totals
3. Any notable observations or recommendations

Summary:"""
    
    def _reserve_movement_prompt(self, data: dict, tone: str) -> str:
        return f"""Generate a {tone} analysis of reserve movements between two periods.

Movement Data:
{json.dumps(data, indent=2)}

Explain the key drivers of the movement in 2-3 paragraphs.
Include percentage changes where relevant.

Analysis:"""
    
    def _variance_commentary_prompt(self, data: dict, tone: str) -> str:
        return f"""Generate {tone} commentary explaining variances between actual and expected results.

Variance Data:
{json.dumps(data, indent=2)}

Explain the significant variances and their potential causes in 2-3 paragraphs.

Commentary:"""
    
    def _executive_summary_prompt(self, data: dict, tone: str) -> str:
        return f"""Generate an executive summary for the following actuarial analysis.
The audience is senior leadership who may not have actuarial backgrounds.

Data:
{json.dumps(data, indent=2)}

Write a clear, {tone} summary in 2-3 paragraphs covering key findings and implications.

Executive Summary:"""
    
    def _scenario_comparison_prompt(self, data: dict, tone: str) -> str:
        return f"""Generate a comparison analysis between multiple scenarios.

Scenario Data:
{json.dumps(data, indent=2)}

Compare the scenarios, highlighting key differences and implications in 2-3 paragraphs.

Comparison:"""
    
    def _generic_summary_prompt(self, data: dict, tone: str) -> str:
        return f"""Generate a {tone} summary of the following data:

{json.dumps(data, indent=2)}

Summary:"""
    
    def _fallback_narrative(self, template: str, data: dict) -> str:
        """Generate a basic narrative when LLM is unavailable."""
        if template == "calculation_summary":
            return (
                f"Calculation completed for {data.get('policy_count', 'N/A')} policies. "
                f"Total reserve: {data.get('result_summary', {}).get('total_reserve', 'N/A')}."
            )
        return "Summary generation unavailable. Please review the detailed data."
    
    async def suggest_column_mapping(
        self,
        source_columns: list[str],
        sample_values: dict[str, list],
        target_type: str,
    ) -> list[dict]:
        """Suggest column mappings for data import."""
        target_fields = self._get_target_fields(target_type)
        
        prompt = f"""Map the following source columns to target fields for a {target_type} import.

Source Columns with sample values:
{self._format_columns_samples(source_columns, sample_values)}

Target Fields:
{', '.join(target_fields)}

For each source column, suggest the best target field match.
Respond with a JSON array of objects, each containing:
- source_column: The source column name
- suggested_field: The suggested target field (or "unmapped" if no match)
- confidence: Confidence score 0-1
- reason: Brief explanation

JSON Array:"""
        
        try:
            response = await self.llm_client.complete(prompt, max_tokens=1000, temperature=0)
            
            json_match = re.search(r'\[[\s\S]*\]', response)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            logger.warning(f"LLM mapping suggestion failed: {e}")
        
        # Fallback to rule-based mapping
        return self._rule_based_mapping(source_columns, sample_values, target_fields)
    
    def _get_target_fields(self, target_type: str) -> list[str]:
        """Get target fields for a resource type."""
        fields = {
            "policy": [
                "policy_number", "product_code", "product_name", "status",
                "issue_date", "effective_date", "maturity_date",
                "sum_assured", "premium_amount", "premium_frequency", "currency",
            ],
            "policyholder": [
                "first_name", "last_name", "date_of_birth", "gender",
                "email", "phone", "address_line1", "city", "country",
                "id_number", "smoker_status", "occupation",
            ],
            "claim": [
                "claim_number", "policy_id", "claim_type", "claim_date",
                "notification_date", "claimed_amount", "settlement_amount",
                "status", "adjuster_notes",
            ],
        }
        return fields.get(target_type, [])
    
    def _format_columns_samples(self, columns: list[str], samples: dict) -> str:
        """Format columns and samples for prompt."""
        lines = []
        for col in columns:
            sample_vals = samples.get(col, [])[:3]
            lines.append(f"- {col}: {sample_vals}")
        return "\n".join(lines)
    
    def _rule_based_mapping(
        self,
        columns: list[str],
        samples: dict,
        target_fields: list[str],
    ) -> list[dict]:
        """Rule-based column mapping."""
        mappings = []
        
        # Common aliases
        aliases = {
            "policy_number": ["policy_no", "pol_num", "policy_id", "polno"],
            "first_name": ["fname", "given_name", "first"],
            "last_name": ["lname", "surname", "family_name", "last"],
            "date_of_birth": ["dob", "birth_date", "birthdate"],
            "sum_assured": ["face_amount", "sum_insured", "coverage_amount"],
            "premium_amount": ["premium", "prem_amt", "annual_premium"],
            "issue_date": ["issue_dt", "inception_date", "start_date"],
            "email": ["email_address", "e_mail"],
            "phone": ["telephone", "phone_number", "tel"],
        }
        
        for col in columns:
            col_lower = col.lower().replace(" ", "_").replace("-", "_")
            
            # Direct match
            if col_lower in target_fields:
                mappings.append({
                    "source_column": col,
                    "suggested_field": col_lower,
                    "confidence": 1.0,
                    "reason": "Direct name match",
                })
                continue
            
            # Alias match
            matched = False
            for field, field_aliases in aliases.items():
                if col_lower in field_aliases and field in target_fields:
                    mappings.append({
                        "source_column": col,
                        "suggested_field": field,
                        "confidence": 0.9,
                        "reason": f"Alias match for {field}",
                    })
                    matched = True
                    break
            
            if not matched:
                mappings.append({
                    "source_column": col,
                    "suggested_field": "unmapped",
                    "confidence": 0.0,
                    "reason": "No match found",
                })
        
        return mappings
    
    async def analyze_data_quality(self, data: dict) -> list[dict]:
        """Analyze data quality issues."""
        issues = []
        
        for column, values in data.items():
            # Check for missing values
            missing_count = sum(1 for v in values if v is None or v == "")
            if missing_count > 0:
                issues.append({
                    "column": column,
                    "issue_type": "missing",
                    "description": f"{missing_count} missing values",
                    "affected_rows": missing_count,
                    "suggestion": "Review and fill in missing values",
                })
            
            # Check for outliers in numeric columns
            numeric_values = [v for v in values if isinstance(v, (int, float)) and v is not None]
            if len(numeric_values) > 10:
                import numpy as np
                arr = np.array(numeric_values)
                mean, std = arr.mean(), arr.std()
                outliers = sum(1 for v in arr if abs(v - mean) > 3 * std)
                if outliers > 0:
                    issues.append({
                        "column": column,
                        "issue_type": "outlier",
                        "description": f"{outliers} potential outliers detected",
                        "affected_rows": outliers,
                        "suggestion": "Verify these values are correct",
                    })
            
            # Check for format inconsistencies
            types = set(type(v).__name__ for v in values if v is not None)
            if len(types) > 1:
                issues.append({
                    "column": column,
                    "issue_type": "inconsistent",
                    "description": f"Mixed data types: {', '.join(types)}",
                    "affected_rows": len(values),
                    "suggestion": "Standardize the data format",
                })
        
        return issues
