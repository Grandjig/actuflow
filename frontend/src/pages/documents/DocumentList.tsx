import { Card, Table, Tag, Button } from 'antd';
import { UploadOutlined, EyeOutlined } from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';
import { formatDate } from '@/utils/formatters';

const mockDocs = [
  { id: '1', file_name: 'policy_application.pdf', document_type: 'application', created_at: '2024-01-15' },
  { id: '2', file_name: 'claim_form_001.pdf', document_type: 'claim_form', created_at: '2024-02-01' },
];

export default function DocumentList() {
  const columns = [
    { title: 'File', dataIndex: 'file_name', key: 'file' },
    { title: 'Type', dataIndex: 'document_type', key: 'type', render: (v: string) => <Tag>{v}</Tag> },
    { title: 'Uploaded', dataIndex: 'created_at', key: 'date', render: formatDate },
    { title: 'Actions', key: 'actions', render: () => <Button icon={<EyeOutlined />} size="small">View</Button> },
  ];

  return (
    <>
      <PageHeader title="Documents" extra={<Button type="primary" icon={<UploadOutlined />}>Upload</Button>} />
      <Card>
        <Table columns={columns} dataSource={mockDocs} rowKey="id" />
      </Card>
    </>
  );
}
