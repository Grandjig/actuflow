/**
 * User API functions.
 */

import { get, post, put, del } from './client';
import type { User, Role } from '@/types/models';

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export async function getUsers(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<User>> {
  return get('/users', params);
}

export async function getUser(id: string): Promise<User> {
  return get(`/users/${id}`);
}

export async function createUser(data: Partial<User>): Promise<User> {
  return post('/users', data);
}

export async function updateUser(
  id: string,
  data: Partial<User>
): Promise<User> {
  return put(`/users/${id}`, data);
}

export async function deleteUser(id: string): Promise<void> {
  return del(`/users/${id}`);
}

export async function updateProfile(
  data: Partial<User>
): Promise<User> {
  return put('/users/me', data);
}

export async function getRoles(): Promise<Role[]> {
  return get('/roles');
}

export async function updateUserRole(
  userId: string,
  roleId: string
): Promise<User> {
  return put(`/users/${userId}/role`, { role_id: roleId });
}
