import { useMemo } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import {
  DashboardOutlined,
  FileTextOutlined,
  TeamOutlined,
  SafetyOutlined,
  CalculatorOutlined,
  LineChartOutlined,
  ExperimentOutlined,
  BarChartOutlined,
  AppstoreOutlined,
  ImportOutlined,
  CheckSquareOutlined,
  SettingOutlined,
  AuditOutlined,
  FileSearchOutlined,
  RobotOutlined,
  ClockCircleOutlined,
} from '@ant-design/icons';
import type { MenuProps } from 'antd';
import { useUIStore } from '@/stores/uiStore';
import { useAuth } from '@/hooks/useAuth';

const { Sider } = Layout;

type MenuItem = Required<MenuProps>['items'][number];

export default function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();
  const { sidebarCollapsed, toggleSidebar } = useUIStore();
  const { hasPermission } = useAuth();

  const menuItems: MenuItem[] = useMemo(() => {
    const items: MenuItem[] = [
      {
        key: '/',
        icon: <DashboardOutlined />,
        label: 'Dashboard',
      },
    ];

    // Policy Management
    if (hasPermission('policy', 'read')) {
      items.push({
        key: 'policies-group',
        icon: <FileTextOutlined />,
        label: 'Policy Management',
        children: [
          { key: '/policies', label: 'Policies' },
          { key: '/policyholders', label: 'Policyholders' },
          { key: '/claims', label: 'Claims' },
        ],
      });
    }

    // Actuarial
    if (hasPermission('assumption', 'read') || hasPermission('model', 'read')) {
      items.push({
        key: 'actuarial-group',
        icon: <CalculatorOutlined />,
        label: 'Actuarial',
        children: [
          { key: '/assumptions', label: 'Assumption Sets' },
          { key: '/models', label: 'Models' },
          { key: '/calculations', label: 'Calculations' },
          { key: '/scenarios', label: 'Scenarios' },
          { key: '/experience', label: 'Experience Studies' },
        ],
      });
    }

    // Reporting
    if (hasPermission('report', 'read')) {
      items.push({
        key: 'reporting-group',
        icon: <BarChartOutlined />,
        label: 'Reporting',
        children: [
          { key: '/reports', label: 'Generated Reports' },
          { key: '/reports/templates', label: 'Report Templates' },
          { key: '/dashboards', label: 'Dashboards' },
        ],
      });
    }

    // Data Management
    if (hasPermission('import', 'read') || hasPermission('document', 'read')) {
      items.push({
        key: 'data-group',
        icon: <ImportOutlined />,
        label: 'Data Management',
        children: [
          { key: '/imports', label: 'Data Imports' },
          { key: '/documents', label: 'Documents' },
        ],
      });
    }

    // Workflow
    items.push({
      key: '/tasks',
      icon: <CheckSquareOutlined />,
      label: 'Tasks',
    });

    // Automation
    if (hasPermission('automation', 'read')) {
      items.push({
        key: 'automation-group',
        icon: <ClockCircleOutlined />,
        label: 'Automation',
        children: [
          { key: '/automation/jobs', label: 'Scheduled Jobs' },
          { key: '/automation/rules', label: 'Automation Rules' },
        ],
      });
    }

    // Audit
    if (hasPermission('audit', 'read')) {
      items.push({
        key: '/audit',
        icon: <AuditOutlined />,
        label: 'Audit Log',
      });
    }

    // Admin
    if (hasPermission('user', 'read')) {
      items.push({
        key: 'admin-group',
        icon: <SettingOutlined />,
        label: 'Administration',
        children: [
          { key: '/admin/users', label: 'Users' },
          { key: '/admin/roles', label: 'Roles' },
        ],
      });
    }

    return items;
  }, [hasPermission]);

  const selectedKeys = useMemo(() => {
    const path = location.pathname;
    return [path];
  }, [location.pathname]);

  const openKeys = useMemo(() => {
    const path = location.pathname;
    if (path.startsWith('/policies') || path.startsWith('/policyholders') || path.startsWith('/claims')) {
      return ['policies-group'];
    }
    if (path.startsWith('/assumptions') || path.startsWith('/models') || path.startsWith('/calculations') || path.startsWith('/scenarios') || path.startsWith('/experience')) {
      return ['actuarial-group'];
    }
    if (path.startsWith('/reports') || path.startsWith('/dashboards')) {
      return ['reporting-group'];
    }
    if (path.startsWith('/imports') || path.startsWith('/documents')) {
      return ['data-group'];
    }
    if (path.startsWith('/automation')) {
      return ['automation-group'];
    }
    if (path.startsWith('/admin')) {
      return ['admin-group'];
    }
    return [];
  }, [location.pathname]);

  const handleMenuClick: MenuProps['onClick'] = ({ key }) => {
    if (!key.endsWith('-group')) {
      navigate(key);
    }
  };

  return (
    <Sider
      collapsible
      collapsed={sidebarCollapsed}
      onCollapse={toggleSidebar}
      style={{
        overflow: 'auto',
        height: '100vh',
        position: 'fixed',
        left: 0,
        top: 0,
        bottom: 0,
        zIndex: 100,
      }}
      theme="dark"
    >
      <div
        style={{
          height: 64,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
          fontSize: sidebarCollapsed ? 16 : 20,
          fontWeight: 'bold',
        }}
      >
        {sidebarCollapsed ? 'AF' : 'ActuFlow'}
      </div>
      <Menu
        theme="dark"
        mode="inline"
        selectedKeys={selectedKeys}
        defaultOpenKeys={openKeys}
        items={menuItems}
        onClick={handleMenuClick}
      />
    </Sider>
  );
}
