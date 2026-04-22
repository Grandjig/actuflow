/**
 * Claims list page.
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Card,
  Table,
  Button,
  Space,
  Input,
  Select,
  Tag,
  Typography,
  Tooltip,
} from 'antd';
import {
  PlusOutlined,
  SearchOutlined,
  EyeOutlined,
  WarningOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import { useQuery } from '@tanstack/react-query';
import { getClaims } from '@/api/claims';
import type { Claim, ClaimStatus } from '@/types/models';
import { formatCurrency, formatDate } from '@/utils/helpers';

const { Title } = Typography;

const statusColors: Record<ClaimStatus, string> = {
  open: 'blue',
  under_review: 'orange',
  approved: 'green',
  denied: 'red',
  paid: 'purple',
  closed: 'default',
};

export default function ClaimList() {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<string | undefined>();
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);

  const { data, isLoading } = useQuery({
    queryKey: ['claims', { search, status: statusFilter, page, pageSize }],
    queryFn: () => getClaims({ search, status: statusFilter, page, page_size: pageSize }),
  });

  const columns: ColumnsType<Claim> = [
    {
      key: 'claim_number',
      title: 'Claim Number',
      dataIndex: 'claim_number',
      render: (value: string, record: Claim) => (
        <Space>
          <a onClick={() => navigate(`/claims/${record.id}`)}>{value}</a>
          {record.anomaly_score && record.anomaly_score > 0.7 && (
            <Tooltip title={`Anomaly score: ${(record.anomaly_score * 100).toFixed(0)}%`}>
              <WarningOutlined style={{ color: '#faad14' }} />
            </Tooltip>
          )}
        </Space>
      ),
    },
    {
      key: 'policy_number',
      title: 'Policy',
      dataIndex: ['policy', 'policy_number'],
      render: (value: string) => value || '-',
    },
    {
      key: 'claim_type',
      title: 'Type',
      dataIndex: 'claim_type',
    },
    {
      key: 'claim_date',
      title: 'Claim Date',
      dataIndex: 'claim_date',
      render: (value: string) => formatDate(value),
    },
    {
      key: 'claim_amount',
      title: 'Amount',
      dataIndex: 'claim_amount',
      align: 'right',
      render: (value: number) => formatCurrency(value),
    },
    {
      key: 'status',
      title: 'Status',
      dataIndex: 'status',
      render: (status: ClaimStatus) => (
        <Tag color={statusColors[status]}>
          {status.replace('_', ' ').toUpperCase()}
        </Tag>
      ),
    },
    {
      key: 'actions',
      title: 'Actions',
      width: 100,
      render: (_: unknown, record: Claim) => (
        <Button
          type="text"
          icon={<EyeOutlined />}
          onClick={() => navigate(`/claims/${record.id}`)}
        />
      ),
    },
  ];

  return (
    <div>
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
        <Title level={2}>Claims</Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => navigate('/claims/new')}
        >
          New Claim
        </Button>
      </div>

      <Card>
        <Space style={{ marginBottom: 16 }}>
          <Input
            placeholder="Search claims..."
            prefix={<SearchOutlined />}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ width: 250 }}
          />
          <Select
            placeholder="Status"
            allowClear
            value={statusFilter}
            onChange={setStatusFilter}
            style={{ width: 150 }}
            options={[
              { value: 'open', label: 'Open' },
              { value: 'under_review', label: 'Under Review' },
              { value: 'approved', label: 'Approved' },
              { value: 'denied', label: 'Denied' },
              { value: 'paid', label: 'Paid' },
              { value: 'closed', label: 'Closed' },
            ]}
          />
        </Space>

        <Table
          columns={columns}
          dataSource={data?.items || []}
          rowKey="id"
          loading={isLoading}
          pagination={{
            current: page,
            pageSize,
            total: data?.total || 0,
            showSizeChanger: true,
            showTotal: (total) => `Total ${total} claims`,
            onChange: (p, ps) => {
              setPage(p);
              setPageSize(ps);
            },
          }}
        />
      </Card>
    </div>
  );
}
