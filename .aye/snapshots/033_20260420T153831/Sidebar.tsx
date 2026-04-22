import { useMemo } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import type { MenuProps } from 'antd';
import {
  DashboardOutlined,
  FileTextOutlined,
  TeamOutlined,
  AlertOutlined,
  SettingOutlined,
  CalculatorOutlined,
  LineChartOutlined,
  BarChartOutlined,
  CloudUploadOutlined,
  CheckSquareOutlined,
  AuditOutlined,
  ScheduleOutlined,
  FileSearchOutlined,
  ExperimentOutlined,
  FolderOutlined,
  UserOutlined,
} from '@ant-design/icons';

import { useAuth } from '@/hooks/useAuth';
import { useUIStore } from '@/stores/uiStore';

const { Sider } = Layout;

type MenuItem = Required<MenuProps>['items'][number];

export default function Sidebar() {
  const location = useLocation();
  const { sidebarCollapsed } = useUIStore();
  const { hasPermission, hasAnyPermission } = useAuth();

  const menuItems = useMemo<MenuItem[]>(() => {
    const items: MenuItem[] = [
      {
        key: '/',
        icon: <DashboardOutlined />,
        label: <Link to="/">Dashboard</Link>,
      },
    ];

    // Policy Management
    if (hasAnyPermission(['policy:read', 'policyholder:read', 'claim:read'])) {
      items.push({
        key: 'policy-mgmt',
        icon: <FileTextOutlined />,
        label: 'Policy Management',
        children: [
          hasPermission('policy', 'read') && {
            key: '/policies',
            label: <Link to="/policies">Policies</Link>,
          },
          hasPermission('policyholder', 'read') && {
            key: '/policyholders',
            label: <Link to="/policyholders">Policyholders</Link>,
          },
          hasPermission('claim', 'read') && {
            key: '/claims',
            label: <Link to="/claims">Claims</Link>,
          },
        ].filter(Boolean),
      });
    }

    // Actuarial
    if (hasAnyPermission(['assumption:read', 'model:read', 'calculation:read', 'scenario:read'])) {
      items.push({
        key: 'actuarial',
        icon: <CalculatorOutlined />,
        label: 'Actuarial',
        children: [
          hasPermission('assumption', 'read') && {
            key: '/assumptions',
            label: <Link to="/assumptions">Assumptions</Link>,
          },
          hasPermission('model', 'read') && {
            key: '/models',
            label: <Link to="/models">Models</Link>,
          },
          hasPermission('calculation', 'read') && {
            key: '/calculations',
            label: <Link to="/calculations">Calculations</Link>,
          },
          hasPermission('scenario', 'read') && {
            key: '/scenarios',
            label: <Link to="/scenarios">Scenarios</Link>,
          },
        ].filter(Boolean),
      });
    }

    // Experience Analysis
    if (hasPermission('calculation', 'read')) {
      items.push({
        key: '/experience',
        icon: <ExperimentOutlined />,
        label: <Link to="/experience">Experience Studies</Link>,
      });
    }

    // Reports & Dashboards
    if (hasAnyPermission(['report:read', 'dashboard:read'])) {
      items.push({
        key: 'reporting',
        icon: <BarChartOutlined />,
        label: 'Reporting',
        children: [
          hasPermission('report', 'read') && {
            key: '/reports',
            label: <Link to="/reports">Reports</Link>,
          },
          hasPermission('dashboard', 'read') && {
            key: '/dashboards',
            label: <Link to="/dashboards">Dashboards</Link>,
          },
        ].filter(Boolean),
      });
    }

    // Data Management
    if (hasAnyPermission(['import:read', 'policy:create'])) {
      items.push({
        key: 'data',
        icon: <CloudUploadOutlined />,
        label: 'Data',
        children: [
          {
            key: '/imports',
            label: <Link to="/imports">Imports</Link>,
          },
          {
            key: '/documents',
            label: <Link to="/documents">Documents</Link>,
          },
        ],
      });
    }

    // Tasks
    if (hasPermission('task', 'read')) {
      items.push({
        key: '/tasks',
        icon: <CheckSquareOutlined />,
        label: <Link to="/tasks">Tasks</Link>,
      });
    }

    // Automation
    if (hasPermission('automation', 'read')) {
      items.push({
        key: 'automation',
        icon: <ScheduleOutlined />,
        label: 'Automation',
        children: [
          {
            key: '/automation/scheduled-jobs',
            label: <Link to="/automation/scheduled-jobs">Scheduled Jobs</Link>,
          },
          {
            key: '/automation/rules',
            label: <Link to="/automation/rules">Automation Rules</Link>,
          },
        ],
      });
    }

    // Audit
    if (hasPermission('audit', 'read')) {
      items.push({
        key: '/audit',
        icon: <AuditOutlined />,
        label: <Link to="/audit">Audit Log</Link>,
      });
    }

    // Admin
    if (hasAnyPermission(['user:read', 'role:read'])) {
      items.push({
        key: 'admin',
        icon: <SettingOutlined />,
        label: 'Administration',
        children: [
          hasPermission('user', 'read') && {
            key: '/admin/users',
            label: <Link to="/admin/users">Users</Link>,
          },
          hasPermission('role', 'read') && {
            key: '/admin/roles',
            label: <Link to="/admin/roles">Roles</Link>,
          },
        ].filter(Boolean),
      });
    }

    return items;
  }, [hasPermission, hasAnyPermission]);

  const selectedKeys = useMemo(() => {
    const path = location.pathname;
    return [path];
  }, [location.pathname]);

  const openKeys = useMemo(() => {
    const path = location.pathname;
    if (path.startsWith('/policies') || path.startsWith('/policyholders') || path.startsWith('/claims')) {
      return ['policy-mgmt'];
    }
    if (path.startsWith('/assumptions') || path.startsWith('/models') || path.startsWith('/calculations') || path.startsWith('/scenarios')) {
      return ['actuarial'];
    }
    if (path.startsWith('/reports') || path.startsWith('/dashboards')) {
      return ['reporting'];
    }
    if (path.startsWith('/imports') || path.startsWith('/documents')) {
      return ['data'];
    }
    if (path.startsWith('/automation')) {
      return ['automation'];
    }
    if (path.startsWith('/admin')) {
      return ['admin'];
    }
    return [];
  }, [location.pathname]);

  return (
    <Sider
      collapsed={sidebarCollapsed}
      collapsible
      trigger={null}
      width={240}
      style={{
        height: '100vh',
        position: 'fixed',
        left: 0,
        top: 0,
        bottom: 0,
        overflow: 'auto',
      }}
    >
      <div
        style={{
          height: 64,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          borderBottom: '1px solid rgba(255,255,255,0.1)',
        }}
      >
        <span
          style={{
            color: '#fff',
            fontSize: sidebarCollapsed ? 16 : 20,
            fontWeight: 700,
          }}
        >
          {sidebarCollapsed ? 'AF' : 'ActuFlow'}
        </span>
      </div>

      <Menu
        theme="dark"
        mode="inline"
        selectedKeys={selectedKeys}
        defaultOpenKeys={openKeys}
        items={menuItems}
        style={{ borderRight: 0 }}
      />
    </Sider>
  );
}
