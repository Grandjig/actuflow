import { get, put } from './client';
import type { Notification } from '@/types/models';

export const notificationsApi = {
  list: (unreadOnly?: boolean) =>
    get<Notification[]>('/notifications', { unread_only: unreadOnly }),

  markAsRead: (id: string) =>
    put<Notification>(`/notifications/${id}/read`),

  markAllAsRead: () =>
    put<{ count: number }>('/notifications/read-all'),

  getUnreadCount: () =>
    get<{ count: number }>('/notifications/unread-count'),
};
