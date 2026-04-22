import { ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { Dropdown, List, Typography, Button, Empty, Tag, Badge } from 'antd';
import {
  BellOutlined,
  CheckOutlined,
  InfoCircleOutlined,
  WarningOutlined,
  ExclamationCircleOutlined,
  CheckCircleOutlined,
} from '@ant-design/icons';

import { useNotifications, useMarkNotificationRead, useMarkAllNotificationsRead } from '@/hooks/useNotifications';
import { useNotificationStore } from '@/stores/notificationStore';
import { formatRelativeTime } from '@/utils/formatters';
import { getResourceUrl } from '@/utils/helpers';
import type { Notification } from '@/types/models';

const { Text } = Typography;

interface NotificationDropdownProps {
  children: ReactNode;
}

const typeIcons: Record<string, ReactNode> = {
  info: <InfoCircleOutlined style={{ color: '#1890ff' }} />,
  warning: <WarningOutlined style={{ color: '#faad14' }} />,
  error: <ExclamationCircleOutlined style={{ color: '#ff4d4f' }} />,
  success: <CheckCircleOutlined style={{ color: '#52c41a' }} />,
  task: <CheckOutlined style={{ color: '#722ed1' }} />,
  approval: <ExclamationCircleOutlined style={{ color: '#eb2f96' }} />,
};

export default function NotificationDropdown({ children }: NotificationDropdownProps) {
  const navigate = useNavigate();
  const { notifications, unreadCount, isLoading } = useNotificationStore();
  const markRead = useMarkNotificationRead();
  const markAllRead = useMarkAllNotificationsRead();

  // Fetch notifications
  useNotifications({ page_size: 10 });

  const handleClick = (notification: Notification) => {
    if (!notification.is_read) {
      markRead.mutate(notification.id);
    }
    if (notification.resource_type && notification.resource_id) {
      const url = getResourceUrl(notification.resource_type, notification.resource_id);
      navigate(url);
    }
  };

  const content = (
    <div style={{ width: 360 }}>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          padding: '12px 16px',
          borderBottom: '1px solid #f0f0f0',
        }}
      >
        <Text strong>Notifications</Text>
        {unreadCount > 0 && (
          <Button type="link" size="small" onClick={() => markAllRead.mutate()}>
            Mark all as read
          </Button>
        )}
      </div>

      <div style={{ maxHeight: 400, overflow: 'auto' }}>
        {notifications.length === 0 ? (
          <Empty
            image={Empty.PRESENTED_IMAGE_SIMPLE}
            description="No notifications"
            style={{ padding: 24 }}
          />
        ) : (
          <List
            dataSource={notifications}
            loading={isLoading}
            renderItem={(notification) => (
              <List.Item
                style={{
                  padding: '12px 16px',
                  cursor: 'pointer',
                  background: notification.is_read ? 'transparent' : '#f6ffed',
                }}
                onClick={() => handleClick(notification)}
              >
                <List.Item.Meta
                  avatar={typeIcons[notification.type] || typeIcons.info}
                  title={
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Text strong={!notification.is_read}>{notification.title}</Text>
                      {!notification.is_read && (
                        <Badge status="processing" />
                      )}
                    </div>
                  }
                  description={
                    <div>
                      <div
                        style={{
                          fontSize: 12,
                          color: '#666',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap',
                        }}
                      >
                        {notification.message}
                      </div>
                      <Text type="secondary" style={{ fontSize: 11 }}>
                        {formatRelativeTime(notification.created_at)}
                      </Text>
                    </div>
                  }
                />
              </List.Item>
            )}
          />
        )}
      </div>

      <div
        style={{
          padding: '8px 16px',
          borderTop: '1px solid #f0f0f0',
          textAlign: 'center',
        }}
      >
        <Button type="link" onClick={() => navigate('/notifications')}>
          View All Notifications
        </Button>
      </div>
    </div>
  );

  return (
    <Dropdown
      dropdownRender={() => content}
      trigger={['click']}
      placement="bottomRight"
    >
      {children}
    </Dropdown>
  );
}
