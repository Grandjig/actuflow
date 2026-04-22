import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Space, Tag, Card, Progress } from 'antd';
import { PlusOutlined, PlayCircleOutlined } from '@ant-design/icons';

import PageHeader from '@/components/common/PageHeader';
import DataTable from '@/components/common/DataTable';
import StatusBadge from '@/components/common/StatusBadge';
import { useCalculations } from '@/hooks/useCalculations';
import { useAuthStore } from '@/stores/authStore';
import { formatDate, formatDuration } from '@/utils/formatters';
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

  const columns = [
    {
      key: 'run_name',
      title: 'Run Name',
      dataIndex: 'run_name',
      render: (value: string, record: CalculationRun) => (
        <a onClick={() => navigate(`/calculations/${record.id}`)}>
          {value}
        </a>
      ),
    },
    {
      key: 'model_name',
      title: 'Model',
      dataIndex: 'model_name',
      width: 180,
    },
    {
      key: 'status',
      title: 'Status',
      dataIndex: 'status',
      width: 120,
      render: (status: string) => <StatusBadge status={status} />,
    },
    {
      key: 'progress',
      title: 'Progress',
      width: 150,
      render: (_: unknown, record: CalculationRun) => {
        if (record.status === 'running') {
          return <Progress percent={50} size="small" />;
        }
        if (record.status === 'completed') {
          return <Progress percent={100} size="small" status="success" />;
        }
        if (record.status === 'failed') {
          return <Progress percent={100} size="small" status="exception" />;
        }
        return '-';
      },
    },
    {
      key: 'policies_count',
      title: 'Policies',
      dataIndex: 'policies_count',
      width: 100,
      render: (count: number) => count?.toLocaleString() || '-',
    },
    {
      key: 'duration',
      title: 'Duration',
      dataIndex: 'duration_seconds',
      width: 100,
      render: formatDuration,
    },
    {
      key: 'trigger_type',
      title: 'Trigger',
      dataIndex: 'trigger_type',
      width: 100,
      render: (type: string) => (
        <Tag color={type === 'manual' ? 'blue' : type === 'scheduled' ? 'green' : 'purple'}>
          {type}
        </Tag>
      ),
    },
    {
      key: 'started_at',
      title: 'Started',
      dataIndex: 'started_at',
      width: 150,
      render: formatDate,
    },
  ];

  return (
    <>
      <PageHeader
        title="Calculations"
        subtitle="Run and monitor actuarial calculations"
        breadcrumbs={[{ title: 'Calculations' }]}
        extra={
          hasPermission('calculation', 'create') && (
            <Button
              type="primary"
              icon={<PlayCircleOutlined />}
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
          onSearch={(value) =>
            setFilters((f) => ({ ...f, search: value, page: 1 }))
          }
          onRefresh={refetch}
        />
      </Card>
    </>
  );
}
