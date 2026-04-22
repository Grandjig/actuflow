import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { assumptionsApi } from '@/api/assumptions';
import type { AssumptionSetFilters } from '@/types/api';

export function useAssumptionSets(params: AssumptionSetFilters = {}) {
  return useQuery({
    queryKey: ['assumption-sets', params],
    queryFn: () => assumptionsApi.list(params),
  });
}

export function useAssumptionSet(id: string) {
  return useQuery({
    queryKey: ['assumption-sets', id],
    queryFn: () => assumptionsApi.get(id),
    enabled: !!id,
  });
}

export function useApprovedAssumptionSets() {
  return useQuery({
    queryKey: ['assumption-sets', 'approved'],
    queryFn: () => assumptionsApi.getApproved(),
  });
}

export function useAssumptionTables(setId: string) {
  return useQuery({
    queryKey: ['assumption-sets', setId, 'tables'],
    queryFn: () => assumptionsApi.getTables(setId),
    enabled: !!setId,
  });
}

export function useAssumptionRecommendations(setId: string) {
  return useQuery({
    queryKey: ['assumption-sets', setId, 'recommendations'],
    queryFn: () => assumptionsApi.getExperienceRecommendations(setId),
    enabled: !!setId,
  });
}

export function useCreateAssumptionSet() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: assumptionsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assumption-sets'] });
    },
  });
}

export function useUpdateAssumptionSet() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: any }) =>
      assumptionsApi.update(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['assumption-sets'] });
      queryClient.invalidateQueries({ queryKey: ['assumption-sets', id] });
    },
  });
}

export function useDeleteAssumptionSet() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: assumptionsApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assumption-sets'] });
    },
  });
}

export function useSubmitAssumptionSet() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: assumptionsApi.submit,
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ['assumption-sets'] });
      queryClient.invalidateQueries({ queryKey: ['assumption-sets', id] });
    },
  });
}

export function useApproveAssumptionSet() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, comments }: { id: string; comments?: string }) =>
      assumptionsApi.approve(id, comments),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['assumption-sets'] });
      queryClient.invalidateQueries({ queryKey: ['assumption-sets', id] });
    },
  });
}
