import { useNavigate } from 'react-router-dom';
import { Card, Table, Tag } from 'antd';
import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';

const mockModels = [
  { id: '1', name: 'Term Life Valuation', model_type: 'valuation', status: 'active', version: '1.0.0' },
  { id: '2', name: 'Whole Life Pricing', model_type: 'pricing', status: 'draft', version: '0.9.0' },
];

export default function ModelList() {
  const navigate = useNavigate();
  const columns = [
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Type', dataIndex: 'model_type', key: 'type', render: (v: string) => <Tag>{v}</Tag> },
    { title: 'Version', dataIndex: 'version', key: 'version' },
    { title: 'Status', dataIndex: 'status', key: 'status', render: (v: string) => <StatusBadge status={v} /> },
  ];

  return (
    <>
      <PageHeader title="Model Definitions" subtitle="Actuarial calculation models" />
      <Card>
        <Table
          columns={columns}
          dataSource={mockModels}
          rowKey="id"
          onRow={(r) => ({ onClick: () => navigate(`/models/${r.id}`) })}
        />
      </Card>
    </>
  );
}
