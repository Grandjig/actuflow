import { useNavigate } from 'react-router-dom';
import {
  Card,
  Form,
  Input,
  Select,
  Button,
  Space,
  Row,
  Col,
  Divider,
  message,
} from 'antd';

import PageHeader from '@/components/common/PageHeader';
import { useCreateCalculation } from '@/hooks/useCalculations';
import { useApprovedAssumptionSets } from '@/hooks/useAssumptions';

const { TextArea } = Input;

export default function CalculationCreate() {
  const navigate = useNavigate();
  const [form] = Form.useForm();

  const createMutation = useCreateCalculation();
  const { data: assumptionSets } = useApprovedAssumptionSets();

  // Mock models - in real app, fetch from API
  const models = [
    { id: 'model-1', name: 'Standard Reserve Model' },
    { id: 'model-2', name: 'IFRS17 Valuation Model' },
  ];

  const handleSubmit = async (values: any) => {
    try {
      const result = await createMutation.mutateAsync({
        run_name: values.run_name,
        model_definition_id: values.model_definition_id,
        assumption_set_id: values.assumption_set_id,
        policy_filter: values.policy_filter ? JSON.parse(values.policy_filter) : undefined,
        parameters: values.parameters ? JSON.parse(values.parameters) : undefined,
      });
      message.success('Calculation started successfully');
      navigate(`/calculations/${result.id}`);
    } catch (error: any) {
      message.error(error.message || 'Failed to start calculation');
    }
  };

  return (
    <>
      <PageHeader
        title="New Calculation"
        subtitle="Run a new actuarial calculation"
        backUrl="/calculations"
        breadcrumbs={[
          { title: 'Calculations', path: '/calculations' },
          { title: 'New Calculation' },
        ]}
      />

      <Card>
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          initialValues={{
            run_name: `Calculation - ${new Date().toLocaleDateString()}`,
          }}
        >
          <Row gutter={24}>
            <Col xs={24} md={12}>
              <Form.Item
                name="run_name"
                label="Run Name"
                rules={[{ required: true, message: 'Please enter a name' }]}
              >
                <Input placeholder="e.g., Monthly Valuation - January 2024" />
              </Form.Item>
            </Col>
          </Row>

          <Divider>Model & Assumptions</Divider>

          <Row gutter={24}>
            <Col xs={24} md={12}>
              <Form.Item
                name="model_definition_id"
                label="Model"
                rules={[{ required: true, message: 'Please select a model' }]}
              >
                <Select
                  placeholder="Select calculation model"
                  options={models.map((m) => ({ label: m.name, value: m.id }))}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item
                name="assumption_set_id"
                label="Assumption Set"
                rules={[{ required: true, message: 'Please select assumptions' }]}
              >
                <Select
                  placeholder="Select assumption set"
                  options={assumptionSets?.map((a) => ({
                    label: `${a.name} (v${a.version})`,
                    value: a.id,
                  }))}
                />
              </Form.Item>
            </Col>
          </Row>

          <Divider>Filters (Optional)</Divider>

          <Row gutter={24}>
            <Col xs={24}>
              <Form.Item
                name="policy_filter"
                label="Policy Filter (JSON)"
                help="Filter policies to include in calculation"
              >
                <TextArea
                  rows={3}
                  placeholder='{"status": "active", "product_type": "term_life"}'
                />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item style={{ marginTop: 24 }}>
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
