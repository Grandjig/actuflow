import { Card, Table, Tag, Button } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';

const mockTemplates = [
  { id: '1', name: 'IFRS17 Disclosure', report_type: 'regulatory', output_format: 'PDF' },
  { id: '2', name: 'Monthly Summary', report_type: 'internal', output_format: 'Excel' },
];

export default function ReportTemplateList() {
  const columns = [
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Type', dataIndex: 'report_type', key: 'type', render: (v: string) => <Tag>{v}</Tag> },
    { title: 'Format', dataIndex: 'output_format', key: 'format' },
  ];

  return (
    <>
      <PageHeader title="Report Templates" extra={<Button type="primary" icon={<PlusOutlined />}>New Template</Button>} />
      <Card>
        <Table columns={columns} dataSource={mockTemplates} rowKey="id" />
      </Card>
    </>
  );
}
