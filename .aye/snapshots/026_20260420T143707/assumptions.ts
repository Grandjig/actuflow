import { get, post, put, del } from './client';
import type { PaginatedResponse, AssumptionSetFilters } from '@/types/api';
import type { AssumptionSet, AssumptionTable, ExperienceRecommendation } from '@/types/models';

export interface AssumptionSetCreate {
  name: string;
  version: string;
  description?: string;
  effective_date?: string;
  line_of_business?: string;
}

export interface AssumptionSetUpdate {
  name?: string;
  description?: string;
  effective_date?: string;
}

export interface AssumptionTableCreate {
  table_type: string;
  name: string;
  description?: string;
  data: Record<string, unknown>;
  metadata?: Record<string, unknown>;
}

export const assumptionsApi = {
  list: (params?: AssumptionSetFilters) =>
    get<PaginatedResponse<AssumptionSet>>('/assumption-sets', params),

  get: (id: string) =>
    get<AssumptionSet>(`/assumption-sets/${id}`),

  getApproved: () =>
    get<AssumptionSet[]>('/assumption-sets/approved'),

  create: (data: AssumptionSetCreate) =>
    post<AssumptionSet>('/assumption-sets', data),

  update: (id: string, data: AssumptionSetUpdate) =>
    put<AssumptionSet>(`/assumption-sets/${id}`, data),

  delete: (id: string) =>
    del<void>(`/assumption-sets/${id}`),

  submit: (id: string) =>
    post<AssumptionSet>(`/assumption-sets/${id}/submit`),

  approve: (id: string, notes?: string) =>
    post<AssumptionSet>(`/assumption-sets/${id}/approve`, { approval_notes: notes }),

  reject: (id: string, reason: string) =>
    post<AssumptionSet>(`/assumption-sets/${id}/reject`, { rejection_reason: reason }),

  // Tables
  getTables: (setId: string) =>
    get<AssumptionTable[]>(`/assumption-sets/${setId}/tables`),

  getTable: (setId: string, tableId: string) =>
    get<AssumptionTable>(`/assumption-sets/${setId}/tables/${tableId}`),

  createTable: (setId: string, data: AssumptionTableCreate) =>
    post<AssumptionTable>(`/assumption-sets/${setId}/tables`, data),

  updateTable: (setId: string, tableId: string, data: Partial<AssumptionTableCreate>) =>
    put<AssumptionTable>(`/assumption-sets/${setId}/tables/${tableId}`, data),

  deleteTable: (setId: string, tableId: string) =>
    del<void>(`/assumption-sets/${setId}/tables/${tableId}`),

  // Comparison
  compare: (id1: string, id2: string) =>
    get<any>(`/assumption-sets/${id1}/compare/${id2}`),

  // AI recommendations
  getExperienceRecommendations: (setId: string) =>
    get<ExperienceRecommendation[]>(`/assumption-sets/${setId}/recommendations`),
};
