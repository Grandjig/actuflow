import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as automationApi from '@/api/automation';
import type { ListParams } from '@/types/api';

// Scheduled Jobs
export function useScheduledJobs(params: ListParams = {}) {
  return useQuery({
    queryKey: ['scheduled-jobs', params],
    queryFn: () => automationApi.getScheduledJobs(params),
  });
}

export function useScheduledJob(id: string) {
  return useQuery({
    queryKey: ['scheduled-jobs', id],
    queryFn: () => automationApi.getScheduledJob(id),
    enabled: !!id,
  });
}

export function useJobExecutions(jobId: string) {
  return useQuery({
    queryKey: ['scheduled-jobs', jobId, 'executions'],
    queryFn: () => automationApi.getJobExecutions(jobId),
    enabled: !!jobId,
  });
}

export function useCreateScheduledJob() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: automationApi.createScheduledJob,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scheduled-jobs'] });
    },
  });
}

export function useUpdateScheduledJob() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: any }) =>
      automationApi.updateScheduledJob(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['scheduled-jobs'] });
      queryClient.invalidateQueries({ queryKey: ['scheduled-jobs', id] });
    },
  });
}

export function useDeleteScheduledJob() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: automationApi.deleteScheduledJob,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scheduled-jobs'] });
    },
  });
}

export function useTriggerJobNow() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: automationApi.triggerJobNow,
    onSuccess: (_, jobId) => {
      queryClient.invalidateQueries({ queryKey: ['scheduled-jobs', jobId, 'executions'] });
    },
  });
}

// Automation Rules
export function useAutomationRules(params: ListParams = {}) {
  return useQuery({
    queryKey: ['automation-rules', params],
    queryFn: () => automationApi.getAutomationRules(params),
  });
}

export function useAutomationRule(id: string) {
  return useQuery({
    queryKey: ['automation-rules', id],
    queryFn: () => automationApi.getAutomationRule(id),
    enabled: !!id,
  });
}

export function useCreateAutomationRule() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: automationApi.createAutomationRule,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['automation-rules'] });
    },
  });
}

export function useUpdateAutomationRule() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: any }) =>
      automationApi.updateAutomationRule(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['automation-rules'] });
      queryClient.invalidateQueries({ queryKey: ['automation-rules', id] });
    },
  });
}

export function useDeleteAutomationRule() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: automationApi.deleteAutomationRule,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['automation-rules'] });
    },
  });
}

export function useTestAutomationRule() {
  return useMutation({
    mutationFn: automationApi.testAutomationRule,
  });
}
