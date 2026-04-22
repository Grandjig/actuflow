/**
 * Reports API functions.
 */

import { get, post, put, del } from './client';
import type { ReportTemplate, GeneratedReport } from '@/types/models';

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

// Report Templates

export async function getReportTemplates(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<ReportTemplate>> {
  return get('/report-templates', params);
}

export async function getReportTemplate(id: string): Promise<ReportTemplate> {
  return get(`/report-templates/${id}`);
}

export async function createReportTemplate(
  data: Partial<ReportTemplate>
): Promise<ReportTemplate> {
  return post('/report-templates', data);
}

export async function updateReportTemplate(
  id: string,
  data: Partial<ReportTemplate>
): Promise<ReportTemplate> {
  return put(`/report-templates/${id}`, data);
}

export async function deleteReportTemplate(id: string): Promise<void> {
  return del(`/report-templates/${id}`);
}

// Generated Reports

export async function getGeneratedReports(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<GeneratedReport>> {
  return get('/reports', params);
}

export async function getGeneratedReport(id: string): Promise<GeneratedReport> {
  return get(`/reports/${id}`);
}

export async function generateReport(
  data: Record<string, unknown>
): Promise<GeneratedReport> {
  return post('/reports/generate', data);
}

export async function downloadReport(id: string): Promise<Blob> {
  const response = await fetch(`/api/v1/reports/${id}/download`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    },
  });
  return response.blob();
}
