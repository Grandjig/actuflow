/**
 * Calculations API functions.
 */

import { get, post, del } from './client';
import type { CalculationRun, CalculationResult, CalculationProgress } from '@/types/models';

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export async function getCalculationRuns(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<CalculationRun>> {
  return get('/calculations', params);
}

export async function getCalculationRun(id: string): Promise<CalculationRun> {
  return get(`/calculations/${id}`);
}

export async function createCalculationRun(
  data: Record<string, unknown>
): Promise<CalculationRun> {
  return post('/calculations', data);
}

export async function cancelCalculationRun(id: string): Promise<void> {
  return del(`/calculations/${id}/cancel`);
}

export async function getCalculationProgress(
  id: string
): Promise<CalculationProgress> {
  return get(`/calculations/${id}/progress`);
}

export async function getCalculationResults(
  runId: string,
  params?: Record<string, unknown>
): Promise<PaginatedResponse<CalculationResult>> {
  return get(`/calculations/${runId}/results`, params);
}

export async function getCalculationSummary(
  runId: string
): Promise<Record<string, unknown>> {
  return get(`/calculations/${runId}/summary`);
}

export async function getCalculationNarrative(runId: string): Promise<string> {
  const response = await get<{ narrative: string }>(`/calculations/${runId}/narrative`);
  return response.narrative;
}

export async function getCalculationAnomalies(
  runId: string,
  params?: Record<string, unknown>
): Promise<PaginatedResponse<CalculationResult>> {
  return get(`/calculations/${runId}/anomalies`, params);
}

export async function exportCalculationResults(
  runId: string,
  format: 'csv' | 'excel' = 'csv'
): Promise<Blob> {
  const response = await fetch(
    `/api/v1/calculations/${runId}/results/export?format=${format}`,
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    }
  );
  return response.blob();
}

export async function compareCalculations(
  runIds: string[]
): Promise<Record<string, unknown>> {
  return post('/calculations/compare', { run_ids: runIds });
}
