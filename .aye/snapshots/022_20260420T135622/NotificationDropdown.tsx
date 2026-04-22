import { ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { Dropdown, List, Button, Empty, Spin, Typography } from 'antd';
import { CheckOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import { useNotifications, useMarkNotificationRead, useMarkAllNotificationsRead } from '@/hooks/useNotifications';
import { useNotificationStore } from '@/stores/notificationStore';
import { getResourceUrl } from '@/utils/helpers';

interface NotificationDropdownProps {
  children: ReactNode;
}

export default function NotificationDropdown({ children }: NotificationDropdownProps) {
  const navigate = useNavigate();
  const { notifications, isLoading } = useNotificationStore();
  const markRead = useMarkNotificationRead();
  const markAllRead = useMarkAllNotificationsRead();

  // Initial fetch
  useNotifications({ page_size: 10 });

  const handleNotificationClick = (notification: typeof notifications[0]) => {
    if (!notification.is_read) {
      markRead.mutate(notification.id);
    }
    if (notification.resource_type && notification.resource_id) {
      const url = getResourceUrl(notification.resource_type, notification.resource_id);
      navigate(url);
    }
  };

  const dropdownContent = (
    <div
      style={{
        width: 360,
        maxHeight: 400,
        overflow: 'auto',
        background: 'white',
        borderRadius: 8,
        boxShadow: '0 6px 16px rgba(0,0,0,0.12)',
      }}
    >
      <div
        style={{
          padding: '12px 16px',
          borderBottom: '1px solid #f0f0f0',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <Typography.Text strong>Notifications</Typography.Text>
        <Button
          type="link"
          size="small"
          icon={<CheckOutlined />}
          onClick={() => markAllRead.mutate()}
          disabled={notifications.every((n) => n.is_read)}
        >
          Mark all read
        </Button>
      </div>

      {isLoading ? (
        <div style={{ padding: 40, textAlign: 'center' }}>
          <Spin />
        </div>
      ) : notifications.length === 0 ? (
        <Empty
          description="No notifications"
          style={{ padding: 40 }}
          image={Empty.PRESENTED_IMAGE_SIMPLE}
        />
      ) : (
        <List
          dataSource={notifications.slice(0, 10)}
          renderItem={(notification) => (
            <List.Item
              onClick={() => handleNotificationClick(notification)}
              style={{
                padding: '12px 16px',
                cursor: 'pointer',
                background: notification.is_read ? 'white' : '#f6ffed',
              }}
            >
              <List.Item.Meta
                title={notification.title}
                description={
                  <>
                    <div>{notification.message}</div>
                    <Typography.Text type="secondary" style={{ fontSize: 12 }}>
                      {dayjs(notification.created_at).fromNow()}
                    </Typography.Text>
                  </>
                }
              />
            </List.Item>
          )}
        />
      )}

      <div
        style={{
          padding: '8px 16px',
          borderTop: '1px solid #f0f0f0',
          textAlign: 'center',
        }}
      >
        <Button type="link" onClick={() => navigate('/notifications')}>
          View all notifications
        </Button>
      </div>
    </div>
  );

  return (
    <Dropdown
      dropdownRender={() => dropdownContent}
      trigger={['click']}
      placement="bottomRight"
    >
      {children}
    </Dropdown>
  );
}
