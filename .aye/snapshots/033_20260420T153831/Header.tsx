import { useState } from 'react';
import { Layout, Button, Space, Dropdown, Badge, Avatar, Typography } from 'antd';
import {
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  BellOutlined,
  UserOutlined,
  LogoutOutlined,
  SettingOutlined,
  SearchOutlined,
} from '@ant-design/icons';
import type { MenuProps } from 'antd';

import AISearchBar from '@/components/ai/AISearchBar';
import { useAuthStore } from '@/stores/authStore';
import { useUIStore } from '@/stores/uiStore';
import { useNotificationStore } from '@/stores/notificationStore';
import { useNotifications } from '@/hooks/useNotifications';
import { getInitials } from '@/utils/helpers';

const { Header: AntHeader } = Layout;
const { Text } = Typography;

export default function Header() {
  const { user, logout } = useAuthStore();
  const { sidebarCollapsed, toggleSidebar } = useUIStore();
  const { unreadCount } = useNotificationStore();
  const [searchOpen, setSearchOpen] = useState(false);

  // Fetch notifications
  useNotifications();

  const userMenuItems: MenuProps['items'] = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: 'Profile',
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: 'Settings',
    },
    { type: 'divider' },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'Logout',
      danger: true,
    },
  ];

  const handleUserMenuClick: MenuProps['onClick'] = ({ key }) => {
    if (key === 'logout') {
      logout();
    } else if (key === 'settings') {
      window.location.href = '/settings';
    }
  };

  return (
    <>
      <AntHeader
        style={{
          padding: '0 24px',
          background: '#fff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          borderBottom: '1px solid #f0f0f0',
          marginLeft: sidebarCollapsed ? 80 : 240,
          transition: 'margin-left 0.2s',
        }}
      >
        <Space>
          <Button
            type="text"
            icon={sidebarCollapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            onClick={toggleSidebar}
          />
          <Button
            type="text"
            icon={<SearchOutlined />}
            onClick={() => setSearchOpen(true)}
          >
            Search
            <kbd style={{ marginLeft: 8, opacity: 0.6 }}>⌘K</kbd>
          </Button>
        </Space>

        <Space size={16}>
          <Badge count={unreadCount} size="small">
            <Button type="text" icon={<BellOutlined />} />
          </Badge>

          <Dropdown
            menu={{ items: userMenuItems, onClick: handleUserMenuClick }}
            placement="bottomRight"
          >
            <Space style={{ cursor: 'pointer' }}>
              <Avatar style={{ backgroundColor: '#1890ff' }}>
                {user?.full_name ? getInitials(user.full_name) : 'U'}
              </Avatar>
              <Text>{user?.full_name}</Text>
            </Space>
          </Dropdown>
        </Space>
      </AntHeader>

      <AISearchBar open={searchOpen} onClose={() => setSearchOpen(false)} />
    </>
  );
}
