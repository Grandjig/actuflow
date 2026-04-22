import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as notificationsApi from '@/api/notifications';
import { useNotificationStore } from '@/stores/notificationStore';
import { useEffect } from 'react';

export function useNotifications() {
  const queryClient = useQueryClient();
  const { addNotification } = useNotificationStore();

  const query = useQuery({
    queryKey: ['notifications'],
    queryFn: notificationsApi.getNotifications,
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  const unreadCountQuery = useQuery({
    queryKey: ['notifications', 'unread-count'],
    queryFn: notificationsApi.getUnreadCount,
    refetchInterval: 30000,
  });

  const markAsReadMutation = useMutation({
    mutationFn: notificationsApi.markAsRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
    },
  });

  const markAllAsReadMutation = useMutation({
    mutationFn: notificationsApi.markAllAsRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
    },
  });

  return {
    notifications: query.data?.items || [],
    isLoading: query.isLoading,
    unreadCount: unreadCountQuery.data?.count || 0,
    markAsRead: markAsReadMutation.mutate,
    markAllAsRead: markAllAsReadMutation.mutate,
    refetch: query.refetch,
  };
}

export function useNotificationSubscription() {
  const queryClient = useQueryClient();
  const { addNotification } = useNotificationStore();

  // This would connect to WebSocket for real-time notifications
  // For now, it's a placeholder that polls
  useEffect(() => {
    const interval = setInterval(() => {
      queryClient.invalidateQueries({ queryKey: ['notifications', 'unread-count'] });
    }, 30000);

    return () => clearInterval(interval);
  }, [queryClient]);
}
