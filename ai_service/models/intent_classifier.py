"""Intent Classifier."""

import re
from typing import Any


class IntentClassifier:
    """Classifies user query intent."""
    
    def __init__(self):
        self.patterns = {
            "search": [
                r"\b(find|search|look\s?up|show|get|where|which)\b",
                r"\b(policy|policies|policyholder|claim)\b.*\b(number|#|id)\b",
            ],
            "filter": [
                r"\b(filter|with|having|where|that\s+have|only)\b",
                r"\b(greater|less|more|under|over|between|above|below)\b.*\b(than)?\b",
                r"\b(status|type|date|amount)\b.*\b(is|equals?|=)\b",
            ],
            "navigate": [
                r"\b(go\s+to|open|navigate|take\s+me|show\s+me)\b",
                r"\b(dashboard|settings|report|calculation|assumption)\s*(page)?\b",
            ],
            "aggregate": [
                r"\b(total|sum|count|average|mean|how\s+many|number\s+of)\b",
                r"\b(statistics|stats|summary|overview)\b",
            ],
            "report": [
                r"\b(generate|create|run|produce)\b.*\b(report)\b",
                r"\b(export|download)\b",
            ],
            "explain": [
                r"\b(explain|why|how|what\s+is|tell\s+me\s+about)\b",
                r"\b(help|understand)\b",
            ],
            "compare": [
                r"\b(compare|difference|versus|vs|between)\b",
                r"\b(comparison)\b",
            ],
        }
        
        self.keywords = {
            "search": ["find", "search", "lookup", "show", "get", "list"],
            "filter": ["filter", "where", "with", "having"],
            "navigate": ["go", "open", "navigate"],
            "aggregate": ["total", "count", "sum", "average", "how many"],
            "report": ["report", "generate", "export"],
            "explain": ["explain", "why", "how", "what"],
            "compare": ["compare", "versus", "difference"],
        }
    
    def classify(self, query: str) -> dict[str, Any]:
        """Classify the intent of a query."""
        query_lower = query.lower()
        
        scores = {intent: 0.0 for intent in self.patterns.keys()}
        
        # Pattern matching
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    scores[intent] += 0.3
        
        # Keyword matching
        for intent, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    scores[intent] += 0.2
        
        # Question words
        if query_lower.startswith(("what", "who", "where", "when", "which")):
            scores["search"] += 0.1
            scores["explain"] += 0.1
        
        if query_lower.startswith("how"):
            if "many" in query_lower or "much" in query_lower:
                scores["aggregate"] += 0.3
            else:
                scores["explain"] += 0.2
        
        # Find best intent
        best_intent = max(scores, key=scores.get)
        best_score = scores[best_intent]
        
        # Confidence normalization
        if best_score > 0:
            confidence = min(best_score / 0.6, 1.0)
        else:
            confidence = 0.3
            best_intent = "search"  # Default to search
        
        return {
            "type": best_intent,
            "confidence": confidence,
            "all_scores": scores,
        }
