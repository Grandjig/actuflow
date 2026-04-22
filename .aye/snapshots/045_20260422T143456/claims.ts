import { get, post, put, del } from './client';
import type { PaginatedResponse } from '@/types/api';
import type { ClaimListParams, ClaimCreateRequest, ClaimUpdateRequest } from '@/types/api';
import type { Claim } from '@/types/models';

export const claimsApi = {
  list: (params?: ClaimListParams) =>
    get<PaginatedResponse<Claim>>('/claims', params),

  get: (id: string) =>
    get<Claim>(`/claims/${id}`),

  create: (data: ClaimCreateRequest) =>
    post<Claim>('/claims', data),

  update: (id: string, data: ClaimUpdateRequest) =>
    put<Claim>(`/claims/${id}`, data),

  delete: (id: string) =>
    del<void>(`/claims/${id}`),

  getStats: () =>
    get<{
      total_claims: number;
      open_claims: number;
      total_claimed: number;
      total_settled: number;
      by_status: Record<string, number>;
      by_type: Record<string, number>;
    }>('/claims/stats'),

  getAnomalies: (limit?: number) =>
    get<Claim[]>('/claims/anomalies', { limit }),
};
