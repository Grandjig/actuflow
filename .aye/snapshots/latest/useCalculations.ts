import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { calculationsApi } from '@/api/calculations';
import type { CalculationListParams, CalculationCreateRequest } from '@/types/api';

export function useCalculations(params: CalculationListParams = {}) {
  return useQuery({
    queryKey: ['calculations', params],
    queryFn: () => calculationsApi.list(params),
  });
}

export function useCalculation(id: string) {
  return useQuery({
    queryKey: ['calculations', id],
    queryFn: () => calculationsApi.get(id),
    enabled: !!id,
  });
}

export function useCalculationProgress(id: string) {
  return useQuery({
    queryKey: ['calculations', id, 'progress'],
    queryFn: () => calculationsApi.getProgress(id),
    enabled: !!id,
    refetchInterval: (data) => {
      // Poll while running
      if (data?.status === 'running' || data?.status === 'queued') {
        return 2000;
      }
      return false;
    },
  });
}

export function useCalculationSummary(id: string) {
  return useQuery({
    queryKey: ['calculations', id, 'summary'],
    queryFn: () => calculationsApi.getSummary(id),
    enabled: !!id,
  });
}

export function useCalculationResults(id: string, params?: Record<string, unknown>) {
  return useQuery({
    queryKey: ['calculations', id, 'results', params],
    queryFn: () => calculationsApi.getResults(id, params),
    enabled: !!id,
  });
}

export function useCreateCalculation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CalculationCreateRequest) => calculationsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['calculations'] });
    },
  });
}

export function useCancelCalculation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: calculationsApi.cancel,
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ['calculations'] });
      queryClient.invalidateQueries({ queryKey: ['calculations', id] });
    },
  });
}
