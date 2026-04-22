import { Card, Table, Tag, Button } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';
import { formatDate } from '@/utils/formatters';

const mockStudies = [
  { id: '1', name: 'Mortality Study 2023', analysis_type: 'mortality', status: 'completed', created_at: '2024-01-01' },
  { id: '2', name: 'Lapse Analysis Q4', analysis_type: 'lapse', status: 'running', created_at: '2024-02-01' },
];

export default function ExperienceStudyList() {
  const columns = [
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Type', dataIndex: 'analysis_type', key: 'type', render: (v: string) => <Tag>{v}</Tag> },
    { title: 'Status', dataIndex: 'status', key: 'status', render: (v: string) => <StatusBadge status={v} /> },
    { title: 'Created', dataIndex: 'created_at', key: 'created', render: formatDate },
  ];

  return (
    <>
      <PageHeader title="Experience Studies" subtitle="Actual vs expected analysis" extra={<Button type="primary" icon={<PlusOutlined />}>New Study</Button>} />
      <Card>
        <Table columns={columns} dataSource={mockStudies} rowKey="id" />
      </Card>
    </>
  );
}
