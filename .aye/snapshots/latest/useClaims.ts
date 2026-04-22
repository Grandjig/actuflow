import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { claimsApi } from '@/api/claims';
import type { ClaimListParams } from '@/types/api';

export function useClaims(params: ClaimListParams = {}) {
  return useQuery({
    queryKey: ['claims', params],
    queryFn: () => claimsApi.list(params),
  });
}

export function useClaim(id: string) {
  return useQuery({
    queryKey: ['claims', id],
    queryFn: () => claimsApi.get(id),
    enabled: !!id,
  });
}

export function useClaimStats() {
  return useQuery({
    queryKey: ['claims', 'stats'],
    queryFn: () => claimsApi.getStats(),
  });
}

export function useClaimAnomalies(limit?: number) {
  return useQuery({
    queryKey: ['claims', 'anomalies', limit],
    queryFn: () => claimsApi.getAnomalies(limit),
  });
}

export function useCreateClaim() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: claimsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['claims'] });
    },
  });
}

export function useUpdateClaim() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: any }) =>
      claimsApi.update(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['claims'] });
      queryClient.invalidateQueries({ queryKey: ['claims', id] });
    },
  });
}

export function useDeleteClaim() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: claimsApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['claims'] });
    },
  });
}
