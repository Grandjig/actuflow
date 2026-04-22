import { useNavigate } from 'react-router-dom';
import { Card, Form, Input, Select, Button, Space, message } from 'antd';
import PageHeader from '@/components/common/PageHeader';
import { useCreateCalculation } from '@/hooks/useCalculations';

export default function CalculationCreate() {
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const mutation = useCreateCalculation();

  const handleSubmit = async (values: any) => {
    try {
      const result = await mutation.mutateAsync(values);
      message.success('Calculation started');
      navigate(`/calculations/${result.id}`);
    } catch (e: any) {
      message.error(e.message || 'Failed');
    }
  };

  return (
    <>
      <PageHeader title="New Calculation Run" backUrl="/calculations" />
      <Card>
        <Form form={form} layout="vertical" onFinish={handleSubmit} style={{ maxWidth: 600 }}>
          <Form.Item name="run_name" label="Run Name" rules={[{ required: true }]}>
            <Input placeholder="Monthly Valuation - January 2024" />
          </Form.Item>
          <Form.Item name="model_definition_id" label="Model" rules={[{ required: true }]}>
            <Select placeholder="Select model" options={[]} />
          </Form.Item>
          <Form.Item name="assumption_set_id" label="Assumption Set" rules={[{ required: true }]}>
            <Select placeholder="Select assumptions" options={[]} />
          </Form.Item>
          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit" loading={mutation.isPending}>Start Calculation</Button>
              <Button onClick={() => navigate('/calculations')}>Cancel</Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </>
  );
}
