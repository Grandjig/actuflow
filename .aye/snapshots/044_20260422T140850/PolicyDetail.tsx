import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Descriptions,
  Button,
  Space,
  Tag,
  Row,
  Col,
  Statistic,
  Table,
  Tabs,
  Timeline,
} from 'antd';
import { EditOutlined, CalculatorOutlined, FileTextOutlined } from '@ant-design/icons';

import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import { usePolicy } from '@/hooks/usePolicies';
import { useAuthStore } from '@/stores/authStore';
import { formatCurrency, formatDate } from '@/utils/formatters';

export default function PolicyDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { hasPermission } = useAuthStore();

  const { data: policy, isLoading } = usePolicy(id!);

  if (isLoading) {
    return <LoadingSpinner fullScreen tip="Loading policy..." />;
  }

  if (!policy) {
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
    { key: 'coverage_name', title: 'Coverage', dataIndex: 'coverage_name' },
    { key: 'coverage_type', title: 'Type', dataIndex: 'coverage_type' },
    {
      key: 'benefit_amount',
      title: 'Benefit',
      dataIndex: 'benefit_amount',
      render: formatCurrency,
      align: 'right' as const,
    },
    {
      key: 'premium_amount',
      title: 'Premium',
      dataIndex: 'premium_amount',
      render: formatCurrency,
      align: 'right' as const,
    },
    {
      key: 'is_rider',
      title: 'Rider',
      dataIndex: 'is_rider',
      render: (v: boolean) => (v ? <Tag>Rider</Tag> : <Tag color="blue">Base</Tag>),
    },
  ];

  return (
    <>
      <PageHeader
        title={policy.policy_number}
        subtitle={policy.product_name || policy.product_type}
        backUrl="/policies"
        breadcrumbs={[
          { title: 'Policies', path: '/policies' },
          { title: policy.policy_number },
        ]}
        tags={[<StatusBadge key="status" status={policy.status} />]}
        extra={
          <Space>
            {hasPermission('policy', 'update') && (
              <Button icon={<EditOutlined />} onClick={() => navigate(`/policies/${id}/edit`)}>
                Edit
              </Button>
            )}
            <Button icon={<CalculatorOutlined />}>Run Calculation</Button>
          </Space>
        }
      />

      {/* Summary Stats */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic title="Sum Assured" value={formatCurrency(policy.sum_assured)} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Premium"
              value={formatCurrency(policy.premium_amount)}
              suffix={`/ ${policy.premium_frequency}`}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="Issue Date" value={formatDate(policy.issue_date)} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Term"
              value={policy.term_years || '-'}
              suffix={policy.term_years ? 'years' : ''}
            />
          </Card>
        </Col>
      </Row>

      {/* Details Tabs */}
      <Card>
        <Tabs
          items={[
            {
              key: 'details',
              label: 'Policy Details',
              children: (
                <Descriptions bordered column={2}>
                  <Descriptions.Item label="Policy Number">
                    {policy.policy_number}
                  </Descriptions.Item>
                  <Descriptions.Item label="Status">
                    <StatusBadge status={policy.status} />
                  </Descriptions.Item>
                  <Descriptions.Item label="Product Type">
                    <Tag>{policy.product_type}</Tag>
                  </Descriptions.Item>
                  <Descriptions.Item label="Product Code">
                    {policy.product_code}
                  </Descriptions.Item>
                  <Descriptions.Item label="Product Name">
                    {policy.product_name || '-'}
                  </Descriptions.Item>
                  <Descriptions.Item label="Currency">{policy.currency}</Descriptions.Item>
                  <Descriptions.Item label="Issue Date">
                    {formatDate(policy.issue_date)}
                  </Descriptions.Item>
                  <Descriptions.Item label="Effective Date">
                    {formatDate(policy.effective_date)}
                  </Descriptions.Item>
                  <Descriptions.Item label="Maturity Date">
                    {policy.maturity_date ? formatDate(policy.maturity_date) : '-'}
                  </Descriptions.Item>
                  <Descriptions.Item label="Termination Date">
                    {policy.termination_date ? formatDate(policy.termination_date) : '-'}
                  </Descriptions.Item>
                  <Descriptions.Item label="Sum Assured">
                    {formatCurrency(policy.sum_assured)}
                  </Descriptions.Item>
                  <Descriptions.Item label="Premium">
                    {formatCurrency(policy.premium_amount)} / {policy.premium_frequency}
                  </Descriptions.Item>
                  <Descriptions.Item label="Risk Class">
                    {policy.risk_class || '-'}
                  </Descriptions.Item>
                  <Descriptions.Item label="Branch">{policy.branch_code || '-'}</Descriptions.Item>
                </Descriptions>
              ),
            },
            {
              key: 'policyholder',
              label: 'Policyholder',
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
                <div>No policyholder information</div>
              ),
            },
            {
              key: 'coverages',
              label: 'Coverages',
              children: (
                <Table
                  columns={coverageColumns}
                  dataSource={policy.coverages || []}
                  rowKey="id"
                  pagination={false}
                />
              ),
            },
            {
              key: 'history',
              label: 'History',
              children: (
                <Timeline
                  items={[
                    {
                      color: 'green',
                      children: `Policy issued on ${formatDate(policy.issue_date)}`,
                    },
                    {
                      color: 'blue',
                      children: `Created in system on ${formatDate(policy.created_at)}`,
                    },
                    {
                      color: 'gray',
                      children: `Last updated ${formatDate(policy.updated_at)}`,
                    },
                  ]}
                />
              ),
            },
          ]}
        />
      </Card>
    </>
  );
}
