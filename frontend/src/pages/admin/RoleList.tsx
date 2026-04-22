import { Card, Table, Tag, Button } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';

const mockRoles = [
  { id: '1', name: 'admin', description: 'Full access', permissions_count: 50 },
  { id: '2', name: 'actuary', description: 'Actuarial operations', permissions_count: 25 },
  { id: '3', name: 'viewer', description: 'Read-only access', permissions_count: 10 },
];

export default function RoleList() {
  const columns = [
    { title: 'Role', dataIndex: 'name', key: 'name', render: (v: string) => <Tag color="blue">{v}</Tag> },
    { title: 'Description', dataIndex: 'description', key: 'desc' },
    { title: 'Permissions', dataIndex: 'permissions_count', key: 'perms' },
  ];

  return (
    <>
      <PageHeader title="Roles" subtitle="Role & permission management" extra={<Button type="primary" icon={<PlusOutlined />}>Add Role</Button>} />
      <Card>
        <Table columns={columns} dataSource={mockRoles} rowKey="id" />
      </Card>
    </>
  );
}
