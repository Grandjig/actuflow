import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Descriptions,
  Tag,
  Button,
  Space,
  Tabs,
  Timeline,
  Table,
  Statistic,
  Row,
  Col,
  Modal,
  message,
  Spin,
} from 'antd';
import {
  EditOutlined,
  DeleteOutlined,
  FileTextOutlined,
  HistoryOutlined,
  DollarOutlined,
  UserOutlined,
  CalendarOutlined,
} from '@ant-design/icons';

import PageHeader from '@/components/common/PageHeader';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import { usePolicy, useDeletePolicy, usePolicyHistory } from '@/hooks/usePolicies';
import { useAuthStore } from '@/stores/authStore';
import { formatCurrency, formatDate, formatStatus } from '@/utils/formatters';
import { STATUS_COLORS } from '@/utils/constants';
import type { Coverage, Claim } from '@/types/models';

export default function PolicyDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { hasPermission } = useAuthStore();

  const { data: policy, isLoading, error } = usePolicy(id!);
  const { data: historyData } = usePolicyHistory(id!);
  const deleteMutation = useDeletePolicy();

  const handleDelete = () => {
    Modal.confirm({
      title: 'Delete Policy',
      content: `Are you sure you want to delete policy ${policy?.policy_number}? This action cannot be undone.`,
      okText: 'Delete',
      okType: 'danger',
      onOk: async () => {
        await deleteMutation.mutateAsync(id!);
        message.success('Policy deleted successfully');
        navigate('/policies');
      },
    });
  };

  if (isLoading) {
    return <LoadingSpinner fullScreen tip="Loading policy..." />;
  }

  if (error || !policy) {
    return (
      <Card>
        <div style={{ textAlign: 'center', padding: 48 }}>
          <h3>Policy not found</h3>
          <Button onClick={() => navigate('/policies')}>Back to Policies</Button>
        </div>
      </Card>
    );
  }

  const coverageColumns = [
    { title: 'Coverage', dataIndex: 'coverage_name', key: 'name' },
    { title: 'Type', dataIndex: 'coverage_type', key: 'type' },
    {
      title: 'Benefit',
      dataIndex: 'benefit_amount',
      key: 'benefit',
      render: (v: number) => formatCurrency(v, policy.currency),
    },
    {
      title: 'Premium',
      dataIndex: 'premium_amount',
      key: 'premium',
      render: (v: number) => formatCurrency(v, policy.currency),
    },
    {
      title: 'Rider',
      dataIndex: 'is_rider',
      key: 'rider',
      render: (v: boolean) => (v ? <Tag>Rider</Tag> : '-'),
    },
  ];

  const claimColumns = [
    {
      title: 'Claim #',
      dataIndex: 'claim_number',
      key: 'number',
      render: (v: string, r: Claim) => (
        <a onClick={() => navigate(`/claims/${r.id}`)}>{v}</a>
      ),
    },
    { title: 'Type', dataIndex: 'claim_type', key: 'type' },
    { title: 'Date', dataIndex: 'claim_date', key: 'date', render: formatDate },
    {
      title: 'Amount',
      dataIndex: 'claimed_amount',
      key: 'amount',
      render: (v: number) => formatCurrency(v, policy.currency),
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (s: string) => (
        <Tag color={STATUS_COLORS[s]}>{formatStatus(s)}</Tag>
      ),
    },
  ];

  return (
    <>
      <PageHeader
        title={policy.policy_number}
        subtitle={policy.product_name || policy.product_code}
        tags={[
          <Tag key="status" color={STATUS_COLORS[policy.status]}>
            {formatStatus(policy.status)}
          </Tag>,
        ]}
        breadcrumbs={[
          { title: 'Policies', path: '/policies' },
          { title: policy.policy_number },
        ]}
        extra={
          <Space>
            {hasPermission('policy', 'update') && (
              <Button
                icon={<EditOutlined />}
                onClick={() => navigate(`/policies/${id}/edit`)}
              >
                Edit
              </Button>
            )}
            {hasPermission('policy', 'delete') && (
              <Button
                danger
                icon={<DeleteOutlined />}
                onClick={handleDelete}
              >
                Delete
              </Button>
            )}
          </Space>
        }
      />

      {/* Summary Stats */}
      <Row gutter={16} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Sum Assured"
              value={policy.sum_assured}
              prefix={<DollarOutlined />}
              formatter={(v) => formatCurrency(Number(v), policy.currency)}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Premium"
              value={policy.premium_amount}
              suffix={`/ ${policy.premium_frequency}`}
              formatter={(v) => formatCurrency(Number(v), policy.currency)}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Issue Date"
              value={formatDate(policy.issue_date)}
              prefix={<CalendarOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Policyholder"
              value={policy.policyholder?.full_name || '-'}
              prefix={<UserOutlined />}
            />
          </Card>
        </Col>
      </Row>

      {/* Tabs */}
      <Card>
        <Tabs
          items={[
            {
              key: 'details',
              label: 'Details',
              icon: <FileTextOutlined />,
              children: (
                <Descriptions bordered column={2}>
                  <Descriptions.Item label="Policy Number">
                    {policy.policy_number}
                  </Descriptions.Item>
                  <Descriptions.Item label="Status">
                    <Tag color={STATUS_COLORS[policy.status]}>
                      {formatStatus(policy.status)}
                    </Tag>
                  </Descriptions.Item>
                  <Descriptions.Item label="Product Type">
                    {policy.product_type}
                  </Descriptions.Item>
                  <Descriptions.Item label="Product Code">
                    {policy.product_code}
                  </Descriptions.Item>
                  <Descriptions.Item label="Product Name">
                    {policy.product_name || '-'}
                  </Descriptions.Item>
                  <Descriptions.Item label="Currency">
                    {policy.currency}
                  </Descriptions.Item>
                  <Descriptions.Item label="Sum Assured">
                    {formatCurrency(policy.sum_assured, policy.currency)}
                  </Descriptions.Item>
                  <Descriptions.Item label="Premium">
                    {formatCurrency(policy.premium_amount, policy.currency)} /{' '}
                    {policy.premium_frequency}
                  </Descriptions.Item>
                  <Descriptions.Item label="Issue Date">
                    {formatDate(policy.issue_date)}
                  </Descriptions.Item>
                  <Descriptions.Item label="Effective Date">
                    {formatDate(policy.effective_date)}
                  </Descriptions.Item>
                  <Descriptions.Item label="Maturity Date">
                    {formatDate(policy.maturity_date)}
                  </Descriptions.Item>
                  <Descriptions.Item label="Branch">
                    {policy.branch_code || '-'}
                  </Descriptions.Item>
                </Descriptions>
              ),
            },
            {
              key: 'policyholder',
              label: 'Policyholder',
              icon: <UserOutlined />,
              children: policy.policyholder ? (
                <Descriptions bordered column={2}>
                  <Descriptions.Item label="Name">
                    {policy.policyholder.full_name}
                  </Descriptions.Item>
                  <Descriptions.Item label="Date of Birth">
                    {formatDate(policy.policyholder.date_of_birth)}
                  </Descriptions.Item>
                  <Descriptions.Item label="Gender">
                    {policy.policyholder.gender}
                  </Descriptions.Item>
                  <Descriptions.Item label="Smoker Status">
                    {policy.policyholder.smoker_status}
                  </Descriptions.Item>
                  <Descriptions.Item label="Email">
                    {policy.policyholder.email || '-'}
                  </Descriptions.Item>
                  <Descriptions.Item label="Phone">
                    {policy.policyholder.phone || '-'}
                  </Descriptions.Item>
                </Descriptions>
              ) : (
                <p>No policyholder information available</p>
              ),
            },
            {
              key: 'coverages',
              label: 'Coverages',
              children: (
                <Table
                  dataSource={policy.coverages || []}
                  columns={coverageColumns}
                  rowKey="id"
                  pagination={false}
                />
              ),
            },
            {
              key: 'claims',
              label: 'Claims',
              children: (
                <Table
                  dataSource={(policy as any).claims || []}
                  columns={claimColumns}
                  rowKey="id"
                  pagination={false}
                  locale={{ emptyText: 'No claims filed' }}
                />
              ),
            },
            {
              key: 'history',
              label: 'History',
              icon: <HistoryOutlined />,
              children: (
                <Timeline
                  items={
                    historyData?.map((item: any) => ({
                      children: (
                        <>
                          <strong>{item.action}</strong>
                          <br />
                          <small>
                            {formatDate(item.timestamp)} by {item.user?.full_name}
                          </small>
                        </>
                      ),
                    })) || []
                  }
                />
              ),
            },
          ]}
        />
      </Card>
    </>
  );
}
