import { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Dropdown, Space, Tag } from 'antd';
import {
  PlusOutlined,
  MoreOutlined,
  EyeOutlined,
  EditOutlined,
  CopyOutlined,
  CheckOutlined,
  DeleteOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import PageHeader from '@/components/common/PageHeader';
import DataTable from '@/components/common/DataTable';
import FilterPanel from '@/components/common/FilterPanel';
import StatusBadge from '@/components/common/StatusBadge';
import { useAssumptionSets } from '@/hooks/useAssumptions';
import { formatDate } from '@/utils/formatters';
import { ASSUMPTION_STATUSES } from '@/utils/constants';
import type { AssumptionSet } from '@/types/models';
import type { FilterConfig } from '@/types/ui';

export default function AssumptionSetList() {
  const navigate = useNavigate();
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [search, setSearch] = useState('');
  const [filters, setFilters] = useState<Record<string, unknown>>({});

  const queryParams = useMemo(() => ({
    page,
    page_size: pageSize,
    search: search || undefined,
    ...filters,
  }), [page, pageSize, search, filters]);

  const { data, isLoading, refetch } = useAssumptionSets(queryParams);

  const filterConfigs: FilterConfig[] = [
    {
      key: 'status',
      label: 'Status',
      type: 'select',
      options: ASSUMPTION_STATUSES,
    },
  ];

  const columns: ColumnsType<AssumptionSet> = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      render: (value: string, record: AssumptionSet) => (
        <a onClick={() => navigate(`/assumptions/${record.id}`)}>{value}</a>
      ),
    },
    {
      title: 'Version',
      dataIndex: 'version',
      key: 'version',
      render: (value: string) => <Tag>{value}</Tag>,
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (value: string) => <StatusBadge status={value} />,
    },
    {
      title: 'Effective Date',
      dataIndex: 'effective_date',
      key: 'effective_date',
      render: (value: string | undefined) => (value ? formatDate(value) : '-'),
    },
    {
      title: 'Approved By',
      key: 'approved_by',
      render: (_: unknown, record: AssumptionSet) =>
        record.approved_by?.full_name || '-',
    },
    {
      title: 'Approval Date',
      dataIndex: 'approval_date',
      key: 'approval_date',
      render: (value: string | undefined) => (value ? formatDate(value) : '-'),
    },
    {
      title: 'Locked',
      dataIndex: 'locked',
      key: 'locked',
      render: (value: boolean) =>
        value ? <Tag color="red">Locked</Tag> : <Tag color="green">Editable</Tag>,
    },
    {
      title: 'Created',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (value: string) => formatDate(value),
    },
  ];

  const actionMenu = (record: AssumptionSet) => ({
    items: [
      {
        key: 'view',
        icon: <EyeOutlined />,
        label: 'View Details',
        onClick: () => navigate(`/assumptions/${record.id}`),
      },
      {
        key: 'edit',
        icon: <EditOutlined />,
        label: 'Edit',
        disabled: record.locked,
        onClick: () => navigate(`/assumptions/${record.id}/edit`),
      },
      {
        key: 'clone',
        icon: <CopyOutlined />,
        label: 'Clone',
      },
      {
        key: 'submit',
        icon: <CheckOutlined />,
        label: 'Submit for Approval',
        disabled: record.status !== 'draft',
      },
      { type: 'divider' as const },
      {
        key: 'delete',
        icon: <DeleteOutlined />,
        label: 'Delete',
        danger: true,
        disabled: record.locked,
      },
    ],
  });

  return (
    <div>
      <PageHeader
        title="Assumption Sets"
        subtitle={`${data?.total || 0} assumption sets`}
        breadcrumb={[{ title: 'Home', path: '/' }, { title: 'Assumptions' }]}
        extra={
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => navigate('/assumptions/new')}
          >
            New Assumption Set
          </Button>
        }
      />

      <FilterPanel
        filters={filterConfigs}
        values={filters}
        onChange={setFilters}
        onReset={() => setFilters({})}
      />

      <DataTable<AssumptionSet>
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
    </div>
  );
}
