/**
 * Assumption set detail page.
 */

import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Descriptions,
  Button,
  Space,
  Tag,
  Tabs,
  Table,
  Spin,
  Typography,
  Divider,
} from 'antd';
import {
  ArrowLeftOutlined,
  EditOutlined,
  CheckOutlined,
  CopyOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import { useQuery } from '@tanstack/react-query';
import { getAssumptionSet } from '@/api/assumptions';
import type { AssumptionTable, AssumptionStatus } from '@/types/models';
import { formatDate } from '@/utils/helpers';

const { Title } = Typography;

const statusColors: Record<AssumptionStatus, string> = {
  draft: 'default',
  pending_approval: 'orange',
  approved: 'green',
  archived: 'gray',
};

export default function AssumptionSetDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: assumptionSet, isLoading } = useQuery({
    queryKey: ['assumptionSet', id],
    queryFn: () => getAssumptionSet(id!),
    enabled: !!id,
  });

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: 100 }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!assumptionSet) {
    return <div>Assumption set not found</div>;
  }

  const tableColumns: ColumnsType<AssumptionTable> = [
    {
      key: 'name',
      title: 'Table Name',
      dataIndex: 'name',
    },
    {
      key: 'table_type',
      title: 'Type',
      dataIndex: 'table_type',
      render: (value: string) => <Tag>{value.toUpperCase()}</Tag>,
    },
    {
      key: 'description',
      title: 'Description',
      dataIndex: 'description',
      render: (value: string) => value || '-',
    },
    {
      key: 'actions',
      title: 'Actions',
      width: 100,
      render: (_: unknown, record: AssumptionTable) => (
        <Button
          type="link"
          onClick={() => navigate(`/assumptions/${id}/tables/${record.id}`)}
        >
          View
        </Button>
      ),
    },
  ];

  const tabItems = [
    {
      key: 'tables',
      label: 'Tables',
      children: (
        <Table
          columns={tableColumns}
          dataSource={assumptionSet.tables || []}
          rowKey="id"
          pagination={false}
        />
      ),
    },
    {
      key: 'history',
      label: 'History',
      children: <div>Version history will go here</div>,
    },
    {
      key: 'recommendations',
      label: 'AI Recommendations',
      children: <div>Experience-based recommendations will go here</div>,
    },
  ];

  return (
    <div>
      <Space style={{ marginBottom: 16 }}>
        <Button
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate('/assumptions')}
        >
          Back
        </Button>
      </Space>

      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div>
            <Title level={3} style={{ marginBottom: 8 }}>
              {assumptionSet.name}
            </Title>
            <Space>
              <Tag color={statusColors[assumptionSet.status]}>
                {assumptionSet.status.replace('_', ' ').toUpperCase()}
              </Tag>
              <span>Version {assumptionSet.version}</span>
              {assumptionSet.line_of_business && (
                <Tag>{assumptionSet.line_of_business}</Tag>
              )}
            </Space>
          </div>
          <Space>
            <Button icon={<CopyOutlined />}>Clone</Button>
            {assumptionSet.status === 'draft' && (
              <Button icon={<CheckOutlined />} type="primary">
                Submit for Approval
              </Button>
            )}
            <Button
              icon={<EditOutlined />}
              disabled={assumptionSet.status !== 'draft'}
            >
              Edit
            </Button>
          </Space>
        </div>

        <Divider />

        <Descriptions column={3}>
          <Descriptions.Item label="Effective Date">
            {formatDate(assumptionSet.effective_date)}
          </Descriptions.Item>
          <Descriptions.Item label="Expiry Date">
            {formatDate(assumptionSet.expiry_date)}
          </Descriptions.Item>
          <Descriptions.Item label="Line of Business">
            {assumptionSet.line_of_business || '-'}
          </Descriptions.Item>
          {assumptionSet.status === 'approved' && (
            <>
              <Descriptions.Item label="Approved By">
                {assumptionSet.approved_by || '-'}
              </Descriptions.Item>
              <Descriptions.Item label="Approval Date">
                {formatDate(assumptionSet.approval_date)}
              </Descriptions.Item>
            </>
          )}
        </Descriptions>

        {assumptionSet.description && (
          <>
            <Divider orientation="left">Description</Divider>
            <p>{assumptionSet.description}</p>
          </>
        )}

        <Divider />

        <Tabs items={tabItems} />
      </Card>
    </div>
  );
}
