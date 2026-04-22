import { useParams, useNavigate } from 'react-router-dom';
import { Card, Descriptions, Button, Spin } from 'antd';
import PageHeader from '@/components/common/PageHeader';
import { usePolicyholder } from '@/hooks/usePolicyholders';
import { formatDate } from '@/utils/formatters';

export default function PolicyholderDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data, isLoading } = usePolicyholder(id!);

  if (isLoading) return <Spin size="large" />;
  if (!data) return <Card><p>Policyholder not found</p></Card>;

  return (
    <>
      <PageHeader
        title={`${data.first_name} ${data.last_name}`}
        backUrl="/policyholders"
        extra={<Button onClick={() => navigate(`/policyholders/${id}/edit`)}>Edit</Button>}
      />
      <Card>
        <Descriptions bordered column={2}>
          <Descriptions.Item label="First Name">{data.first_name}</Descriptions.Item>
          <Descriptions.Item label="Last Name">{data.last_name}</Descriptions.Item>
          <Descriptions.Item label="Date of Birth">{formatDate(data.date_of_birth)}</Descriptions.Item>
          <Descriptions.Item label="Gender">{data.gender}</Descriptions.Item>
          <Descriptions.Item label="Email">{data.email || '-'}</Descriptions.Item>
          <Descriptions.Item label="Phone">{data.phone || '-'}</Descriptions.Item>
        </Descriptions>
      </Card>
    </>
  );
}
