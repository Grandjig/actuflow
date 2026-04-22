import { get, post } from './client';
import type { SearchRequest, SearchResponse } from '@/types/api';
import type { SemanticSearchRequest, SemanticSearchResult } from '@/types/ai';

export const searchApi = {
  search: (params: SearchRequest) =>
    get<SearchResponse>('/search', params),

  semanticSearch: (data: SemanticSearchRequest) =>
    post<SemanticSearchResult[]>('/search/semantic', data),
};
