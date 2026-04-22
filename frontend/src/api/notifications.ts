/**
 * Notifications API functions.
 */

import { get, put } from './client';
import type { Notification } from '@/types/models';

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export async function getNotifications(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<Notification>> {
  return get('/notifications', params);
}

export async function markAsRead(id: string): Promise<Notification> {
  return put(`/notifications/${id}/read`);
}

export async function markAllAsRead(): Promise<void> {
  return put('/notifications/read-all');
}

export async function getUnreadCount(): Promise<number> {
  const response = await get<{ count: number }>('/notifications/unread-count');
  return response.count;
}
