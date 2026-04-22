import { useParams } from 'react-router-dom';
import { Card, Descriptions, Spin, Button, Space } from 'antd';
import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';
import { useAssumptionSet } from '@/hooks/useAssumptions';
import { formatDate } from '@/utils/formatters';

export default function AssumptionSetDetail() {
  const { id } = useParams<{ id: string }>();
  const { data, isLoading } = useAssumptionSet(id!);

  if (isLoading) return <Spin size="large" />;
  if (!data) return <Card><p>Not found</p></Card>;

  return (
    <>
      <PageHeader
        title={data.name}
        subtitle={`Version ${data.version}`}
        backUrl="/assumptions"
        tags={[<StatusBadge key="s" status={data.status} />]}
        extra={<Space><Button>Edit</Button><Button type="primary">Submit for Approval</Button></Space>}
      />
      <Card>
        <Descriptions bordered column={2}>
          <Descriptions.Item label="Name">{data.name}</Descriptions.Item>
          <Descriptions.Item label="Version">{data.version}</Descriptions.Item>
          <Descriptions.Item label="Status"><StatusBadge status={data.status} /></Descriptions.Item>
          <Descriptions.Item label="Line of Business">{data.line_of_business || '-'}</Descriptions.Item>
          <Descriptions.Item label="Effective Date">{formatDate(data.effective_date)}</Descriptions.Item>
          <Descriptions.Item label="Created">{formatDate(data.created_at)}</Descriptions.Item>
          <Descriptions.Item label="Description" span={2}>{data.description || '-'}</Descriptions.Item>
        </Descriptions>
      </Card>
    </>
  );
}
