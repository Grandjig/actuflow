import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { policyholdersApi } from '@/api/policyholders';
import type { ListParams } from '@/types/api';

export function usePolicyholders(params: ListParams = {}) {
  return useQuery({
    queryKey: ['policyholders', params],
    queryFn: () => policyholdersApi.list(params),
  });
}

export function usePolicyholder(id: string) {
  return useQuery({
    queryKey: ['policyholders', id],
    queryFn: () => policyholdersApi.get(id),
    enabled: !!id,
  });
}

export function usePolicyholderPolicies(id: string) {
  return useQuery({
    queryKey: ['policyholders', id, 'policies'],
    queryFn: () => policyholdersApi.getPolicies(id),
    enabled: !!id,
  });
}

export function useCreatePolicyholder() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: policyholdersApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['policyholders'] });
    },
  });
}

export function useUpdatePolicyholder() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: any }) =>
      policyholdersApi.update(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['policyholders'] });
      queryClient.invalidateQueries({ queryKey: ['policyholders', id] });
    },
  });
}

export function useDeletePolicyholder() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: policyholdersApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['policyholders'] });
    },
  });
}
