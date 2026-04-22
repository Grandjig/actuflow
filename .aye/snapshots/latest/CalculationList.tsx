import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Button, Table, Tag, Input } from 'antd';
import { PlusOutlined, SearchOutlined } from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';
import { useCalculations } from '@/hooks/useCalculations';
import { formatDate, formatDuration } from '@/utils/formatters';

export default function CalculationList() {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const { data, isLoading } = useCalculations({ search });

  const columns = [
    { title: 'Run Name', dataIndex: 'run_name', key: 'name' },
    { title: 'Status', dataIndex: 'status', key: 'status', render: (v: string) => <StatusBadge status={v} /> },
    { title: 'Trigger', dataIndex: 'trigger_type', key: 'trigger', render: (v: string) => <Tag>{v}</Tag> },
    { title: 'Policies', dataIndex: 'policies_count', key: 'policies', render: (v: number) => v?.toLocaleString() || '-' },
    { title: 'Duration', dataIndex: 'duration_seconds', key: 'duration', render: formatDuration },
    { title: 'Started', dataIndex: 'started_at', key: 'started', render: formatDate },
  ];

  return (
    <>
      <PageHeader
        title="Calculations"
        subtitle="Actuarial calculation runs"
        extra={<Button type="primary" icon={<PlusOutlined />} onClick={() => navigate('/calculations/new')}>New Run</Button>}
      />
      <Card>
        <Input
          placeholder="Search..."
          prefix={<SearchOutlined />}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ width: 300, marginBottom: 16 }}
        />
        <Table
          columns={columns}
          dataSource={data?.items || []}
          rowKey="id"
          loading={isLoading}
          onRow={(r) => ({ onClick: () => navigate(`/calculations/${r.id}`) })}
        />
      </Card>
    </>
  );
}
