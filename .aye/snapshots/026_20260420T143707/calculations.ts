import { get, post } from './client';
import type { PaginatedResponse, CalculationListParams, CalculationProgress, CalculationSummary } from '@/types/api';
import type { CalculationRun } from '@/types/models';

export interface CalculationCreateData {
  run_name: string;
  model_definition_id: string;
  assumption_set_id: string;
  policy_filter?: Record<string, unknown>;
  parameters?: Record<string, unknown>;
}

export const calculationsApi = {
  list: (params?: CalculationListParams) =>
    get<PaginatedResponse<CalculationRun>>('/calculations', params),

  get: (id: string) =>
    get<CalculationRun>(`/calculations/${id}`),

  create: (data: CalculationCreateData) =>
    post<CalculationRun>('/calculations', data),

  cancel: (id: string) =>
    post<void>(`/calculations/${id}/cancel`),

  getProgress: (id: string) =>
    get<CalculationProgress>(`/calculations/${id}/progress`),

  getSummary: (id: string) =>
    get<CalculationSummary>(`/calculations/${id}/summary`),

  getNarrative: (id: string) =>
    get<{ narrative: string; generated_at: string }>(`/calculations/${id}/narrative`),

  getResults: (id: string, params?: Record<string, unknown>) =>
    get<PaginatedResponse<any>>(`/calculations/${id}/results`, params),
};
