import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Space, Tag, Card, Dropdown } from 'antd';
import {
  PlusOutlined,
  MoreOutlined,
  EyeOutlined,
  EditOutlined,
  CopyOutlined,
  DeleteOutlined,
  CheckOutlined,
} from '@ant-design/icons';
import type { MenuProps } from 'antd';

import PageHeader from '@/components/common/PageHeader';
import DataTable from '@/components/common/DataTable';
import StatusBadge from '@/components/common/StatusBadge';
import { useAssumptionSets, useDeleteAssumptionSet } from '@/hooks/useAssumptions';
import { useAuthStore } from '@/stores/authStore';
import { formatDate } from '@/utils/formatters';
import type { AssumptionSet } from '@/types/models';
import type { AssumptionSetFilters } from '@/types/api';

export default function AssumptionSetList() {
  const navigate = useNavigate();
  const { hasPermission } = useAuthStore();
  const [filters, setFilters] = useState<AssumptionSetFilters>({
    page: 1,
    page_size: 20,
  });

  const { data, isLoading, refetch } = useAssumptionSets(filters);
  const deleteMutation = useDeleteAssumptionSet();

  const getRowActions = (record: AssumptionSet): MenuProps['items'] => [
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
      disabled: record.status === 'approved' || !hasPermission('assumption', 'update'),
      onClick: () => navigate(`/assumptions/${record.id}/edit`),
    },
    {
      key: 'clone',
      icon: <CopyOutlined />,
      label: 'Clone',
      disabled: !hasPermission('assumption', 'create'),
    },
    { type: 'divider' },
    {
      key: 'delete',
      icon: <DeleteOutlined />,
      label: 'Delete',
      danger: true,
      disabled: record.status === 'approved' || !hasPermission('assumption', 'delete'),
      onClick: () => deleteMutation.mutate(record.id),
    },
  ];

  const columns = [
    {
      key: 'name',
      title: 'Name',
      dataIndex: 'name',
      render: (value: string, record: AssumptionSet) => (
        <a onClick={() => navigate(`/assumptions/${record.id}`)}>
          {value}
        </a>
      ),
    },
    {
      key: 'version',
      title: 'Version',
      dataIndex: 'version',
      width: 100,
    },
    {
      key: 'status',
      title: 'Status',
      dataIndex: 'status',
      width: 140,
      render: (status: string) => <StatusBadge status={status} />,
    },
    {
      key: 'effective_date',
      title: 'Effective Date',
      dataIndex: 'effective_date',
      render: formatDate,
      width: 140,
    },
    {
      key: 'tables',
      title: 'Tables',
      dataIndex: 'table_count',
      width: 80,
      render: (count: number) => count || 0,
    },
    {
      key: 'created_at',
      title: 'Created',
      dataIndex: 'created_at',
      render: formatDate,
      width: 140,
    },
    {
      key: 'actions',
      title: '',
      width: 50,
      render: (_: unknown, record: AssumptionSet) => (
        <Dropdown menu={{ items: getRowActions(record) }} trigger={['click']}>
          <Button type="text" icon={<MoreOutlined />} />
        </Dropdown>
      ),
    },
  ];

  return (
    <>
      <PageHeader
        title="Assumption Sets"
        subtitle="Manage actuarial assumptions for calculations"
        breadcrumbs={[{ title: 'Assumptions' }]}
        extra={
          hasPermission('assumption', 'create') && (
            <Button
              type="primary"
              icon={<PlusOutlined />}
              onClick={() => navigate('/assumptions/new')}
            >
              New Assumption Set
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
