/**
 * AI API functions.
 */

import { get, post } from './client';

interface NaturalLanguageResponse {
  intent: string;
  results: Array<{
    type: string;
    id: string;
    title: string;
    description?: string;
    score?: number;
  }>;
  message?: string;
}

export async function sendNaturalLanguageQuery(
  query: string
): Promise<NaturalLanguageResponse> {
  return post('/ai/query', { query });
}

export async function getQueryHistory(): Promise<
  Array<{
    id: string;
    query_text: string;
    timestamp: string;
  }>
> {
  return get('/ai/query-history');
}

export async function submitQueryFeedback(
  queryId: string,
  helpful: boolean
): Promise<void> {
  return post(`/ai/query/${queryId}/feedback`, { was_helpful: helpful });
}

export async function extractDocumentData(
  documentId: string
): Promise<Record<string, unknown>> {
  return post(`/ai/extract-document`, { document_id: documentId });
}

export async function semanticSearch(
  query: string,
  resourceType?: string,
  limit?: number
): Promise<
  Array<{
    id: string;
    type: string;
    title: string;
    score: number;
  }>
> {
  return post('/search/semantic', { query, resource_type: resourceType, limit });
}

export async function generateNarrative(
  resourceType: string,
  resourceId: string
): Promise<{ narrative: string }> {
  return post('/ai/generate-narrative', {
    resource_type: resourceType,
    resource_id: resourceId,
  });
}
