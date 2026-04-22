import { useNavigate } from 'react-router-dom';
import { Card, Form, Input, DatePicker, Button, Space, Row, Col } from 'antd';
import PageHeader from '@/components/common/PageHeader';
import { useCreateAssumptionSet } from '@/hooks/useAssumptions';
import type { AssumptionSetCreate as AssumptionSetCreateType } from '@/api/assumptions';

const { TextArea } = Input;

export default function AssumptionSetCreate() {
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const createAssumptionSet = useCreateAssumptionSet();

  const handleSubmit = (values: AssumptionSetCreateType) => {
    const formattedValues = {
      ...values,
      effective_date: values.effective_date?.format('YYYY-MM-DD'),
    };

    createAssumptionSet.mutate(formattedValues as any, {
      onSuccess: (data) => {
        navigate(`/assumptions/${data.id}`);
      },
    });
  };

  return (
    <div>
      <PageHeader
        title="Create Assumption Set"
        backUrl="/assumptions"
        breadcrumb={[
          { title: 'Home', path: '/' },
          { title: 'Assumptions', path: '/assumptions' },
          { title: 'New Assumption Set' },
        ]}
      />

      <Card>
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Row gutter={24}>
            <Col xs={24} md={12}>
              <Form.Item
                name="name"
                label="Name"
                rules={[{ required: true, message: 'Please enter a name' }]}
              >
                <Input placeholder="e.g., Q4 2024 Assumptions" />
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
              <Form.Item
                name="version"
                label="Version"
                rules={[{ required: true, message: 'Please enter version' }]}
              >
                <Input placeholder="e.g., 1.0.0" />
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
              <Form.Item name="effective_date" label="Effective Date">
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col xs={24}>
              <Form.Item name="description" label="Description">
                <TextArea
                  rows={4}
                  placeholder="Describe the purpose and context of this assumption set..."
                />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item style={{ marginTop: 24 }}>
            <Space>
              <Button
                type="primary"
                htmlType="submit"
                loading={createAssumptionSet.isPending}
              >
                Create Assumption Set
              </Button>
              <Button onClick={() => navigate('/assumptions')}>Cancel</Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
}
