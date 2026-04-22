/**
 * Automation API functions.
 */

import { get, post, put, del } from './client';
import type { ScheduledJob, JobExecution, AutomationRule } from '@/types/models';

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

// Scheduled Jobs

export async function getScheduledJobs(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<ScheduledJob>> {
  return get('/scheduled-jobs', params);
}

export async function getScheduledJob(id: string): Promise<ScheduledJob> {
  return get(`/scheduled-jobs/${id}`);
}

export async function createScheduledJob(
  data: Partial<ScheduledJob>
): Promise<ScheduledJob> {
  return post('/scheduled-jobs', data);
}

export async function updateScheduledJob(
  id: string,
  data: Partial<ScheduledJob>
): Promise<ScheduledJob> {
  return put(`/scheduled-jobs/${id}`, data);
}

export async function deleteScheduledJob(id: string): Promise<void> {
  return del(`/scheduled-jobs/${id}`);
}

export async function triggerJobNow(id: string): Promise<JobExecution> {
  return post(`/scheduled-jobs/${id}/run-now`);
}

export async function getJobExecutions(
  jobId: string,
  params?: Record<string, unknown>
): Promise<PaginatedResponse<JobExecution>> {
  return get(`/scheduled-jobs/${jobId}/executions`, params);
}

// Automation Rules

export async function getAutomationRules(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<AutomationRule>> {
  return get('/automation-rules', params);
}

export async function getAutomationRule(id: string): Promise<AutomationRule> {
  return get(`/automation-rules/${id}`);
}

export async function createAutomationRule(
  data: Partial<AutomationRule>
): Promise<AutomationRule> {
  return post('/automation-rules', data);
}

export async function updateAutomationRule(
  id: string,
  data: Partial<AutomationRule>
): Promise<AutomationRule> {
  return put(`/automation-rules/${id}`, data);
}

export async function deleteAutomationRule(id: string): Promise<void> {
  return del(`/automation-rules/${id}`);
}

export async function testAutomationRule(
  id: string,
  testData: Record<string, unknown>
): Promise<{ would_trigger: boolean; reason: string }> {
  return post(`/automation-rules/${id}/test`, testData);
}
