import { useParams } from 'react-router-dom';
import { Card, Descriptions } from 'antd';
import PageHeader from '@/components/common/PageHeader';

export default function ScenarioDetail() {
  const { id } = useParams();
  return (
    <>
      <PageHeader title="Scenario" subtitle={`ID: ${id}`} backUrl="/scenarios" />
      <Card>
        <Descriptions bordered>
          <Descriptions.Item label="ID">{id}</Descriptions.Item>
        </Descriptions>
      </Card>
    </>
  );
}
