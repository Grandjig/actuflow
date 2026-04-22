import { useNavigate } from 'react-router-dom';
import { Card, Form, Input, Select, DatePicker, InputNumber, Button, Space, Row, Col } from 'antd';
import PageHeader from '@/components/common/PageHeader';
import { useCreatePolicy } from '@/hooks/usePolicies';
import { PRODUCT_TYPES, PREMIUM_FREQUENCIES } from '@/utils/constants';
import type { PolicyCreate as PolicyCreateType } from '@/api/policies';

export default function PolicyCreate() {
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const createPolicy = useCreatePolicy();

  const handleSubmit = (values: PolicyCreateType) => {
    const formattedValues = {
      ...values,
      issue_date: values.issue_date.format('YYYY-MM-DD'),
      effective_date: values.effective_date.format('YYYY-MM-DD'),
      maturity_date: values.maturity_date?.format('YYYY-MM-DD'),
    };

    createPolicy.mutate(formattedValues as any, {
      onSuccess: (data) => {
        navigate(`/policies/${data.id}`);
      },
    });
  };

  return (
    <div>
      <PageHeader
        title="Create Policy"
        backUrl="/policies"
        breadcrumb={[
          { title: 'Home', path: '/' },
          { title: 'Policies', path: '/policies' },
          { title: 'New Policy' },
        ]}
      />

      <Card>
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          initialValues={{
            currency: 'USD',
            premium_frequency: 'annual',
          }}
        >
          <Row gutter={24}>
            <Col xs={24} md={12}>
              <Form.Item
                name="policy_number"
                label="Policy Number"
                rules={[{ required: true, message: 'Please enter policy number' }]}
              >
                <Input placeholder="e.g., POL-2024-0001" />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item
                name="product_type"
                label="Product Type"
                rules={[{ required: true, message: 'Please select product type' }]}
              >
                <Select options={PRODUCT_TYPES} placeholder="Select product type" />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item
                name="product_code"
                label="Product Code"
                rules={[{ required: true, message: 'Please enter product code' }]}
              >
                <Input placeholder="e.g., TERM20" />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item name="product_name" label="Product Name">
                <Input placeholder="e.g., 20-Year Term Life" />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item
                name="policyholder_id"
                label="Policyholder ID"
                rules={[{ required: true, message: 'Please enter policyholder ID' }]}
              >
                <Input placeholder="Enter policyholder UUID" />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item name="branch_code" label="Branch Code">
                <Input placeholder="e.g., NYC001" />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item
                name="issue_date"
                label="Issue Date"
                rules={[{ required: true, message: 'Please select issue date' }]}
              >
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item
                name="effective_date"
                label="Effective Date"
                rules={[{ required: true, message: 'Please select effective date' }]}
              >
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item name="maturity_date" label="Maturity Date">
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item
                name="sum_assured"
                label="Sum Assured"
                rules={[{ required: true, message: 'Please enter sum assured' }]}
              >
                <InputNumber
                  style={{ width: '100%' }}
                  min={0}
                  formatter={(value) => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  parser={(value) => value!.replace(/\$\s?|(,*)/g, '') as any}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item
                name="premium_amount"
                label="Premium Amount"
                rules={[{ required: true, message: 'Please enter premium' }]}
              >
                <InputNumber
                  style={{ width: '100%' }}
                  min={0}
                  formatter={(value) => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  parser={(value) => value!.replace(/\$\s?|(,*)/g, '') as any}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={4}>
              <Form.Item
                name="premium_frequency"
                label="Frequency"
                rules={[{ required: true }]}
              >
                <Select options={PREMIUM_FREQUENCIES} />
              </Form.Item>
            </Col>
            <Col xs={24} md={4}>
              <Form.Item name="currency" label="Currency" rules={[{ required: true }]}>
                <Select
                  options={[
                    { label: 'USD', value: 'USD' },
                    { label: 'EUR', value: 'EUR' },
                    { label: 'GBP', value: 'GBP' },
                  ]}
                />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item style={{ marginTop: 24 }}>
            <Space>
              <Button type="primary" htmlType="submit" loading={createPolicy.isPending}>
                Create Policy
              </Button>
              <Button onClick={() => navigate('/policies')}>Cancel</Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
}
