import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Button, Input, Table, Tag } from 'antd';
import { PlusOutlined, SearchOutlined } from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';
import { useAssumptionSets } from '@/hooks/useAssumptions';
import { formatDate } from '@/utils/formatters';

export default function AssumptionSetList() {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const { data, isLoading } = useAssumptionSets({ search });

  const columns = [
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Version', dataIndex: 'version', key: 'version' },
    { title: 'Status', dataIndex: 'status', key: 'status', render: (v: string) => <StatusBadge status={v} /> },
    { title: 'Line of Business', dataIndex: 'line_of_business', key: 'lob', render: (v: string) => v ? <Tag>{v}</Tag> : '-' },
    { title: 'Effective Date', dataIndex: 'effective_date', key: 'date', render: formatDate },
    { title: 'Created', dataIndex: 'created_at', key: 'created', render: formatDate },
  ];

  return (
    <>
      <PageHeader
        title="Assumption Sets"
        subtitle="Manage actuarial assumptions"
        extra={<Button type="primary" icon={<PlusOutlined />} onClick={() => navigate('/assumptions/new')}>New Set</Button>}
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
          onRow={(r) => ({ onClick: () => navigate(`/assumptions/${r.id}`) })}
        />
      </Card>
    </>
  );
}
