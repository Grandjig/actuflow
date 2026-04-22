import { get, post, put, del } from './client';
import type { PaginatedResponse, PaginationParams, SuccessResponse } from '@/types/api';
import type { ScheduledJob, JobExecution, AutomationRule } from '@/types/models';

export interface ScheduledJobCreateData {
  name: string;
  description?: string;
  job_type: string;
  cron_expression: string;
  config: Record<string, unknown>;
}

export interface ScheduledJobUpdateData {
  name?: string;
  description?: string;
  cron_expression?: string;
  config?: Record<string, unknown>;
  is_active?: boolean;
}

export interface AutomationRuleCreateData {
  name: string;
  description?: string;
  trigger_type: string;
  trigger_config: Record<string, unknown>;
  action_type: string;
  action_config: Record<string, unknown>;
}

export interface AutomationRuleUpdateData {
  name?: string;
  description?: string;
  trigger_config?: Record<string, unknown>;
  action_config?: Record<string, unknown>;
  is_active?: boolean;
}

export const automationApi = {
  // Scheduled Jobs
  listJobs: (params?: PaginationParams & { is_active?: boolean; job_type?: string }) =>
    get<PaginatedResponse<ScheduledJob>>('/automation/scheduled-jobs', params),

  getJob: (id: string) => 
    get<ScheduledJob>(`/automation/scheduled-jobs/${id}`),

  createJob: (data: ScheduledJobCreateData) => 
    post<ScheduledJob>('/automation/scheduled-jobs', data),

  updateJob: (id: string, data: ScheduledJobUpdateData) => 
    put<ScheduledJob>(`/automation/scheduled-jobs/${id}`, data),

  deleteJob: (id: string) => 
    del<SuccessResponse>(`/automation/scheduled-jobs/${id}`),

  getJobExecutions: (id: string, limit?: number) =>
    get<JobExecution[]>(`/automation/scheduled-jobs/${id}/executions`, { limit }),

  runJobNow: (id: string) =>
    post<SuccessResponse>(`/automation/scheduled-jobs/${id}/run-now`),

  // Automation Rules
  listRules: (params?: PaginationParams & { trigger_type?: string; is_active?: boolean }) =>
    get<PaginatedResponse<AutomationRule>>('/automation/rules', params),

  getRule: (id: string) => 
    get<AutomationRule>(`/automation/rules/${id}`),

  createRule: (data: AutomationRuleCreateData) => 
    post<AutomationRule>('/automation/rules', data),

  updateRule: (id: string, data: AutomationRuleUpdateData) => 
    put<AutomationRule>(`/automation/rules/${id}`, data),

  deleteRule: (id: string) => 
    del<SuccessResponse>(`/automation/rules/${id}`),
};
