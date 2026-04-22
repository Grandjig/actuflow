import { Outlet } from 'react-router-dom';
import { Layout, Typography } from 'antd';

const { Content } = Layout;
const { Title } = Typography;

export default function AuthLayout() {
  return (
    <Layout style={{ minHeight: '100vh', background: '#f0f2f5' }}>
      <Content
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: 24,
        }}
      >
        <div style={{ marginBottom: 32, textAlign: 'center' }}>
          <Title level={1} style={{ margin: 0, color: '#1890ff' }}>
            ActuFlow
          </Title>
          <p style={{ color: '#666', marginTop: 8 }}>
            Actuarial Data Management & Analysis Platform
          </p>
        </div>
        <Outlet />
      </Content>
    </Layout>
  );
}
