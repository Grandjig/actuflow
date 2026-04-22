import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Descriptions,
  Button,
  Space,
  Tag,
  Tabs,
  Table,
  Alert,
  List,
  Typography,
  Popconfirm,
  message,
} from 'antd';
import {
  EditOutlined,
  CheckOutlined,
  CloseOutlined,
  SendOutlined,
  RobotOutlined,
  PlusOutlined,
} from '@ant-design/icons';

import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import {
  useAssumptionSet,
  useAssumptionTables,
  useAssumptionRecommendations,
  useSubmitAssumptionSet,
  useApproveAssumptionSet,
  useRejectAssumptionSet,
} from '@/hooks/useAssumptions';
import { useAuthStore } from '@/stores/authStore';
import { formatDate } from '@/utils/formatters';

const { Text, Paragraph } = Typography;

export default function AssumptionSetDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { hasPermission } = useAuthStore();

  const { data: assumptionSet, isLoading } = useAssumptionSet(id!);
  const { data: tables } = useAssumptionTables(id!);
  const { data: recommendations } = useAssumptionRecommendations(id!);
  
  const submitMutation = useSubmitAssumptionSet();
  const approveMutation = useApproveAssumptionSet();
  const rejectMutation = useRejectAssumptionSet();

  if (isLoading) {
    return <LoadingSpinner fullScreen tip="Loading assumption set..." />;
  }

  if (!assumptionSet) {
    return (
      <Card>
        <div style={{ textAlign: 'center', padding: 48 }}>
          <h3>Assumption set not found</h3>
          <Button onClick={() => navigate('/assumptions')}>Back</Button>
        </div>
      </Card>
    );
  }

  const handleSubmit = async () => {
    try {
      await submitMutation.mutateAsync(id!);
      message.success('Submitted for approval');
    } catch (error: any) {
      message.error(error.message);
    }
  };

  const handleApprove = async () => {
    try {
      await approveMutation.mutateAsync({ id: id! });
      message.success('Assumption set approved');
    } catch (error: any) {
      message.error(error.message);
    }
  };

  const handleReject = async () => {
    try {
      await rejectMutation.mutateAsync({ id: id!, reason: 'Needs revision' });
      message.success('Assumption set rejected');
    } catch (error: any) {
      message.error(error.message);
    }
  };

  const tableColumns = [
    { key: 'name', title: 'Name', dataIndex: 'name' },
    {
      key: 'table_type',
      title: 'Type',
      dataIndex: 'table_type',
      render: (v: string) => <Tag>{v}</Tag>,
    },
    { key: 'description', title: 'Description', dataIndex: 'description' },
    {
      key: 'updated_at',
      title: 'Updated',
      dataIndex: 'updated_at',
      render: formatDate,
    },
    {
      key: 'actions',
      title: '',
      width: 100,
      render: () => (
        <Button type="link" size="small">
          View
        </Button>
      ),
    },
  ];

  const canEdit = assumptionSet.status === 'draft';
  const canSubmit = assumptionSet.status === 'draft' && hasPermission('assumption', 'update');
  const canApprove = assumptionSet.status === 'pending_approval' && hasPermission('assumption', 'approve');

  return (
    <>
      <PageHeader
        title={assumptionSet.name}
        subtitle={`Version ${assumptionSet.version}`}
        backUrl="/assumptions"
        breadcrumbs={[
          { title: 'Assumptions', path: '/assumptions' },
          { title: assumptionSet.name },
        ]}
        tags={[<StatusBadge key="status" status={assumptionSet.status} />]}
        extra={
          <Space>
            {canEdit && (
              <Button
                icon={<EditOutlined />}
                onClick={() => navigate(`/assumptions/${id}/edit`)}
              >
                Edit
              </Button>
            )}
            {canSubmit && (
              <Button
                icon={<SendOutlined />}
                onClick={handleSubmit}
                loading={submitMutation.isPending}
              >
                Submit for Approval
              </Button>
            )}
            {canApprove && (
              <>
                <Popconfirm title="Approve this set?" onConfirm={handleApprove}>
                  <Button
                    type="primary"
                    icon={<CheckOutlined />}
                    loading={approveMutation.isPending}
                  >
                    Approve
                  </Button>
                </Popconfirm>
                <Popconfirm title="Reject this set?" onConfirm={handleReject}>
                  <Button
                    danger
                    icon={<CloseOutlined />}
                    loading={rejectMutation.isPending}
                  >
                    Reject
                  </Button>
                </Popconfirm>
              </>
            )}
          </Space>
        }
      />

      {assumptionSet.rejection_reason && (
        <Alert
          message="Rejection Reason"
          description={assumptionSet.rejection_reason}
          type="error"
          showIcon
          style={{ marginBottom: 24 }}
        />
      )}

      <Card style={{ marginBottom: 24 }}>
        <Descriptions bordered column={2}>
          <Descriptions.Item label="Name">{assumptionSet.name}</Descriptions.Item>
          <Descriptions.Item label="Version">{assumptionSet.version}</Descriptions.Item>
          <Descriptions.Item label="Status">
            <StatusBadge status={assumptionSet.status} />
          </Descriptions.Item>
          <Descriptions.Item label="Effective Date">
            {assumptionSet.effective_date ? formatDate(assumptionSet.effective_date) : '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Line of Business">
            {assumptionSet.line_of_business || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Tables">{tables?.length || 0}</Descriptions.Item>
          <Descriptions.Item label="Description" span={2}>
            {assumptionSet.description || '-'}
          </Descriptions.Item>
          {assumptionSet.approval_notes && (
            <Descriptions.Item label="Approval Notes" span={2}>
              {assumptionSet.approval_notes}
            </Descriptions.Item>
          )}
        </Descriptions>
      </Card>

      <Tabs
        items={[
          {
            key: 'tables',
            label: 'Tables',
            children: (
              <Card
                title="Assumption Tables"
                extra={
                  canEdit && (
                    <Button icon={<PlusOutlined />} type="primary">
                      Add Table
                    </Button>
                  )
                }
              >
                <Table
                  columns={tableColumns}
                  dataSource={tables || []}
                  rowKey="id"
                  pagination={false}
                />
              </Card>
            ),
          },
          {
            key: 'recommendations',
            label: (
              <Space>
                <RobotOutlined />
                AI Recommendations
              </Space>
            ),
            children: (
              <Card>
                {recommendations && recommendations.length > 0 ? (
                  <List
                    dataSource={recommendations}
                    renderItem={(rec: any) => (
                      <List.Item>
                        <List.Item.Meta
                          avatar={<RobotOutlined style={{ fontSize: 24, color: '#722ed1' }} />}
                          title={rec.description}
                          description={
                            <Space direction="vertical">
                              <Text>Confidence: {(rec.confidence * 100).toFixed(0)}%</Text>
                              {rec.suggested_factor && (
                                <Text>Suggested factor: {rec.suggested_factor.toFixed(4)}</Text>
                              )}
                            </Space>
                          }
                        />
                        <Button>Apply</Button>
                      </List.Item>
                    )}
                  />
                ) : (
                  <div style={{ textAlign: 'center', padding: 40, color: '#999' }}>
                    No recommendations available. Run an experience study to generate suggestions.
                  </div>
                )}
              </Card>
            ),
          },
        ]}
      />
    </>
  );
}
