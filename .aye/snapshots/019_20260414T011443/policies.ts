import { get, post, put, del, downloadFile } from './client';
import type { PaginatedResponse, PolicyFilters, SuccessResponse } from '@/types/api';
import type { Policy, Coverage } from '@/types/models';

export interface PolicyCreateData {
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
}

export interface PolicyUpdateData {
  product_name?: string;
  status?: string;
  maturity_date?: string;
  sum_assured?: number;
  premium_amount?: number;
  premium_frequency?: string;
}

export interface PolicyStats {
  total_policies: number;
  active_policies: number;
  total_sum_assured: number;
  total_premium: number;
  by_status: Record<string, number>;
  by_product_type: Record<string, number>;
}

export const policiesApi = {
  list: (params?: PolicyFilters) =>
    get<PaginatedResponse<Policy>>('/policies', params),

  get: (id: string) => 
    get<Policy>(`/policies/${id}`),

  create: (data: PolicyCreateData) => 
    post<Policy>('/policies', data),

  update: (id: string, data: PolicyUpdateData) => 
    put<Policy>(`/policies/${id}`, data),

  delete: (id: string) => 
    del<SuccessResponse>(`/policies/${id}`),

  getStats: () => 
    get<PolicyStats>('/policies/stats'),

  export: (params?: PolicyFilters) =>
    downloadFile('/policies/export', 'policies.csv'),

  getHistory: (id: string) =>
    get<{ timestamp: string; user: string; changes: Record<string, unknown> }[]>(`/policies/${id}/history`),

  getCoverages: (id: string) =>
    get<Coverage[]>(`/policies/${id}/coverages`),

  addCoverage: (policyId: string, data: Omit<Coverage, 'id' | 'policy_id'>) =>
    post<Coverage>(`/policies/${policyId}/coverages`, data),

  updateCoverage: (policyId: string, coverageId: string, data: Partial<Coverage>) =>
    put<Coverage>(`/policies/${policyId}/coverages/${coverageId}`, data),

  deleteCoverage: (policyId: string, coverageId: string) =>
    del<SuccessResponse>(`/policies/${policyId}/coverages/${coverageId}`),

  // AI-powered similar policy finder
  findSimilar: (id: string, limit?: number) =>
    get<{ id: string; policy_number: string; score: number }[]>(`/policies/${id}/similar`, { limit }),
};
