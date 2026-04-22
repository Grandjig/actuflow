import { Card, Table, Tag, Button } from 'antd';
import { DownloadOutlined } from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';
import { formatDate } from '@/utils/formatters';

const mockReports = [
  { id: '1', name: 'Q4 2023 Reserve Report', template: 'IFRS17', status: 'completed', generated_at: '2024-01-15' },
  { id: '2', name: 'January 2024 Summary', template: 'Internal', status: 'generating', generated_at: '2024-02-01' },
];

export default function GeneratedReportList() {
  const columns = [
    { title: 'Report', dataIndex: 'name', key: 'name' },
    { title: 'Template', dataIndex: 'template', key: 'template', render: (v: string) => <Tag>{v}</Tag> },
    { title: 'Status', dataIndex: 'status', key: 'status', render: (v: string) => <StatusBadge status={v} /> },
    { title: 'Generated', dataIndex: 'generated_at', key: 'date', render: formatDate },
    { title: 'Actions', key: 'actions', render: () => <Button icon={<DownloadOutlined />} size="small">Download</Button> },
  ];

  return (
    <>
      <PageHeader title="Generated Reports" subtitle="View and download reports" extra={<Button type="primary">Generate Report</Button>} />
      <Card>
        <Table columns={columns} dataSource={mockReports} rowKey="id" />
      </Card>
    </>
  );
}
