/**
 * Main application layout with sidebar navigation.
 */

import { useState } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
  Layout,
  Menu,
  Button,
  Avatar,
  Dropdown,
  Space,
  Typography,
  Badge,
} from 'antd';
import {
  DashboardOutlined,
  FileTextOutlined,
  TeamOutlined,
  CalculatorOutlined,
  BarChartOutlined,
  SettingOutlined,
  BellOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  LogoutOutlined,
  UserOutlined,
  ExperimentOutlined,
  CloudUploadOutlined,
} from '@ant-design/icons';
import type { MenuProps } from 'antd';
import { useAuth } from '@/hooks/useAuth';
import { getInitials } from '@/utils/helpers';

const { Header, Sider, Content } = Layout;
const { Text } = Typography;

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

const menuItems: MenuItem[] = [
  getItem('Dashboard', '/', <DashboardOutlined />),
  getItem('Policies', '/policies', <FileTextOutlined />),
  getItem('Claims', '/claims', <TeamOutlined />),
  getItem('Assumptions', '/assumptions', <ExperimentOutlined />),
  getItem('Calculations', '/calculations', <CalculatorOutlined />),
  getItem('Reports', '/reports', <BarChartOutlined />, [
    getItem('Generated Reports', '/reports/generated'),
    getItem('Templates', '/reports/templates'),
  ]),
  getItem('Data Import', '/imports', <CloudUploadOutlined />),
  getItem('Settings', '/settings', <SettingOutlined />, [
    getItem('Profile', '/settings/profile'),
    getItem('Users', '/settings/users'),
  ]),
];

export default function MainLayout() {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();

  const handleMenuClick: MenuProps['onClick'] = (e) => {
    navigate(e.key);
  };

  const userMenuItems: MenuProps['items'] = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: 'Profile',
      onClick: () => navigate('/settings/profile'),
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

  // Find the selected key based on current path
  const selectedKeys = [location.pathname];
  const openKeys = menuItems
    .filter((item): item is MenuItem & { children?: MenuItem[] } => 
      item !== null && 'children' in item && Array.isArray(item.children)
    )
    .filter((item) => 
      item.children?.some((child) => 
        child !== null && 'key' in child && location.pathname.startsWith(String(child.key))
      )
    )
    .map((item) => String(item.key));

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider
        trigger={null}
        collapsible
        collapsed={collapsed}
        theme="light"
        style={{
          borderRight: '1px solid #f0f0f0',
        }}
      >
        <div
          style={{
            height: 64,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            borderBottom: '1px solid #f0f0f0',
          }}
        >
          <Text strong style={{ fontSize: collapsed ? 16 : 20 }}>
            {collapsed ? 'AF' : 'ActuFlow'}
          </Text>
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
            background: '#fff',
            borderBottom: '1px solid #f0f0f0',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <Button
            type="text"
            icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            onClick={() => setCollapsed(!collapsed)}
          />
          <Space size="large">
            <Badge count={3}>
              <Button type="text" icon={<BellOutlined />} />
            </Badge>
            <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
              <Space style={{ cursor: 'pointer' }}>
                <Avatar style={{ backgroundColor: '#1890ff' }}>
                  {user ? getInitials(user.full_name) : 'U'}
                </Avatar>
                <Text>{user?.full_name || 'User'}</Text>
              </Space>
            </Dropdown>
          </Space>
        </Header>
        <Content
          style={{
            margin: 24,
            padding: 24,
            background: '#fff',
            borderRadius: 8,
            minHeight: 'auto',
          }}
        >
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
}
