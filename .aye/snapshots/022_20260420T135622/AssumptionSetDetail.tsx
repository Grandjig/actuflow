import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Descriptions,
  Tag,
  Button,
  Space,
  Tabs,
  Table,
  Spin,
  message,
} from 'antd';
import {
  EditOutlined,
  CopyOutlined,
  CheckOutlined,
  BulbOutlined,
} from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';
import EmptyState from '@/components/common/EmptyState';
import ExperienceRecommendations from '@/components/ai/ExperienceRecommendations';
import {
  useAssumptionSet,
  useAssumptionTables,
  useAssumptionRecommendations,
  useSubmitAssumptionSet,
} from '@/hooks/useAssumptions';
import { formatDate } from '@/utils/formatters';
import type { AssumptionTable, ExperienceRecommendation } from '@/types/models';

export default function AssumptionSetDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: assumptionSet, isLoading, error } = useAssumptionSet(id!);
  const { data: tables } = useAssumptionTables(id!);
  const { data: recommendations } = useAssumptionRecommendations(id!);
  const submitForApproval = useSubmitAssumptionSet();

  if (isLoading) {
    return (
      <div style={{ padding: 100, textAlign: 'center' }}>
        <Spin size="large" />
      </div>
    );
  }

  if (error || !assumptionSet) {
    return (
      <EmptyState
        title="Assumption Set Not Found"
        description="The assumption set you're looking for doesn't exist."
        action={{ label: 'Back to Assumptions', onClick: () => navigate('/assumptions') }}
      />
    );
  }

  const tableColumns = [
    {
      title: 'Table Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Type',
      dataIndex: 'table_type',
      key: 'table_type',
      render: (value: string) => <Tag color="blue">{value}</Tag>,
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
    },
    {
      title: 'Created',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (value: string) => formatDate(value),
    },
    {
      title: 'Action',
      key: 'action',
      render: (_: unknown, record: AssumptionTable) => (
        <Button
          type="link"
          size="small"
          onClick={() => navigate(`/assumptions/${id}/tables/${record.id}`)}
        >
          View
        </Button>
      ),
    },
  ];

  const handleApplyRecommendation = (rec: ExperienceRecommendation) => {
    message.info(`Would apply recommendation: ${rec.assumption_type}`);
  };

  const tabItems = [
    {
      key: 'tables',
      label: 'Assumption Tables',
      children: (
        <Table<AssumptionTable>
          columns={tableColumns}
          dataSource={tables || []}
          rowKey="id"
          pagination={false}
        />
      ),
    },
    {
      key: 'recommendations',
      label: (
        <span>
          <BulbOutlined /> AI Recommendations
          {recommendations && recommendations.length > 0 && (
            <Tag color="purple" style={{ marginLeft: 8 }}>
              {recommendations.length}
            </Tag>
          )}
        </span>
      ),
      children: (
        <ExperienceRecommendations
          recommendations={recommendations || []}
          onApply={assumptionSet.locked ? undefined : handleApplyRecommendation}
        />
      ),
    },
    {
      key: 'history',
      label: 'History',
      children: (
        <EmptyState
          title="No History"
          description="Version history would be displayed here."
        />
      ),
    },
  ];

  return (
    <div>
      <PageHeader
        title={assumptionSet.name}
        subtitle={`Version ${assumptionSet.version}`}
        backUrl="/assumptions"
        breadcrumb={[
          { title: 'Home', path: '/' },
          { title: 'Assumptions', path: '/assumptions' },
          { title: assumptionSet.name },
        ]}
        extra={
          <Space>
            {assumptionSet.status === 'draft' && (
              <Button
                icon={<CheckOutlined />}
                onClick={() => submitForApproval.mutate(assumptionSet.id)}
                loading={submitForApproval.isPending}
              >
                Submit for Approval
              </Button>
            )}
            <Button icon={<CopyOutlined />}>Clone</Button>
            <Button
              icon={<EditOutlined />}
              disabled={assumptionSet.locked}
            >
              Edit
            </Button>
          </Space>
        }
      />

      <Card style={{ marginBottom: 24 }}>
        <Descriptions>
          <Descriptions.Item label="Status">
            <StatusBadge status={assumptionSet.status} />
          </Descriptions.Item>
          <Descriptions.Item label="Effective Date">
            {assumptionSet.effective_date ? formatDate(assumptionSet.effective_date) : '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Locked">
            {assumptionSet.locked ? (
              <Tag color="red">Locked</Tag>
            ) : (
              <Tag color="green">Editable</Tag>
            )}
          </Descriptions.Item>
          <Descriptions.Item label="Approved By">
            {assumptionSet.approved_by?.full_name || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Approval Date">
            {assumptionSet.approval_date ? formatDate(assumptionSet.approval_date) : '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Tables">
            {tables?.length || 0}
          </Descriptions.Item>
        </Descriptions>
        {assumptionSet.description && (
          <div style={{ marginTop: 16 }}>
            <strong>Description:</strong> {assumptionSet.description}
          </div>
        )}
      </Card>

      <Tabs items={tabItems} />
    </div>
  );
}
