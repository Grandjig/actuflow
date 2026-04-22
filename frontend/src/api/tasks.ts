import { get, post, put, del } from './client';
import type { PaginatedResponse, TaskFilters, SuccessResponse } from '@/types/api';
import type { Task } from '@/types/models';

export interface TaskCreateData {
  title: string;
  description?: string;
  task_type?: string;
  priority?: string;
  due_date?: string;
  assigned_to_id?: string;
  related_resource_type?: string;
  related_resource_id?: string;
}

export interface TaskUpdateData {
  title?: string;
  description?: string;
  priority?: string;
  due_date?: string;
  status?: string;
  completion_notes?: string;
}

export const tasksApi = {
  list: (params?: TaskFilters) =>
    get<PaginatedResponse<Task>>('/tasks', params),

  get: (id: string) => 
    get<Task>(`/tasks/${id}`),

  create: (data: TaskCreateData) => 
    post<Task>('/tasks', data),

  update: (id: string, data: TaskUpdateData) => 
    put<Task>(`/tasks/${id}`, data),

  delete: (id: string) => 
    del<SuccessResponse>(`/tasks/${id}`),

  assign: (id: string, userId: string) =>
    put<Task>(`/tasks/${id}/assign`, { assigned_to_id: userId }),

  updateStatus: (id: string, status: string, notes?: string) =>
    put<Task>(`/tasks/${id}/status`, { status, completion_notes: notes }),

  getMyTasks: (includeCompleted?: boolean) =>
    get<Task[]>('/tasks/my', { include_completed: includeCompleted }),
};
