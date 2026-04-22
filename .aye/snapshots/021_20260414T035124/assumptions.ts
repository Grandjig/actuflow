import { get, post, put, del } from './client';
import type { PaginatedResponse, AssumptionSetFilters, SuccessResponse } from '@/types/api';
import type { AssumptionSet, AssumptionTable } from '@/types/models';
import type { AIRecommendation } from '@/types/models';

export interface AssumptionSetCreateData {
  name: string;
  version: string;
  description?: string;
  effective_date: string;
  line_of_business?: string;
}

export interface AssumptionSetUpdateData {
  name?: string;
  description?: string;
  effective_date?: string;
}

export interface AssumptionTableCreateData {
  table_type: string;
  name: string;
  description?: string;
  data: Record<string, unknown>[];
}

export interface AssumptionComparison {
  table_type: string;
  differences: {
    key: string;
    value1: unknown;
    value2: unknown;
    change_percent?: number;
  }[];
}

export const assumptionsApi = {
  // Assumption Sets
  list: (params?: AssumptionSetFilters) =>
    get<PaginatedResponse<AssumptionSet>>('/assumption-sets', params),

  get: (id: string) => 
    get<AssumptionSet>(`/assumption-sets/${id}`),

  create: (data: AssumptionSetCreateData) => 
    post<AssumptionSet>('/assumption-sets', data),

  update: (id: string, data: AssumptionSetUpdateData) => 
    put<AssumptionSet>(`/assumption-sets/${id}`, data),

  delete: (id: string) => 
    del<SuccessResponse>(`/assumption-sets/${id}`),

  clone: (id: string, newName: string, newVersion: string) =>
    post<AssumptionSet>(`/assumption-sets/${id}/clone`, { name: newName, version: newVersion }),

  submit: (id: string) =>
    post<AssumptionSet>(`/assumption-sets/${id}/submit`),

  approve: (id: string, comments?: string) =>
    post<AssumptionSet>(`/assumption-sets/${id}/approve`, { comments }),

  reject: (id: string, reason: string) =>
    post<AssumptionSet>(`/assumption-sets/${id}/reject`, { reason }),

  compare: (id1: string, id2: string) =>
    get<AssumptionComparison[]>(`/assumption-sets/${id1}/compare/${id2}`),

  getApproved: () =>
    get<AssumptionSet[]>('/assumption-sets/approved'),

  // Experience recommendations
  getExperienceRecommendations: (id: string) =>
    get<AIRecommendation[]>(`/assumption-sets/${id}/experience-recommendations`),

  // Assumption Tables
  getTables: (setId: string) =>
    get<AssumptionTable[]>(`/assumption-sets/${setId}/tables`),

  getTable: (setId: string, tableId: string) =>
    get<AssumptionTable>(`/assumption-sets/${setId}/tables/${tableId}`),

  createTable: (setId: string, data: AssumptionTableCreateData) =>
    post<AssumptionTable>(`/assumption-sets/${setId}/tables`, data),

  updateTable: (setId: string, tableId: string, data: Partial<AssumptionTableCreateData>) =>
    put<AssumptionTable>(`/assumption-sets/${setId}/tables/${tableId}`, data),

  deleteTable: (setId: string, tableId: string) =>
    del<SuccessResponse>(`/assumption-sets/${setId}/tables/${tableId}`),
};
