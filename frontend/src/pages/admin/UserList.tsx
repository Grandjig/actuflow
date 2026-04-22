import { Card, Table, Tag, Button, Switch } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';
import { formatDate } from '@/utils/formatters';

const mockUsers = [
  { id: '1', email: 'admin@actuflow.com', full_name: 'System Admin', role: 'admin', is_active: true, created_at: '2024-01-01' },
  { id: '2', email: 'actuary@actuflow.com', full_name: 'John Actuary', role: 'actuary', is_active: true, created_at: '2024-01-01' },
  { id: '3', email: 'viewer@actuflow.com', full_name: 'Jane Viewer', role: 'viewer', is_active: false, created_at: '2024-01-15' },
];

export default function UserList() {
  const columns = [
    { title: 'Name', dataIndex: 'full_name', key: 'name' },
    { title: 'Email', dataIndex: 'email', key: 'email' },
    { title: 'Role', dataIndex: 'role', key: 'role', render: (v: string) => <Tag color="blue">{v}</Tag> },
    { title: 'Active', dataIndex: 'is_active', key: 'active', render: (v: boolean) => <Switch checked={v} size="small" /> },
    { title: 'Created', dataIndex: 'created_at', key: 'created', render: formatDate },
  ];

  return (
    <>
      <PageHeader title="Users" subtitle="User management" extra={<Button type="primary" icon={<PlusOutlined />}>Add User</Button>} />
      <Card>
        <Table columns={columns} dataSource={mockUsers} rowKey="id" />
      </Card>
    </>
  );
}
