import { get, post, put, del } from './client';
import type { PaginatedResponse, PaginationParams, SuccessResponse } from '@/types/api';
import type { Scenario, ScenarioResult } from '@/types/models';

export interface ScenarioCreateData {
  name: string;
  description?: string;
  scenario_type: string;
  base_assumption_set_id: string;
  adjustments: Record<string, unknown>;
}

export interface ScenarioUpdateData {
  name?: string;
  description?: string;
  adjustments?: Record<string, unknown>;
  status?: string;
}

export interface ScenarioRunRequest {
  model_definition_id: string;
  policy_filter?: Record<string, unknown>;
  parameters?: Record<string, unknown>;
  comparison_base_run_id?: string;
}

export interface ScenarioComparison {
  scenarios: Scenario[];
  metrics: Record<string, Record<string, number>>;
  differences: Record<string, Record<string, number>>;
}

export const scenariosApi = {
  list: (params?: PaginationParams & { status?: string; scenario_type?: string; search?: string }) =>
    get<PaginatedResponse<Scenario>>('/scenarios', params),

  get: (id: string) => 
    get<Scenario>(`/scenarios/${id}`),

  create: (data: ScenarioCreateData) => 
    post<Scenario>('/scenarios', data),

  update: (id: string, data: ScenarioUpdateData) => 
    put<Scenario>(`/scenarios/${id}`, data),

  delete: (id: string) => 
    del<SuccessResponse>(`/scenarios/${id}`),

  run: (id: string, data: ScenarioRunRequest) =>
    post<ScenarioResult>(`/scenarios/${id}/run`, data),

  getResults: (id: string) =>
    get<ScenarioResult[]>(`/scenarios/${id}/results`),

  compare: (scenarioIds: string[]) =>
    get<ScenarioComparison>('/scenarios/compare', { scenario_ids: scenarioIds.join(',') }),
};
