import { get, post } from './client';
import type {
  AIFeatures,
  NaturalLanguageQuery,
  ParsedIntent,
  QueryFeedback,
  QueryHistoryItem,
  NarrativeRequest,
  NarrativeResponse,
  SemanticSearchRequest,
  SemanticSearchResult,
  DocumentExtractionResult,
} from '@/types/ai';

export const aiApi = {
  // Features
  getFeatures: () =>
    get<AIFeatures>('/ai/features'),

  checkHealth: () =>
    get<{ healthy: boolean }>('/ai/health'),

  // Natural Language Queries
  query: (data: NaturalLanguageQuery) =>
    post<ParsedIntent>('/ai/query', data),

  submitFeedback: (queryId: string, feedback: QueryFeedback) =>
    post<{ message: string }>(`/ai/query/${queryId}/feedback`, feedback),

  getQueryHistory: (limit?: number) =>
    get<QueryHistoryItem[]>('/ai/query-history', { limit }),

  // Narrative Generation
  generateNarrative: (data: NarrativeRequest) =>
    post<NarrativeResponse>('/ai/generate-narrative', data),

  // Semantic Search
  search: (data: SemanticSearchRequest) =>
    post<SemanticSearchResult[]>('/ai/search', data),

  // Document Extraction (base64 encoded)
  extractDocument: (contentBase64: string, filename: string, documentType?: string) =>
    post<DocumentExtractionResult>('/extract/document-base64', {
      content_base64: contentBase64,
      filename,
      document_type: documentType,
    }),
};
