import { useParams } from 'react-router-dom';
import { Card } from 'antd';
import PageHeader from '@/components/common/PageHeader';

export default function DashboardEditor() {
  const { id } = useParams();
  return (
    <>
      <PageHeader title="Dashboard Editor" subtitle={`Editing dashboard ${id}`} backUrl="/dashboards" />
      <Card>
        <div style={{ height: 400, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#999' }}>
          Dashboard editor coming soon
        </div>
      </Card>
    </>
  );
}
