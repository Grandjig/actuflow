import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { get, post, put, del } from '@/api/client';
import type { PaginatedResponse, ListParams } from '@/types/api';
import type { Policyholder } from '@/types/models';

const policyholderApi = {
  list: (params?: ListParams) => get<PaginatedResponse<Policyholder>>('/policyholders', params),
  get: (id: string) => get<Policyholder>(`/policyholders/${id}`),
  create: (data: any) => post<Policyholder>('/policyholders', data),
  update: (id: string, data: any) => put<Policyholder>(`/policyholders/${id}`, data),
  delete: (id: string) => del<void>(`/policyholders/${id}`),
};

export function usePolicyholders(params: ListParams = {}) {
  return useQuery({
    queryKey: ['policyholders', params],
    queryFn: () => policyholderApi.list(params),
  });
}

export function usePolicyholder(id: string) {
  return useQuery({
    queryKey: ['policyholders', id],
    queryFn: () => policyholderApi.get(id),
    enabled: !!id,
  });
}

export function useCreatePolicyholder() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: policyholderApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['policyholders'] });
    },
  });
}

export function useUpdatePolicyholder() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: any }) =>
      policyholderApi.update(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['policyholders'] });
      queryClient.invalidateQueries({ queryKey: ['policyholders', id] });
    },
  });
}

export function useDeletePolicyholder() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: policyholderApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['policyholders'] });
    },
  });
}
