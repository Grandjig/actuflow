import { useNavigate } from 'react-router-dom';
import { Card, Table, Button, Tag } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';
import { formatDate } from '@/utils/formatters';

const mockImports = [
  { id: '1', file_name: 'policies_jan2024.csv', import_type: 'policy', status: 'completed', total_rows: 1500, created_at: '2024-01-15' },
  { id: '2', file_name: 'claims_q4.xlsx', import_type: 'claim', status: 'failed', total_rows: 234, created_at: '2024-01-10' },
];

export default function ImportList() {
  const navigate = useNavigate();
  const columns = [
    { title: 'File', dataIndex: 'file_name', key: 'file' },
    { title: 'Type', dataIndex: 'import_type', key: 'type', render: (v: string) => <Tag>{v}</Tag> },
    { title: 'Status', dataIndex: 'status', key: 'status', render: (v: string) => <StatusBadge status={v} /> },
    { title: 'Rows', dataIndex: 'total_rows', key: 'rows' },
    { title: 'Date', dataIndex: 'created_at', key: 'date', render: formatDate },
  ];

  return (
    <>
      <PageHeader title="Data Imports" extra={<Button type="primary" icon={<UploadOutlined />} onClick={() => navigate('/imports/new')}>New Import</Button>} />
      <Card>
        <Table columns={columns} dataSource={mockImports} rowKey="id" />
      </Card>
    </>
  );
}
