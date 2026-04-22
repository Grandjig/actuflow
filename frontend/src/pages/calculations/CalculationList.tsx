/**
 * Calculations list page.
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
  Progress,
} from 'antd';
import {
  PlusOutlined,
  SearchOutlined,
  EyeOutlined,
  PlayCircleOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  LoadingOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import { useCalculationRuns } from '@/hooks/useCalculations';
import type { CalculationRun, CalculationStatus } from '@/types/models';
import { formatDateTime } from '@/utils/helpers';

const { Title } = Typography;

const statusConfig: Record<CalculationStatus, { icon: React.ReactNode; color: string }> = {
  queued: { icon: <PlayCircleOutlined />, color: 'default' },
  running: { icon: <LoadingOutlined />, color: 'processing' },
  completed: { icon: <CheckCircleOutlined />, color: 'success' },
  failed: { icon: <CloseCircleOutlined />, color: 'error' },
  cancelled: { icon: <CloseCircleOutlined />, color: 'default' },
};

export default function CalculationList() {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<string | undefined>();
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);

  const { data, isLoading } = useCalculationRuns({
    search: search || undefined,
    status: statusFilter,
    page,
    page_size: pageSize,
  });

  const columns: ColumnsType<CalculationRun> = [
    {
      key: 'run_name',
      title: 'Run Name',
      dataIndex: 'run_name',
      render: (value: string, record: CalculationRun) => (
        <a onClick={() => navigate(`/calculations/${record.id}`)}>{value}</a>
      ),
    },
    {
      key: 'model',
      title: 'Model',
      dataIndex: ['model_definition', 'name'],
      render: (value: string) => value || '-',
    },
    {
      key: 'status',
      title: 'Status',
      dataIndex: 'status',
      render: (status: CalculationStatus) => {
        const config = statusConfig[status];
        return (
          <Tag icon={config.icon} color={config.color}>
            {status.toUpperCase()}
          </Tag>
        );
      },
    },
    {
      key: 'started_at',
      title: 'Started',
      dataIndex: 'started_at',
      render: (value: string) => formatDateTime(value),
    },
    {
      key: 'duration',
      title: 'Duration',
      dataIndex: 'duration_seconds',
      render: (value: number) => (value ? `${value}s` : '-'),
    },
    {
      key: 'policies_count',
      title: 'Policies',
      dataIndex: 'policies_count',
      render: (value: number) => (value ? value.toLocaleString() : '-'),
    },
    {
      key: 'actions',
      title: 'Actions',
      width: 100,
      render: (_: unknown, record: CalculationRun) => (
        <Button
          type="text"
          icon={<EyeOutlined />}
          onClick={() => navigate(`/calculations/${record.id}`)}
        />
      ),
    },
  ];

  return (
    <div>
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
        <Title level={2}>Calculations</Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => navigate('/calculations/new')}
        >
          New Calculation
        </Button>
      </div>

      <Card>
        <Space style={{ marginBottom: 16 }}>
          <Input
            placeholder="Search calculations..."
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
              { value: 'queued', label: 'Queued' },
              { value: 'running', label: 'Running' },
              { value: 'completed', label: 'Completed' },
              { value: 'failed', label: 'Failed' },
              { value: 'cancelled', label: 'Cancelled' },
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
            showTotal: (total) => `Total ${total} calculations`,
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
