/**
 * Automation hooks.
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getScheduledJobs,
  getScheduledJob,
  createScheduledJob,
  updateScheduledJob,
  deleteScheduledJob,
  triggerJobNow,
  getJobExecutions,
  getAutomationRules,
  getAutomationRule,
  createAutomationRule,
  updateAutomationRule,
  deleteAutomationRule,
} from '@/api/automation';
import type { ScheduledJob, JobExecution, AutomationRule } from '@/types/models';

interface ListParams {
  page?: number;
  page_size?: number;
  search?: string;
  [key: string]: unknown;
}

// Scheduled Jobs

export function useScheduledJobs(params?: ListParams) {
  return useQuery({
    queryKey: ['scheduledJobs', params],
    queryFn: () => getScheduledJobs(params as Record<string, unknown>),
  });
}

export function useScheduledJob(id: string) {
  return useQuery({
    queryKey: ['scheduledJob', id],
    queryFn: () => getScheduledJob(id),
    enabled: !!id,
  });
}

export function useCreateScheduledJob() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: createScheduledJob,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scheduledJobs'] });
    },
  });
}

export function useUpdateScheduledJob() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<ScheduledJob> }) =>
      updateScheduledJob(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scheduledJobs'] });
    },
  });
}

export function useDeleteScheduledJob() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: deleteScheduledJob,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scheduledJobs'] });
    },
  });
}

export function useTriggerJobNow() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: triggerJobNow,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scheduledJobs'] });
      queryClient.invalidateQueries({ queryKey: ['jobExecutions'] });
    },
  });
}

export function useJobExecutions(jobId: string, params?: ListParams) {
  return useQuery({
    queryKey: ['jobExecutions', jobId, params],
    queryFn: () => getJobExecutions(jobId, params as Record<string, unknown>),
    enabled: !!jobId,
  });
}

// Automation Rules

export function useAutomationRules(params?: ListParams) {
  return useQuery({
    queryKey: ['automationRules', params],
    queryFn: () => getAutomationRules(params as Record<string, unknown>),
  });
}

export function useAutomationRule(id: string) {
  return useQuery({
    queryKey: ['automationRule', id],
    queryFn: () => getAutomationRule(id),
    enabled: !!id,
  });
}

export function useCreateAutomationRule() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: createAutomationRule,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['automationRules'] });
    },
  });
}

export function useUpdateAutomationRule() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<AutomationRule> }) =>
      updateAutomationRule(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['automationRules'] });
    },
  });
}

export function useDeleteAutomationRule() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: deleteAutomationRule,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['automationRules'] });
    },
  });
}
