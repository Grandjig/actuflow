import { useNavigate } from 'react-router-dom';
import { Card, Form, Input, Select, Button, Space, Row, Col, Alert } from 'antd';
import PageHeader from '@/components/common/PageHeader';
import { useCreateCalculation } from '@/hooks/useCalculations';
import type { CalculationRunCreate } from '@/api/calculations';

export default function CalculationCreate() {
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const createCalculation = useCreateCalculation();

  // In real app, these would come from API
  const modelOptions = [
    { label: 'Term Life Reserving - IFRS 17', value: 'model-1' },
    { label: 'Whole Life Cash Flow', value: 'model-2' },
  ];

  const assumptionOptions = [
    { label: 'Q4 2024 Approved', value: 'assumption-1' },
    { label: 'Q3 2024 Approved', value: 'assumption-2' },
  ];

  const handleSubmit = (values: CalculationRunCreate) => {
    createCalculation.mutate(values, {
      onSuccess: (data) => {
        navigate(`/calculations/${data.id}`);
      },
    });
  };

  return (
    <div>
      <PageHeader
        title="New Calculation Run"
        backUrl="/calculations"
        breadcrumb={[
          { title: 'Home', path: '/' },
          { title: 'Calculations', path: '/calculations' },
          { title: 'New Calculation' },
        ]}
      />

      <Card>
        <Alert
          message="Calculation runs process policies in the background"
          description="Depending on the number of policies and model complexity, calculations may take several minutes to complete. You'll be notified when done."
          type="info"
          showIcon
          style={{ marginBottom: 24 }}
        />

        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Row gutter={24}>
            <Col xs={24} md={12}>
              <Form.Item
                name="run_name"
                label="Run Name"
                rules={[{ required: true, message: 'Please enter a run name' }]}
              >
                <Input placeholder="e.g., Q4 2024 Reserve Calculation" />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item
                name="model_definition_id"
                label="Model"
                rules={[{ required: true, message: 'Please select a model' }]}
              >
                <Select options={modelOptions} placeholder="Select calculation model" />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item
                name="assumption_set_id"
                label="Assumption Set"
                rules={[{ required: true, message: 'Please select assumptions' }]}
              >
                <Select options={assumptionOptions} placeholder="Select assumption set" />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item style={{ marginTop: 24 }}>
            <Space>
              <Button type="primary" htmlType="submit" loading={createCalculation.isPending}>
                Start Calculation
              </Button>
              <Button onClick={() => navigate('/calculations')}>Cancel</Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
}
