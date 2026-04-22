/**
 * Policies hooks.
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getPolicies,
  getPolicy,
  createPolicy,
  updatePolicy,
  deletePolicy,
  getPolicyStats,
  getPolicyholders,
  getPolicyholder,
  createPolicyholder,
  updatePolicyholder,
} from '@/api/policies';
import type { Policy, Policyholder } from '@/types/models';

// Policies

export function usePolicies(params?: Record<string, unknown>) {
  return useQuery({
    queryKey: ['policies', params],
    queryFn: () => getPolicies(params),
  });
}

export function usePolicy(id: string) {
  return useQuery({
    queryKey: ['policy', id],
    queryFn: () => getPolicy(id),
    enabled: !!id,
  });
}

export function useCreatePolicy() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createPolicy,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['policies'] });
    },
  });
}

export function useUpdatePolicy() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Policy> }) =>
      updatePolicy(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['policies'] });
    },
  });
}

export function useDeletePolicy() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deletePolicy,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['policies'] });
    },
  });
}

export function usePolicyStats() {
  return useQuery({
    queryKey: ['policyStats'],
    queryFn: getPolicyStats,
  });
}

// Policyholders

export function usePolicyholders(params?: Record<string, unknown>) {
  return useQuery({
    queryKey: ['policyholders', params],
    queryFn: () => getPolicyholders(params),
  });
}

export function usePolicyholder(id: string) {
  return useQuery({
    queryKey: ['policyholder', id],
    queryFn: () => getPolicyholder(id),
    enabled: !!id,
  });
}

export function useCreatePolicyholder() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createPolicyholder,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['policyholders'] });
    },
  });
}

export function useUpdatePolicyholder() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Policyholder> }) =>
      updatePolicyholder(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['policyholders'] });
    },
  });
}
