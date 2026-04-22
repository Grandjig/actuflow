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
  POLICY_STATUSES,
  PRODUCT_TYPES,
  PREMIUM_FREQUENCIES,
  CURRENCIES,
} from '@/utils/constants';

export default function PolicyCreate() {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const isEdit = Boolean(id);
  const [form] = Form.useForm();

  const { data: policy, isLoading: loadingPolicy } = usePolicy(id || '');
  const { data: policyholders } = usePolicyholders({ page_size: 100 });
  const createMutation = useCreatePolicy();
  const updateMutation = useUpdatePolicy();

  // Set form values when editing
  if (isEdit && policy && !form.getFieldValue('policy_number')) {
    form.setFieldsValue({
      ...policy,
      issue_date: policy.issue_date ? dayjs(policy.issue_date) : undefined,
      effective_date: policy.effective_date ? dayjs(policy.effective_date) : undefined,
      maturity_date: policy.maturity_date ? dayjs(policy.maturity_date) : undefined,
    });
  }

  const handleSubmit = async (values: any) => {
    const formattedValues = {
      ...values,
      issue_date: values.issue_date?.format('YYYY-MM-DD'),
      effective_date: values.effective_date?.format('YYYY-MM-DD'),
      maturity_date: values.maturity_date?.format('YYYY-MM-DD'),
    };

    try {
      if (isEdit) {
        await updateMutation.mutateAsync({ id: id!, data: formattedValues });
        message.success('Policy updated successfully');
      } else {
        const result = await createMutation.mutateAsync(formattedValues);
        message.success('Policy created successfully');
        navigate(`/policies/${result.id}`);
        return;
      }
      navigate(`/policies/${id}`);
    } catch (error: any) {
      message.error(error.message || 'Failed to save policy');
    }
  };

  const policyholderOptions = policyholders?.items?.map((ph) => ({
    value: ph.id,
    label: `${ph.full_name} (${ph.external_id || ph.id.slice(0, 8)})`,
  })) || [];

  return (
    <>
      <PageHeader
        title={isEdit ? 'Edit Policy' : 'New Policy'}
        backUrl={isEdit ? `/policies/${id}` : '/policies'}
        breadcrumbs={[
          { title: 'Policies', path: '/policies' },
          { title: isEdit ? 'Edit' : 'New Policy' },
        ]}
      />

      <Card loading={isEdit && loadingPolicy}>
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          initialValues={{
            currency: 'USD',
            premium_frequency: 'monthly',
            status: 'active',
          }}
        >
          <Row gutter={24}>
            <Col xs={24} md={8}>
              <Form.Item
                name="policy_number"
                label="Policy Number"
                rules={[{ required: true, message: 'Required' }]}
              >
                <Input placeholder="POL-000001" disabled={isEdit} />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item
                name="policyholder_id"
                label="Policyholder"
                rules={[{ required: true, message: 'Required' }]}
              >
                <Select
                  showSearch
                  placeholder="Select policyholder"
                  options={policyholderOptions}
                  filterOption={(input, option) =>
                    (option?.label as string)?.toLowerCase().includes(input.toLowerCase())
                  }
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item name="status" label="Status">
                <Select options={POLICY_STATUSES} />
              </Form.Item>
            </Col>
          </Row>

          <Divider>Product Details</Divider>

          <Row gutter={24}>
            <Col xs={24} md={8}>
              <Form.Item
                name="product_type"
                label="Product Type"
                rules={[{ required: true, message: 'Required' }]}
              >
                <Select options={PRODUCT_TYPES} />
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
            <Col xs={24} md={8}>
              <Form.Item name="product_name" label="Product Name">
                <Input placeholder="20-Year Term Life" />
              </Form.Item>
            </Col>
          </Row>

          <Divider>Financial Details</Divider>

          <Row gutter={24}>
            <Col xs={24} md={6}>
              <Form.Item
                name="sum_assured"
                label="Sum Assured"
                rules={[{ required: true, message: 'Required' }]}
              >
                <InputNumber
                  style={{ width: '100%' }}
                  min={0}
                  formatter={(value) => `${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  parser={(value) => value!.replace(/,/g, '') as any}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
              <Form.Item
                name="premium_amount"
                label="Premium Amount"
                rules={[{ required: true, message: 'Required' }]}
              >
                <InputNumber
                  style={{ width: '100%' }}
                  min={0}
                  formatter={(value) => `${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  parser={(value) => value!.replace(/,/g, '') as any}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
              <Form.Item name="premium_frequency" label="Premium Frequency">
                <Select options={PREMIUM_FREQUENCIES} />
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
              <Form.Item name="currency" label="Currency">
                <Select options={CURRENCIES} />
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

          <Form.Item style={{ marginTop: 24 }}>
            <Space>
              <Button
                type="primary"
                htmlType="submit"
                loading={createMutation.isPending || updateMutation.isPending}
              >
                {isEdit ? 'Update Policy' : 'Create Policy'}
              </Button>
              <Button onClick={() => navigate(isEdit ? `/policies/${id}` : '/policies')}>
                Cancel
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </>
  );
}
