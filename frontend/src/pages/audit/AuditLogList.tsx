import { Card, Table, Tag, Input } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';
import { formatDate } from '@/utils/formatters';

const mockLogs = [
  { id: '1', user_email: 'admin@actuflow.com', action: 'create', resource_type: 'policy', timestamp: '2024-02-01T10:30:00Z' },
  { id: '2', user_email: 'actuary@actuflow.com', action: 'update', resource_type: 'assumption_set', timestamp: '2024-02-01T09:15:00Z' },
  { id: '3', user_email: 'admin@actuflow.com', action: 'approve', resource_type: 'calculation_run', timestamp: '2024-01-31T16:00:00Z' },
];

export default function AuditLogList() {
  const columns = [
    { title: 'Timestamp', dataIndex: 'timestamp', key: 'time', render: formatDate },
    { title: 'User', dataIndex: 'user_email', key: 'user' },
    { title: 'Action', dataIndex: 'action', key: 'action',
      render: (v: string) => <Tag color={v === 'delete' ? 'red' : v === 'create' ? 'green' : 'blue'}>{v}</Tag> },
    { title: 'Resource', dataIndex: 'resource_type', key: 'resource', render: (v: string) => <Tag>{v}</Tag> },
  ];

  return (
    <>
      <PageHeader title="Audit Log" subtitle="System activity history" />
      <Card>
        <Input placeholder="Search logs..." prefix={<SearchOutlined />} style={{ width: 300, marginBottom: 16 }} />
        <Table columns={columns} dataSource={mockLogs} rowKey="id" />
      </Card>
    </>
  );
}
