import { get, post, put, del } from './client';
import type { PaginatedResponse, PaginationParams, SuccessResponse } from '@/types/api';
import type { User, Role } from '@/types/models';

export interface UserCreateData {
  email: string;
  full_name: string;
  password: string;
  role_id: string;
  department?: string;
}

export interface UserUpdateData {
  full_name?: string;
  department?: string;
  is_active?: boolean;
}

export const usersApi = {
  list: (params?: PaginationParams & { search?: string; role_id?: string; is_active?: boolean }) =>
    get<PaginatedResponse<User>>('/users', params),

  get: (id: string) => 
    get<User>(`/users/${id}`),

  create: (data: UserCreateData) => 
    post<User>('/users', data),

  update: (id: string, data: UserUpdateData) => 
    put<User>(`/users/${id}`, data),

  delete: (id: string) => 
    del<SuccessResponse>(`/users/${id}`),

  updateRole: (id: string, roleId: string) =>
    put<User>(`/users/${id}/role`, { role_id: roleId }),

  activate: (id: string) =>
    post<User>(`/users/${id}/activate`),

  deactivate: (id: string) =>
    post<User>(`/users/${id}/deactivate`),
};

export const rolesApi = {
  list: () => 
    get<Role[]>('/roles'),

  get: (id: string) => 
    get<Role>(`/roles/${id}`),

  create: (data: { name: string; description?: string; permission_ids: string[] }) =>
    post<Role>('/roles', data),

  update: (id: string, data: { name?: string; description?: string; permission_ids?: string[] }) =>
    put<Role>(`/roles/${id}`, data),

  delete: (id: string) => 
    del<SuccessResponse>(`/roles/${id}`),

  getPermissions: () => 
    get<{ resource: string; actions: string[] }[]>('/roles/permissions'),
};
