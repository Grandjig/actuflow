import { get, post, put, del } from './client';
import type { PaginatedResponse, ListParams } from '@/types/api';
import type { User, Role, Permission } from '@/types/models';

export interface UserCreate {
  email: string;
  full_name: string;
  password: string;
  role_id?: string;
  department?: string;
  job_title?: string;
  is_active?: boolean;
}

export interface UserUpdate {
  email?: string;
  full_name?: string;
  password?: string;
  role_id?: string;
  department?: string;
  job_title?: string;
  is_active?: boolean;
}

export const usersApi = {
  list: (params?: ListParams) =>
    get<PaginatedResponse<User>>('/users', params),

  get: (id: string) =>
    get<User>(`/users/${id}`),

  create: (data: UserCreate) =>
    post<User>('/users', data),

  update: (id: string, data: UserUpdate) =>
    put<User>(`/users/${id}`, data),

  delete: (id: string) =>
    del<void>(`/users/${id}`),
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
    del<void>(`/roles/${id}`),

  getPermissions: () =>
    get<Permission[]>('/roles/permissions'),
};
