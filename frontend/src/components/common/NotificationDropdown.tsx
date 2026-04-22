/**
 * Notification dropdown component.
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Dropdown,
  Badge,
  Button,
  List,
  Typography,
  Space,
  Empty,
  Spin,
} from 'antd';
import { BellOutlined, CheckOutlined } from '@ant-design/icons';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getNotifications, markAsRead, markAllAsRead } from '@/api/notifications';
import { getResourceUrl, getRelativeTime } from '@/utils/helpers';
import type { Notification } from '@/types/models';

const { Text } = Typography;

export default function NotificationDropdown() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [open, setOpen] = useState(false);

  const { data, isLoading } = useQuery({
    queryKey: ['notifications', { limit: 10 }],
    queryFn: () => getNotifications({ limit: 10 }),
    enabled: open,
  });

  const { data: unreadCount } = useQuery({
    queryKey: ['notificationsUnreadCount'],
    queryFn: () => getNotifications({ is_read: false, limit: 1 }).then((r) => r.total),
    refetchInterval: 30000, // Refresh every 30 seconds
  });

  const markReadMutation = useMutation({
    mutationFn: markAsRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
      queryClient.invalidateQueries({ queryKey: ['notificationsUnreadCount'] });
    },
  });

  const markAllReadMutation = useMutation({
    mutationFn: markAllAsRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
      queryClient.invalidateQueries({ queryKey: ['notificationsUnreadCount'] });
    },
  });

  const handleNotificationClick = (notification: Notification) => {
    if (!notification.is_read) {
      markReadMutation.mutate(notification.id);
    }
    if (notification.resource_type && notification.resource_id) {
      navigate(getResourceUrl(notification.resource_type, notification.resource_id));
    }
    setOpen(false);
  };

  const content = (
    <div style={{ width: 350 }}>
      <div
        style={{
          padding: '12px 16px',
          borderBottom: '1px solid #f0f0f0',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <Text strong>Notifications</Text>
        {(unreadCount ?? 0) > 0 && (
          <Button
            type="link"
            size="small"
            onClick={() => markAllReadMutation.mutate()}
            loading={markAllReadMutation.isPending}
          >
            Mark all as read
          </Button>
        )}
      </div>

      {isLoading ? (
        <div style={{ padding: 20, textAlign: 'center' }}>
          <Spin />
        </div>
      ) : data?.items && data.items.length > 0 ? (
        <List
          dataSource={data.items}
          renderItem={(item: Notification) => (
            <List.Item
              onClick={() => handleNotificationClick(item)}
              style={{
                cursor: 'pointer',
                backgroundColor: item.is_read ? 'transparent' : '#e6f7ff',
                padding: '12px 16px',
              }}
            >
              <List.Item.Meta
                title={
                  <Space>
                    {!item.is_read && (
                      <Badge status="processing" />
                    )}
                    <span>{item.title}</span>
                  </Space>
                }
                description={
                  <Space direction="vertical" size={0}>
                    <Text type="secondary" style={{ fontSize: 12 }}>
                      {item.message}
                    </Text>
                    <Text type="secondary" style={{ fontSize: 11 }}>
                      {getRelativeTime(item.created_at)}
                    </Text>
                  </Space>
                }
              />
            </List.Item>
          )}
          style={{ maxHeight: 400, overflow: 'auto' }}
        />
      ) : (
        <Empty
          image={Empty.PRESENTED_IMAGE_SIMPLE}
          description="No notifications"
          style={{ padding: 20 }}
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
      trigger={['click']}
      open={open}
      onOpenChange={setOpen}
      dropdownRender={() => content}
      placement="bottomRight"
    >
      <Badge count={unreadCount ?? 0} size="small">
        <Button type="text" icon={<BellOutlined />} />
      </Badge>
    </Dropdown>
  );
}
