import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Descriptions,
  Tag,
  Button,
  Space,
  Tabs,
  Table,
  Timeline,
  Spin,
  Row,
  Col,
} from 'antd';
import { EditOutlined, HistoryOutlined, FileTextOutlined } from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';
import EmptyState from '@/components/common/EmptyState';
import { usePolicy } from '@/hooks/usePolicies';
import { formatCurrency, formatDate, formatStatus } from '@/utils/formatters';
import type { Coverage } from '@/types/models';

export default function PolicyDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: policy, isLoading, error } = usePolicy(id!);

  if (isLoading) {
    return (
      <div style={{ padding: 100, textAlign: 'center' }}>
        <Spin size="large" />
      </div>
    );
  }

  if (error || !policy) {
    return (
      <EmptyState
        title="Policy Not Found"
        description="The policy you're looking for doesn't exist or you don't have access."
        action={{ label: 'Back to Policies', onClick: () => navigate('/policies') }}
      />
    );
  }

  const coverageColumns = [
    { title: 'Coverage Type', dataIndex: 'coverage_type', key: 'coverage_type' },
    {
      title: 'Benefit Amount',
      dataIndex: 'benefit_amount',
      key: 'benefit_amount',
      render: (value: number) => formatCurrency(value, policy.currency),
    },
    {
      title: 'Start Date',
      dataIndex: 'start_date',
      key: 'start_date',
      render: (value: string) => formatDate(value),
    },
    {
      title: 'End Date',
      dataIndex: 'end_date',
      key: 'end_date',
      render: (value: string | undefined) => (value ? formatDate(value) : '-'),
    },
    {
      title: 'Rider',
      dataIndex: 'is_rider',
      key: 'is_rider',
      render: (value: boolean) => (value ? <Tag>Rider</Tag> : <Tag color="blue">Base</Tag>),
    },
  ];

  const tabItems = [
    {
      key: 'details',
      label: 'Details',
      children: (
        <Row gutter={[24, 24]}>
          <Col xs={24} lg={12}>
            <Card title="Policy Information" size="small">
              <Descriptions column={1} size="small">
                <Descriptions.Item label="Policy Number">
                  {policy.policy_number}
                </Descriptions.Item>
                <Descriptions.Item label="Product">
                  {policy.product_name || policy.product_code}
                </Descriptions.Item>
                <Descriptions.Item label="Product Type">
                  <Tag>{policy.product_type}</Tag>
                </Descriptions.Item>
                <Descriptions.Item label="Status">
                  <StatusBadge status={policy.status} />
                </Descriptions.Item>
                <Descriptions.Item label="Issue Date">
                  {formatDate(policy.issue_date)}
                </Descriptions.Item>
                <Descriptions.Item label="Effective Date">
                  {formatDate(policy.effective_date)}
                </Descriptions.Item>
                <Descriptions.Item label="Maturity Date">
                  {policy.maturity_date ? formatDate(policy.maturity_date) : '-'}
                </Descriptions.Item>
              </Descriptions>
            </Card>
          </Col>
          <Col xs={24} lg={12}>
            <Card title="Financial Details" size="small">
              <Descriptions column={1} size="small">
                <Descriptions.Item label="Sum Assured">
                  {formatCurrency(policy.sum_assured, policy.currency)}
                </Descriptions.Item>
                <Descriptions.Item label="Premium">
                  {formatCurrency(policy.premium_amount, policy.currency)}
                </Descriptions.Item>
                <Descriptions.Item label="Premium Frequency">
                  {formatStatus(policy.premium_frequency)}
                </Descriptions.Item>
                <Descriptions.Item label="Currency">
                  {policy.currency}
                </Descriptions.Item>
              </Descriptions>
            </Card>
          </Col>
          {policy.policyholder && (
            <Col xs={24}>
              <Card title="Policyholder" size="small">
                <Descriptions column={2} size="small">
                  <Descriptions.Item label="Name">
                    {policy.policyholder.first_name} {policy.policyholder.last_name}
                  </Descriptions.Item>
                  <Descriptions.Item label="Date of Birth">
                    {formatDate(policy.policyholder.date_of_birth)}
                  </Descriptions.Item>
                  <Descriptions.Item label="Gender">
                    {formatStatus(policy.policyholder.gender)}
                  </Descriptions.Item>
                  <Descriptions.Item label="Smoker Status">
                    {formatStatus(policy.policyholder.smoker_status)}
                  </Descriptions.Item>
                  <Descriptions.Item label="Email">
                    {policy.policyholder.email || '-'}
                  </Descriptions.Item>
                  <Descriptions.Item label="Phone">
                    {policy.policyholder.phone || '-'}
                  </Descriptions.Item>
                </Descriptions>
              </Card>
            </Col>
          )}
        </Row>
      ),
    },
    {
      key: 'coverages',
      label: 'Coverages',
      children: (
        <Table<Coverage>
          columns={coverageColumns}
          dataSource={policy.coverages || []}
          rowKey="id"
          pagination={false}
        />
      ),
    },
    {
      key: 'claims',
      label: 'Claims',
      children: (
        <EmptyState
          title="No Claims"
          description="No claims have been filed for this policy."
        />
      ),
    },
    {
      key: 'history',
      label: (
        <span>
          <HistoryOutlined /> History
        </span>
      ),
      children: (
        <Timeline
          items={[
            {
              children: `Policy created on ${formatDate(policy.created_at)}`,
            },
            {
              children: `Status: ${formatStatus(policy.status)}`,
            },
          ]}
        />
      ),
    },
  ];

  return (
    <div>
      <PageHeader
        title={`Policy ${policy.policy_number}`}
        subtitle={policy.product_name || policy.product_code}
        backUrl="/policies"
        breadcrumb={[
          { title: 'Home', path: '/' },
          { title: 'Policies', path: '/policies' },
          { title: policy.policy_number },
        ]}
        extra={
          <Space>
            <Button
              icon={<EditOutlined />}
              onClick={() => navigate(`/policies/${policy.id}/edit`)}
            >
              Edit
            </Button>
          </Space>
        }
      />

      <Tabs items={tabItems} />
    </div>
  );
}
