import { get, del, uploadFile } from './client';
import type { PaginatedResponse, PaginationParams, SuccessResponse } from '@/types/api';
import type { Document } from '@/types/models';
import type { SemanticSearchResult } from '@/types/ai';

export interface DocumentUploadParams {
  document_type?: string;
  related_resource_type?: string;
  related_resource_id?: string;
  extract_data?: boolean;
}

export const documentsApi = {
  list: (params?: PaginationParams & { document_type?: string; related_resource_type?: string; related_resource_id?: string }) =>
    get<PaginatedResponse<Document>>('/documents', params),

  get: (id: string) => 
    get<Document>(`/documents/${id}`),

  upload: (file: File, params?: DocumentUploadParams, onProgress?: (progress: number) => void) => {
    const additionalData: Record<string, string> = {};
    if (params?.document_type) additionalData.document_type = params.document_type;
    if (params?.related_resource_type) additionalData.related_resource_type = params.related_resource_type;
    if (params?.related_resource_id) additionalData.related_resource_id = params.related_resource_id;
    if (params?.extract_data !== undefined) additionalData.extract_data = String(params.extract_data);
    
    return uploadFile<Document>('/documents/upload', file, additionalData, onProgress);
  },

  search: (query: string, limit?: number) =>
    get<SemanticSearchResult[]>('/documents/search', { query, limit }),

  delete: (id: string) => 
    del<SuccessResponse>(`/documents/${id}`),
};
