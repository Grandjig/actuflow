import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Card, Tag, Space, Dropdown, message } from 'antd';
import {
  PlusOutlined,
  MoreOutlined,
  EyeOutlined,
  EditOutlined,
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

  const handleDelete = async (set: AssumptionSet) => {
    try {
      await deleteMutation.mutateAsync(set.id);
      message.success('Assumption set deleted');
    } catch (error: any) {
      message.error(error.message || 'Failed to delete');
    }
  };

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
      disabled: record.status !== 'draft' || !hasPermission('assumption', 'update'),
      onClick: () => navigate(`/assumptions/${record.id}/edit`),
    },
    { type: 'divider' },
    {
      key: 'delete',
      icon: <DeleteOutlined />,
      label: 'Delete',
      danger: true,
      disabled: record.status === 'approved' || !hasPermission('assumption', 'delete'),
      onClick: () => handleDelete(record),
    },
  ];

  const columns = [
    {
      key: 'name',
      title: 'Name',
      dataIndex: 'name',
      render: (value: string, record: AssumptionSet) => (
        <a onClick={() => navigate(`/assumptions/${record.id}`)}>{value}</a>
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
      render: (status: string) => <StatusBadge status={status} />,
      width: 140,
    },
    {
      key: 'effective_date',
      title: 'Effective Date',
      dataIndex: 'effective_date',
      render: formatDate,
      width: 130,
    },
    {
      key: 'table_count',
      title: 'Tables',
      dataIndex: 'table_count',
      width: 80,
      render: (v: number) => v || 0,
    },
    {
      key: 'updated_at',
      title: 'Updated',
      dataIndex: 'updated_at',
      render: formatDate,
      width: 130,
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
        subtitle="Manage actuarial assumptions"
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
          onSearch={(value) => setFilters((f) => ({ ...f, search: value, page: 1 }))}
          onRefresh={refetch}
        />
      </Card>
    </>
  );
}
