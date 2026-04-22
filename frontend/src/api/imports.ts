/**
 * Data import API functions.
 */

import { get, post, del } from './client';
import type { DataImport, DataQualityIssue } from '@/types/models';

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export async function getImports(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<DataImport>> {
  return get('/imports', params);
}

export async function getImport(id: string): Promise<DataImport> {
  return get(`/imports/${id}`);
}

export async function uploadImport(
  file: File,
  importType: string
): Promise<DataImport> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('import_type', importType);

  return post('/imports/upload', formData);
}

export async function setColumnMapping(
  id: string,
  mapping: Record<string, string>
): Promise<DataImport> {
  return post(`/imports/${id}/mapping`, { column_mapping: mapping });
}

export async function validateImport(
  id: string
): Promise<{ valid: boolean; issues: DataQualityIssue[] }> {
  return post(`/imports/${id}/validate`);
}

export async function commitImport(id: string): Promise<DataImport> {
  return post(`/imports/${id}/commit`);
}

export async function cancelImport(id: string): Promise<void> {
  return del(`/imports/${id}`);
}

export async function getAISuggestions(
  id: string
): Promise<{
  column_mapping: Record<string, string>;
  data_issues: DataQualityIssue[];
}> {
  return get(`/imports/${id}/ai-suggestions`);
}
