/**
 * Claims hooks.
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getClaims,
  getClaim,
  createClaim,
  updateClaim,
  deleteClaim,
  updateClaimStatus,
  getClaimStats,
  getClaimAnomalies,
} from '@/api/claims';
import type { Claim } from '@/types/models';

export function useClaims(params?: Record<string, unknown>) {
  return useQuery({
    queryKey: ['claims', params],
    queryFn: () => getClaims(params),
  });
}

export function useClaim(id: string) {
  return useQuery({
    queryKey: ['claim', id],
    queryFn: () => getClaim(id),
    enabled: !!id,
  });
}

export function useCreateClaim() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createClaim,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['claims'] });
    },
  });
}

export function useUpdateClaim() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Claim> }) =>
      updateClaim(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['claims'] });
    },
  });
}

export function useDeleteClaim() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteClaim,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['claims'] });
    },
  });
}

export function useUpdateClaimStatus() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, status, notes }: { id: string; status: string; notes?: string }) =>
      updateClaimStatus(id, status, notes),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['claims'] });
    },
  });
}

export function useClaimStats() {
  return useQuery({
    queryKey: ['claimStats'],
    queryFn: getClaimStats,
  });
}

export function useClaimAnomalies() {
  return useQuery({
    queryKey: ['claimAnomalies'],
    queryFn: getClaimAnomalies,
  });
}
