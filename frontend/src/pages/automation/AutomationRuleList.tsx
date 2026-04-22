import { Card, Table, Tag, Button, Switch } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';

const mockRules = [
  { id: '1', name: 'High Value Claim Alert', trigger_type: 'claim_filed', action_type: 'send_notification', is_active: true },
  { id: '2', name: 'Auto-approve Low Risk', trigger_type: 'assumption_submitted', action_type: 'auto_approve', is_active: false },
];

export default function AutomationRuleList() {
  const columns = [
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Trigger', dataIndex: 'trigger_type', key: 'trigger', render: (v: string) => <Tag color="blue">{v}</Tag> },
    { title: 'Action', dataIndex: 'action_type', key: 'action', render: (v: string) => <Tag color="green">{v}</Tag> },
    { title: 'Active', dataIndex: 'is_active', key: 'active', render: (v: boolean) => <Switch checked={v} size="small" /> },
  ];

  return (
    <>
      <PageHeader title="Automation Rules" extra={<Button type="primary" icon={<PlusOutlined />}>New Rule</Button>} />
      <Card>
        <Table columns={columns} dataSource={mockRules} rowKey="id" />
      </Card>
    </>
  );
}
