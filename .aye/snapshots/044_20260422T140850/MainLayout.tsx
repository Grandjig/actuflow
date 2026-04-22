import { useState } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu, Button, Avatar, Dropdown, Badge, Space, Input, theme } from 'antd';
import {
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  DashboardOutlined,
  FileTextOutlined,
  TeamOutlined,
  CalculatorOutlined,
  LineChartOutlined,
  SettingOutlined,
  BellOutlined,
  UserOutlined,
  LogoutOutlined,
  SearchOutlined,
  RobotOutlined,
  ExclamationCircleOutlined,
  BarChartOutlined,
  ImportOutlined,
  CheckSquareOutlined,
  FieldTimeOutlined,
} from '@ant-design/icons';
import type { MenuProps } from 'antd';
import { useAuthStore } from '@/stores/authStore';
import { useNotificationStore } from '@/stores/notificationStore';
import NotificationDropdown from '@/components/common/NotificationDropdown';
import AISearchBar from '@/components/ai/AISearchBar';
import { getInitials } from '@/utils/helpers';

const { Header, Sider, Content } = Layout;

type MenuItem = Required<MenuProps>['items'][number];

function getItem(
  label: React.ReactNode,
  key: string,
  icon?: React.ReactNode,
  children?: MenuItem[]
): MenuItem {
  return {
    key,
    icon,
    children,
    label,
  } as MenuItem;
}

export default function MainLayout() {
  const [collapsed, setCollapsed] = useState(false);
  const [aiSearchOpen, setAISearchOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuthStore();
  const { unreadCount } = useNotificationStore();
  const { token } = theme.useToken();

  const menuItems: MenuItem[] = [
    getItem('Dashboard', '/', <DashboardOutlined />),
    getItem('Policy Data', 'policy-data', <FileTextOutlined />, [
      getItem('Policies', '/policies'),
      getItem('Policyholders', '/policyholders'),
      getItem('Claims', '/claims'),
    ]),
    getItem('Actuarial', 'actuarial', <CalculatorOutlined />, [
      getItem('Assumptions', '/assumptions'),
      getItem('Models', '/models'),
      getItem('Calculations', '/calculations'),
      getItem('Scenarios', '/scenarios'),
    ]),
    getItem('Reporting', 'reporting', <BarChartOutlined />, [
      getItem('Reports', '/reports'),
      getItem('Experience Analysis', '/experience'),
    ]),
    getItem('Data Management', 'data', <ImportOutlined />, [
      getItem('Imports', '/imports'),
      getItem('Documents', '/documents'),
    ]),
    getItem('Tasks', '/tasks', <CheckSquareOutlined />),
    getItem('Automation', 'automation', <FieldTimeOutlined />, [
      getItem('Scheduled Jobs', '/automation/jobs'),
      getItem('Rules', '/automation/rules'),
    ]),
    getItem('Settings', 'settings', <SettingOutlined />, [
      getItem('Users', '/settings/users'),
      getItem('Roles', '/settings/roles'),
      getItem('Audit Log', '/audit'),
    ]),
  ];

  const handleMenuClick: MenuProps['onClick'] = (e) => {
    if (e.key.startsWith('/')) {
      navigate(e.key);
    }
  };

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
      onClick: () => navigate('/settings'),
    },
    { type: 'divider' },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'Logout',
      onClick: () => {
        logout();
        navigate('/login');
      },
    },
  ];

  // Get selected keys based on current path
  const selectedKeys = [location.pathname];
  const openKeys = menuItems
    .filter((item: any) => item?.children?.some((child: any) => child?.key === location.pathname))
    .map((item: any) => item?.key)
    .filter(Boolean) as string[];

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider
        trigger={null}
        collapsible
        collapsed={collapsed}
        width={240}
        style={{
          background: token.colorBgContainer,
          borderRight: `1px solid ${token.colorBorderSecondary}`,
        }}
      >
        <div
          style={{
            height: 64,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            borderBottom: `1px solid ${token.colorBorderSecondary}`,
          }}
        >
          <h1 style={{ margin: 0, fontSize: collapsed ? 18 : 22, fontWeight: 700, color: token.colorPrimary }}>
            {collapsed ? 'AF' : 'ActuFlow'}
          </h1>
        </div>
        <Menu
          mode="inline"
          selectedKeys={selectedKeys}
          defaultOpenKeys={openKeys}
          items={menuItems}
          onClick={handleMenuClick}
          style={{ borderRight: 0 }}
        />
      </Sider>

      <Layout>
        <Header
          style={{
            padding: '0 24px',
            background: token.colorBgContainer,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            borderBottom: `1px solid ${token.colorBorderSecondary}`,
          }}
        >
          <Space>
            <Button
              type="text"
              icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
              onClick={() => setCollapsed(!collapsed)}
            />
            <Input
              placeholder="Search or ask AI (Ctrl+K)"
              prefix={<SearchOutlined />}
              suffix={<RobotOutlined style={{ color: '#8c8c8c' }} />}
              style={{ width: 300 }}
              onClick={() => setAISearchOpen(true)}
              readOnly
            />
          </Space>

          <Space size="middle">
            <NotificationDropdown>
              <Badge count={unreadCount} size="small">
                <Button type="text" icon={<BellOutlined style={{ fontSize: 18 }} />} />
              </Badge>
            </NotificationDropdown>

            <Dropdown menu={{ items: userMenuItems }} trigger={['click']}>
              <Space style={{ cursor: 'pointer' }}>
                <Avatar style={{ backgroundColor: token.colorPrimary }}>
                  {getInitials(user?.full_name)}
                </Avatar>
                <span>{user?.full_name}</span>
              </Space>
            </Dropdown>
          </Space>
        </Header>

        <Content
          style={{
            margin: 24,
            padding: 24,
            background: token.colorBgContainer,
            borderRadius: token.borderRadiusLG,
            minHeight: 280,
            overflow: 'auto',
          }}
        >
          <Outlet />
        </Content>
      </Layout>

      <AISearchBar open={aiSearchOpen} onClose={() => setAISearchOpen(false)} />
    </Layout>
  );
}
