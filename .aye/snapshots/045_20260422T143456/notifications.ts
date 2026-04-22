import { get, post, put } from './client';
import type { PaginatedResponse } from '@/types/api';
import type { Notification } from '@/types/models';

export interface NotificationListParams {
  page?: number;
  page_size?: number;
  is_read?: boolean;
}

export const getNotifications = (params?: NotificationListParams) =>
  get<PaginatedResponse<Notification>>('/notifications', params);

export const getUnreadCount = () =>
  get<{ count: number }>('/notifications/unread-count');

export const markAsRead = (id: string) =>
  put<Notification>(`/notifications/${id}/read`);

export const markAllAsRead = () =>
  put<{ success: boolean }>('/notifications/read-all');
