import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Card, Tag, Space, Dropdown, Progress } from 'antd';
import {
  PlusOutlined,
  MoreOutlined,
  EyeOutlined,
  StopOutlined,
  ReloadOutlined,
} from '@ant-design/icons';
import type { MenuProps } from 'antd';

import PageHeader from '@/components/common/PageHeader';
import DataTable from '@/components/common/DataTable';
import StatusBadge from '@/components/common/StatusBadge';
import { useCalculations, useCancelCalculation } from '@/hooks/useCalculations';
import { useAuthStore } from '@/stores/authStore';
import { formatDate, formatDuration, formatRelativeTime } from '@/utils/formatters';
import { CALCULATION_STATUSES } from '@/utils/constants';
import type { CalculationRun } from '@/types/models';
import type { CalculationListParams } from '@/types/api';

export default function CalculationList() {
  const navigate = useNavigate();
  const { hasPermission } = useAuthStore();
  const [filters, setFilters] = useState<CalculationListParams>({
    page: 1,
    page_size: 20,
  });

  const { data, isLoading, refetch } = useCalculations(filters);
  const cancelMutation = useCancelCalculation();

  const handleCancel = async (id: string) => {
    await cancelMutation.mutateAsync(id);
    refetch();
  };

  const getRowActions = (record: CalculationRun): MenuProps['items'] => {
    const isRunning = record.status === 'running' || record.status === 'queued';
    
    return [
      {
        key: 'view',
        icon: <EyeOutlined />,
        label: 'View Details',
        onClick: () => navigate(`/calculations/${record.id}`),
      },
      {
        key: 'cancel',
        icon: <StopOutlined />,
        label: 'Cancel',
        disabled: !isRunning || !hasPermission('calculation', 'update'),
        danger: true,
        onClick: () => handleCancel(record.id),
      },
    ];
  };

  const columns = [
    {
      key: 'run_name',
      title: 'Run Name',
      dataIndex: 'run_name',
      render: (value: string, record: CalculationRun) => (
        <a onClick={() => navigate(`/calculations/${record.id}`)}>{value}</a>
      ),
    },
    {
      key: 'model_name',
      title: 'Model',
      dataIndex: 'model_name',
      render: (v: string) => v || '-',
    },
    {
      key: 'status',
      title: 'Status',
      dataIndex: 'status',
      render: (status: string) => {
        if (status === 'running') {
          return (
            <Space>
              <StatusBadge status={status} />
              <Progress percent={50} size="small" style={{ width: 60 }} />
            </Space>
          );
        }
        return <StatusBadge status={status} />;
      },
      width: 180,
    },
    {
      key: 'policies_count',
      title: 'Policies',
      dataIndex: 'policies_count',
      render: (v: number) => v?.toLocaleString() || '-',
      width: 100,
      align: 'right' as const,
    },
    {
      key: 'trigger_type',
      title: 'Trigger',
      dataIndex: 'trigger_type',
      render: (v: string) => <Tag>{v}</Tag>,
      width: 100,
    },
    {
      key: 'duration_seconds',
      title: 'Duration',
      dataIndex: 'duration_seconds',
      render: formatDuration,
      width: 100,
    },
    {
      key: 'created_at',
      title: 'Started',
      dataIndex: 'created_at',
      render: formatRelativeTime,
      width: 130,
    },
    {
      key: 'actions',
      title: '',
      width: 50,
      render: (_: unknown, record: CalculationRun) => (
        <Dropdown menu={{ items: getRowActions(record) }} trigger={['click']}>
          <Button type="text" icon={<MoreOutlined />} />
        </Dropdown>
      ),
    },
  ];

  return (
    <>
      <PageHeader
        title="Calculations"
        subtitle="View and manage calculation runs"
        breadcrumbs={[{ title: 'Calculations' }]}
        extra={
          hasPermission('calculation', 'create') && (
            <Button
              type="primary"
              icon={<PlusOutlined />}
              onClick={() => navigate('/calculations/new')}
            >
              New Calculation
            </Button>
          )
        }
      />

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
        />
      </Card>
    </>
  );
}
