import { Card, Table, Tag, Button } from 'antd';
import { CheckOutlined } from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';
import { formatDate } from '@/utils/formatters';

const mockTasks = [
  { id: '1', title: 'Review Q4 Assumptions', status: 'pending', priority: 'high', due_date: '2024-02-15' },
  { id: '2', title: 'Approve Reserve Report', status: 'completed', priority: 'medium', due_date: '2024-02-10' },
];

export default function TaskList() {
  const columns = [
    { title: 'Task', dataIndex: 'title', key: 'title' },
    { title: 'Status', dataIndex: 'status', key: 'status', render: (v: string) => <StatusBadge status={v} /> },
    { title: 'Priority', dataIndex: 'priority', key: 'priority',
      render: (v: string) => <Tag color={v === 'high' ? 'red' : v === 'medium' ? 'orange' : 'blue'}>{v}</Tag> },
    { title: 'Due', dataIndex: 'due_date', key: 'due', render: formatDate },
    { title: 'Actions', key: 'actions', render: () => <Button icon={<CheckOutlined />} size="small">Complete</Button> },
  ];

  return (
    <>
      <PageHeader title="Tasks" subtitle="Workflow tasks and approvals" />
      <Card>
        <Table columns={columns} dataSource={mockTasks} rowKey="id" />
      </Card>
    </>
  );
}
