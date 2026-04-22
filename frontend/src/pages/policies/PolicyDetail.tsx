/**
 * Policy detail page.
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
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import { useQuery } from '@tanstack/react-query';
import { getPolicy } from '@/api/policies';
import type { Coverage, PolicyStatus } from '@/types/models';
import { formatCurrency, formatDate } from '@/utils/helpers';

const { Title } = Typography;

const statusColors: Record<PolicyStatus, string> = {
  active: 'green',
  lapsed: 'red',
  surrendered: 'orange',
  matured: 'blue',
  claimed: 'purple',
  pending: 'gold',
  cancelled: 'default',
};

export default function PolicyDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: policy, isLoading } = useQuery({
    queryKey: ['policy', id],
    queryFn: () => getPolicy(id!),
    enabled: !!id,
  });

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: 100 }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!policy) {
    return <div>Policy not found</div>;
  }

  const coverageColumns: ColumnsType<Coverage> = [
    {
      key: 'coverage_name',
      title: 'Coverage',
      dataIndex: 'coverage_name',
    },
    {
      key: 'coverage_type',
      title: 'Type',
      dataIndex: 'coverage_type',
    },
    {
      key: 'benefit_amount',
      title: 'Benefit Amount',
      dataIndex: 'benefit_amount',
      align: 'right',
      render: (value: number) => formatCurrency(value, policy.currency),
    },
    {
      key: 'premium_amount',
      title: 'Premium',
      dataIndex: 'premium_amount',
      align: 'right',
      render: (value: number) => formatCurrency(value, policy.currency),
    },
    {
      key: 'is_rider',
      title: 'Rider',
      dataIndex: 'is_rider',
      render: (value: boolean) => (value ? <Tag>Rider</Tag> : '-'),
    },
  ];

  const tabItems = [
    {
      key: 'coverages',
      label: 'Coverages',
      children: (
        <Table
          columns={coverageColumns}
          dataSource={policy.policy_data?.coverages as Coverage[] || []}
          rowKey="id"
          pagination={false}
          size="small"
        />
      ),
    },
    {
      key: 'claims',
      label: 'Claims',
      children: <div>Claims list will go here</div>,
    },
    {
      key: 'documents',
      label: 'Documents',
      children: <div>Documents list will go here</div>,
    },
    {
      key: 'history',
      label: 'History',
      children: <div>Audit history will go here</div>,
    },
  ];

  return (
    <div>
      <Space style={{ marginBottom: 16 }}>
        <Button
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate('/policies')}
        >
          Back
        </Button>
      </Space>

      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div>
            <Title level={3} style={{ marginBottom: 8 }}>
              {policy.policy_number}
            </Title>
            <Space>
              <Tag color={statusColors[policy.status]}>
                {policy.status.toUpperCase()}
              </Tag>
              <span>{policy.product_name || policy.product_code}</span>
            </Space>
          </div>
          <Button
            type="primary"
            icon={<EditOutlined />}
            onClick={() => navigate(`/policies/${id}/edit`)}
          >
            Edit
          </Button>
        </div>

        <Divider />

        <Descriptions column={3}>
          <Descriptions.Item label="Product Type">
            {policy.product_type}
          </Descriptions.Item>
          <Descriptions.Item label="Product Code">
            {policy.product_code}
          </Descriptions.Item>
          <Descriptions.Item label="Currency">
            {policy.currency}
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
          <Descriptions.Item label="Sum Assured">
            {formatCurrency(policy.sum_assured, policy.currency)}
          </Descriptions.Item>
          <Descriptions.Item label="Premium">
            {formatCurrency(policy.premium_amount, policy.currency)} / {policy.premium_frequency}
          </Descriptions.Item>
          <Descriptions.Item label="Risk Class">
            {policy.risk_class || '-'}
          </Descriptions.Item>
        </Descriptions>

        {policy.policyholder && (
          <>
            <Divider orientation="left">Policyholder</Divider>
            <Descriptions column={3}>
              <Descriptions.Item label="Name">
                {policy.policyholder.full_name}
              </Descriptions.Item>
              <Descriptions.Item label="Date of Birth">
                {formatDate(policy.policyholder.date_of_birth)}
              </Descriptions.Item>
              <Descriptions.Item label="Gender">
                {policy.policyholder.gender || '-'}
              </Descriptions.Item>
              <Descriptions.Item label="Smoker Status">
                {policy.policyholder.smoker_status || '-'}
              </Descriptions.Item>
              <Descriptions.Item label="Email">
                {policy.policyholder.email || '-'}
              </Descriptions.Item>
              <Descriptions.Item label="Phone">
                {policy.policyholder.phone || '-'}
              </Descriptions.Item>
            </Descriptions>
          </>
        )}

        <Divider />

        <Tabs items={tabItems} />
      </Card>
    </div>
  );
}
