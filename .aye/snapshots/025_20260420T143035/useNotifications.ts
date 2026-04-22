import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as notificationsApi from '@/api/notifications';
import { useNotificationStore } from '@/stores/notificationStore';
import { useEffect } from 'react';

export function useNotifications(params?: { page?: number; page_size?: number }) {
  const { setNotifications, setLoading } = useNotificationStore();

  const query = useQuery({
    queryKey: ['notifications', params],
    queryFn: () => notificationsApi.getNotifications(params),
  });

  useEffect(() => {
    setLoading(query.isLoading);
    if (query.data) {
      setNotifications(query.data.items);
    }
  }, [query.data, query.isLoading, setNotifications, setLoading]);

  return query;
}

export function useUnreadCount() {
  const { setUnreadCount } = useNotificationStore();

  const query = useQuery({
    queryKey: ['notifications', 'unread-count'],
    queryFn: notificationsApi.getUnreadCount,
    refetchInterval: 30000, // Refresh every 30 seconds
  });

  useEffect(() => {
    if (query.data) {
      setUnreadCount(query.data.count);
    }
  }, [query.data, setUnreadCount]);

  return query;
}

export function useMarkNotificationRead() {
  const queryClient = useQueryClient();
  const { markAsRead } = useNotificationStore();

  return useMutation({
    mutationFn: notificationsApi.markAsRead,
    onSuccess: (_, id) => {
      markAsRead(id);
      queryClient.invalidateQueries({ queryKey: ['notifications', 'unread-count'] });
    },
  });
}

export function useMarkAllNotificationsRead() {
  const queryClient = useQueryClient();
  const { markAllAsRead } = useNotificationStore();

  return useMutation({
    mutationFn: notificationsApi.markAllAsRead,
    onSuccess: () => {
      markAllAsRead();
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
      queryClient.invalidateQueries({ queryKey: ['notifications', 'unread-count'] });
    },
  });
}
