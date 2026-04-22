import { useParams } from 'react-router-dom';
import { Card, Descriptions } from 'antd';
import PageHeader from '@/components/common/PageHeader';

export default function ModelDetail() {
  const { id } = useParams();
  return (
    <>
      <PageHeader title="Model Definition" subtitle={`ID: ${id}`} backUrl="/models" />
      <Card>
        <Descriptions bordered>
          <Descriptions.Item label="ID">{id}</Descriptions.Item>
          <Descriptions.Item label="Status">Active</Descriptions.Item>
        </Descriptions>
      </Card>
    </>
  );
}
