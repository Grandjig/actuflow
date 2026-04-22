import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Card, Tag, Space, Dropdown, message, Switch } from 'antd';
import {
  PlusOutlined,
  MoreOutlined,
  EyeOutlined,
  EditOutlined,
  WarningOutlined,
} from '@ant-design/icons';
import type { MenuProps } from 'antd';

import PageHeader from '@/components/common/PageHeader';
import DataTable from '@/components/common/DataTable';
import StatusBadge from '@/components/common/StatusBadge';
import { useClaims, useClaimStats } from '@/hooks/useClaims';
import { useAuthStore } from '@/stores/authStore';
import { formatCurrency, formatDate } from '@/utils/formatters';
import { CLAIM_STATUSES, CLAIM_TYPES } from '@/utils/constants';
import type { Claim } from '@/types/models';
import type { ClaimListParams } from '@/types/api';

export default function ClaimList() {
  const navigate = useNavigate();
  const { hasPermission } = useAuthStore();
  const [filters, setFilters] = useState<ClaimListParams>({
    page: 1,
    page_size: 20,
  });
  const [anomalyOnly, setAnomalyOnly] = useState(false);

  const { data, isLoading, refetch } = useClaims({ ...filters, anomaly_only: anomalyOnly });
  const { data: stats } = useClaimStats();

  const getRowActions = (record: Claim): MenuProps['items'] => [
    {
      key: 'view',
      icon: <EyeOutlined />,
      label: 'View Details',
      onClick: () => navigate(`/claims/${record.id}`),
    },
    {
      key: 'edit',
      icon: <EditOutlined />,
      label: 'Edit',
      disabled: !hasPermission('claim', 'update'),
      onClick: () => navigate(`/claims/${record.id}/edit`),
    },
  ];

  const columns = [
    {
      key: 'claim_number',
      title: 'Claim Number',
      dataIndex: 'claim_number',
      render: (value: string, record: Claim) => (
        <Space>
          <a onClick={() => navigate(`/claims/${record.id}`)}>{value}</a>
          {record.anomaly_score && record.anomaly_score > 0.5 && (
            <WarningOutlined style={{ color: '#ff4d4f' }} />
          )}
        </Space>
      ),
    },
    {
      key: 'claim_type',
      title: 'Type',
      dataIndex: 'claim_type',
      render: (type: string) => <Tag>{type}</Tag>,
      width: 120,
    },
    {
      key: 'status',
      title: 'Status',
      dataIndex: 'status',
      render: (status: string) => <StatusBadge status={status} />,
      width: 120,
    },
    {
      key: 'claimed_amount',
      title: 'Claimed',
      dataIndex: 'claimed_amount',
      render: (v: number) => formatCurrency(v),
      align: 'right' as const,
      width: 130,
    },
    {
      key: 'settlement_amount',
      title: 'Settled',
      dataIndex: 'settlement_amount',
      render: (v: number) => (v ? formatCurrency(v) : '-'),
      align: 'right' as const,
      width: 130,
    },
    {
      key: 'claim_date',
      title: 'Claim Date',
      dataIndex: 'claim_date',
      render: formatDate,
      width: 120,
    },
    {
      key: 'anomaly_score',
      title: 'Risk Score',
      dataIndex: 'anomaly_score',
      width: 100,
      render: (score: number | null) => {
        if (!score) return '-';
        const color = score > 0.7 ? 'red' : score > 0.4 ? 'orange' : 'green';
        return <Tag color={color}>{(score * 100).toFixed(0)}%</Tag>;
      },
    },
    {
      key: 'actions',
      title: '',
      width: 50,
      render: (_: unknown, record: Claim) => (
        <Dropdown menu={{ items: getRowActions(record) }} trigger={['click']}>
          <Button type="text" icon={<MoreOutlined />} />
        </Dropdown>
      ),
    },
  ];

  return (
    <>
      <PageHeader
        title="Claims"
        subtitle={`${stats?.open_claims || 0} open claims`}
        breadcrumbs={[{ title: 'Claims' }]}
        extra={
          <Space>
            <span>Anomalies only:</span>
            <Switch checked={anomalyOnly} onChange={setAnomalyOnly} />
            {hasPermission('claim', 'create') && (
              <Button
                type="primary"
                icon={<PlusOutlined />}
                onClick={() => navigate('/claims/new')}
              >
                New Claim
              </Button>
            )}
          </Space>
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
