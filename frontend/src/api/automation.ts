import { get, post, put, del } from './client';
import type { PaginatedResponse, ListParams, SuccessResponse } from '@/types/api';
import type { ScheduledJob, JobExecution, AutomationRule } from '@/types/models';

export interface ScheduledJobCreate {
  name: string;
  description?: string;
  job_type: string;
  cron_expression: string;
  config: Record<string, unknown>;
  is_active?: boolean;
}

export interface AutomationRuleCreate {
  name: string;
  description?: string;
  trigger_type: string;
  trigger_config: Record<string, unknown>;
  action_type: string;
  action_config: Record<string, unknown>;
  is_active?: boolean;
}

// Scheduled Jobs
export const getScheduledJobs = (params?: ListParams & { is_active?: boolean; job_type?: string }) =>
  get<PaginatedResponse<ScheduledJob>>('/automation/jobs', params);

export const getScheduledJob = (id: string) =>
  get<ScheduledJob>(`/automation/jobs/${id}`);

export const createScheduledJob = (data: ScheduledJobCreate) =>
  post<ScheduledJob>('/automation/jobs', data);

export const updateScheduledJob = (id: string, data: Partial<ScheduledJobCreate>) =>
  put<ScheduledJob>(`/automation/jobs/${id}`, data);

export const deleteScheduledJob = (id: string) =>
  del<void>(`/automation/jobs/${id}`);

export const triggerJobNow = (id: string) =>
  post<{ execution_id: string; status: string }>(`/automation/jobs/${id}/run`);

export const getJobExecutions = (jobId: string) =>
  get<JobExecution[]>(`/automation/jobs/${jobId}/executions`);

// Automation Rules
export const getAutomationRules = (params?: ListParams & { is_active?: boolean }) =>
  get<AutomationRule[]>('/automation/rules', params);

export const getAutomationRule = (id: string) =>
  get<AutomationRule>(`/automation/rules/${id}`);

export const createAutomationRule = (data: AutomationRuleCreate) =>
  post<AutomationRule>('/automation/rules', data);

export const updateAutomationRule = (id: string, data: Partial<AutomationRuleCreate>) =>
  put<AutomationRule>(`/automation/rules/${id}`, data);

export const deleteAutomationRule = (id: string) =>
  del<void>(`/automation/rules/${id}`);

export const testAutomationRule = (id: string) =>
  post<{ success: boolean; message: string }>(`/automation/rules/${id}/test`);
