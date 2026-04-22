import { Card, Table, Tag, Button, Switch } from 'antd';
import { PlusOutlined, PlayCircleOutlined } from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';
import { formatDate } from '@/utils/formatters';

const mockJobs = [
  { id: '1', name: 'Monthly Valuation', job_type: 'calculation', cron_expression: '0 2 1 * *', is_active: true, next_run: '2024-03-01' },
  { id: '2', name: 'Daily Data Check', job_type: 'data_check', cron_expression: '0 6 * * *', is_active: false, next_run: null },
];

export default function ScheduledJobList() {
  const columns = [
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Type', dataIndex: 'job_type', key: 'type', render: (v: string) => <Tag>{v}</Tag> },
    { title: 'Schedule', dataIndex: 'cron_expression', key: 'cron', render: (v: string) => <code>{v}</code> },
    { title: 'Active', dataIndex: 'is_active', key: 'active', render: (v: boolean) => <Switch checked={v} size="small" /> },
    { title: 'Next Run', dataIndex: 'next_run', key: 'next', render: (v: string) => v ? formatDate(v) : '-' },
    { title: 'Actions', key: 'actions', render: () => <Button icon={<PlayCircleOutlined />} size="small">Run Now</Button> },
  ];

  return (
    <>
      <PageHeader title="Scheduled Jobs" extra={<Button type="primary" icon={<PlusOutlined />}>New Job</Button>} />
      <Card>
        <Table columns={columns} dataSource={mockJobs} rowKey="id" />
      </Card>
    </>
  );
}
