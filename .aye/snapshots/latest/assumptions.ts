import { get, post, put, del } from './client';
import type { PaginatedResponse } from '@/types/api';
import type {
  AssumptionSetFilters,
  AssumptionSetCreateRequest,
  AssumptionSetUpdateRequest,
  AssumptionTableCreateRequest,
} from '@/types/api';
import type { AssumptionSet, AssumptionTable, ExperienceRecommendation } from '@/types/models';

export const assumptionsApi = {
  list: (params?: AssumptionSetFilters) =>
    get<PaginatedResponse<AssumptionSet>>('/assumption-sets', params),

  get: (id: string) =>
    get<AssumptionSet>(`/assumption-sets/${id}`),

  create: (data: AssumptionSetCreateRequest) =>
    post<AssumptionSet>('/assumption-sets', data),

  update: (id: string, data: AssumptionSetUpdateRequest) =>
    put<AssumptionSet>(`/assumption-sets/${id}`, data),

  delete: (id: string) =>
    del<void>(`/assumption-sets/${id}`),

  getApproved: () =>
    get<AssumptionSet[]>('/assumption-sets/approved'),

  submit: (id: string) =>
    post<AssumptionSet>(`/assumption-sets/${id}/submit`),

  approve: (id: string, notes?: string) =>
    post<AssumptionSet>(`/assumption-sets/${id}/approve`, { approval_notes: notes }),

  reject: (id: string, reason: string) =>
    post<AssumptionSet>(`/assumption-sets/${id}/reject`, { rejection_reason: reason }),

  compare: (id: string, otherId: string) =>
    get<any>(`/assumption-sets/${id}/compare/${otherId}`),

  // Tables
  getTables: (setId: string) =>
    get<AssumptionTable[]>(`/assumption-sets/${setId}/tables`),

  createTable: (setId: string, data: AssumptionTableCreateRequest) =>
    post<AssumptionTable>(`/assumption-sets/${setId}/tables`, data),

  updateTable: (setId: string, tableId: string, data: Partial<AssumptionTableCreateRequest>) =>
    put<AssumptionTable>(`/assumption-sets/${setId}/tables/${tableId}`, data),

  deleteTable: (setId: string, tableId: string) =>
    del<void>(`/assumption-sets/${setId}/tables/${tableId}`),

  // AI Recommendations
  getExperienceRecommendations: (setId: string) =>
    get<ExperienceRecommendation[]>(`/assumption-sets/${setId}/recommendations`),
};
