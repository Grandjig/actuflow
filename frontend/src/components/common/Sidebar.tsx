import { useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import {
  DashboardOutlined,
  FileTextOutlined,
  TeamOutlined,
  AlertOutlined,
  SettingOutlined,
  CalculatorOutlined,
  ExperimentOutlined,
  BarChartOutlined,
  UploadOutlined,
  CheckSquareOutlined,
  ClockCircleOutlined,
  AuditOutlined,
  FolderOutlined,
  UserOutlined,
} from '@ant-design/icons';

const { Sider } = Layout;

interface Props {
  collapsed: boolean;
}

export default function Sidebar({ collapsed }: Props) {
  const navigate = useNavigate();
  const location = useLocation();

  const items = [
    { key: '/', icon: <DashboardOutlined />, label: 'Dashboard' },
    { key: '/policies', icon: <FileTextOutlined />, label: 'Policies' },
    { key: '/policyholders', icon: <TeamOutlined />, label: 'Policyholders' },
    { key: '/claims', icon: <AlertOutlined />, label: 'Claims' },
    { key: '/assumptions', icon: <SettingOutlined />, label: 'Assumptions' },
    { key: '/calculations', icon: <CalculatorOutlined />, label: 'Calculations' },
    { key: '/scenarios', icon: <ExperimentOutlined />, label: 'Scenarios' },
    { key: '/reports', icon: <BarChartOutlined />, label: 'Reports' },
    { key: '/imports', icon: <UploadOutlined />, label: 'Imports' },
    { key: '/tasks', icon: <CheckSquareOutlined />, label: 'Tasks' },
    { key: 'automation', icon: <ClockCircleOutlined />, label: 'Automation', children: [
      { key: '/automation/jobs', label: 'Scheduled Jobs' },
      { key: '/automation/rules', label: 'Rules' },
    ]},
    { key: '/documents', icon: <FolderOutlined />, label: 'Documents' },
    { key: '/audit', icon: <AuditOutlined />, label: 'Audit Log' },
    { key: 'admin', icon: <UserOutlined />, label: 'Admin', children: [
      { key: '/admin/users', label: 'Users' },
      { key: '/admin/roles', label: 'Roles' },
    ]},
  ];

  return (
    <Sider collapsible collapsed={collapsed} trigger={null} theme="light" width={240}>
      <div style={{ height: 64, display: 'flex', alignItems: 'center', justifyContent: 'center', borderBottom: '1px solid #f0f0f0' }}>
        <span style={{ fontSize: collapsed ? 16 : 20, fontWeight: 'bold', color: '#1890ff' }}>
          {collapsed ? 'AF' : 'ActuFlow'}
        </span>
      </div>
      <Menu
        mode="inline"
        selectedKeys={[location.pathname]}
        items={items}
        onClick={({ key }) => navigate(key)}
        style={{ borderRight: 0 }}
      />
    </Sider>
  );
}
