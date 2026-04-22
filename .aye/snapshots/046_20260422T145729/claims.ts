/**
 * Claims API functions.
 */

import { get, post, put, del } from './client';
import type { Claim } from '@/types/models';

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export async function getClaims(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<Claim>> {
  return get('/claims', params);
}

export async function getClaim(id: string): Promise<Claim> {
  return get(`/claims/${id}`);
}

export async function createClaim(data: Partial<Claim>): Promise<Claim> {
  return post('/claims', data);
}

export async function updateClaim(
  id: string,
  data: Partial<Claim>
): Promise<Claim> {
  return put(`/claims/${id}`, data);
}

export async function deleteClaim(id: string): Promise<void> {
  return del(`/claims/${id}`);
}

export async function updateClaimStatus(
  id: string,
  status: string,
  notes?: string
): Promise<Claim> {
  return put(`/claims/${id}/status`, { status, notes });
}

export async function getClaimStats(): Promise<Record<string, unknown>> {
  return get('/claims/stats');
}

export async function getClaimAnomalies(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<Claim>> {
  return get('/claims/anomalies', params);
}
