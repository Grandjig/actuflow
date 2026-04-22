// API request/response types

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface SuccessResponse {
  success: boolean;
  message: string;
}

export interface ErrorResponse {
  detail: string;
  code?: string;
  field?: string;
}

export interface ListParams {
  page?: number;
  page_size?: number;
  search?: string;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

// Policy API
export interface PolicyListParams extends ListParams {
  status?: string;
  product_type?: string;
  product_code?: string;
  policyholder_id?: string;
  issue_date_from?: string;
  issue_date_to?: string;
}

export interface PolicyCreateRequest {
  policy_number: string;
  product_type: string;
  product_code: string;
  product_name?: string;
  policyholder_id: string;
  issue_date: string;
  effective_date: string;
  maturity_date?: string;
  sum_assured: number;
  premium_amount: number;
  premium_frequency: string;
  currency: string;
  risk_class?: string;
  branch_code?: string;
  status?: string;
}

export interface PolicyUpdateRequest extends Partial<PolicyCreateRequest> {}

// Claim API
export interface ClaimListParams extends ListParams {
  status?: string;
  claim_type?: string;
  policy_id?: string;
  anomaly_only?: boolean;
}

export interface ClaimCreateRequest {
  policy_id: string;
  claim_type: string;
  claim_date: string;
  incident_date?: string;
  notification_date?: string;
  claimed_amount: number;
  adjuster_notes?: string;
}

export interface ClaimUpdateRequest {
  status?: string;
  settlement_date?: string;
  settlement_amount?: number;
  adjuster_id?: string;
  adjuster_notes?: string;
  denial_reason?: string;
}

// Assumption API
export interface AssumptionSetFilters extends ListParams {
  status?: string;
  line_of_business?: string;
}

export interface AssumptionSetCreateRequest {
  name: string;
  version: string;
  description?: string;
  effective_date?: string;
  line_of_business?: string;
}

export interface AssumptionSetUpdateRequest extends Partial<AssumptionSetCreateRequest> {}

export interface AssumptionTableCreateRequest {
  table_type: string;
  name: string;
  description?: string;
  data: Record<string, any>;
  metadata?: Record<string, any>;
}

// Calculation API
export interface CalculationListParams extends ListParams {
  status?: string;
  model_id?: string;
  trigger_type?: string;
}

export interface CalculationCreateRequest {
  run_name: string;
  model_definition_id: string;
  assumption_set_id: string;
  policy_filter?: Record<string, any>;
  parameters?: Record<string, any>;
}

export interface CalculationProgress {
  status: string;
  progress_percent: number;
  progress_message: string;
  policies_processed: number;
  policies_total: number;
  started_at?: string;
  estimated_completion?: string;
}

export interface CalculationSummary {
  total_policies: number;
  total_reserves: number;
  total_premiums: number;
  by_product_type: Record<string, Record<string, number>>;
  by_status: Record<string, number>;
  anomaly_count: number;
}

// Report API
export interface ReportGenerateRequest {
  template_id: string;
  name?: string;
  parameters?: Record<string, any>;
}

// Import API
export interface ImportCreateRequest {
  file: File;
  import_type: string;
}

export interface ColumnMapping {
  source_column: string;
  target_field: string;
}

// AI API
export interface NLQueryRequest {
  query: string;
  context?: Record<string, any>;
}

export interface NLQueryResponse {
  query: string;
  parsed_intent: {
    intent: string;
    entity_type?: string;
    filters: Record<string, any>;
  };
  explanation: string;
  result_count?: number;
  suggested_api_call?: {
    endpoint: string;
    method: string;
    params: Record<string, any>;
  };
}

export interface NarrativeRequest {
  template: string;
  data: Record<string, any>;
  max_length?: number;
  tone?: string;
}

export interface NarrativeResponse {
  text: string;
  generated_at?: string;
}

// Automation API
export interface ScheduledJobCreateRequest {
  name: string;
  description?: string;
  job_type: string;
  cron_expression: string;
  config: Record<string, any>;
  is_active?: boolean;
}

export interface AutomationRuleCreateRequest {
  name: string;
  description?: string;
  trigger_type: string;
  trigger_config: Record<string, any>;
  action_type: string;
  action_config: Record<string, any>;
  is_active?: boolean;
}
