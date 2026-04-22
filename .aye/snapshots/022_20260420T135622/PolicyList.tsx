import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button, Space, Tag, Input, Select, DatePicker, Card, Dropdown, Modal, message } from 'antd';
import {
  PlusOutlined,
  SearchOutlined,
  FilterOutlined,
  DownloadOutlined,
  MoreOutlined,
  EyeOutlined,
  EditOutlined,
  DeleteOutlined,
} from '@ant-design/icons';
import type { MenuProps } from 'antd';
import dayjs from 'dayjs';

import PageHeader from '@/components/common/PageHeader';
import DataTable from '@/components/common/DataTable';
import FilterPanel from '@/components/common/FilterPanel';
import { usePolicies, useDeletePolicy } from '@/hooks/usePolicies';
import { useAuthStore } from '@/stores/authStore';
import { formatCurrency, formatDate } from '@/utils/formatters';
import { STATUS_COLORS, POLICY_STATUSES, PRODUCT_TYPES } from '@/utils/constants';
import type { Policy } from '@/types/models';
import type { PolicyListParams } from '@/types/api';

const { RangePicker } = DatePicker;

export default function PolicyList() {
  const navigate = useNavigate();
  const { hasPermission } = useAuthStore();
  const [filters, setFilters] = useState<PolicyListParams>({
    page: 1,
    page_size: 20,
  });
  const [showFilters, setShowFilters] = useState(false);

  const { data, isLoading } = usePolicies(filters);
  const deleteMutation = useDeletePolicy();

  const handleDelete = (policy: Policy) => {
    Modal.confirm({
      title: 'Delete Policy',
      content: `Are you sure you want to delete policy ${policy.policy_number}?`,
      okText: 'Delete',
      okType: 'danger',
      onOk: async () => {
        await deleteMutation.mutateAsync(policy.id);
        message.success('Policy deleted successfully');
      },
    });
  };

  const getRowActions = (record: Policy): MenuProps['items'] => [
    {
      key: 'view',
      icon: <EyeOutlined />,
      label: 'View Details',
      onClick: () => navigate(`/policies/${record.id}`),
    },
    {
      key: 'edit',
      icon: <EditOutlined />,
      label: 'Edit',
      disabled: !hasPermission('policy', 'update'),
      onClick: () => navigate(`/policies/${record.id}/edit`),
    },
    { type: 'divider' },
    {
      key: 'delete',
      icon: <DeleteOutlined />,
      label: 'Delete',
      danger: true,
      disabled: !hasPermission('policy', 'delete'),
      onClick: () => handleDelete(record),
    },
  ];

  const columns = [
    {
      key: 'policy_number',
      title: 'Policy Number',
      dataIndex: 'policy_number',
      sorter: true,
      render: (value: string, record: Policy) => (
        <Link to={`/policies/${record.id}`} style={{ fontWeight: 500 }}>
          {value}
        </Link>
      ),
    },
    {
      key: 'policyholder',
      title: 'Policyholder',
      dataIndex: ['policyholder', 'full_name'],
      render: (value: string, record: Policy) => (
        <Link to={`/policyholders/${record.policyholder?.id}`}>
          {value || '-'}
        </Link>
      ),
    },
    {
      key: 'product_name',
      title: 'Product',
      dataIndex: 'product_name',
      ellipsis: true,
      render: (value: string, record: Policy) => value || record.product_code,
    },
    {
      key: 'status',
      title: 'Status',
      dataIndex: 'status',
      render: (status: string) => (
        <Tag color={STATUS_COLORS[status] || 'default'}>
          {status.replace('_', ' ').toUpperCase()}
        </Tag>
      ),
    },
    {
      key: 'sum_assured',
      title: 'Sum Assured',
      dataIndex: 'sum_assured',
      align: 'right' as const,
      render: (value: number, record: Policy) =>
        formatCurrency(value, record.currency),
    },
    {
      key: 'premium_amount',
      title: 'Premium',
      dataIndex: 'premium_amount',
      align: 'right' as const,
      render: (value: number, record: Policy) =>
        `${formatCurrency(value, record.currency)} / ${record.premium_frequency}`,
    },
    {
      key: 'issue_date',
      title: 'Issue Date',
      dataIndex: 'issue_date',
      sorter: true,
      render: (date: string) => formatDate(date),
    },
    {
      key: 'actions',
      title: '',
      width: 50,
      render: (_: unknown, record: Policy) => (
        <Dropdown menu={{ items: getRowActions(record) }} trigger={['click']}>
          <Button type="text" icon={<MoreOutlined />} />
        </Dropdown>
      ),
    },
  ];

  const filterConfig = [
    {
      key: 'status',
      label: 'Status',
      type: 'select' as const,
      options: POLICY_STATUSES,
    },
    {
      key: 'product_type',
      label: 'Product Type',
      type: 'select' as const,
      options: PRODUCT_TYPES,
    },
    {
      key: 'issue_date',
      label: 'Issue Date',
      type: 'dateRange' as const,
    },
  ];

  return (
    <>
      <PageHeader
        title="Policies"
        subtitle="Manage insurance policies"
        breadcrumbs={[{ title: 'Policies' }]}
        extra={
          <Space>
            <Button
              icon={<FilterOutlined />}
              onClick={() => setShowFilters(!showFilters)}
            >
              Filters
            </Button>
            <Button icon={<DownloadOutlined />}>Export</Button>
            {hasPermission('policy', 'create') && (
              <Button
                type="primary"
                icon={<PlusOutlined />}
                onClick={() => navigate('/policies/new')}
              >
                New Policy
              </Button>
            )}
          </Space>
        }
      />

      <Card>
        <Space direction="vertical" style={{ width: '100%' }} size="middle">
          {/* Search bar */}
          <Input
            placeholder="Search by policy number, holder name..."
            prefix={<SearchOutlined />}
            style={{ maxWidth: 400 }}
            allowClear
            onChange={(e) =>
              setFilters((f) => ({ ...f, search: e.target.value, page: 1 }))
            }
          />

          {/* Filter panel */}
          {showFilters && (
            <FilterPanel
              config={filterConfig}
              values={filters}
              onChange={(newFilters) =>
                setFilters((f) => ({ ...f, ...newFilters, page: 1 }))
              }
              onReset={() =>
                setFilters({ page: 1, page_size: filters.page_size })
              }
            />
          )}

          {/* Data table */}
          <DataTable
            columns={columns}
            dataSource={data?.items || []}
            loading={isLoading}
            pagination={{
              current: filters.page,
              pageSize: filters.page_size,
              total: data?.total || 0,
              onChange: (page, pageSize) =>
                setFilters((f) => ({ ...f, page, page_size: pageSize })),
            }}
            rowKey="id"
            onRow={(record) => ({
              onClick: () => navigate(`/policies/${record.id}`),
              style: { cursor: 'pointer' },
            })}
          />
        </Space>
      </Card>
    </>
  );
}
