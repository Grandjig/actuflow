import { useParams } from 'react-router-dom';
import { Card, Descriptions, Spin, Tag } from 'antd';
import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';
import { useClaim } from '@/hooks/useClaims';
import { formatDate, formatCurrency } from '@/utils/formatters';

export default function ClaimDetail() {
  const { id } = useParams<{ id: string }>();
  const { data, isLoading } = useClaim(id!);

  if (isLoading) return <Spin size="large" />;
  if (!data) return <Card><p>Claim not found</p></Card>;

  return (
    <>
      <PageHeader title={data.claim_number} backUrl="/claims" tags={[<StatusBadge key="s" status={data.status} />]} />
      <Card>
        <Descriptions bordered column={2}>
          <Descriptions.Item label="Claim Number">{data.claim_number}</Descriptions.Item>
          <Descriptions.Item label="Status"><StatusBadge status={data.status} /></Descriptions.Item>
          <Descriptions.Item label="Type"><Tag>{data.claim_type}</Tag></Descriptions.Item>
          <Descriptions.Item label="Claim Date">{formatDate(data.claim_date)}</Descriptions.Item>
          <Descriptions.Item label="Claimed Amount">{formatCurrency(data.claimed_amount)}</Descriptions.Item>
          <Descriptions.Item label="Settlement">{data.settlement_amount ? formatCurrency(data.settlement_amount) : '-'}</Descriptions.Item>
          {data.anomaly_score && (
            <Descriptions.Item label="Anomaly Score"><Tag color="red">{(data.anomaly_score * 100).toFixed(0)}%</Tag></Descriptions.Item>
          )}
        </Descriptions>
      </Card>
    </>
  );
}
