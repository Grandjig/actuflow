import { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Dropdown, Space, Tag } from 'antd';
import {
  PlusOutlined,
  MoreOutlined,
  EyeOutlined,
  EditOutlined,
  DeleteOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import PageHeader from '@/components/common/PageHeader';
import DataTable from '@/components/common/DataTable';
import FilterPanel from '@/components/common/FilterPanel';
import StatusBadge from '@/components/common/StatusBadge';
import ConfirmModal from '@/components/common/ConfirmModal';
import { usePolicies, useDeletePolicy } from '@/hooks/usePolicies';
import { formatCurrency, formatDate } from '@/utils/formatters';
import { POLICY_STATUSES, PRODUCT_TYPES } from '@/utils/constants';
import type { Policy } from '@/types/models';
import type { FilterConfig } from '@/types/ui';

export default function PolicyList() {
  const navigate = useNavigate();
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [search, setSearch] = useState('');
  const [filters, setFilters] = useState<Record<string, unknown>>({});
  const [deleteId, setDeleteId] = useState<string | null>(null);

  const queryParams = useMemo(() => ({
    page,
    page_size: pageSize,
    search: search || undefined,
    ...filters,
  }), [page, pageSize, search, filters]);

  const { data, isLoading, refetch } = usePolicies(queryParams);
  const deletePolicy = useDeletePolicy();

  const filterConfigs: FilterConfig[] = [
    {
      key: 'status',
      label: 'Status',
      type: 'select',
      options: POLICY_STATUSES,
    },
    {
      key: 'product_type',
      label: 'Product Type',
      type: 'select',
      options: PRODUCT_TYPES,
    },
  ];

  const columns: ColumnsType<Policy> = [
    {
      title: 'Policy Number',
      dataIndex: 'policy_number',
      key: 'policy_number',
      sorter: true,
      render: (value: string, record: Policy) => (
        <a onClick={() => navigate(`/policies/${record.id}`)}>{value}</a>
      ),
    },
    {
      title: 'Product',
      dataIndex: 'product_name',
      key: 'product_name',
      ellipsis: true,
    },
    {
      title: 'Product Type',
      dataIndex: 'product_type',
      key: 'product_type',
      render: (value: string) => <Tag>{value}</Tag>,
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (value: string) => <StatusBadge status={value} />,
    },
    {
      title: 'Policyholder',
      key: 'policyholder',
      render: (_: unknown, record: Policy) =>
        record.policyholder
          ? `${record.policyholder.first_name} ${record.policyholder.last_name}`
          : '-',
    },
    {
      title: 'Issue Date',
      dataIndex: 'issue_date',
      key: 'issue_date',
      sorter: true,
      render: (value: string) => formatDate(value),
    },
    {
      title: 'Sum Assured',
      dataIndex: 'sum_assured',
      key: 'sum_assured',
      align: 'right',
      sorter: true,
      render: (value: number, record: Policy) =>
        formatCurrency(value, record.currency),
    },
    {
      title: 'Premium',
      dataIndex: 'premium_amount',
      key: 'premium_amount',
      align: 'right',
      render: (value: number, record: Policy) =>
        formatCurrency(value, record.currency),
    },
  ];

  const handleDelete = () => {
    if (deleteId) {
      deletePolicy.mutate(deleteId, {
        onSuccess: () => setDeleteId(null),
      });
    }
  };

  const actionMenu = (record: Policy) => ({
    items: [
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
        onClick: () => navigate(`/policies/${record.id}/edit`),
      },
      { type: 'divider' as const },
      {
        key: 'delete',
        icon: <DeleteOutlined />,
        label: 'Delete',
        danger: true,
        onClick: () => setDeleteId(record.id),
      },
    ],
  });

  return (
    <div>
      <PageHeader
        title="Policies"
        subtitle={`${data?.total || 0} policies`}
        breadcrumb={[{ title: 'Home', path: '/' }, { title: 'Policies' }]}
        extra={
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => navigate('/policies/new')}
          >
            New Policy
          </Button>
        }
      />

      <FilterPanel
        filters={filterConfigs}
        values={filters}
        onChange={setFilters}
        onReset={() => setFilters({})}
      />

      <DataTable<Policy>
        columns={columns}
        data={data?.items || []}
        loading={isLoading}
        total={data?.total}
        page={page}
        pageSize={pageSize}
        onPaginationChange={(p, ps) => {
          setPage(p);
          setPageSize(ps);
        }}
        onSearch={setSearch}
        onRefresh={refetch}
        actions={(record) => (
          <Dropdown menu={actionMenu(record)} trigger={['click']}>
            <Button icon={<MoreOutlined />} type="text" />
          </Dropdown>
        )}
      />

      <ConfirmModal
        open={!!deleteId}
        title="Delete Policy"
        content="Are you sure you want to delete this policy? This action cannot be undone."
        onConfirm={handleDelete}
        onCancel={() => setDeleteId(null)}
        danger
        loading={deletePolicy.isPending}
      />
    </div>
  );
}
