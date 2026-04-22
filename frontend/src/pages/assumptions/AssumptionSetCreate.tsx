import { useNavigate } from 'react-router-dom';
import { Card, Form, Input, Select, DatePicker, Button, Space, message } from 'antd';
import PageHeader from '@/components/common/PageHeader';
import { useCreateAssumptionSet } from '@/hooks/useAssumptions';

export default function AssumptionSetCreate() {
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const mutation = useCreateAssumptionSet();

  const handleSubmit = async (values: any) => {
    try {
      await mutation.mutateAsync({
        ...values,
        effective_date: values.effective_date?.format('YYYY-MM-DD'),
      });
      message.success('Created');
      navigate('/assumptions');
    } catch (e: any) {
      message.error(e.message || 'Failed');
    }
  };

  return (
    <>
      <PageHeader title="New Assumption Set" backUrl="/assumptions" />
      <Card>
        <Form form={form} layout="vertical" onFinish={handleSubmit} style={{ maxWidth: 600 }}>
          <Form.Item name="name" label="Name" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="version" label="Version" rules={[{ required: true }]}>
            <Input placeholder="1.0.0" />
          </Form.Item>
          <Form.Item name="line_of_business" label="Line of Business">
            <Select options={[{ label: 'Life', value: 'life' }, { label: 'Health', value: 'health' }]} />
          </Form.Item>
          <Form.Item name="effective_date" label="Effective Date">
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="description" label="Description">
            <Input.TextArea rows={3} />
          </Form.Item>
          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit" loading={mutation.isPending}>Create</Button>
              <Button onClick={() => navigate('/assumptions')}>Cancel</Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </>
  );
}
