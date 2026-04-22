/**
 * Model definitions API functions.
 */

import { get, post, put, del } from './client';
import type { ModelDefinition } from '@/types/models';

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export async function getModelDefinitions(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<ModelDefinition>> {
  return get('/models', params);
}

export async function getModelDefinition(id: string): Promise<ModelDefinition> {
  return get(`/models/${id}`);
}

export async function createModelDefinition(
  data: Partial<ModelDefinition>
): Promise<ModelDefinition> {
  return post('/models', data);
}

export async function updateModelDefinition(
  id: string,
  data: Partial<ModelDefinition>
): Promise<ModelDefinition> {
  return put(`/models/${id}`, data);
}

export async function deleteModelDefinition(id: string): Promise<void> {
  return del(`/models/${id}`);
}

export async function cloneModelDefinition(
  id: string,
  name: string
): Promise<ModelDefinition> {
  return post(`/models/${id}/clone`, { name });
}

export async function validateModelDefinition(
  id: string
): Promise<{ valid: boolean; errors: string[] }> {
  return post(`/models/${id}/validate`);
}

export async function getModelTemplates(): Promise<ModelDefinition[]> {
  return get('/model-templates');
}
