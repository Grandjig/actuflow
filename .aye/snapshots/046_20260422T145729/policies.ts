/**
 * Policy API functions.
 */

import { get, post, put, del } from './client';
import type { Policy, Policyholder } from '@/types/models';

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export async function getPolicies(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<Policy>> {
  return get('/policies', params);
}

export async function getPolicy(id: string): Promise<Policy> {
  return get(`/policies/${id}`);
}

export async function createPolicy(data: Partial<Policy>): Promise<Policy> {
  return post('/policies', data);
}

export async function updatePolicy(
  id: string,
  data: Partial<Policy>
): Promise<Policy> {
  return put(`/policies/${id}`, data);
}

export async function deletePolicy(id: string): Promise<void> {
  return del(`/policies/${id}`);
}

export async function getPolicyStats(): Promise<Record<string, unknown>> {
  return get('/policies/stats');
}

export async function exportPolicies(
  params?: Record<string, unknown>
): Promise<Blob> {
  const response = await fetch(`/api/v1/policies/export?${new URLSearchParams(params as Record<string, string>)}`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    },
  });
  return response.blob();
}

// Policyholders

export async function getPolicyholders(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<Policyholder>> {
  return get('/policyholders', params);
}

export async function getPolicyholder(id: string): Promise<Policyholder> {
  return get(`/policyholders/${id}`);
}

export async function createPolicyholder(
  data: Partial<Policyholder>
): Promise<Policyholder> {
  return post('/policyholders', data);
}

export async function updatePolicyholder(
  id: string,
  data: Partial<Policyholder>
): Promise<Policyholder> {
  return put(`/policyholders/${id}`, data);
}
