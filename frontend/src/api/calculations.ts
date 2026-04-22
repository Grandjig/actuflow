import { get, post, put, del } from './client';
import type { PaginatedResponse } from '@/types/api';
import type {
  CalculationListParams,
  CalculationCreateRequest,
  CalculationProgress,
  CalculationSummary,
} from '@/types/api';
import type { CalculationRun } from '@/types/models';

export const calculationsApi = {
  list: (params?: CalculationListParams) =>
    get<PaginatedResponse<CalculationRun>>('/calculations', params),

  get: (id: string) =>
    get<CalculationRun>(`/calculations/${id}`),

  create: (data: CalculationCreateRequest) =>
    post<CalculationRun>('/calculations', data),

  cancel: (id: string) =>
    post<CalculationRun>(`/calculations/${id}/cancel`),

  getProgress: (id: string) =>
    get<CalculationProgress>(`/calculations/${id}/progress`),

  getSummary: (id: string) =>
    get<CalculationSummary>(`/calculations/${id}/summary`),

  getResults: (id: string, params?: Record<string, unknown>) =>
    get<PaginatedResponse<any>>(`/calculations/${id}/results`, params),

  getNarrative: (id: string) =>
    get<{ narrative: string; generated: boolean }>(`/calculations/${id}/narrative`),

  getAnomalies: (id: string) =>
    get<any[]>(`/calculations/${id}/anomalies`),

  compare: (id1: string, id2: string) =>
    get<any>('/calculations/compare', { run_id_1: id1, run_id_2: id2 }),
};
