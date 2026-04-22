import { get, post, put, del } from './client';
import type { PaginatedResponse, ModelFilters, SuccessResponse } from '@/types/api';
import type { ModelDefinition } from '@/types/models';

export interface ModelCreateData {
  name: string;
  code: string;
  version: string;
  description?: string;
  model_type: string;
  line_of_business?: string;
  regulatory_standard?: string;
  configuration: Record<string, unknown>;
}

export interface ModelUpdateData {
  name?: string;
  description?: string;
  configuration?: Record<string, unknown>;
  status?: string;
}

export interface ModelValidationResult {
  is_valid: boolean;
  errors: string[];
  warnings: string[];
}

export const modelsApi = {
  list: (params?: ModelFilters) =>
    get<PaginatedResponse<ModelDefinition>>('/models', params),

  get: (id: string) => 
    get<ModelDefinition>(`/models/${id}`),

  create: (data: ModelCreateData) => 
    post<ModelDefinition>('/models', data),

  update: (id: string, data: ModelUpdateData) => 
    put<ModelDefinition>(`/models/${id}`, data),

  delete: (id: string) => 
    del<SuccessResponse>(`/models/${id}`),

  clone: (id: string, newCode: string, newName: string, newVersion: string) =>
    post<ModelDefinition>(`/models/${id}/clone`, {
      new_code: newCode,
      new_name: newName,
      new_version: newVersion,
    }),

  validate: (id: string) =>
    post<ModelValidationResult>(`/models/${id}/validate`),

  activate: (id: string) =>
    post<ModelDefinition>(`/models/${id}/activate`),

  getTemplates: () =>
    get<ModelDefinition[]>('/models/templates'),

  getActive: () =>
    get<ModelDefinition[]>('/models/active'),
};
