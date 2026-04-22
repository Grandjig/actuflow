import { useMutation, useQuery } from '@tanstack/react-query';
import { get, post } from '@/api/client';
import { useAIStore } from '@/stores/aiStore';
import type { NLQueryRequest, NLQueryResponse, NarrativeRequest, NarrativeResponse } from '@/types/ai';

const aiApi = {
  status: () => get<{ enabled: boolean; healthy: boolean; features: Record<string, boolean> }>('/ai/status'),
  query: (data: NLQueryRequest) => post<NLQueryResponse>('/ai/query', data),
  narrative: (data: NarrativeRequest) => post<NarrativeResponse>('/ai/narrative', data),
  search: (query: string, resourceType?: string) =>
    post<{ results: any[]; total: number }>('/ai/search', { query, resource_type: resourceType }),
};

export function useAIStatus() {
  return useQuery({
    queryKey: ['ai', 'status'],
    queryFn: aiApi.status,
    staleTime: 5 * 60 * 1000, // Cache for 5 minutes
  });
}

export function useNaturalLanguageQuery() {
  const { setLastQuery, setLastResponse, addToHistory, setIsPending, setError } = useAIStore();

  return useMutation({
    mutationFn: aiApi.query,
    onMutate: (variables) => {
      setIsPending(true);
      setLastQuery(variables.query);
      setError(null);
    },
    onSuccess: (data) => {
      setLastResponse(data);
      addToHistory(data.query);
      setIsPending(false);
    },
    onError: (error: any) => {
      setError(error.message || 'AI query failed');
      setIsPending(false);
    },
  });
}

export function useGenerateNarrative() {
  return useMutation({
    mutationFn: aiApi.narrative,
  });
}

export function useSemanticSearch() {
  return useMutation({
    mutationFn: ({ query, resourceType }: { query: string; resourceType?: string }) =>
      aiApi.search(query, resourceType),
  });
}
