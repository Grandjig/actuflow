import { useState } from 'react';
import { Layout, Button, Space, Dropdown, Badge, Avatar, Empty, List, Typography } from 'antd';
import {
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  BellOutlined,
  UserOutlined,
  LogoutOutlined,
  CheckOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';
import { formatRelativeTime } from '@/utils/formatters';

const { Header: AntHeader } = Layout;
const { Text } = Typography;

interface Props {
  collapsed: boolean;
  onToggle: () => void;
}

// Mock notifications for demo
const mockNotifications = [
  {
    id: '1',
    title: 'Calculation Completed',
    message: 'Monthly valuation run finished successfully',
    is_read: false,
    created_at: new Date(Date.now() - 1000 * 60 * 30).toISOString(), // 30 mins ago
  },
  {
    id: '2',
    title: 'New Claim Filed',
    message: 'Claim CLM-2024-000045 requires review',
    is_read: false,
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(), // 2 hours ago
  },
  {
    id: '3',
    title: 'Assumption Set Approved',
    message: 'Q1 2024 assumptions have been approved',
    is_read: false,
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 5).toISOString(), // 5 hours ago
  },
];

export default function Header({ collapsed, onToggle }: Props) {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  const [notifications, setNotifications] = useState(mockNotifications);

  const unreadCount = notifications.filter(n => !n.is_read).length;

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const markAsRead = (id: string) => {
    setNotifications(prev => 
      prev.map(n => n.id === id ? { ...n, is_read: true } : n)
    );
  };

  const markAllAsRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, is_read: true })));
  };

  const userMenu = {
    items: [
      { key: 'profile', icon: <UserOutlined />, label: 'Profile' },
      { type: 'divider' as const },
      { key: 'logout', icon: <LogoutOutlined />, label: 'Logout', onClick: handleLogout },
    ],
  };

  const notificationContent = (
    <div style={{ width: 360, background: '#fff', borderRadius: 8, boxShadow: '0 6px 16px rgba(0,0,0,0.08)' }}>
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
          <Button type="link" size="small" onClick={markAllAsRead}>
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
            renderItem={(notification) => (
              <List.Item
                style={{
                  padding: '12px 16px',
                  cursor: 'pointer',
                  background: notification.is_read ? 'transparent' : '#f6ffed',
                }}
                onClick={() => markAsRead(notification.id)}
              >
                <List.Item.Meta
                  avatar={
                    <div style={{ 
                      width: 8, 
                      height: 8, 
                      borderRadius: '50%', 
                      background: notification.is_read ? 'transparent' : '#1890ff',
                      marginTop: 6,
                    }} />
                  }
                  title={
                    <Text strong={!notification.is_read}>{notification.title}</Text>
                  }
                  description={
                    <div>
                      <div style={{ fontSize: 12, color: '#666' }}>
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
        <Button type="link" onClick={() => navigate('/tasks')}>
          View All Notifications
        </Button>
      </div>
    </div>
  );

  return (
    <AntHeader style={{ background: '#fff', padding: '0 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid #f0f0f0' }}>
      <Button type="text" icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />} onClick={onToggle} />
      <Space size="middle">
        <Dropdown
          dropdownRender={() => notificationContent}
          trigger={['click']}
          placement="bottomRight"
        >
          <Badge count={unreadCount}>
            <Button type="text" icon={<BellOutlined style={{ fontSize: 18 }} />} />
          </Badge>
        </Dropdown>
        <Dropdown menu={userMenu}>
          <Space style={{ cursor: 'pointer' }}>
            <Avatar icon={<UserOutlined />} />
            <span>{user?.full_name || 'User'}</span>
          </Space>
        </Dropdown>
      </Space>
    </AntHeader>
  );
}
