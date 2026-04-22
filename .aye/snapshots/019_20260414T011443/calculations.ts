import { get, post, del, downloadFile } from './client';
import type { PaginatedResponse, CalculationRunFilters, SuccessResponse } from '@/types/api';
import type { CalculationRun, CalculationResult } from '@/types/models';
import type { AnomalyAlert } from '@/types/ai';

export interface CalculationRunCreateData {
  run_name: string;
  model_definition_id: string;
  assumption_set_id: string;
  policy_filter?: Record<string, unknown>;
  parameters?: Record<string, unknown>;
}

export interface CalculationProgress {
  run_id: string;
  status: string;
  progress_percent: number;
  progress_message?: string;
  started_at?: string;
  estimated_completion?: string;
}

export interface CalculationSummary {
  run_id: string;
  policy_count: number;
  result_summary: Record<string, unknown>;
  duration_seconds?: number;
}

export interface CalculationResultFilter {
  policy_id?: string;
  result_type?: string;
  projection_month?: number;
  anomaly_only?: boolean;
  page?: number;
  page_size?: number;
}

export const calculationsApi = {
  list: (params?: CalculationRunFilters) =>
    get<PaginatedResponse<CalculationRun>>('/calculations', params),

  get: (id: string) => 
    get<CalculationRun>(`/calculations/${id}`),

  create: (data: CalculationRunCreateData) => 
    post<CalculationRun>('/calculations', data),

  cancel: (id: string) => 
    del<SuccessResponse>(`/calculations/${id}/cancel`),

  getProgress: (id: string) =>
    get<CalculationProgress>(`/calculations/${id}/progress`),

  getResults: (id: string, params?: CalculationResultFilter) =>
    get<PaginatedResponse<CalculationResult>>(`/calculations/${id}/results`, params),

  exportResults: (id: string, format: 'csv' | 'excel' = 'csv') =>
    downloadFile(`/calculations/${id}/results/export?format=${format}`, `calculation_${id}.${format === 'excel' ? 'xlsx' : 'csv'}`),

  getSummary: (id: string) =>
    get<CalculationSummary>(`/calculations/${id}/summary`),

  // AI-generated narrative
  getNarrative: (id: string) =>
    get<{ narrative: string; generated_at: string }>(`/calculations/${id}/narrative`),

  // AI-detected anomalies in results
  getAnomalies: (id: string) =>
    get<(CalculationResult & { anomaly_details: AnomalyAlert })[]>(`/calculations/${id}/anomalies`),

  rerun: (id: string) =>
    post<CalculationRun>(`/calculations/${id}/rerun`),

  compare: (runIds: string[]) =>
    get<{ runs: CalculationRun[]; comparison: Record<string, unknown> }>('/calculations/compare', { run_ids: runIds.join(',') }),
};
