import { useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu, Typography } from 'antd';
import type { MenuProps } from 'antd';
import {
  DashboardOutlined,
  FileTextOutlined,
  TeamOutlined,
  AlertOutlined,
  SettingOutlined,
  CalculatorOutlined,
  LineChartOutlined,
  UploadOutlined,
  FileSearchOutlined,
  ClockCircleOutlined,
  AuditOutlined,
} from '@ant-design/icons';

import { useAuthStore } from '@/stores/authStore';

const { Sider } = Layout;
const { Text } = Typography;

interface SidebarProps {
  collapsed: boolean;
}

export default function Sidebar({ collapsed }: SidebarProps) {
  const navigate = useNavigate();
  const location = useLocation();
  const { hasPermission } = useAuthStore();

  const menuItems: MenuProps['items'] = [
    {
      key: '/dashboard',
      icon: <DashboardOutlined />,
      label: 'Dashboard',
    },
    {
      key: 'data',
      icon: <FileTextOutlined />,
      label: 'Policy Data',
      children: [
        {
          key: '/policies',
          label: 'Policies',
        },
        {
          key: '/policyholders',
          label: 'Policyholders',
        },
        {
          key: '/claims',
          label: 'Claims',
        },
      ],
    },
    {
      key: 'actuarial',
      icon: <CalculatorOutlined />,
      label: 'Actuarial',
      children: [
        {
          key: '/assumptions',
          label: 'Assumptions',
        },
        {
          key: '/models',
          label: 'Models',
        },
        {
          key: '/calculations',
          label: 'Calculations',
        },
        {
          key: '/scenarios',
          label: 'Scenarios',
        },
      ],
    },
    {
      key: '/reports',
      icon: <LineChartOutlined />,
      label: 'Reports',
    },
    {
      key: '/imports',
      icon: <UploadOutlined />,
      label: 'Data Import',
    },
    {
      key: 'automation',
      icon: <ClockCircleOutlined />,
      label: 'Automation',
      children: [
        {
          key: '/automation/jobs',
          label: 'Scheduled Jobs',
        },
        {
          key: '/automation/rules',
          label: 'Rules',
        },
      ],
    },
    {
      key: '/audit',
      icon: <AuditOutlined />,
      label: 'Audit Log',
    },
    {
      key: '/settings',
      icon: <SettingOutlined />,
      label: 'Settings',
    },
  ];

  const handleMenuClick: MenuProps['onClick'] = ({ key }) => {
    if (!key.startsWith('/')) return;
    navigate(key);
  };

  const getSelectedKeys = () => {
    const path = location.pathname;
    if (path.startsWith('/policies')) return ['/policies'];
    if (path.startsWith('/claims')) return ['/claims'];
    if (path.startsWith('/assumptions')) return ['/assumptions'];
    if (path.startsWith('/calculations')) return ['/calculations'];
    return [path];
  };

  const getOpenKeys = () => {
    const path = location.pathname;
    if (path.startsWith('/policies') || path.startsWith('/policyholders') || path.startsWith('/claims')) {
      return ['data'];
    }
    if (path.startsWith('/assumptions') || path.startsWith('/models') || path.startsWith('/calculations') || path.startsWith('/scenarios')) {
      return ['actuarial'];
    }
    if (path.startsWith('/automation')) {
      return ['automation'];
    }
    return [];
  };

  return (
    <Sider
      trigger={null}
      collapsible
      collapsed={collapsed}
      width={240}
      style={{
        overflow: 'auto',
        height: '100vh',
        position: 'fixed',
        left: 0,
        top: 0,
        bottom: 0,
        background: '#001529',
      }}
    >
      <div
        style={{
          height: 64,
          display: 'flex',
          alignItems: 'center',
          justifyContent: collapsed ? 'center' : 'flex-start',
          padding: collapsed ? 0 : '0 24px',
          borderBottom: '1px solid rgba(255,255,255,0.1)',
        }}
      >
        <CalculatorOutlined style={{ fontSize: 24, color: '#fff' }} />
        {!collapsed && (
          <Text
            strong
            style={{
              color: '#fff',
              fontSize: 18,
              marginLeft: 12,
            }}
          >
            ActuFlow
          </Text>
        )}
      </div>

      <Menu
        theme="dark"
        mode="inline"
        selectedKeys={getSelectedKeys()}
        defaultOpenKeys={collapsed ? [] : getOpenKeys()}
        items={menuItems}
        onClick={handleMenuClick}
        style={{ borderRight: 0 }}
      />
    </Sider>
  );
}
