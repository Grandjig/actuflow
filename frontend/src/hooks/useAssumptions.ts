/**
 * Assumptions hooks.
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getAssumptionSets,
  getAssumptionSet,
  createAssumptionSet,
  updateAssumptionSet,
  deleteAssumptionSet,
  cloneAssumptionSet,
  submitForApproval,
  approveAssumptionSet,
  rejectAssumptionSet,
} from '@/api/assumptions';
import type { AssumptionSet } from '@/types/models';

export function useAssumptionSets(params?: Record<string, unknown>) {
  return useQuery({
    queryKey: ['assumptionSets', params],
    queryFn: () => getAssumptionSets(params),
  });
}

export function useAssumptionSet(id: string) {
  return useQuery({
    queryKey: ['assumptionSet', id],
    queryFn: () => getAssumptionSet(id),
    enabled: !!id,
  });
}

export function useCreateAssumptionSet() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createAssumptionSet,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assumptionSets'] });
    },
  });
}

export function useUpdateAssumptionSet() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<AssumptionSet> }) =>
      updateAssumptionSet(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assumptionSets'] });
    },
  });
}

export function useDeleteAssumptionSet() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteAssumptionSet,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assumptionSets'] });
    },
  });
}

export function useCloneAssumptionSet() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, name }: { id: string; name: string }) =>
      cloneAssumptionSet(id, name),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assumptionSets'] });
    },
  });
}

export function useSubmitForApproval() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: submitForApproval,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assumptionSets'] });
    },
  });
}

export function useApproveAssumptionSet() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, notes }: { id: string; notes?: string }) =>
      approveAssumptionSet(id, notes),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assumptionSets'] });
    },
  });
}

export function useRejectAssumptionSet() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, notes }: { id: string; notes: string }) =>
      rejectAssumptionSet(id, notes),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assumptionSets'] });
    },
  });
}
