import { get, post, put, del } from './client';
import type { PaginatedResponse, ClaimFilters, SuccessResponse } from '@/types/api';
import type { Claim } from '@/types/models';
import type { AnomalyAlert } from '@/types/ai';

export interface ClaimCreateData {
  policy_id: string;
  claim_type: string;
  claim_date: string;
  notification_date: string;
  claimed_amount: number;
  adjuster_notes?: string;
}

export interface ClaimUpdateData {
  status?: string;
  settlement_amount?: number;
  settlement_date?: string;
  adjuster_notes?: string;
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
  list: (params?: ClaimFilters) =>
    get<PaginatedResponse<Claim>>('/claims', params),

  get: (id: string) => 
    get<Claim>(`/claims/${id}`),

  create: (data: ClaimCreateData) => 
    post<Claim>('/claims', data),

  update: (id: string, data: ClaimUpdateData) => 
    put<Claim>(`/claims/${id}`, data),

  delete: (id: string) => 
    del<SuccessResponse>(`/claims/${id}`),

  updateStatus: (id: string, status: string, notes?: string) =>
    put<Claim>(`/claims/${id}/status`, { status, notes }),

  getStats: () => 
    get<ClaimStats>('/claims/stats'),

  // AI-flagged anomalies
  getAnomalies: (limit?: number) =>
    get<(Claim & { anomaly_details: AnomalyAlert })[]>('/claims/anomalies', { limit }),
};
