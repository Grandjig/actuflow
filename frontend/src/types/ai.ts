// AI-related types

export interface NLQueryRequest {
  query: string;
  context?: Record<string, any>;
}

export interface ParsedIntent {
  intent: string;
  entity_type?: string;
  filters: Record<string, any>;
  clarification_needed?: boolean;
  clarification_question?: string;
  type?: string;
}

export interface SuggestedAction {
  action: string;
  parameters: Record<string, any>;
  explanation: string;
}

export interface NLQueryResponse {
  query: string;
  parsed_intent: ParsedIntent;
  explanation: string;
  result_count?: number;
  suggested_api_call?: {
    endpoint: string;
    method: string;
    params: Record<string, any>;
  };
  suggested_action?: SuggestedAction;
}

export interface NarrativeRequest {
  template: string;
  data: Record<string, any>;
  max_length?: number;
  tone?: 'professional' | 'casual' | 'technical';
}

export interface NarrativeResponse {
  text: string;
  generated_at?: string;
  tokens_used?: number;
}

export interface AnomalyAlert {
  id: string;
  resource_type: string;
  resource_id: string;
  record_type?: string;
  record_id?: string;
  anomaly_type: string;
  score: number;
  description: string;
  explanation: string;
  reasons?: string[];
  detected_at: string;
  resolved?: boolean;
}

export interface DocumentExtractionResult {
  document_id: string;
  extracted_text: string;
  entities: ExtractedEntity[];
  structured_data: Record<string, ExtractedField>;
  confidence: number;
}

export interface ExtractedEntity {
  type: string;
  value: string;
  confidence: number;
  start_pos?: number;
  end_pos?: number;
}

export interface ExtractedField {
  value: any;
  confidence: number;
  source?: string;
}

export interface SemanticSearchResult {
  id: string;
  resource_type: string;
  title: string;
  snippet: string;
  score: number;
  metadata?: Record<string, any>;
}

export interface SemanticSearchRequest {
  query: string;
  resource_types?: string[];
  limit?: number;
  offset?: number;
}

export interface ExperienceRecommendation {
  assumption_type: string;
  segment?: string;
  current_value: number;
  recommended_value: number;
  change_percent: number;
  confidence: number;
  sample_size: number;
  rationale: string;
  impact?: {
    reserve_change: number;
    direction: 'increase' | 'decrease';
  };
}

export interface AIFeatureStatus {
  enabled: boolean;
  healthy: boolean;
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

export interface AIFeatures {
  smart_import: boolean;
  natural_language: boolean;
  anomaly_detection: boolean;
  narrative_generation: boolean;
  semantic_search: boolean;
  document_extraction: boolean;
  experience_recommendations: boolean;
}

export interface NaturalLanguageQuery {
  query: string;
  context?: Record<string, any>;
}

export interface QueryFeedback {
  query_id: string;
  helpful: boolean;
  feedback?: string;
}

export interface QueryHistoryItem {
  id: string;
  query: string;
  result: NLQueryResponse;
  timestamp: string;
}

export interface ColumnMappingSuggestion {
  source_column: string;
  suggested_field: string;
  confidence: number;
  type?: string;
}

export interface DataQualityIssue {
  row_number: number;
  column: string;
  issue_type: string;
  description: string;
  severity: 'error' | 'warning' | 'info';
}
