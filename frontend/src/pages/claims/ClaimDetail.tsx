/**
 * Claim detail page.
 */

import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Descriptions,
  Button,
  Space,
  Tag,
  Spin,
  Typography,
  Divider,
  Alert,
} from 'antd';
import {
  ArrowLeftOutlined,
  EditOutlined,
  WarningOutlined,
} from '@ant-design/icons';
import { useQuery } from '@tanstack/react-query';
import { getClaim } from '@/api/claims';
import type { ClaimStatus } from '@/types/models';
import { formatCurrency, formatDate } from '@/utils/helpers';

const { Title } = Typography;

const statusColors: Record<ClaimStatus, string> = {
  open: 'blue',
  under_review: 'orange',
  approved: 'green',
  denied: 'red',
  paid: 'purple',
  closed: 'default',
};

export default function ClaimDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: claim, isLoading } = useQuery({
    queryKey: ['claim', id],
    queryFn: () => getClaim(id!),
    enabled: !!id,
  });

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: 100 }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!claim) {
    return <div>Claim not found</div>;
  }

  const claimedAmount = claim.claimed_amount ?? claim.claim_amount;

  return (
    <div>
      <Space style={{ marginBottom: 16 }}>
        <Button
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate('/claims')}
        >
          Back
        </Button>
      </Space>

      {claim.anomaly_score && claim.anomaly_score > 0.7 && (
        <Alert
          type="warning"
          icon={<WarningOutlined />}
          message="Anomaly Detected"
          description={`This claim has been flagged with an anomaly score of ${(claim.anomaly_score * 100).toFixed(0)}%. Please review carefully.`}
          style={{ marginBottom: 16 }}
          showIcon
        />
      )}

      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div>
            <Title level={3} style={{ marginBottom: 8 }}>
              {claim.claim_number}
            </Title>
            <Space>
              <Tag color={statusColors[claim.status]}>
                {claim.status.replace('_', ' ').toUpperCase()}
              </Tag>
              <span>{claim.claim_type}</span>
            </Space>
          </div>
          <Button
            type="primary"
            icon={<EditOutlined />}
            onClick={() => navigate(`/claims/${id}/edit`)}
          >
            Edit
          </Button>
        </div>

        <Divider />

        <Descriptions column={3}>
          <Descriptions.Item label="Claim Date">
            {formatDate(claim.claim_date)}
          </Descriptions.Item>
          <Descriptions.Item label="Incident Date">
            {formatDate(claim.incident_date)}
          </Descriptions.Item>
          <Descriptions.Item label="Claim Type">
            {claim.claim_type}
          </Descriptions.Item>
          <Descriptions.Item label="Claimed Amount">
            {formatCurrency(claimedAmount)}
          </Descriptions.Item>
          <Descriptions.Item label="Settlement Amount">
            {claim.settlement_amount ? formatCurrency(claim.settlement_amount) : '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Settlement Date">
            {formatDate(claim.settlement_date)}
          </Descriptions.Item>
        </Descriptions>

        {claim.policy && (
          <>
            <Divider orientation="left">Policy Information</Divider>
            <Descriptions column={3}>
              <Descriptions.Item label="Policy Number">
                <a onClick={() => navigate(`/policies/${claim.policy_id}`)}>
                  {claim.policy.policy_number}
                </a>
              </Descriptions.Item>
              <Descriptions.Item label="Product">
                {claim.policy.product_name || claim.policy.product_code}
              </Descriptions.Item>
              <Descriptions.Item label="Sum Assured">
                {formatCurrency(claim.policy.sum_assured, claim.policy.currency)}
              </Descriptions.Item>
            </Descriptions>
          </>
        )}

        {claim.adjuster_notes && (
          <>
            <Divider orientation="left">Adjuster Notes</Divider>
            <p>{claim.adjuster_notes}</p>
          </>
        )}

        {claim.denial_reason && (
          <>
            <Divider orientation="left">Denial Reason</Divider>
            <Alert type="error" message={claim.denial_reason} />
          </>
        )}
      </Card>
    </div>
  );
}
