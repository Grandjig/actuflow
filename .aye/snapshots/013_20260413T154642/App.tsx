import { useEffect } from 'react';
import { useRoutes } from 'react-router-dom';
import { App as AntApp } from 'antd';
import { routes } from './routes';
import { useAuthStore } from './stores/authStore';
import { useNotificationStore } from './stores/notificationStore';
import { useWebSocket } from './hooks/useWebSocket';
import LoadingSpinner from './components/common/LoadingSpinner';

export default function App() {
  const { message, notification } = AntApp.useApp();
  const { isInitialized, initAuth } = useAuthStore();
  const { addNotification } = useNotificationStore();

  // Initialize auth on app load
  useEffect(() => {
    initAuth();
  }, [initAuth]);

  // Connect to WebSocket for real-time notifications
  const { lastMessage } = useWebSocket('/ws/notifications', {
    enabled: isInitialized && useAuthStore.getState().isAuthenticated,
  });

  // Handle incoming WebSocket messages
  useEffect(() => {
    if (lastMessage) {
      const data = JSON.parse(lastMessage.data);
      if (data.type === 'notification') {
        addNotification(data.payload);
        notification.info({
          message: data.payload.title,
          description: data.payload.message,
          placement: 'topRight',
        });
      }
    }
  }, [lastMessage, addNotification, notification]);

  // Make message and notification available globally
  useEffect(() => {
    (window as any).__antMessage = message;
    (window as any).__antNotification = notification;
  }, [message, notification]);

  // Show loading spinner while initializing auth
  if (!isInitialized) {
    return <LoadingSpinner fullScreen tip="Loading..." />;
  }

  const element = useRoutes(routes);
  return element;
}
