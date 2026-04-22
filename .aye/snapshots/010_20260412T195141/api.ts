// API types for requests and responses

import type { User, Role, Permission } from './models';

// Generic paginated response
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
}

// Generic success response
export interface SuccessResponse {
  message: string;
}

// Error response
export interface ErrorResponse {
  detail: string;
  code?: string;
  errors?: Record<string, string[]>;
}

// Auth types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

export interface RefreshTokenResponse {
  access_token: string;
  token_type: string;
}

// Pagination params
export interface PaginationParams {
  page?: number;
  page_size?: number;
}

// Sort params
export interface SortParams {
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

// Common filter params
export interface DateRangeFilter {
  start_date?: string;
  end_date?: string;
}

// Policy filters
export interface PolicyFilters extends PaginationParams, SortParams {
  status?: string;
  product_type?: string;
  product_code?: string;
  policyholder_id?: string;
  search?: string;
}

// Policyholder filters
export interface PolicyholderFilters extends PaginationParams, SortParams {
  search?: string;
  gender?: string;
  smoker_status?: string;
}

// Claim filters
export interface ClaimFilters extends PaginationParams, SortParams {
  status?: string;
  claim_type?: string;
  policy_id?: string;
  anomaly_flagged?: boolean;
  date_from?: string;
  date_to?: string;
}

// Assumption set filters
export interface AssumptionSetFilters extends PaginationParams, SortParams {
  status?: string;
  search?: string;
}

// Model filters
export interface ModelFilters extends PaginationParams, SortParams {
  status?: string;
  model_type?: string;
  line_of_business?: string;
  search?: string;
}

// Calculation run filters
export interface CalculationRunFilters extends PaginationParams, SortParams {
  status?: string;
  model_definition_id?: string;
  triggered_by_id?: string;
  date_from?: string;
  date_to?: string;
}

// Task filters
export interface TaskFilters extends PaginationParams {
  status?: string;
  priority?: string;
  task_type?: string;
  assigned_to_id?: string;
  overdue_only?: boolean;
}

// Audit log filters
export interface AuditLogFilters extends PaginationParams {
  user_id?: string;
  action?: string;
  resource_type?: string;
  date_from?: string;
  date_to?: string;
}

// Search request
export interface SearchRequest {
  q: string;
  types?: string;
  limit?: number;
}

export interface SearchResult {
  id: string;
  type: string;
  title: string;
  subtitle?: string;
  score?: number;
}

export interface SearchResponse {
  query: string;
  results: Record<string, SearchResult[]>;
  total: number;
}
