import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Layout,
  Input,
  Badge,
  Avatar,
  Dropdown,
  Space,
  Button,
  Tooltip,
} from 'antd';
import {
  BellOutlined,
  UserOutlined,
  LogoutOutlined,
  SettingOutlined,
  SearchOutlined,
  RobotOutlined,
} from '@ant-design/icons';
import type { MenuProps } from 'antd';
import { useAuth } from '@/hooks/useAuth';
import { useNotificationStore } from '@/stores/notificationStore';
import { useUIStore } from '@/stores/uiStore';
import AISearchBar from '../ai/AISearchBar';
import NotificationDropdown from './NotificationDropdown';

const { Header: AntHeader } = Layout;

export default function Header() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { unreadCount } = useNotificationStore();
  const { openCommandPalette } = useUIStore();
  const [showAISearch, setShowAISearch] = useState(false);

  const userMenuItems: MenuProps['items'] = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: 'Profile',
      onClick: () => navigate('/profile'),
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: 'Settings',
      onClick: () => navigate('/settings'),
    },
    { type: 'divider' },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'Logout',
      onClick: logout,
    },
  ];

  return (
    <>
      <AntHeader
        style={{
          background: '#fff',
          padding: '0 24px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          boxShadow: '0 1px 4px rgba(0,0,0,0.08)',
          position: 'sticky',
          top: 0,
          zIndex: 10,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 16, flex: 1 }}>
          <Input
            placeholder="Search... (Ctrl+K for AI)"
            prefix={<SearchOutlined />}
            style={{ maxWidth: 400 }}
            onClick={() => setShowAISearch(true)}
            readOnly
          />
          <Tooltip title="AI Assistant (Ctrl+K)">
            <Button
              icon={<RobotOutlined />}
              onClick={() => setShowAISearch(true)}
            >
              Ask AI
            </Button>
          </Tooltip>
        </div>

        <Space size="middle">
          <NotificationDropdown>
            <Badge count={unreadCount} size="small">
              <Button icon={<BellOutlined />} type="text" />
            </Badge>
          </NotificationDropdown>

          <Dropdown menu={{ items: userMenuItems }} trigger={['click']}>
            <Space style={{ cursor: 'pointer' }}>
              <Avatar icon={<UserOutlined />} />
              <span>{user?.full_name}</span>
            </Space>
          </Dropdown>
        </Space>
      </AntHeader>

      <AISearchBar
        open={showAISearch}
        onClose={() => setShowAISearch(false)}
      />
    </>
  );
}
