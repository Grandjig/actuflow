import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Card, Form, Input, Button, Alert, Checkbox } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { useAuthStore } from '@/stores/authStore';

interface LoginForm {
  email: string;
  password: string;
  remember: boolean;
}

export default function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, isLoading, error } = useAuthStore();
  const [form] = Form.useForm();

  const from = (location.state as any)?.from?.pathname || '/';

  const handleSubmit = async (values: LoginForm) => {
    try {
      await login(values.email, values.password);
      navigate(from, { replace: true });
    } catch (err) {
      // Error is handled in the store
    }
  };

  return (
    <Card style={{ width: 400, boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        initialValues={{
          email: 'admin@actuflow.com',
          password: 'admin123',
          remember: true,
        }}
      >
        {error && (
          <Alert
            message={error}
            type="error"
            showIcon
            style={{ marginBottom: 24 }}
          />
        )}

        <Form.Item
          name="email"
          label="Email"
          rules={[
            { required: true, message: 'Please enter your email' },
            { type: 'email', message: 'Please enter a valid email' },
          ]}
        >
          <Input prefix={<UserOutlined />} placeholder="Email" size="large" />
        </Form.Item>

        <Form.Item
          name="password"
          label="Password"
          rules={[{ required: true, message: 'Please enter your password' }]}
        >
          <Input.Password
            prefix={<LockOutlined />}
            placeholder="Password"
            size="large"
          />
        </Form.Item>

        <Form.Item name="remember" valuePropName="checked">
          <Checkbox>Remember me</Checkbox>
        </Form.Item>

        <Form.Item>
          <Button
            type="primary"
            htmlType="submit"
            loading={isLoading}
            block
            size="large"
          >
            Sign In
          </Button>
        </Form.Item>

        <div style={{ textAlign: 'center', color: '#666', fontSize: 12 }}>
          Demo credentials: admin@actuflow.com / admin123
        </div>
      </Form>
    </Card>
  );
}
