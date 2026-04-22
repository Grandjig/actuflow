import { Form, Input, Button, Space, message, Divider } from 'antd';
import { useAuthStore } from '@/stores/authStore';

export default function ProfileSettings() {
  const { user } = useAuthStore();
  const [form] = Form.useForm();

  const handleSubmit = async (values: any) => {
    // TODO: Implement profile update
    message.success('Profile updated successfully');
  };

  return (
    <div style={{ maxWidth: 600 }}>
      <h3>Profile Information</h3>
      <p style={{ color: '#666', marginBottom: 24 }}>
        Update your personal information and contact details.
      </p>

      <Form
        form={form}
        layout="vertical"
        initialValues={{
          email: user?.email,
          full_name: user?.full_name,
          department: user?.department,
          job_title: user?.job_title,
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
          <Button type="primary" htmlType="submit">
            Save Changes
          </Button>
        </Form.Item>
      </Form>

      <Divider />

      <h3>Change Password</h3>
      <Form layout="vertical">
        <Form.Item name="current_password" label="Current Password">
          <Input.Password />
        </Form.Item>
        <Form.Item name="new_password" label="New Password">
          <Input.Password />
        </Form.Item>
        <Form.Item name="confirm_password" label="Confirm Password">
          <Input.Password />
        </Form.Item>
        <Form.Item>
          <Button>Change Password</Button>
        </Form.Item>
      </Form>
    </div>
  );
}
