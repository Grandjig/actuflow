/**
 * Assumption sets list page.
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
} from 'antd';
import {
  PlusOutlined,
  SearchOutlined,
  EyeOutlined,
  CopyOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import { useAssumptionSets } from '@/hooks/useAssumptions';
import type { AssumptionSet, AssumptionStatus } from '@/types/models';
import { formatDate } from '@/utils/helpers';

const { Title } = Typography;

const statusColors: Record<AssumptionStatus, string> = {
  draft: 'default',
  pending_approval: 'orange',
  approved: 'green',
  archived: 'gray',
};

export default function AssumptionSetList() {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<string | undefined>();
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);

  const { data, isLoading } = useAssumptionSets({
    search,
    status: statusFilter,
    page,
    page_size: pageSize,
  });

  const columns: ColumnsType<AssumptionSet> = [
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
    },
    {
      key: 'status',
      title: 'Status',
      dataIndex: 'status',
      render: (status: AssumptionStatus) => (
        <Tag color={statusColors[status]}>
          {status.replace('_', ' ').toUpperCase()}
        </Tag>
      ),
    },
    {
      key: 'effective_date',
      title: 'Effective Date',
      dataIndex: 'effective_date',
      render: (value: string) => formatDate(value),
    },
    {
      key: 'created_at',
      title: 'Created',
      dataIndex: 'created_at',
      render: (value: string) => formatDate(value),
    },
    {
      key: 'actions',
      title: 'Actions',
      width: 120,
      render: (_: unknown, record: AssumptionSet) => (
        <Space>
          <Button
            type="text"
            icon={<EyeOutlined />}
            onClick={() => navigate(`/assumptions/${record.id}`)}
          />
          <Button
            type="text"
            icon={<CopyOutlined />}
            onClick={() => {
              // Clone functionality
            }}
          />
        </Space>
      ),
    },
  ];

  return (
    <div>
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
        <Title level={2}>Assumption Sets</Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => navigate('/assumptions/new')}
        >
          New Assumption Set
        </Button>
      </div>

      <Card>
        <Space style={{ marginBottom: 16 }}>
          <Input
            placeholder="Search assumption sets..."
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
            style={{ width: 180 }}
            options={[
              { value: 'draft', label: 'Draft' },
              { value: 'pending_approval', label: 'Pending Approval' },
              { value: 'approved', label: 'Approved' },
              { value: 'archived', label: 'Archived' },
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
            showTotal: (total) => `Total ${total} assumption sets`,
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
