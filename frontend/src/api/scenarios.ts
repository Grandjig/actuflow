/**
 * Scenarios API functions.
 */

import { get, post, put, del } from './client';
import type { Scenario, ScenarioResult } from '@/types/models';

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export async function getScenarios(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<Scenario>> {
  return get('/scenarios', params);
}

export async function getScenario(id: string): Promise<Scenario> {
  return get(`/scenarios/${id}`);
}

export async function createScenario(
  data: Partial<Scenario>
): Promise<Scenario> {
  return post('/scenarios', data);
}

export async function updateScenario(
  id: string,
  data: Partial<Scenario>
): Promise<Scenario> {
  return put(`/scenarios/${id}`, data);
}

export async function deleteScenario(id: string): Promise<void> {
  return del(`/scenarios/${id}`);
}

export async function runScenario(id: string): Promise<ScenarioResult> {
  return post(`/scenarios/${id}/run`);
}

export async function getScenarioResults(
  id: string
): Promise<ScenarioResult[]> {
  return get(`/scenarios/${id}/results`);
}

export async function compareScenarios(
  scenarioIds: string[]
): Promise<Record<string, unknown>> {
  return post('/scenarios/compare', { scenario_ids: scenarioIds });
}
