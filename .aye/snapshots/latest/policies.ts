import { get, post, put, del } from './client';
import type { PaginatedResponse } from '@/types/api';
import type { PolicyListParams, PolicyCreateRequest, PolicyUpdateRequest } from '@/types/api';
import type { Policy } from '@/types/models';

export const policiesApi = {
  list: (params?: PolicyListParams) =>
    get<PaginatedResponse<Policy>>('/policies', params),

  get: (id: string) =>
    get<Policy>(`/policies/${id}`),

  create: (data: PolicyCreateRequest) =>
    post<Policy>('/policies', data),

  update: (id: string, data: PolicyUpdateRequest) =>
    put<Policy>(`/policies/${id}`, data),

  delete: (id: string) =>
    del<void>(`/policies/${id}`),

  getStats: () =>
    get<{
      total_policies: number;
      active_policies: number;
      total_premium: number;
      by_status: Record<string, number>;
      by_product_type: Record<string, number>;
    }>('/policies/stats'),

  export: (params?: PolicyListParams) =>
    get<Blob>('/policies/export', params),

  getHistory: (id: string) =>
    get<any[]>(`/policies/${id}/history`),

  getSimilar: (id: string) =>
    get<Policy[]>(`/policies/${id}/similar`),
};
