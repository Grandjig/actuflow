// AI-specific types

export interface NaturalLanguageQuery {
  query: string;
  context?: Record<string, unknown>;
}

export interface ParsedIntent {
  intent: string;
  entities: Record<string, unknown>;
  confidence: number;
  suggested_action: SuggestedAction | null;
  raw_interpretation: string;
  query_id?: string;
}

export interface SuggestedAction {
  action: string;
  parameters: Record<string, unknown>;
  explanation: string;
}

export interface QueryFeedback {
  was_helpful: boolean;
  feedback_text?: string;
}

export interface NarrativeRequest {
  template: string;
  data: Record<string, unknown>;
  max_length?: number;
  tone?: 'professional' | 'casual' | 'technical';
}

export interface NarrativeResponse {
  text: string;
  template: string;
  ai_generated: boolean;
}

export interface SemanticSearchRequest {
  query: string;
  resource_type?: string;
  limit?: number;
}

export interface SemanticSearchResult {
  id: string;
  resource_type: string;
  title: string;
  score: number;
  metadata?: Record<string, unknown>;
}

export interface DocumentExtractionResult {
  raw_text: string;
  entities: ExtractedEntity[];
  structured_data: Record<string, unknown>;
  page_count: number;
  confidence_score: number;
  warnings: string[];
}

export interface ExtractedEntity {
  entity_type: string;
  value: string;
  confidence: number;
  location?: {
    page?: number;
    x?: number;
    y?: number;
    width?: number;
    height?: number;
  };
}

export interface AnomalyAlert {
  record_id: string;
  is_anomaly: boolean;
  anomaly_score: number;
  anomaly_reasons: string[];
  feature_contributions: Record<string, number>;
}

export interface AnomalyExplanation {
  is_anomaly: boolean;
  anomaly_score: number;
  explanation: string;
  contributing_factors: ContributingFactor[];
  similar_normal_records: number;
}

export interface ContributingFactor {
  feature: string;
  value: unknown;
  expected_range: string;
  deviation: string;
}

export interface ColumnMappingSuggestion {
  source_column: string;
  suggested_field: string;
  confidence: number;
  reason?: string;
}

export interface DataQualityIssue {
  column: string;
  issue_type: 'missing' | 'outlier' | 'format' | 'inconsistent';
  description: string;
  affected_rows: number;
  suggestion?: string;
}

export interface AIFeatures {
  ai_enabled: boolean;
  features: {
    smart_import: boolean;
    natural_language: boolean;
    anomaly_detection: boolean;
    narrative_generation: boolean;
    semantic_search: boolean;
    document_extraction: boolean;
    experience_recommendations: boolean;
  };
}

export interface QueryHistoryItem {
  id: string;
  query: string;
  intent?: string;
  was_helpful?: boolean;
  created_at: string;
}
