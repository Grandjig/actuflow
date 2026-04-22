import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useEffect } from 'react';
import * as notificationsApi from '@/api/notifications';
import { useNotificationStore } from '@/stores/notificationStore';

export function useNotifications(params?: notificationsApi.NotificationListParams) {
  const { setNotifications, setUnreadCount, setLoading } = useNotificationStore();

  const query = useQuery({
    queryKey: ['notifications', params],
    queryFn: () => notificationsApi.getNotifications(params),
    refetchInterval: 60000, // Refetch every minute
  });

  useEffect(() => {
    setLoading(query.isLoading);
    if (query.data) {
      setNotifications(query.data.items);
    }
  }, [query.data, query.isLoading, setNotifications, setLoading]);

  // Also fetch unread count
  const countQuery = useQuery({
    queryKey: ['notifications', 'unread-count'],
    queryFn: () => notificationsApi.getUnreadCount(),
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  useEffect(() => {
    if (countQuery.data) {
      setUnreadCount(countQuery.data.count);
    }
  }, [countQuery.data, setUnreadCount]);

  return {
    ...query,
    unreadCount: countQuery.data?.count || 0,
  };
}

export function useMarkNotificationRead() {
  const queryClient = useQueryClient();
  const { markAsRead } = useNotificationStore();

  return useMutation({
    mutationFn: notificationsApi.markAsRead,
    onSuccess: (_, id) => {
      markAsRead(id);
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
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
    },
  });
}
