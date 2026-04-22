/**
 * Generated reports list page.
 */

import { useState } from 'react';
import {
  Card,
  Table,
  Button,
  Space,
  Input,
  Tag,
  Typography,
  Tooltip,
} from 'antd';
import {
  SearchOutlined,
  DownloadOutlined,
  EyeOutlined,
  SyncOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import { useQuery } from '@tanstack/react-query';
import { getGeneratedReports } from '@/api/reports';
import type { GeneratedReport } from '@/types/models';
import { formatDate, formatDateTime } from '@/utils/helpers';

const { Title } = Typography;

const statusIcons: Record<string, React.ReactNode> = {
  generating: <SyncOutlined spin style={{ color: '#1890ff' }} />,
  completed: <CheckCircleOutlined style={{ color: '#52c41a' }} />,
  failed: <CloseCircleOutlined style={{ color: '#ff4d4f' }} />,
};

export default function GeneratedReportList() {
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);

  const { data, isLoading } = useQuery({
    queryKey: ['generatedReports', { search, page, pageSize }],
    queryFn: () => getGeneratedReports({ search, page, page_size: pageSize }),
  });

  const columns: ColumnsType<GeneratedReport> = [
    {
      key: 'name',
      title: 'Report Name',
      dataIndex: 'name',
    },
    {
      key: 'template',
      title: 'Template',
      dataIndex: ['report_template', 'name'],
      render: (value: string) => value || '-',
    },
    {
      key: 'period',
      title: 'Period',
      render: (_: unknown, record: GeneratedReport) => (
        <span>
          {formatDate(record.reporting_period_start)} - {formatDate(record.reporting_period_end)}
        </span>
      ),
    },
    {
      key: 'status',
      title: 'Status',
      dataIndex: 'status',
      render: (status: string) => (
        <Space>
          {statusIcons[status]}
          <span>{status.toUpperCase()}</span>
        </Space>
      ),
    },
    {
      key: 'generated_at',
      title: 'Generated',
      dataIndex: 'generated_at',
      render: (value: string) => formatDateTime(value),
    },
    {
      key: 'actions',
      title: 'Actions',
      width: 120,
      render: (_: unknown, record: GeneratedReport) => (
        <Space>
          <Tooltip title="View">
            <Button
              type="text"
              icon={<EyeOutlined />}
              disabled={record.status !== 'completed'}
            />
          </Tooltip>
          <Tooltip title="Download">
            <Button
              type="text"
              icon={<DownloadOutlined />}
              disabled={record.status !== 'completed'}
            />
          </Tooltip>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
        <Title level={2}>Generated Reports</Title>
      </div>

      <Card>
        <Space style={{ marginBottom: 16 }}>
          <Input
            placeholder="Search reports..."
            prefix={<SearchOutlined />}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ width: 250 }}
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
            showTotal: (total) => `Total ${total} reports`,
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
