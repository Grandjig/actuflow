import { useNavigate } from 'react-router-dom';
import {
  Card,
  Form,
  Input,
  Select,
  DatePicker,
  Button,
  Space,
  Row,
  Col,
  message,
} from 'antd';

import PageHeader from '@/components/common/PageHeader';
import { useCreateAssumptionSet } from '@/hooks/useAssumptions';

const { TextArea } = Input;

const lineOfBusinessOptions = [
  { label: 'Life', value: 'life' },
  { label: 'Health', value: 'health' },
  { label: 'Property', value: 'property' },
  { label: 'Casualty', value: 'casualty' },
  { label: 'All', value: 'all' },
];

export default function AssumptionSetCreate() {
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const createMutation = useCreateAssumptionSet();

  const handleSubmit = async (values: any) => {
    try {
      const data = {
        ...values,
        effective_date: values.effective_date?.format('YYYY-MM-DD'),
      };
      const result = await createMutation.mutateAsync(data);
      message.success('Assumption set created');
      navigate(`/assumptions/${result.id}`);
    } catch (error: any) {
      message.error(error.message || 'Failed to create assumption set');
    }
  };

  return (
    <>
      <PageHeader
        title="New Assumption Set"
        subtitle="Create a new set of actuarial assumptions"
        backUrl="/assumptions"
        breadcrumbs={[
          { title: 'Assumptions', path: '/assumptions' },
          { title: 'New' },
        ]}
      />

      <Card>
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          initialValues={{ version: '1.0.0' }}
        >
          <Row gutter={24}>
            <Col xs={24} md={12}>
              <Form.Item
                name="name"
                label="Name"
                rules={[{ required: true, message: 'Required' }]}
              >
                <Input placeholder="e.g., Base Assumptions Q1 2024" />
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
              <Form.Item
                name="version"
                label="Version"
                rules={[{ required: true, message: 'Required' }]}
              >
                <Input placeholder="1.0.0" />
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
              <Form.Item name="effective_date" label="Effective Date">
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col xs={24} md={12}>
              <Form.Item name="line_of_business" label="Line of Business">
                <Select
                  options={lineOfBusinessOptions}
                  placeholder="Select line of business"
                />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item name="description" label="Description">
            <TextArea rows={4} placeholder="Describe the purpose of this assumption set" />
          </Form.Item>

          <Form.Item style={{ marginTop: 24 }}>
            <Space>
              <Button
                type="primary"
                htmlType="submit"
                loading={createMutation.isPending}
              >
                Create Assumption Set
              </Button>
              <Button onClick={() => navigate('/assumptions')}>Cancel</Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </>
  );
}
