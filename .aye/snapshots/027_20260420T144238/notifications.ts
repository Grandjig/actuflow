import { get, post, put } from './client';
import type { PaginatedResponse } from '@/types/api';
import type { Notification } from '@/types/models';

export const getNotifications = (params?: { page?: number; page_size?: number }) =>
  get<PaginatedResponse<Notification>>('/notifications', params);

export const getUnreadCount = () =>
  get<{ count: number }>('/notifications/unread-count');

export const markAsRead = (id: string) =>
  put<void>(`/notifications/${id}/read`);

export const markAllAsRead = () =>
  put<void>('/notifications/read-all');

export const getNotificationPreferences = () =>
  get<Record<string, boolean>>('/notifications/preferences');

export const updateNotificationPreferences = (preferences: Record<string, boolean>) =>
  put<void>('/notifications/preferences', preferences);
