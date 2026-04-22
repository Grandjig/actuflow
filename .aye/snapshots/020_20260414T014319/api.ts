// Generic API response types
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface ApiError {
  detail: string;
  code?: string;
  field?: string;
}

export interface BulkActionResponse {
  success_count: number;
  error_count: number;
  errors?: Array<{
    id: string;
    error: string;
  }>;
}

// Auth types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

// Query parameter types
export interface PaginationParams {
  page?: number;
  page_size?: number;
}

export interface SortParams {
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export interface SearchParams {
  search?: string;
}

export interface DateRangeParams {
  start_date?: string;
  end_date?: string;
}

export type ListParams = PaginationParams & SortParams & SearchParams;

// Policy API types
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
  branch_code?: string;
}

export interface PolicyUpdateRequest extends Partial<PolicyCreateRequest> {
  status?: string;
}

// Claim API types
export interface ClaimListParams extends ListParams {
  status?: string;
  claim_type?: string;
  policy_id?: string;
  ai_flagged?: boolean;
}

export interface ClaimCreateRequest {
  policy_id: string;
  claim_date: string;
  notification_date?: string;
  claim_type: string;
  claimed_amount: number;
  description?: string;
}

// Assumption API types
export interface AssumptionSetListParams extends ListParams {
  status?: string;
}

export interface AssumptionSetCreateRequest {
  name: string;
  version: string;
  description?: string;
  effective_date?: string;
}

// Calculation API types
export interface CalculationListParams extends ListParams {
  status?: string;
  model_definition_id?: string;
  trigger_type?: string;
}

export interface CalculationCreateRequest {
  run_name: string;
  model_definition_id: string;
  assumption_set_id: string;
  policy_filter?: Record<string, unknown>;
  parameters?: Record<string, unknown>;
}

export interface CalculationProgress {
  status: string;
  progress_percent: number;
  progress_message?: string;
  policies_processed: number;
  policies_total: number;
}

export interface CalculationSummary {
  total_policies: number;
  successful: number;
  failed: number;
  total_reserve: number;
  total_liability: number;
  by_product: Record<string, {
    count: number;
    reserve: number;
  }>;
}

// Scenario API types
export interface ScenarioListParams extends ListParams {
  status?: string;
  scenario_type?: string;
}

// Report API types
export interface ReportGenerateRequest {
  report_template_id: string;
  reporting_period_start: string;
  reporting_period_end: string;
  parameters?: Record<string, unknown>;
}

// Import API types
export interface ImportUploadResponse {
  id: string;
  file_name: string;
  total_rows: number;
  columns: string[];
  sample_data: Array<Record<string, unknown>>;
}

export interface ColumnMappingRequest {
  mapping: Record<string, string>;
}

export interface ImportValidationResult {
  is_valid: boolean;
  total_rows: number;
  valid_rows: number;
  error_rows: number;
  errors: Array<{
    row: number;
    column: string;
    error: string;
  }>;
}

// Task API types
export interface TaskListParams extends ListParams {
  status?: string;
  priority?: string;
  assigned_to_id?: string;
  task_type?: string;
}

// Notification API types  
export interface NotificationListParams extends PaginationParams {
  is_read?: boolean;
}

// Audit API types
export interface AuditLogListParams extends ListParams {
  action?: string;
  resource_type?: string;
  user_id?: string;
  start_date?: string;
  end_date?: string;
}

// User API types
export interface UserListParams extends ListParams {
  role_id?: string;
  is_active?: boolean;
}

export interface UserCreateRequest {
  email: string;
  full_name: string;
  password: string;
  role_id?: string;
  department?: string;
}

export interface UserUpdateRequest {
  email?: string;
  full_name?: string;
  role_id?: string;
  department?: string;
  is_active?: boolean;
}
