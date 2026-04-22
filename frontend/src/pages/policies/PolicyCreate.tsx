import { useNavigate, useParams } from 'react-router-dom';
import {
  Card,
  Form,
  Input,
  Select,
  DatePicker,
  InputNumber,
  Button,
  Space,
  Row,
  Col,
  Divider,
  message,
} from 'antd';
import dayjs from 'dayjs';

import PageHeader from '@/components/common/PageHeader';
import { usePolicy, useCreatePolicy, useUpdatePolicy } from '@/hooks/usePolicies';
import { usePolicyholders } from '@/hooks/usePolicyholders';
import {
  PRODUCT_TYPES,
  POLICY_STATUSES,
  PREMIUM_FREQUENCIES,
  CURRENCIES,
} from '@/utils/constants';

export default function PolicyCreate() {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = !!id;
  const [form] = Form.useForm();

  const { data: existingPolicy, isLoading: loadingPolicy } = usePolicy(id || '');
  const { data: policyholders } = usePolicyholders({ page_size: 100 });
  const createMutation = useCreatePolicy();
  const updateMutation = useUpdatePolicy();

  // Set form values when editing
  if (isEdit && existingPolicy && !form.isFieldsTouched()) {
    form.setFieldsValue({
      ...existingPolicy,
      issue_date: existingPolicy.issue_date ? dayjs(existingPolicy.issue_date) : null,
      effective_date: existingPolicy.effective_date ? dayjs(existingPolicy.effective_date) : null,
      maturity_date: existingPolicy.maturity_date ? dayjs(existingPolicy.maturity_date) : null,
    });
  }

  const handleSubmit = async (values: any) => {
    const data = {
      ...values,
      issue_date: values.issue_date?.format('YYYY-MM-DD'),
      effective_date: values.effective_date?.format('YYYY-MM-DD'),
      maturity_date: values.maturity_date?.format('YYYY-MM-DD'),
    };

    try {
      if (isEdit) {
        await updateMutation.mutateAsync({ id: id!, data });
        message.success('Policy updated successfully');
      } else {
        await createMutation.mutateAsync(data);
        message.success('Policy created successfully');
      }
      navigate('/policies');
    } catch (error: any) {
      message.error(error.message || 'Operation failed');
    }
  };

  return (
    <>
      <PageHeader
        title={isEdit ? 'Edit Policy' : 'New Policy'}
        subtitle={isEdit ? existingPolicy?.policy_number : 'Create a new policy record'}
        backUrl="/policies"
        breadcrumbs={[
          { title: 'Policies', path: '/policies' },
          { title: isEdit ? 'Edit' : 'New' },
        ]}
      />

      <Card loading={isEdit && loadingPolicy}>
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          initialValues={{
            status: 'active',
            premium_frequency: 'monthly',
            currency: 'USD',
          }}
        >
          <Row gutter={24}>
            <Col xs={24} md={8}>
              <Form.Item
                name="policy_number"
                label="Policy Number"
                rules={[{ required: true, message: 'Required' }]}
              >
                <Input placeholder="POL-2024-000001" disabled={isEdit} />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item
                name="product_type"
                label="Product Type"
                rules={[{ required: true, message: 'Required' }]}
              >
                <Select options={PRODUCT_TYPES} placeholder="Select product type" />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item
                name="product_code"
                label="Product Code"
                rules={[{ required: true, message: 'Required' }]}
              >
                <Input placeholder="TERM-20" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col xs={24} md={12}>
              <Form.Item name="product_name" label="Product Name">
                <Input placeholder="20-Year Term Life" />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item
                name="policyholder_id"
                label="Policyholder"
                rules={[{ required: true, message: 'Required' }]}
              >
                <Select
                  showSearch
                  placeholder="Search policyholder"
                  optionFilterProp="label"
                  options={policyholders?.items.map((ph) => ({
                    label: `${ph.first_name} ${ph.last_name}`,
                    value: ph.id,
                  }))}
                />
              </Form.Item>
            </Col>
          </Row>

          <Divider>Dates</Divider>

          <Row gutter={24}>
            <Col xs={24} md={8}>
              <Form.Item
                name="issue_date"
                label="Issue Date"
                rules={[{ required: true, message: 'Required' }]}
              >
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item
                name="effective_date"
                label="Effective Date"
                rules={[{ required: true, message: 'Required' }]}
              >
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item name="maturity_date" label="Maturity Date">
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Divider>Financial</Divider>

          <Row gutter={24}>
            <Col xs={24} md={8}>
              <Form.Item
                name="sum_assured"
                label="Sum Assured"
                rules={[{ required: true, message: 'Required' }]}
              >
                <InputNumber
                  style={{ width: '100%' }}
                  formatter={(v) => `$ ${v}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  parser={(v) => v?.replace(/\$\s?|(,*)/g, '') as any}
                  min={0}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item
                name="premium_amount"
                label="Premium Amount"
                rules={[{ required: true, message: 'Required' }]}
              >
                <InputNumber
                  style={{ width: '100%' }}
                  formatter={(v) => `$ ${v}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  parser={(v) => v?.replace(/\$\s?|(,*)/g, '') as any}
                  min={0}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={4}>
              <Form.Item name="premium_frequency" label="Frequency">
                <Select options={PREMIUM_FREQUENCIES} />
              </Form.Item>
            </Col>
            <Col xs={24} md={4}>
              <Form.Item name="currency" label="Currency">
                <Select options={CURRENCIES} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col xs={24} md={8}>
              <Form.Item name="status" label="Status">
                <Select options={POLICY_STATUSES} />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item name="risk_class" label="Risk Class">
                <Input placeholder="Standard" />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item name="branch_code" label="Branch Code">
                <Input placeholder="HQ" />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item style={{ marginTop: 24 }}>
            <Space>
              <Button
                type="primary"
                htmlType="submit"
                loading={createMutation.isPending || updateMutation.isPending}
              >
                {isEdit ? 'Update Policy' : 'Create Policy'}
              </Button>
              <Button onClick={() => navigate('/policies')}>Cancel</Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </>
  );
}
