// AI-related types

export interface NLQueryRequest {
  query: string;
  context?: Record<string, unknown>;
}

export interface NLQueryResponse {
  query: string;
  parsed_intent: {
    type: string;
    entity?: string;
    filters?: Record<string, unknown>;
  };
  explanation: string;
  suggested_action?: {
    action: string;
    parameters: Record<string, unknown>;
    explanation: string;
  };
  result_count?: number;
}

export interface ColumnMappingSuggestion {
  source_column: string;
  suggested_field: string;
  confidence: number;
  reason: string;
}

export interface DataQualityIssue {
  row?: number;
  column: string;
  issue_type: 'missing' | 'invalid_format' | 'outlier' | 'inconsistent' | 'duplicate';
  description: string;
  suggested_fix?: string;
}

export interface AIRecommendation {
  assumption_type: string;
  segment?: string;
  current_value: number;
  recommended_value: number;
  confidence: number;
  sample_size: number;
  rationale: string;
  impact?: {
    reserve_change: number;
    direction: 'increase' | 'decrease';
  };
}

export interface AnomalyAlert {
  id: string;
  record_type: string;
  record_id: string;
  score: number;
  reasons: string[];
  detected_at: string;
}

export interface NarrativeRequest {
  template: string;
  data: Record<string, unknown>;
  max_length?: number;
  tone?: 'professional' | 'concise' | 'detailed';
}

export interface NarrativeResponse {
  text: string;
  generated_at: string;
  tokens_used?: number;
}

export interface DocumentExtractionResult {
  document_id: string;
  extracted_text: string;
  entities: {
    type: string;
    value: string;
    confidence: number;
    position?: { start: number; end: number };
  }[];
  structured_data: Record<string, { value: unknown; confidence: number }>;
  warnings?: string[];
}

export interface AIStatus {
  enabled: boolean;
  features: {
    natural_language: boolean;
    anomaly_detection: boolean;
    narrative_generation: boolean;
    smart_import: boolean;
    document_extraction: boolean;
    semantic_search: boolean;
  };
}
