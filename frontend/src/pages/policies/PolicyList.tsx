/**
 * Policies list page.
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
} from 'antd';
import {
  PlusOutlined,
  SearchOutlined,
  EyeOutlined,
  DownloadOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import { useQuery } from '@tanstack/react-query';
import { getPolicies } from '@/api/policies';
import type { Policy, PolicyStatus } from '@/types/models';
import { formatCurrency, formatDate } from '@/utils/helpers';

const { Title } = Typography;

const statusColors: Record<PolicyStatus, string> = {
  active: 'green',
  lapsed: 'red',
  surrendered: 'orange',
  matured: 'blue',
  claimed: 'purple',
  pending: 'gold',
  cancelled: 'default',
};

interface PolicyListParams {
  search?: string;
  status?: string;
  product_type?: string;
  page: number;
  page_size: number;
}

export default function PolicyList() {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<string | undefined>();
  const [productTypeFilter, setProductTypeFilter] = useState<string | undefined>();
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);

  const params: PolicyListParams = {
    search: search || undefined,
    status: statusFilter,
    product_type: productTypeFilter,
    page,
    page_size: pageSize,
  };

  const { data, isLoading } = useQuery({
    queryKey: ['policies', params],
    queryFn: () => getPolicies(params as unknown as Record<string, unknown>),
  });

  const columns: ColumnsType<Policy> = [
    {
      key: 'policy_number',
      title: 'Policy Number',
      dataIndex: 'policy_number',
      render: (value: string, record: Policy) => (
        <a onClick={() => navigate(`/policies/${record.id}`)}>{value}</a>
      ),
    },
    {
      key: 'product_name',
      title: 'Product',
      dataIndex: 'product_name',
      render: (value: string, record: Policy) => value || record.product_code,
    },
    {
      key: 'product_type',
      title: 'Type',
      dataIndex: 'product_type',
    },
    {
      key: 'policyholder',
      title: 'Policyholder',
      dataIndex: ['policyholder', 'full_name'],
      render: (value: string) => value || '-',
    },
    {
      key: 'issue_date',
      title: 'Issue Date',
      dataIndex: 'issue_date',
      render: (value: string) => formatDate(value),
    },
    {
      key: 'sum_assured',
      title: 'Sum Assured',
      dataIndex: 'sum_assured',
      align: 'right' as const,
      width: 150,
      render: (value: number, record: Policy) => formatCurrency(value, record.currency),
    },
    {
      key: 'status',
      title: 'Status',
      dataIndex: 'status',
      render: (status: PolicyStatus) => (
        <Tag color={statusColors[status]}>
          {status.toUpperCase()}
        </Tag>
      ),
    },
    {
      key: 'actions',
      title: 'Actions',
      width: 100,
      render: (_: unknown, record: Policy) => (
        <Button
          type="text"
          icon={<EyeOutlined />}
          onClick={() => navigate(`/policies/${record.id}`)}
        />
      ),
    },
  ];

  return (
    <div>
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
        <Title level={2}>Policies</Title>
        <Space>
          <Button icon={<DownloadOutlined />}>Export</Button>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => navigate('/policies/new')}
          >
            New Policy
          </Button>
        </Space>
      </div>

      <Card>
        <Space style={{ marginBottom: 16 }}>
          <Input
            placeholder="Search policies..."
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
              { value: 'active', label: 'Active' },
              { value: 'lapsed', label: 'Lapsed' },
              { value: 'surrendered', label: 'Surrendered' },
              { value: 'matured', label: 'Matured' },
              { value: 'claimed', label: 'Claimed' },
            ]}
          />
          <Select
            placeholder="Product Type"
            allowClear
            value={productTypeFilter}
            onChange={setProductTypeFilter}
            style={{ width: 150 }}
            options={[
              { value: 'term_life', label: 'Term Life' },
              { value: 'whole_life', label: 'Whole Life' },
              { value: 'endowment', label: 'Endowment' },
              { value: 'annuity', label: 'Annuity' },
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
            showTotal: (total) => `Total ${total} policies`,
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
