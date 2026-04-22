// Natural Language Query types
export interface NaturalLanguageQuery {
  query: string;
  context?: Record<string, unknown>;
}

export interface ParsedIntent {
  intent: string;
  confidence: number;
  entities: Array<{
    type: string;
    value: string;
    start: number;
    end: number;
  }>;
  filters?: Record<string, unknown>;
}

export interface NaturalLanguageResponse {
  query: string;
  parsed_intent: ParsedIntent;
  explanation: string;
  result_count?: number;
  results?: unknown[];
  suggested_api_call?: {
    endpoint: string;
    method: string;
    params: Record<string, unknown>;
  };
  follow_up_suggestions?: string[];
}

// Anomaly Detection types
export interface AnomalyAlert {
  id: string;
  resource_type: string;
  resource_id: string;
  anomaly_type: string;
  score: number;
  description: string;
  detected_at: string;
  status: 'new' | 'reviewed' | 'dismissed';
  reviewed_by?: string;
  reviewed_at?: string;
  notes?: string;
}

export interface AnomalyDetectionResult {
  anomalies: AnomalyAlert[];
  total_checked: number;
  anomaly_count: number;
  threshold_used: number;
}

// Document Extraction types
export interface ExtractionResult {
  document_id: string;
  extracted_text: string;
  entities: Array<{
    type: string;
    value: string;
    confidence: number;
    bounding_box?: {
      x: number;
      y: number;
      width: number;
      height: number;
    };
  }>;
  structured_data: Record<string, {
    value: unknown;
    confidence: number;
  }>;
  overall_confidence: number;
}

// Data Quality types
export interface DataQualityIssue {
  issue_type: 'missing' | 'invalid_format' | 'outlier' | 'duplicate' | 'inconsistent';
  column: string;
  row?: number;
  description: string;
  suggested_fix?: string;
  severity: 'low' | 'medium' | 'high';
}

export interface DataQualityReport {
  total_rows: number;
  total_issues: number;
  issues: DataQualityIssue[];
  quality_score: number;
  recommendations: string[];
}

// Column Mapping types
export interface ColumnMappingSuggestion {
  source_column: string;
  suggested_field: string;
  confidence: number;
  reason: string;
  alternatives?: Array<{
    field: string;
    confidence: number;
  }>;
}

export interface ImportAISuggestions {
  column_mappings: ColumnMappingSuggestion[];
  data_issues: DataQualityIssue[];
  overall_quality_score: number;
  recommendations: string[];
}

// Narrative Generation types
export interface NarrativeRequest {
  template_type: string;
  data: Record<string, unknown>;
  tone?: 'formal' | 'casual' | 'technical';
  max_length?: number;
}

export interface NarrativeResponse {
  text: string;
  template_used: string;
  generated_at: string;
  word_count: number;
  key_points: string[];
}

// Semantic Search types
export interface SemanticSearchRequest {
  query: string;
  resource_types?: string[];
  limit?: number;
  min_score?: number;
}

export interface SemanticSearchResult {
  resource_type: string;
  resource_id: string;
  title: string;
  snippet: string;
  score: number;
  url: string;
}

// Experience Recommendation types
export interface ExperienceRecommendation {
  assumption_type: string;
  segment?: string;
  current_value: number;
  recommended_value: number;
  actual_value: number;
  credibility: number;
  confidence: 'low' | 'medium' | 'high';
  data_points: number;
  impact?: {
    reserve_change: number;
    direction: 'increase' | 'decrease';
  };
  rationale: string;
}

// AI Query History types
export interface AIQueryHistoryItem {
  id: string;
  query_text: string;
  parsed_intent: ParsedIntent;
  executed_action: string;
  was_helpful?: boolean;
  timestamp: string;
}
