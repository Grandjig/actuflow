import { useNavigate } from 'react-router-dom';
import { Card, Form, Input, Select, Button, Space, Alert, message } from 'antd';

import PageHeader from '@/components/common/PageHeader';
import { useCreateCalculation } from '@/hooks/useCalculations';
import { useAssumptionSets } from '@/hooks/useAssumptions';

export default function CalculationCreate() {
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const createMutation = useCreateCalculation();

  const { data: assumptionSets, isLoading: loadingAssumptions } = useAssumptionSets({
    status: 'approved',
  });

  // Mock models - in real app, this comes from API
  const models = [
    { id: 'model-1', name: 'Standard Reserve Model' },
    { id: 'model-2', name: 'Cash Flow Projection Model' },
  ];

  const handleSubmit = async (values: any) => {
    try {
      const result = await createMutation.mutateAsync(values);
      message.success('Calculation started');
      navigate(`/calculations/${result.id}`);
    } catch (error: any) {
      message.error(error.message || 'Failed to start calculation');
    }
  };

  return (
    <>
      <PageHeader
        title="New Calculation"
        breadcrumbs={[
          { title: 'Calculations', path: '/calculations' },
          { title: 'New Calculation' },
        ]}
      />

      <Card style={{ maxWidth: 600 }}>
        <Alert
          message="Calculation runs are queued and processed in the background. You can monitor progress on the detail page."
          type="info"
          showIcon
          style={{ marginBottom: 24 }}
        />

        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Form.Item
            name="run_name"
            label="Run Name"
            rules={[{ required: true, message: 'Please enter a run name' }]}
          >
            <Input placeholder="e.g., Monthly Valuation - January 2024" />
          </Form.Item>

          <Form.Item
            name="model_definition_id"
            label="Model"
            rules={[{ required: true, message: 'Please select a model' }]}
          >
            <Select
              placeholder="Select calculation model"
              options={models.map((m) => ({ value: m.id, label: m.name }))}
            />
          </Form.Item>

          <Form.Item
            name="assumption_set_id"
            label="Assumption Set"
            rules={[{ required: true, message: 'Please select an assumption set' }]}
          >
            <Select
              placeholder="Select assumption set"
              loading={loadingAssumptions}
              options={assumptionSets?.items?.map((a) => ({
                value: a.id,
                label: `${a.name} (v${a.version})`,
              }))}
            />
          </Form.Item>

          <Form.Item>
            <Space>
              <Button
                type="primary"
                htmlType="submit"
                loading={createMutation.isPending}
              >
                Start Calculation
              </Button>
              <Button onClick={() => navigate('/calculations')}>Cancel</Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </>
  );
}
