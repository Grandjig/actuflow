"""Entity Extractor."""

import re
from datetime import datetime
from typing import Any


class EntityExtractor:
    """Extracts entities from text."""
    
    def __init__(self):
        self._spacy_nlp = None
    
    def _load_spacy(self):
        """Lazy load spaCy model."""
        if self._spacy_nlp is None:
            import spacy
            try:
                self._spacy_nlp = spacy.load("en_core_web_sm")
            except OSError:
                # Fallback if model not installed
                self._spacy_nlp = None
    
    def extract(self, text: str) -> dict[str, Any]:
        """Extract entities from text."""
        entities = {}
        
        # Pattern-based extraction (always works)
        entities.update(self._extract_policy_numbers(text))
        entities.update(self._extract_claim_numbers(text))
        entities.update(self._extract_dates(text))
        entities.update(self._extract_amounts(text))
        entities.update(self._extract_percentages(text))
        entities.update(self._extract_statuses(text))
        entities.update(self._extract_product_types(text))
        
        # spaCy-based extraction (if available)
        self._load_spacy()
        if self._spacy_nlp:
            entities.update(self._extract_spacy_entities(text))
        else:
            # Fallback name extraction
            entities.update(self._extract_names_regex(text))
        
        return entities
    
    def _extract_policy_numbers(self, text: str) -> dict:
        """Extract policy numbers."""
        patterns = [
            r"\b(?:policy|pol)[\s#:.-]*([A-Z0-9][A-Z0-9\-]{3,20})\b",
            r"\bPOL-\d{4}-\d{5}\b",
            r"\b[A-Z]{2,3}\d{6,10}\b",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return {"policy_number": match.group(0).upper()}
        
        return {}
    
    def _extract_claim_numbers(self, text: str) -> dict:
        """Extract claim numbers."""
        patterns = [
            r"\b(?:claim)[\s#:.-]*([A-Z0-9][A-Z0-9\-]{3,20})\b",
            r"\bCLM-\d{4}-\d{5}\b",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return {"claim_number": match.group(0).upper()}
        
        return {}
    
    def _extract_dates(self, text: str) -> dict:
        """Extract dates."""
        dates = []
        
        # Various date formats
        patterns = [
            (r"\b(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})\b", "%m/%d/%Y"),
            (r"\b(\d{4})[/\-](\d{1,2})[/\-](\d{1,2})\b", "%Y-%m-%d"),
            (r"\b(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{4})\b", "%d %b %Y"),
            (r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{1,2}),?\s+(\d{4})\b", "%b %d %Y"),
        ]
        
        for pattern, date_format in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                date_str = " ".join(str(m) for m in match) if isinstance(match, tuple) else match
                date_str = re.sub(r"\s+", " ", date_str)
                dates.append(date_str)
        
        # Time-relative references
        text_lower = text.lower()
        if "today" in text_lower:
            dates.append(datetime.now().strftime("%Y-%m-%d"))
        if "yesterday" in text_lower:
            from datetime import timedelta
            dates.append((datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"))
        if "last month" in text_lower:
            from datetime import timedelta
            dates.append((datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        if "last year" in text_lower:
            dates.append(str(datetime.now().year - 1))
        
        if dates:
            return {"date": dates[0] if len(dates) == 1 else dates}
        return {}
    
    def _extract_amounts(self, text: str) -> dict:
        """Extract monetary amounts."""
        patterns = [
            r"\$([\d,]+(?:\.\d{2})?)\s*(?:million|M)?\b",
            r"\b([\d,]+(?:\.\d{2})?)\s*(?:dollars|USD)\b",
            r"\b(?:amount|sum|premium|reserve)\s*(?:of|:)?\s*\$?([\d,]+(?:\.\d{2})?)\b",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(",", "")
                try:
                    amount = float(amount_str)
                    if "million" in text.lower() or "M" in match.group(0):
                        amount *= 1_000_000
                    return {"amount": amount}
                except ValueError:
                    pass
        
        return {}
    
    def _extract_percentages(self, text: str) -> dict:
        """Extract percentages."""
        match = re.search(r"(\d+(?:\.\d+)?)\s*%", text)
        if match:
            return {"percentage": float(match.group(1))}
        return {}
    
    def _extract_statuses(self, text: str) -> dict:
        """Extract status values."""
        text_lower = text.lower()
        
        policy_statuses = ["active", "lapsed", "surrendered", "matured", "claimed"]
        claim_statuses = ["open", "under review", "approved", "denied", "paid", "closed"]
        
        for status in policy_statuses + claim_statuses:
            if status in text_lower:
                return {"status": status}
        
        return {}
    
    def _extract_product_types(self, text: str) -> dict:
        """Extract product types."""
        text_lower = text.lower()
        
        products = {
            "term life": "life",
            "whole life": "life",
            "universal life": "life",
            "life insurance": "life",
            "health": "health",
            "medical": "health",
            "auto": "property",
            "property": "property",
            "home": "property",
            "liability": "casualty",
            "casualty": "casualty",
        }
        
        for keyword, product_type in products.items():
            if keyword in text_lower:
                return {"product_type": product_type}
        
        return {}
    
    def _extract_spacy_entities(self, text: str) -> dict:
        """Extract entities using spaCy."""
        doc = self._spacy_nlp(text)
        entities = {}
        
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                entities["person_name"] = ent.text
            elif ent.label_ == "ORG":
                entities["organization"] = ent.text
            elif ent.label_ == "GPE" or ent.label_ == "LOC":
                entities["location"] = ent.text
            elif ent.label_ == "MONEY" and "amount" not in entities:
                # Parse money value
                amount_str = re.sub(r"[^\d.]", "", ent.text)
                try:
                    entities["amount"] = float(amount_str)
                except ValueError:
                    pass
        
        return entities
    
    def _extract_names_regex(self, text: str) -> dict:
        """Extract names using regex (fallback when spaCy unavailable)."""
        # Simple pattern for names in context
        patterns = [
            r"(?:policyholder|insured|client|customer|claimant)\s+(?:named?)?\s*:?\s*([A-Z][a-z]+\s+[A-Z][a-z]+)",
            r"(?:Mr\.?|Mrs\.?|Ms\.?|Dr\.?)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return {"person_name": match.group(1)}
        
        return {}
