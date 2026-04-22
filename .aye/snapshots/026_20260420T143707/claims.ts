import { get, post, put, del } from './client';
import type { PaginatedResponse, ClaimListParams } from '@/types/api';
import type { Claim } from '@/types/models';

export interface ClaimCreate {
  policy_id: string;
  claim_type: string;
  claim_date: string;
  claimed_amount: number;
  incident_date?: string;
  notification_date?: string;
  adjuster_notes?: string;
}

export interface ClaimUpdate {
  status?: string;
  settlement_date?: string;
  settlement_amount?: number;
  adjuster_id?: string;
  adjuster_notes?: string;
  denial_reason?: string;
}

export interface ClaimStats {
  total_claims: number;
  open_claims: number;
  total_claimed: number;
  total_settled: number;
  by_status: Record<string, number>;
  by_type: Record<string, number>;
}

export const claimsApi = {
  list: (params?: ClaimListParams) =>
    get<PaginatedResponse<Claim>>('/claims', params),

  get: (id: string) =>
    get<Claim>(`/claims/${id}`),

  create: (data: ClaimCreate) =>
    post<Claim>('/claims', data),

  update: (id: string, data: ClaimUpdate) =>
    put<Claim>(`/claims/${id}`, data),

  delete: (id: string) =>
    del<void>(`/claims/${id}`),

  getStats: () =>
    get<ClaimStats>('/claims/stats'),

  getAnomalies: (limit?: number) =>
    get<Claim[]>('/claims/anomalies', { limit }),
};
