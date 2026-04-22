import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Descriptions,
  Tag,
  Button,
  Space,
  Tabs,
  Table,
  Modal,
  message,
  Alert,
} from 'antd';
import {
  EditOutlined,
  DeleteOutlined,
  CheckOutlined,
  CloseOutlined,
  SendOutlined,
  PlusOutlined,
  RobotOutlined,
} from '@ant-design/icons';

import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import ExperienceRecommendations from '@/components/ai/ExperienceRecommendations';
import {
  useAssumptionSet,
  useAssumptionTables,
  useAssumptionRecommendations,
  useDeleteAssumptionSet,
  useSubmitAssumptionSet,
  useApproveAssumptionSet,
} from '@/hooks/useAssumptions';
import { useAuthStore } from '@/stores/authStore';
import { formatDate } from '@/utils/formatters';
import type { AssumptionTable } from '@/types/models';

export default function AssumptionSetDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { hasPermission } = useAuthStore();

  const { data: assumptionSet, isLoading } = useAssumptionSet(id!);
  const { data: tables } = useAssumptionTables(id!);
  const { data: recommendations } = useAssumptionRecommendations(id!);

  const deleteMutation = useDeleteAssumptionSet();
  const submitMutation = useSubmitAssumptionSet();
  const approveMutation = useApproveAssumptionSet();

  const handleDelete = () => {
    Modal.confirm({
      title: 'Delete Assumption Set',
      content: 'Are you sure you want to delete this assumption set?',
      okText: 'Delete',
      okType: 'danger',
      onOk: async () => {
        await deleteMutation.mutateAsync(id!);
        message.success('Assumption set deleted');
        navigate('/assumptions');
      },
    });
  };

  const handleSubmit = async () => {
    await submitMutation.mutateAsync(id!);
    message.success('Submitted for approval');
  };

  const handleApprove = async () => {
    await approveMutation.mutateAsync({ id: id! });
    message.success('Assumption set approved');
  };

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

  const canEdit = assumptionSet.status === 'draft' && hasPermission('assumption', 'update');
  const canSubmit = assumptionSet.status === 'draft';
  const canApprove = assumptionSet.status === 'pending_approval' && hasPermission('assumption', 'approve');
  const canDelete = assumptionSet.status !== 'approved' && hasPermission('assumption', 'delete');

  const tableColumns = [
    {
      title: 'Table Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Type',
      dataIndex: 'table_type',
      key: 'type',
      render: (type: string) => <Tag>{type}</Tag>,
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
    },
    {
      title: 'Updated',
      dataIndex: 'updated_at',
      key: 'updated',
      render: formatDate,
    },
  ];

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
              <Button
                type="primary"
                icon={<CheckOutlined />}
                onClick={handleApprove}
                loading={approveMutation.isPending}
              >
                Approve
              </Button>
            )}
            {canEdit && (
              <Button
                icon={<EditOutlined />}
                onClick={() => navigate(`/assumptions/${id}/edit`)}
              >
                Edit
              </Button>
            )}
            {canDelete && (
              <Button danger icon={<DeleteOutlined />} onClick={handleDelete}>
                Delete
              </Button>
            )}
          </Space>
        }
      />

      {assumptionSet.status === 'rejected' && assumptionSet.rejection_reason && (
        <Alert
          type="error"
          message="Rejected"
          description={assumptionSet.rejection_reason}
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
            {formatDate(assumptionSet.effective_date)}
          </Descriptions.Item>
          <Descriptions.Item label="Description" span={2}>
            {assumptionSet.description || '-'}
          </Descriptions.Item>
          {assumptionSet.approved_by_id && (
            <>
              <Descriptions.Item label="Approved By">
                {assumptionSet.approved_by_id}
              </Descriptions.Item>
              <Descriptions.Item label="Approval Date">
                {formatDate(assumptionSet.approval_date)}
              </Descriptions.Item>
            </>
          )}
          <Descriptions.Item label="Created">
            {formatDate(assumptionSet.created_at)}
          </Descriptions.Item>
          <Descriptions.Item label="Updated">
            {formatDate(assumptionSet.updated_at)}
          </Descriptions.Item>
        </Descriptions>
      </Card>

      <Tabs
        items={[
          {
            key: 'tables',
            label: 'Assumption Tables',
            children: (
              <Card
                extra={
                  canEdit && (
                    <Button icon={<PlusOutlined />} size="small">
                      Add Table
                    </Button>
                  )
                }
              >
                <Table
                  dataSource={tables || []}
                  columns={tableColumns}
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
              <ExperienceRecommendations
                recommendations={recommendations || []}
                onApply={(rec) => message.info(`Applied: ${rec.assumption_type}`)}
              />
            ),
          },
        ]}
      />
    </>
  );
}
