// API response types

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

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

// Common params
export interface PaginationParams {
  page?: number;
  page_size?: number;
}

export interface ListParams extends PaginationParams {
  search?: string;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

// Policy params
export interface PolicyListParams extends ListParams {
  status?: string;
  product_type?: string;
  product_code?: string;
  policyholder_id?: string;
  issue_date_from?: string;
  issue_date_to?: string;
}

// Calculation params
export interface CalculationListParams extends ListParams {
  status?: string;
  trigger_type?: string;
  model_id?: string;
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

// Assumption params
export interface AssumptionSetFilters extends ListParams {
  status?: string;
  line_of_business?: string;
}

// Claim params
export interface ClaimListParams extends ListParams {
  status?: string;
  claim_type?: string;
  policy_id?: string;
  anomaly_only?: boolean;
}

// Task params
export interface TaskListParams extends ListParams {
  status?: string;
  priority?: string;
  assigned_to_me?: boolean;
}

// Report params
export interface ReportListParams extends ListParams {
  report_type?: string;
  status?: string;
}

// Dashboard data types
export interface DashboardStats {
  total_policies: number;
  active_policies: number;
  total_premium: number;
  total_claims: number;
  pending_tasks: number;
  recent_calculations: number;
}

export interface ChartData {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    backgroundColor?: string | string[];
    borderColor?: string;
  }[];
}
