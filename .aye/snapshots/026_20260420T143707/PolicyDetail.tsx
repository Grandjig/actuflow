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
  Statistic,
  Row,
  Col,
  Dropdown,
} from 'antd';
import {
  EditOutlined,
  DeleteOutlined,
  MoreOutlined,
  FileTextOutlined,
  DollarOutlined,
  HistoryOutlined,
} from '@ant-design/icons';
import type { MenuProps } from 'antd';

import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import { usePolicy, usePolicyClaims, useDeletePolicy } from '@/hooks/usePolicies';
import { useAuthStore } from '@/stores/authStore';
import { formatCurrency, formatDate, formatPercent } from '@/utils/formatters';
import type { Claim } from '@/types/models';

export default function PolicyDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { hasPermission } = useAuthStore();

  const { data: policy, isLoading } = usePolicy(id!);
  const { data: claims } = usePolicyClaims(id!);
  const deleteMutation = useDeletePolicy();

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

  const handleDelete = async () => {
    await deleteMutation.mutateAsync(id!);
    navigate('/policies');
  };

  const menuItems: MenuProps['items'] = [
    {
      key: 'edit',
      icon: <EditOutlined />,
      label: 'Edit Policy',
      disabled: !hasPermission('policy', 'update'),
      onClick: () => navigate(`/policies/${id}/edit`),
    },
    { type: 'divider' },
    {
      key: 'delete',
      icon: <DeleteOutlined />,
      label: 'Delete Policy',
      danger: true,
      disabled: !hasPermission('policy', 'delete') || policy.status === 'active',
      onClick: handleDelete,
    },
  ];

  const claimColumns = [
    {
      title: 'Claim Number',
      dataIndex: 'claim_number',
      key: 'number',
    },
    {
      title: 'Type',
      dataIndex: 'claim_type',
      key: 'type',
      render: (type: string) => <Tag>{type}</Tag>,
    },
    {
      title: 'Amount',
      dataIndex: 'claim_amount',
      key: 'amount',
      render: (amount: number) => formatCurrency(amount),
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => <StatusBadge status={status} />,
    },
    {
      title: 'Date',
      dataIndex: 'claim_date',
      key: 'date',
      render: formatDate,
    },
  ];

  return (
    <>
      <PageHeader
        title={policy.policy_number}
        subtitle={policy.product_name || policy.product_code}
        backUrl="/policies"
        breadcrumbs={[
          { title: 'Policies', path: '/policies' },
          { title: policy.policy_number },
        ]}
        tags={[<StatusBadge key="status" status={policy.status} />]}
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
            <Dropdown menu={{ items: menuItems }} trigger={['click']}>
              <Button icon={<MoreOutlined />} />
            </Dropdown>
          </Space>
        }
      />

      {/* Summary Cards */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Sum Assured"
              value={formatCurrency(policy.sum_assured, policy.currency)}
              prefix={<DollarOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Premium"
              value={formatCurrency(policy.premium_amount, policy.currency)}
              suffix={`/ ${policy.premium_frequency}`}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Policy Term"
              value={policy.term_years || '-'}
              suffix="years"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Claims"
              value={claims?.length || 0}
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
              icon: <FileTextOutlined />,
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
                  <Descriptions.Item label="Currency">
                    {policy.currency}
                  </Descriptions.Item>
                  <Descriptions.Item label="Sum Assured">
                    {formatCurrency(policy.sum_assured, policy.currency)}
                  </Descriptions.Item>
                  <Descriptions.Item label="Premium">
                    {formatCurrency(policy.premium_amount, policy.currency)} / {policy.premium_frequency}
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
                  <Descriptions.Item label="Risk Class">
                    {policy.risk_class || '-'}
                  </Descriptions.Item>
                  {policy.policyholder && (
                    <>
                      <Descriptions.Item label="Policyholder" span={2}>
                        <a onClick={() => navigate(`/policyholders/${policy.policyholder_id}`)}>
                          {policy.policyholder.full_name}
                        </a>
                      </Descriptions.Item>
                    </>
                  )}
                  <Descriptions.Item label="Created">
                    {formatDate(policy.created_at)}
                  </Descriptions.Item>
                  <Descriptions.Item label="Updated">
                    {formatDate(policy.updated_at)}
                  </Descriptions.Item>
                </Descriptions>
              ),
            },
            {
              key: 'claims',
              label: `Claims (${claims?.length || 0})`,
              children: (
                <Table
                  dataSource={claims || []}
                  columns={claimColumns}
                  rowKey="id"
                  pagination={false}
                />
              ),
            },
            {
              key: 'history',
              label: 'History',
              icon: <HistoryOutlined />,
              children: (
                <Timeline
                  items={[
                    {
                      children: `Policy created on ${formatDate(policy.created_at)}`,
                    },
                    {
                      children: `Status: ${policy.status}`,
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
