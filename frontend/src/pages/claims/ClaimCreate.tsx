import { useNavigate } from 'react-router-dom';
import { Card, Form, Input, Select, DatePicker, InputNumber, Button, Space, message } from 'antd';
import PageHeader from '@/components/common/PageHeader';
import { useCreateClaim } from '@/hooks/useClaims';

export default function ClaimCreate() {
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const mutation = useCreateClaim();

  const handleSubmit = async (values: any) => {
    try {
      await mutation.mutateAsync({
        ...values,
        claim_date: values.claim_date?.format('YYYY-MM-DD'),
        incident_date: values.incident_date?.format('YYYY-MM-DD'),
      });
      message.success('Claim created');
      navigate('/claims');
    } catch (e: any) {
      message.error(e.message || 'Failed');
    }
  };

  return (
    <>
      <PageHeader title="New Claim" backUrl="/claims" />
      <Card>
        <Form form={form} layout="vertical" onFinish={handleSubmit} style={{ maxWidth: 600 }}>
          <Form.Item name="policy_id" label="Policy ID" rules={[{ required: true }]}>
            <Input placeholder="Policy UUID" />
          </Form.Item>
          <Form.Item name="claim_type" label="Claim Type" rules={[{ required: true }]}>
            <Select options={[
              { label: 'Death', value: 'death' },
              { label: 'Disability', value: 'disability' },
              { label: 'Critical Illness', value: 'critical_illness' },
              { label: 'Hospitalization', value: 'hospitalization' },
            ]} />
          </Form.Item>
          <Form.Item name="claim_date" label="Claim Date" rules={[{ required: true }]}>
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="incident_date" label="Incident Date">
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="claimed_amount" label="Claimed Amount" rules={[{ required: true }]}>
            <InputNumber style={{ width: '100%' }} min={0} prefix="$" />
          </Form.Item>
          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit" loading={mutation.isPending}>Create</Button>
              <Button onClick={() => navigate('/claims')}>Cancel</Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </>
  );
}
