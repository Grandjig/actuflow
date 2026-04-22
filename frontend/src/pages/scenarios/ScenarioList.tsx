import { useNavigate } from 'react-router-dom';
import { Card, Button, Table, Tag } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';

const mockScenarios = [
  { id: '1', name: 'Interest Rate +200bps', scenario_type: 'deterministic', status: 'active' },
  { id: '2', name: 'Mass Lapse', scenario_type: 'stress', status: 'draft' },
];

export default function ScenarioList() {
  const navigate = useNavigate();
  const columns = [
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Type', dataIndex: 'scenario_type', key: 'type', render: (v: string) => <Tag>{v}</Tag> },
    { title: 'Status', dataIndex: 'status', key: 'status', render: (v: string) => <StatusBadge status={v} /> },
  ];

  return (
    <>
      <PageHeader
        title="Scenarios"
        subtitle="Stress testing and what-if analysis"
        extra={<Button type="primary" icon={<PlusOutlined />}>New Scenario</Button>}
      />
      <Card>
        <Table columns={columns} dataSource={mockScenarios} rowKey="id"
          onRow={(r) => ({ onClick: () => navigate(`/scenarios/${r.id}`) })} />
      </Card>
    </>
  );
}
