import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Button, Input, Space, Table, Tag } from 'antd';
import { PlusOutlined, SearchOutlined } from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';
import { useClaims } from '@/hooks/useClaims';
import { formatDate, formatCurrency } from '@/utils/formatters';

export default function ClaimList() {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const { data, isLoading } = useClaims({ search });

  const columns = [
    { title: 'Claim #', dataIndex: 'claim_number', key: 'number' },
    { title: 'Type', dataIndex: 'claim_type', key: 'type', render: (v: string) => <Tag>{v}</Tag> },
    { title: 'Status', dataIndex: 'status', key: 'status', render: (v: string) => <StatusBadge status={v} /> },
    { title: 'Claim Date', dataIndex: 'claim_date', key: 'date', render: formatDate },
    { title: 'Amount', dataIndex: 'claimed_amount', key: 'amount', render: formatCurrency, align: 'right' as const },
    { title: 'Anomaly', dataIndex: 'anomaly_score', key: 'anomaly',
      render: (v: number) => v ? <Tag color="red">{(v * 100).toFixed(0)}%</Tag> : '-' },
  ];

  return (
    <>
      <PageHeader
        title="Claims"
        subtitle="Manage insurance claims"
        extra={<Button type="primary" icon={<PlusOutlined />} onClick={() => navigate('/claims/new')}>New Claim</Button>}
      />
      <Card>
        <Space style={{ marginBottom: 16 }}>
          <Input
            placeholder="Search claims..."
            prefix={<SearchOutlined />}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ width: 300 }}
          />
        </Space>
        <Table
          columns={columns}
          dataSource={data?.items || []}
          rowKey="id"
          loading={isLoading}
          onRow={(record) => ({ onClick: () => navigate(`/claims/${record.id}`) })}
          pagination={{ total: data?.total, pageSize: 20 }}
        />
      </Card>
    </>
  );
}
