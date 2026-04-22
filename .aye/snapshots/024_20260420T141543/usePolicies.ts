import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { policiesApi } from '@/api/policies';
import type { PolicyListParams } from '@/types/api';
import type { Policy } from '@/types/models';

export function usePolicies(params: PolicyListParams = {}) {
  return useQuery({
    queryKey: ['policies', params],
    queryFn: () => policiesApi.list(params),
  });
}

export function usePolicy(id: string) {
  return useQuery({
    queryKey: ['policies', id],
    queryFn: () => policiesApi.get(id),
    enabled: !!id,
  });
}

export function usePolicyStats() {
  return useQuery({
    queryKey: ['policies', 'stats'],
    queryFn: () => policiesApi.getStats(),
  });
}

export function usePolicyHistory(id: string) {
  return useQuery({
    queryKey: ['policies', id, 'history'],
    queryFn: () => policiesApi.getHistory(id),
    enabled: !!id,
  });
}

export function useCreatePolicy() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: policiesApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['policies'] });
    },
  });
}

export function useUpdatePolicy() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Policy> }) =>
      policiesApi.update(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['policies'] });
      queryClient.invalidateQueries({ queryKey: ['policies', id] });
    },
  });
}

export function useDeletePolicy() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: policiesApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['policies'] });
    },
  });
}
