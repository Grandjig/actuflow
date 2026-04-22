/**
 * Profile settings page.
 */

import {
  Card,
  Form,
  Input,
  Button,
  Typography,
  Divider,
  Switch,
  message,
  Spin,
} from 'antd';
import { useAuth } from '@/hooks/useAuth';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { updateProfile } from '@/api/users';

const { Title } = Typography;

interface ProfileFormValues {
  full_name: string;
  email: string;
  department?: string;
  job_title?: string;
}

export default function ProfileSettings() {
  const { user, isLoading } = useAuth();
  const queryClient = useQueryClient();
  const [form] = Form.useForm<ProfileFormValues>();

  const mutation = useMutation({
    mutationFn: updateProfile,
    onSuccess: () => {
      message.success('Profile updated successfully');
      queryClient.invalidateQueries({ queryKey: ['currentUser'] });
    },
    onError: () => {
      message.error('Failed to update profile');
    },
  });

  if (isLoading || !user) {
    return (
      <div style={{ textAlign: 'center', padding: 100 }}>
        <Spin size="large" />
      </div>
    );
  }

  const handleSubmit = (values: ProfileFormValues) => {
    mutation.mutate(values);
  };

  return (
    <div style={{ maxWidth: 600 }}>
      <Title level={2}>Profile Settings</Title>

      <Card>
        <Form
          form={form}
          layout="vertical"
          initialValues={{
            full_name: user.full_name,
            email: user.email,
            department: user.department,
            job_title: user.job_title,
          }}
          onFinish={handleSubmit}
        >
          <Form.Item
            name="full_name"
            label="Full Name"
            rules={[{ required: true, message: 'Please enter your name' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            name="email"
            label="Email"
            rules={[
              { required: true, message: 'Please enter your email' },
              { type: 'email', message: 'Please enter a valid email' },
            ]}
          >
            <Input disabled />
          </Form.Item>

          <Form.Item name="department" label="Department">
            <Input />
          </Form.Item>

          <Form.Item name="job_title" label="Job Title">
            <Input />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={mutation.isPending}
            >
              Save Changes
            </Button>
          </Form.Item>
        </Form>

        <Divider />

        <Title level={4}>AI Preferences</Title>
        <Form layout="vertical">
          <Form.Item
            label="Enable AI features"
            extra="Allow AI-powered suggestions and assistance"
          >
            <Switch
              defaultChecked={user.ai_preferences?.enabled !== false}
            />
          </Form.Item>

          <Form.Item
            label="Natural language queries"
            extra="Use plain English to search and filter data"
          >
            <Switch
              defaultChecked={user.ai_preferences?.natural_language !== false}
            />
          </Form.Item>

          <Form.Item
            label="AI-generated summaries"
            extra="Auto-generate narrative summaries for reports"
          >
            <Switch
              defaultChecked={user.ai_preferences?.summaries !== false}
            />
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
}
