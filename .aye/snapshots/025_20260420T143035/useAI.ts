import { useMutation, useQuery } from '@tanstack/react-query';
import { post, get } from '@/api/client';
import { useAIStore } from '@/stores/aiStore';
import type { NLQueryResponse, AIStatus } from '@/types/ai';

export function useAIStatus() {
  return useQuery({
    queryKey: ['ai', 'status'],
    queryFn: () => get<AIStatus>('/ai/status'),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useNaturalLanguageQuery() {
  const { setLastQuery, setLastResponse, addToHistory, setIsPending, setError } = useAIStore();

  return useMutation({
    mutationFn: async ({ query, context }: { query: string; context?: Record<string, unknown> }) => {
      setIsPending(true);
      setError(null);
      setLastQuery(query);
      addToHistory(query);

      const response = await post<NLQueryResponse>('/ai/query', { query, context });
      return response;
    },
    onSuccess: (data) => {
      setLastResponse(data as any);
      setIsPending(false);
    },
    onError: (error: Error) => {
      setError(error.message);
      setIsPending(false);
    },
  });
}

export function useQueryFeedback() {
  return useMutation({
    mutationFn: ({ queryId, wasHelpful, feedback }: {
      queryId: string;
      wasHelpful: boolean;
      feedback?: string;
    }) => post(`/ai/feedback/${queryId}`, { was_helpful: wasHelpful, feedback }),
  });
}

export function useGenerateNarrative() {
  return useMutation({
    mutationFn: ({ resourceType, resourceId, style }: {
      resourceType: string;
      resourceId: string;
      style?: string;
    }) =>
      post<{ narrative: string; generated_at: string }>('/ai/narrative', {
        resource_type: resourceType,
        resource_id: resourceId,
        style,
      }),
  });
}

export function useSemanticSearch() {
  return useMutation({
    mutationFn: ({ query, resourceTypes, limit }: {
      query: string;
      resourceTypes?: string[];
      limit?: number;
    }) =>
      post<{ results: any[]; total: number }>('/ai/search', {
        query,
        resource_types: resourceTypes,
        limit,
      }),
  });
}
