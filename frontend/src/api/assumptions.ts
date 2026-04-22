/**
 * Assumptions API functions.
 */

import { get, post, put, del } from './client';
import type { AssumptionSet, AssumptionTable } from '@/types/models';

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

// Assumption Sets

export async function getAssumptionSets(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<AssumptionSet>> {
  return get('/assumption-sets', params);
}

export async function getAssumptionSet(id: string): Promise<AssumptionSet> {
  return get(`/assumption-sets/${id}`);
}

export async function createAssumptionSet(
  data: Partial<AssumptionSet>
): Promise<AssumptionSet> {
  return post('/assumption-sets', data);
}

export async function updateAssumptionSet(
  id: string,
  data: Partial<AssumptionSet>
): Promise<AssumptionSet> {
  return put(`/assumption-sets/${id}`, data);
}

export async function deleteAssumptionSet(id: string): Promise<void> {
  return del(`/assumption-sets/${id}`);
}

export async function cloneAssumptionSet(
  id: string,
  name: string
): Promise<AssumptionSet> {
  return post(`/assumption-sets/${id}/clone`, { name });
}

export async function submitAssumptionSet(id: string): Promise<AssumptionSet> {
  return post(`/assumption-sets/${id}/submit`);
}

export async function approveAssumptionSet(
  id: string,
  notes?: string
): Promise<AssumptionSet> {
  return post(`/assumption-sets/${id}/approve`, { notes });
}

export async function rejectAssumptionSet(
  id: string,
  reason: string
): Promise<AssumptionSet> {
  return post(`/assumption-sets/${id}/reject`, { reason });
}

// Assumption Tables

export async function getAssumptionTable(
  setId: string,
  tableId: string
): Promise<AssumptionTable> {
  return get(`/assumption-sets/${setId}/tables/${tableId}`);
}

export async function createAssumptionTable(
  setId: string,
  data: Partial<AssumptionTable>
): Promise<AssumptionTable> {
  return post(`/assumption-sets/${setId}/tables`, data);
}

export async function updateAssumptionTable(
  setId: string,
  tableId: string,
  data: Partial<AssumptionTable>
): Promise<AssumptionTable> {
  return put(`/assumption-sets/${setId}/tables/${tableId}`, data);
}

export async function deleteAssumptionTable(
  setId: string,
  tableId: string
): Promise<void> {
  return del(`/assumption-sets/${setId}/tables/${tableId}`);
}
