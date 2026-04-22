import { get, post, put, del } from './client';
import type { PaginatedResponse, PolicyListParams } from '@/types/api';
import type { Policy } from '@/types/models';

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
  branch_code?: string;
}

export interface PolicyUpdateData extends Partial<PolicyCreateData> {
  status?: string;
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
  list: (params?: PolicyListParams) =>
    get<PaginatedResponse<Policy>>('/policies', params),

  get: (id: string) =>
    get<Policy>(`/policies/${id}`),

  create: (data: PolicyCreateData) =>
    post<Policy>('/policies', data),

  update: (id: string, data: PolicyUpdateData) =>
    put<Policy>(`/policies/${id}`, data),

  delete: (id: string) =>
    del<void>(`/policies/${id}`),

  getStats: () =>
    get<PolicyStats>('/policies/stats'),

  getHistory: (id: string) =>
    get<any[]>(`/policies/${id}/history`),
};
