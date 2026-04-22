import { Navigate, Outlet } from 'react-router-dom';
import { Layout, Card, Typography } from 'antd';
import { CalculatorOutlined } from '@ant-design/icons';

import { useAuthStore } from '@/stores/authStore';

const { Content } = Layout;
const { Title, Text } = Typography;

export default function AuthLayout() {
  const { isAuthenticated } = useAuthStore();

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <Layout
      style={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
      }}
    >
      <Content
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          padding: 24,
        }}
      >
        <div style={{ width: '100%', maxWidth: 400 }}>
          <div
            style={{
              textAlign: 'center',
              marginBottom: 32,
            }}
          >
            <CalculatorOutlined
              style={{ fontSize: 48, color: '#2563eb', marginBottom: 16 }}
            />
            <Title level={2} style={{ color: '#fff', margin: 0 }}>
              ActuFlow
            </Title>
            <Text style={{ color: 'rgba(255,255,255,0.65)' }}>
              Actuarial Data Management Platform
            </Text>
          </div>

          <Card>
            <Outlet />
          </Card>

          <div
            style={{
              textAlign: 'center',
              marginTop: 24,
              color: 'rgba(255,255,255,0.45)',
            }}
          >
            <Text style={{ color: 'inherit' }}>
              © 2024 ActuFlow. All rights reserved.
            </Text>
          </div>
        </div>
      </Content>
    </Layout>
  );
}
