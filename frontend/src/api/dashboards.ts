import { get, post, put, del } from './client';
import type { SuccessResponse } from '@/types/api';
import type { DashboardConfig, WidgetConfig } from '@/types/models';

export interface DashboardCreateData {
  name: string;
  description?: string;
  layout?: Record<string, unknown>;
  widgets?: WidgetConfig[];
  is_shared?: boolean;
  is_default?: boolean;
}

export interface DashboardUpdateData {
  name?: string;
  description?: string;
  layout?: Record<string, unknown>;
  widgets?: WidgetConfig[];
  is_shared?: boolean;
  is_default?: boolean;
  theme?: Record<string, unknown>;
}

export interface WidgetDataRequest {
  widget_type: string;
  data_source: string;
  config?: Record<string, unknown>;
  filters?: Record<string, unknown>;
  date_range?: { start: string; end: string };
}

export interface WidgetDataResponse {
  widget_type: string;
  data: Record<string, unknown> | unknown[];
  metadata?: Record<string, unknown>;
}

export const dashboardsApi = {
  list: () =>
    get<DashboardConfig[]>('/dashboards'),

  get: (id: string) => 
    get<DashboardConfig>(`/dashboards/${id}`),

  getDefault: () =>
    get<DashboardConfig | null>('/dashboards/default'),

  create: (data: DashboardCreateData) => 
    post<DashboardConfig>('/dashboards', data),

  update: (id: string, data: DashboardUpdateData) => 
    put<DashboardConfig>(`/dashboards/${id}`, data),

  delete: (id: string) => 
    del<SuccessResponse>(`/dashboards/${id}`),

  share: (id: string) =>
    post<DashboardConfig>(`/dashboards/${id}/share`),

  getWidgetData: (data: WidgetDataRequest) =>
    post<WidgetDataResponse>('/dashboards/widgets/data', data),
};
