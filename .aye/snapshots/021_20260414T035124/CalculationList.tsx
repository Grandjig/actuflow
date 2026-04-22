import { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Dropdown, Space, Tag, Progress } from 'antd';
import {
  PlusOutlined,
  MoreOutlined,
  EyeOutlined,
  StopOutlined,
  ReloadOutlined,
  DownloadOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import PageHeader from '@/components/common/PageHeader';
import DataTable from '@/components/common/DataTable';
import FilterPanel from '@/components/common/FilterPanel';
import StatusBadge from '@/components/common/StatusBadge';
import { useCalculations, useCancelCalculation } from '@/hooks/useCalculations';
import { formatDate, formatDuration, formatNumber } from '@/utils/formatters';
import { CALCULATION_STATUSES } from '@/utils/constants';
import type { CalculationRun } from '@/types/models';
import type { FilterConfig } from '@/types/ui';

export default function CalculationList() {
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

  const { data, isLoading, refetch } = useCalculations(queryParams);
  const cancelCalculation = useCancelCalculation();

  const filterConfigs: FilterConfig[] = [
    {
      key: 'status',
      label: 'Status',
      type: 'select',
      options: CALCULATION_STATUSES,
    },
    {
      key: 'trigger_type',
      label: 'Trigger',
      type: 'select',
      options: [
        { label: 'Manual', value: 'manual' },
        { label: 'Scheduled', value: 'scheduled' },
        { label: 'Automated', value: 'automated' },
      ],
    },
  ];

  const columns: ColumnsType<CalculationRun> = [
    {
      title: 'Run Name',
      dataIndex: 'run_name',
      key: 'run_name',
      render: (value: string, record: CalculationRun) => (
        <a onClick={() => navigate(`/calculations/${record.id}`)}>{value}</a>
      ),
    },
    {
      title: 'Model',
      key: 'model',
      render: (_: unknown, record: CalculationRun) =>
        record.model_definition?.name || '-',
    },
    {
      title: 'Assumption Set',
      key: 'assumption_set',
      render: (_: unknown, record: CalculationRun) =>
        record.assumption_set?.name || '-',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string, record: CalculationRun) => (
        <Space>
          <StatusBadge status={status} />
          {status === 'running' && record.progress_percent !== undefined && (
            <Progress
              percent={record.progress_percent}
              size="small"
              style={{ width: 60 }}
            />
          )}
        </Space>
      ),
    },
    {
      title: 'Trigger',
      dataIndex: 'trigger_type',
      key: 'trigger_type',
      render: (value: string) => <Tag>{value}</Tag>,
    },
    {
      title: 'Policies',
      dataIndex: 'policy_count',
      key: 'policy_count',
      render: (value: number | undefined) => (value ? formatNumber(value) : '-'),
    },
    {
      title: 'Started',
      dataIndex: 'started_at',
      key: 'started_at',
      render: (value: string | undefined) => (value ? formatDate(value, 'MMM D, HH:mm') : '-'),
    },
    {
      title: 'Duration',
      dataIndex: 'duration_seconds',
      key: 'duration_seconds',
      render: (value: number | undefined) => (value ? formatDuration(value) : '-'),
    },
  ];

  const actionMenu = (record: CalculationRun) => ({
    items: [
      {
        key: 'view',
        icon: <EyeOutlined />,
        label: 'View Details',
        onClick: () => navigate(`/calculations/${record.id}`),
      },
      {
        key: 'download',
        icon: <DownloadOutlined />,
        label: 'Export Results',
        disabled: record.status !== 'completed',
      },
      {
        key: 'rerun',
        icon: <ReloadOutlined />,
        label: 'Rerun',
        disabled: record.status === 'running',
      },
      { type: 'divider' as const },
      {
        key: 'cancel',
        icon: <StopOutlined />,
        label: 'Cancel',
        danger: true,
        disabled: record.status !== 'running' && record.status !== 'queued',
        onClick: () => cancelCalculation.mutate(record.id),
      },
    ],
  });

  return (
    <div>
      <PageHeader
        title="Calculation Runs"
        subtitle={`${data?.total || 0} runs`}
        breadcrumb={[{ title: 'Home', path: '/' }, { title: 'Calculations' }]}
        extra={
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => navigate('/calculations/new')}
          >
            New Calculation
          </Button>
        }
      />

      <FilterPanel
        filters={filterConfigs}
        values={filters}
        onChange={setFilters}
        onReset={() => setFilters({})}
      />

      <DataTable<CalculationRun>
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
