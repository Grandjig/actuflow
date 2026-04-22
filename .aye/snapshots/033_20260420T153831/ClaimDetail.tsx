import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Descriptions,
  Button,
  Space,
  Tag,
  Alert,
  Row,
  Col,
  Statistic,
  Timeline,
} from 'antd';
import { EditOutlined, WarningOutlined } from '@ant-design/icons';

import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import { useClaim } from '@/hooks/useClaims';
import { useAuthStore } from '@/stores/authStore';
import { formatCurrency, formatDate } from '@/utils/formatters';

export default function ClaimDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { hasPermission } = useAuthStore();

  const { data: claim, isLoading } = useClaim(id!);

  if (isLoading) {
    return <LoadingSpinner fullScreen tip="Loading claim..." />;
  }

  if (!claim) {
    return (
      <Card>
        <div style={{ textAlign: 'center', padding: 48 }}>
          <h3>Claim not found</h3>
          <Button onClick={() => navigate('/claims')}>Back to Claims</Button>
        </div>
      </Card>
    );
  }

  const hasAnomaly = claim.anomaly_score && claim.anomaly_score > 0.5;

  return (
    <>
      <PageHeader
        title={claim.claim_number}
        subtitle={`${claim.claim_type} claim`}
        backUrl="/claims"
        breadcrumbs={[
          { title: 'Claims', path: '/claims' },
          { title: claim.claim_number },
        ]}
        tags={[
          <StatusBadge key="status" status={claim.status} />,
          hasAnomaly && (
            <Tag key="anomaly" color="red" icon={<WarningOutlined />}>
              Anomaly Detected
            </Tag>
          ),
        ].filter(Boolean)}
        extra={
          hasPermission('claim', 'update') && (
            <Button icon={<EditOutlined />} onClick={() => navigate(`/claims/${id}/edit`)}>
              Edit
            </Button>
          )
        }
      />

      {hasAnomaly && (
        <Alert
          type="warning"
          icon={<WarningOutlined />}
          message="AI Anomaly Detection Alert"
          description="This claim has been flagged for review. The claim amount or pattern is unusual compared to historical data."
          style={{ marginBottom: 24 }}
          showIcon
        />
      )}

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic title="Claimed Amount" value={formatCurrency(claim.claimed_amount)} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Settlement Amount"
              value={claim.settlement_amount ? formatCurrency(claim.settlement_amount) : '-'}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="Claim Date" value={formatDate(claim.claim_date)} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Risk Score"
              value={claim.anomaly_score ? `${(claim.anomaly_score * 100).toFixed(0)}%` : 'N/A'}
              valueStyle={{
                color: claim.anomaly_score && claim.anomaly_score > 0.7 ? '#ff4d4f' : undefined,
              }}
            />
          </Card>
        </Col>
      </Row>

      <Card title="Claim Details" style={{ marginBottom: 24 }}>
        <Descriptions bordered column={2}>
          <Descriptions.Item label="Claim Number">{claim.claim_number}</Descriptions.Item>
          <Descriptions.Item label="Status">
            <StatusBadge status={claim.status} />
          </Descriptions.Item>
          <Descriptions.Item label="Claim Type">
            <Tag>{claim.claim_type}</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Policy ID">
            <a onClick={() => navigate(`/policies/${claim.policy_id}`)}>
              {claim.policy_id.slice(0, 8)}...
            </a>
          </Descriptions.Item>
          <Descriptions.Item label="Claim Date">{formatDate(claim.claim_date)}</Descriptions.Item>
          <Descriptions.Item label="Incident Date">
            {claim.incident_date ? formatDate(claim.incident_date) : '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Notification Date">
            {claim.notification_date ? formatDate(claim.notification_date) : '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Settlement Date">
            {claim.settlement_date ? formatDate(claim.settlement_date) : '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Claimed Amount">
            {formatCurrency(claim.claimed_amount)}
          </Descriptions.Item>
          <Descriptions.Item label="Settlement Amount">
            {claim.settlement_amount ? formatCurrency(claim.settlement_amount) : '-'}
          </Descriptions.Item>
          {claim.denial_reason && (
            <Descriptions.Item label="Denial Reason" span={2}>
              {claim.denial_reason}
            </Descriptions.Item>
          )}
          {claim.adjuster_notes && (
            <Descriptions.Item label="Adjuster Notes" span={2}>
              {claim.adjuster_notes}
            </Descriptions.Item>
          )}
          <Descriptions.Item label="Created">{formatDate(claim.created_at)}</Descriptions.Item>
          <Descriptions.Item label="Updated">{formatDate(claim.updated_at)}</Descriptions.Item>
        </Descriptions>
      </Card>

      <Card title="Claim History">
        <Timeline
          items={[
            {
              color: 'green',
              children: `Claim submitted on ${formatDate(claim.created_at)}`,
            },
            {
              color: claim.status === 'under_review' ? 'blue' : 'gray',
              children: `Status: ${claim.status}`,
            },
            ...(claim.settlement_date
              ? [
                  {
                    color: 'green' as const,
                    children: `Settled on ${formatDate(claim.settlement_date)}`,
                  },
                ]
              : []),
          ]}
        />
      </Card>
    </>
  );
}
