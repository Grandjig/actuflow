import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Card, Tag, Space, Dropdown, message } from 'antd';
import {
  PlusOutlined,
  MoreOutlined,
  EyeOutlined,
  EditOutlined,
  DeleteOutlined,
  ExportOutlined,
} from '@ant-design/icons';
import type { MenuProps } from 'antd';

import PageHeader from '@/components/common/PageHeader';
import DataTable from '@/components/common/DataTable';
import StatusBadge from '@/components/common/StatusBadge';
import FilterPanel from '@/components/common/FilterPanel';
import { usePolicies, useDeletePolicy, usePolicyStats } from '@/hooks/usePolicies';
import { useAuthStore } from '@/stores/authStore';
import { formatCurrency, formatDate } from '@/utils/formatters';
import { POLICY_STATUSES, PRODUCT_TYPES } from '@/utils/constants';
import type { Policy } from '@/types/models';
import type { PolicyListParams } from '@/types/api';

export default function PolicyList() {
  const navigate = useNavigate();
  const { hasPermission } = useAuthStore();
  const [filters, setFilters] = useState<PolicyListParams>({
    page: 1,
    page_size: 20,
  });
  const [showFilters, setShowFilters] = useState(false);

  const { data, isLoading, refetch } = usePolicies(filters);
  const { data: stats } = usePolicyStats();
  const deleteMutation = useDeletePolicy();

  const handleDelete = async (policy: Policy) => {
    try {
      await deleteMutation.mutateAsync(policy.id);
      message.success('Policy deleted');
    } catch (error: any) {
      message.error(error.message || 'Failed to delete policy');
    }
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
      render: (value: string, record: Policy) => (
        <a onClick={() => navigate(`/policies/${record.id}`)}>{value}</a>
      ),
    },
    {
      key: 'product_type',
      title: 'Product',
      dataIndex: 'product_type',
      render: (type: string, record: Policy) => (
        <div>
          <div>{record.product_name || type}</div>
          <small style={{ color: '#999' }}>{record.product_code}</small>
        </div>
      ),
    },
    {
      key: 'policyholder',
      title: 'Policyholder',
      dataIndex: 'policyholder',
      render: (ph: any) => ph?.full_name || '-',
    },
    {
      key: 'status',
      title: 'Status',
      dataIndex: 'status',
      render: (status: string) => <StatusBadge status={status} />,
      width: 120,
    },
    {
      key: 'sum_assured',
      title: 'Sum Assured',
      dataIndex: 'sum_assured',
      render: formatCurrency,
      align: 'right' as const,
      width: 140,
    },
    {
      key: 'premium_amount',
      title: 'Premium',
      dataIndex: 'premium_amount',
      render: (v: number, r: Policy) => `${formatCurrency(v)}/${r.premium_frequency?.charAt(0)}`,
      align: 'right' as const,
      width: 130,
    },
    {
      key: 'issue_date',
      title: 'Issue Date',
      dataIndex: 'issue_date',
      render: formatDate,
      width: 120,
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
        subtitle={`${stats?.active_policies || 0} active policies`}
        breadcrumbs={[{ title: 'Policies' }]}
        extra={
          <Space>
            <Button icon={<ExportOutlined />}>Export</Button>
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

      {showFilters && (
        <FilterPanel
          config={filterConfig}
          values={filters}
          onChange={(values) => setFilters({ ...filters, ...values, page: 1 })}
          onReset={() => setFilters({ page: 1, page_size: 20 })}
        />
      )}

      <Card>
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
          onSearch={(value) => setFilters((f) => ({ ...f, search: value, page: 1 }))}
          onRefresh={refetch}
          toolbarExtra={
            <Button onClick={() => setShowFilters(!showFilters)}>
              {showFilters ? 'Hide Filters' : 'Show Filters'}
            </Button>
          }
        />
      </Card>
    </>
  );
}
