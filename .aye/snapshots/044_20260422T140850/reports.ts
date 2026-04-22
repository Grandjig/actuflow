import { get, post, put, del, downloadFile } from './client';
import type { PaginatedResponse, PaginationParams, SuccessResponse } from '@/types/api';
import type { ReportTemplate, GeneratedReport } from '@/types/models';

export interface ReportTemplateCreateData {
  name: string;
  code: string;
  description?: string;
  report_type: string;
  regulatory_standard?: string;
  output_format: string;
  template_config: Record<string, unknown>;
  include_ai_narrative?: boolean;
}

export interface GenerateReportRequest {
  report_template_id: string;
  reporting_period_start: string;
  reporting_period_end: string;
  parameters?: Record<string, unknown>;
}

export const reportsApi = {
  // Templates
  listTemplates: (params?: PaginationParams & { report_type?: string; regulatory_standard?: string }) =>
    get<PaginatedResponse<ReportTemplate>>('/reports/templates', params),

  getTemplate: (id: string) => 
    get<ReportTemplate>(`/reports/templates/${id}`),

  createTemplate: (data: ReportTemplateCreateData) => 
    post<ReportTemplate>('/reports/templates', data),

  updateTemplate: (id: string, data: Partial<ReportTemplateCreateData>) => 
    put<ReportTemplate>(`/reports/templates/${id}`, data),

  deleteTemplate: (id: string) => 
    del<SuccessResponse>(`/reports/templates/${id}`),

  // Generated Reports
  list: (params?: PaginationParams & { template_id?: string; status?: string }) =>
    get<PaginatedResponse<GeneratedReport>>('/reports', params),

  get: (id: string) => 
    get<GeneratedReport>(`/reports/${id}`),

  generate: (data: GenerateReportRequest) => 
    post<GeneratedReport>('/reports/generate', data),

  download: (id: string, filename: string) =>
    downloadFile(`/reports/${id}/download`, filename),
};
