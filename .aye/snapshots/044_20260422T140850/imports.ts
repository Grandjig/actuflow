import { get, post, del, uploadFile } from './client';
import type { PaginatedResponse, PaginationParams, SuccessResponse } from '@/types/api';
import type { DataImport } from '@/types/models';
import type { ColumnMappingSuggestion, DataQualityIssue } from '@/types/ai';

export interface ImportUploadResponse {
  import_id: string;
  file_name: string;
  total_rows: number;
  columns: string[];
  sample_data: Record<string, unknown>[];
}

export interface ColumnMappingRequest {
  column_mapping: Record<string, string>;
}

export interface ValidationResult {
  is_valid: boolean;
  total_rows: number;
  valid_rows: number;
  error_rows: number;
  errors: { row: number; column: string; error: string }[];
}

export interface AISuggestions {
  column_mappings: ColumnMappingSuggestion[];
  data_issues: DataQualityIssue[];
}

export const importsApi = {
  list: (params?: PaginationParams & { status?: string; import_type?: string }) =>
    get<PaginatedResponse<DataImport>>('/imports', params),

  get: (id: string) => 
    get<DataImport>(`/imports/${id}`),

  upload: (file: File, importType: string, onProgress?: (progress: number) => void) =>
    uploadFile<ImportUploadResponse>('/imports/upload', file, { import_type: importType }, onProgress),

  setMapping: (id: string, mapping: ColumnMappingRequest) =>
    post<DataImport>(`/imports/${id}/mapping`, mapping),

  validate: (id: string) =>
    post<ValidationResult>(`/imports/${id}/validate`),

  commit: (id: string) =>
    post<DataImport>(`/imports/${id}/commit`),

  cancel: (id: string) =>
    del<SuccessResponse>(`/imports/${id}/cancel`),

  // AI suggestions
  getAISuggestions: (id: string) =>
    get<AISuggestions>(`/imports/${id}/ai-suggestions`),
};
