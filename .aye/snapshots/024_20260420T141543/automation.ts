import { get, post, put, del } from './client';
import type { PaginatedResponse, ListParams } from '@/types/api';
import type { ScheduledJob, JobExecution, AutomationRule } from '@/types/models';

// Scheduled Jobs
export const getScheduledJobs = (params?: ListParams) =>
  get<PaginatedResponse<ScheduledJob>>('/automation/scheduled-jobs', params);

export const getScheduledJob = (id: string) =>
  get<ScheduledJob>(`/automation/scheduled-jobs/${id}`);

export const createScheduledJob = (data: Partial<ScheduledJob>) =>
  post<ScheduledJob>('/automation/scheduled-jobs', data);

export const updateScheduledJob = (id: string, data: Partial<ScheduledJob>) =>
  put<ScheduledJob>(`/automation/scheduled-jobs/${id}`, data);

export const deleteScheduledJob = (id: string) =>
  del<void>(`/automation/scheduled-jobs/${id}`);

export const triggerJobNow = (id: string) =>
  post<void>(`/automation/scheduled-jobs/${id}/run-now`);

export const getJobExecutions = (jobId: string) =>
  get<JobExecution[]>(`/automation/scheduled-jobs/${jobId}/executions`);

// Automation Rules
export const getAutomationRules = (params?: ListParams) =>
  get<PaginatedResponse<AutomationRule>>('/automation/rules', params);

export const getAutomationRule = (id: string) =>
  get<AutomationRule>(`/automation/rules/${id}`);

export const createAutomationRule = (data: Partial<AutomationRule>) =>
  post<AutomationRule>('/automation/rules', data);

export const updateAutomationRule = (id: string, data: Partial<AutomationRule>) =>
  put<AutomationRule>(`/automation/rules/${id}`, data);

export const deleteAutomationRule = (id: string) =>
  del<void>(`/automation/rules/${id}`);

export const testAutomationRule = (id: string) =>
  post<{ would_trigger: boolean; matched_records: number }>(`/automation/rules/${id}/test`);
