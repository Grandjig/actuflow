import { useNavigate } from 'react-router-dom';
import { Card, Form, Input, Select, DatePicker, InputNumber, Button, Space, message, Row, Col } from 'antd';
import dayjs from 'dayjs';

import PageHeader from '@/components/common/PageHeader';
import { useCreatePolicy } from '@/hooks/usePolicies';
import { usePolicyholders } from '@/hooks/usePolicyholders';
import { PRODUCT_TYPES, PREMIUM_FREQUENCIES, CURRENCIES } from '@/utils/constants';

export default function PolicyCreate() {
  const navigate = useNavigate();
  const [form] = Form.useForm();
  
  const createMutation = useCreatePolicy();
  const { data: policyholders, isLoading: loadingPolicyholders } = usePolicyholders({ page_size: 1000 });

  const handleSubmit = async (values: any) => {
    try {
      const payload = {
        ...values,
        issue_date: values.issue_date.format('YYYY-MM-DD'),
        effective_date: values.effective_date.format('YYYY-MM-DD'),
        maturity_date: values.maturity_date?.format('YYYY-MM-DD'),
      };
      
      const result = await createMutation.mutateAsync(payload);
      message.success('Policy created successfully');
      navigate(`/policies/${result.id}`);
    } catch (error: any) {
      message.error(error.message || 'Failed to create policy');
    }
  };

  return (
    <>
      <PageHeader
        title="New Policy"
        breadcrumbs={[
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
            status: 'active',
            issue_date: dayjs(),
            effective_date: dayjs(),
          }}
          style={{ maxWidth: 800 }}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="policy_number"
                label="Policy Number"
                rules={[{ required: true, message: 'Policy number is required' }]}
              >
                <Input placeholder="e.g., POL-2024-000001" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="policyholder_id"
                label="Policyholder"
                rules={[{ required: true, message: 'Policyholder is required' }]}
              >
                <Select
                  placeholder="Select policyholder"
                  loading={loadingPolicyholders}
                  showSearch
                  optionFilterProp="children"
                  options={policyholders?.items.map((ph) => ({
                    value: ph.id,
                    label: ph.full_name,
                  }))}
                />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="product_type"
                label="Product Type"
                rules={[{ required: true }]}
              >
                <Select placeholder="Select product type" options={PRODUCT_TYPES} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="product_code"
                label="Product Code"
                rules={[{ required: true }]}
              >
                <Input placeholder="e.g., TERM-20" />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item name="product_name" label="Product Name">
                <Input placeholder="e.g., 20-Year Term Life" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="issue_date"
                label="Issue Date"
                rules={[{ required: true }]}
              >
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="effective_date"
                label="Effective Date"
                rules={[{ required: true }]}
              >
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item name="maturity_date" label="Maturity Date">
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="sum_assured"
                label="Sum Assured"
                rules={[{ required: true }]}
              >
                <InputNumber
                  style={{ width: '100%' }}
                  min={0}
                  formatter={(v) => `${v}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  parser={(v) => v!.replace(/\$\s?|(,*)/g, '')}
                />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="premium_amount"
                label="Premium Amount"
                rules={[{ required: true }]}
              >
                <InputNumber
                  style={{ width: '100%' }}
                  min={0}
                  formatter={(v) => `${v}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  parser={(v) => v!.replace(/\$\s?|(,*)/g, '')}
                />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="premium_frequency"
                label="Premium Frequency"
                rules={[{ required: true }]}
              >
                <Select options={PREMIUM_FREQUENCIES} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="currency"
                label="Currency"
                rules={[{ required: true }]}
              >
                <Select options={CURRENCIES} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item name="branch_code" label="Branch Code">
                <Input placeholder="Optional" />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit" loading={createMutation.isPending}>
                Create Policy
              </Button>
              <Button onClick={() => navigate('/policies')}>Cancel</Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </>
  );
}
