/**
 * Calculation hooks.
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getCalculationRuns,
  getCalculationRun,
  createCalculationRun,
  cancelCalculationRun,
  getCalculationResults,
  getCalculationProgress,
} from '@/api/calculations';
import type { CalculationRun, CalculationResult, CalculationProgress } from '@/types/models';

export function useCalculationRuns(params?: Record<string, unknown>) {
  return useQuery({
    queryKey: ['calculationRuns', params],
    queryFn: () => getCalculationRuns(params),
  });
}

export function useCalculationRun(id: string) {
  return useQuery({
    queryKey: ['calculationRun', id],
    queryFn: () => getCalculationRun(id),
    enabled: !!id,
  });
}

export function useCreateCalculationRun() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: createCalculationRun,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['calculationRuns'] });
    },
  });
}

export function useCancelCalculationRun() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: cancelCalculationRun,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['calculationRuns'] });
    },
  });
}

export function useCalculationResults(runId: string, params?: Record<string, unknown>) {
  return useQuery({
    queryKey: ['calculationResults', runId, params],
    queryFn: () => getCalculationResults(runId, params),
    enabled: !!runId,
  });
}

export function useCalculationProgress(runId: string) {
  const query = useQuery({
    queryKey: ['calculationProgress', runId],
    queryFn: () => getCalculationProgress(runId),
    enabled: !!runId,
    refetchInterval: (query) => {
      const data = query.state.data as CalculationProgress | undefined;
      // Stop polling when calculation is complete
      if (data?.status === 'completed' || data?.status === 'failed' || data?.status === 'cancelled') {
        return false;
      }
      return 2000; // Poll every 2 seconds
    },
  });

  return query;
}
