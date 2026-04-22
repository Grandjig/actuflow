import { Layout, Button, Dropdown, Badge, Avatar, Space, Input, Tooltip } from 'antd';
import type { MenuProps } from 'antd';
import {
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  BellOutlined,
  UserOutlined,
  LogoutOutlined,
  SettingOutlined,
  SearchOutlined,
  ThunderboltOutlined,
} from '@ant-design/icons';

import { useAuth } from '@/hooks/useAuth';
import { useNotifications } from '@/hooks/useNotifications';
import { useUIStore } from '@/stores/uiStore';

const { Header: AntHeader } = Layout;

export default function Header() {
  const { user, logout } = useAuth();
  const { unreadCount } = useNotifications();
  const { sidebarCollapsed, toggleSidebar, openCommandPalette } = useUIStore();

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
    {
      type: 'divider',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'Logout',
      onClick: logout,
    },
  ];

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      openCommandPalette();
    }
  };

  return (
    <AntHeader
      style={{
        padding: '0 24px',
        background: '#fff',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        boxShadow: '0 1px 4px rgba(0,0,0,0.08)',
        position: 'sticky',
        top: 0,
        zIndex: 100,
      }}
      onKeyDown={handleKeyDown}
    >
      <Space>
        <Button
          type="text"
          icon={sidebarCollapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
          onClick={toggleSidebar}
        />

        {/* AI Search Button */}
        <Tooltip title="AI Search (Cmd+K)">
          <Button
            icon={<ThunderboltOutlined />}
            onClick={openCommandPalette}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 8,
              color: '#666',
              width: 280,
              justifyContent: 'flex-start',
            }}
          >
            <span>Search or ask anything...</span>
            <kbd
              style={{
                marginLeft: 'auto',
                padding: '2px 6px',
                background: '#f0f0f0',
                borderRadius: 4,
                fontSize: 11,
              }}
            >
              ⌘K
            </kbd>
          </Button>
        </Tooltip>
      </Space>

      <Space size="middle">
        {/* Notifications */}
        <Dropdown
          menu={{
            items: [
              {
                key: 'notifications-header',
                label: <strong>Notifications</strong>,
                disabled: true,
              },
              { type: 'divider' },
              {
                key: 'no-notifications',
                label: 'No new notifications',
                disabled: true,
              },
              { type: 'divider' },
              {
                key: 'view-all',
                label: 'View all notifications',
              },
            ],
          }}
          placement="bottomRight"
          trigger={['click']}
        >
          <Badge count={unreadCount} size="small">
            <Button type="text" icon={<BellOutlined />} />
          </Badge>
        </Dropdown>

        {/* User Menu */}
        <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
          <Space style={{ cursor: 'pointer' }}>
            <Avatar icon={<UserOutlined />} />
            <span>{user?.full_name || user?.email}</span>
          </Space>
        </Dropdown>
      </Space>
    </AntHeader>
  );
}
