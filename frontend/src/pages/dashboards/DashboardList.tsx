import { useNavigate } from 'react-router-dom';
import { Card, Table, Button } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';
import { formatDate } from '@/utils/formatters';

const mockDashboards = [
  { id: '1', name: 'Executive Overview', is_shared: true, created_at: '2024-01-01' },
  { id: '2', name: 'Claims Analysis', is_shared: false, created_at: '2024-01-15' },
];

export default function DashboardList() {
  const navigate = useNavigate();
  const columns = [
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Shared', dataIndex: 'is_shared', key: 'shared', render: (v: boolean) => v ? 'Yes' : 'No' },
    { title: 'Created', dataIndex: 'created_at', key: 'created', render: formatDate },
  ];

  return (
    <>
      <PageHeader title="Dashboards" extra={<Button type="primary" icon={<PlusOutlined />}>New Dashboard</Button>} />
      <Card>
        <Table columns={columns} dataSource={mockDashboards} rowKey="id"
          onRow={(r) => ({ onClick: () => navigate(`/dashboards/${r.id}`) })} />
      </Card>
    </>
  );
}
