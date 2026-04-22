/**
 * Document API functions.
 */

import { get, post, del } from './client';
import type { Document } from '@/types/models';

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export async function getDocuments(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<Document>> {
  return get('/documents', params);
}

export async function getDocument(id: string): Promise<Document> {
  return get(`/documents/${id}`);
}

export async function uploadDocument(
  file: File,
  metadata?: Record<string, unknown>
): Promise<Document> {
  const formData = new FormData();
  formData.append('file', file);
  
  if (metadata) {
    Object.entries(metadata).forEach(([key, value]) => {
      formData.append(key, String(value));
    });
  }

  return post('/documents/upload', formData);
}

export async function deleteDocument(id: string): Promise<void> {
  return del(`/documents/${id}`);
}

export async function getExtractedData(
  id: string
): Promise<Record<string, unknown>> {
  return get(`/documents/${id}/extracted-data`);
}

export async function searchDocuments(
  query: string,
  limit?: number
): Promise<Array<{ id: string; score: number; title: string }>> {
  return post('/documents/search', { query, limit });
}
