/**
 * Create calculation page.
 */

import { useNavigate } from 'react-router-dom';
import {
  Card,
  Form,
  Input,
  Select,
  Button,
  Space,
  Typography,
  DatePicker,
  message,
} from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { useQuery } from '@tanstack/react-query';
import { useCreateCalculationRun } from '@/hooks/useCalculations';
import { getAssumptionSets } from '@/api/assumptions';
import { getModelDefinitions } from '@/api/models';

const { Title } = Typography;

interface FormValues {
  run_name: string;
  model_definition_id: string;
  assumption_set_id: string;
  valuation_date: string;
}

export default function CalculationCreate() {
  const navigate = useNavigate();
  const [form] = Form.useForm<FormValues>();
  const createMutation = useCreateCalculationRun();

  const { data: models } = useQuery({
    queryKey: ['modelDefinitions'],
    queryFn: () => getModelDefinitions({ status: 'active' }),
  });

  const { data: assumptions } = useQuery({
    queryKey: ['assumptionSets'],
    queryFn: () => getAssumptionSets({ status: 'approved' }),
  });

  const handleSubmit = async (values: FormValues) => {
    try {
      const result = await createMutation.mutateAsync({
        run_name: values.run_name,
        model_definition_id: values.model_definition_id,
        assumption_set_id: values.assumption_set_id,
        parameters: {
          valuation_date: values.valuation_date,
        },
      });
      message.success('Calculation started');
      navigate(`/calculations/${result.id}`);
    } catch {
      message.error('Failed to start calculation');
    }
  };

  return (
    <div>
      <Space style={{ marginBottom: 16 }}>
        <Button
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate('/calculations')}
        >
          Back
        </Button>
      </Space>

      <Title level={2}>New Calculation Run</Title>

      <Card style={{ maxWidth: 600 }}>
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
            <Input placeholder="e.g., Q4 2024 Reserve Calculation" />
          </Form.Item>

          <Form.Item
            name="model_definition_id"
            label="Model"
            rules={[{ required: true, message: 'Please select a model' }]}
          >
            <Select
              placeholder="Select model"
              options={models?.items?.map((m) => ({
                value: m.id,
                label: m.name,
              }))}
            />
          </Form.Item>

          <Form.Item
            name="assumption_set_id"
            label="Assumption Set"
            rules={[{ required: true, message: 'Please select an assumption set' }]}
          >
            <Select
              placeholder="Select assumption set"
              options={assumptions?.items?.map((a) => ({
                value: a.id,
                label: `${a.name} (v${a.version})`,
              }))}
            />
          </Form.Item>

          <Form.Item
            name="valuation_date"
            label="Valuation Date"
            rules={[{ required: true, message: 'Please select valuation date' }]}
          >
            <DatePicker style={{ width: '100%' }} />
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
              <Button onClick={() => navigate('/calculations')}>
                Cancel
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
}
