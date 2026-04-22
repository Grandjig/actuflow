import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Layout, Typography, Card, Space, Button } from 'antd'
import { CheckCircleOutlined } from '@ant-design/icons'

const { Content } = Layout
const { Title, Text } = Typography

const queryClient = new QueryClient()

function HomePage() {
  return (
    <Layout style={{ minHeight: '100vh', background: '#f5f5f5' }}>
      <Content style={{ padding: 50 }}>
        <Card style={{ maxWidth: 600, margin: '100px auto' }}>
          <Space direction="vertical" size="large" style={{ width: '100%', textAlign: 'center' }}>
            <CheckCircleOutlined style={{ fontSize: 64, color: '#52c41a' }} />
            <Title level={2}>ActuFlow is Running!</Title>
            <Text type="secondary">
              Your insurance data management platform is ready.
            </Text>
            <Space>
              <Button type="primary" href="http://localhost:8000/docs" target="_blank">
                API Documentation
              </Button>
              <Button href="http://localhost:8000/health" target="_blank">
                Health Check
              </Button>
            </Space>
          </Space>
        </Card>
      </Content>
    </Layout>
  )
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="*" element={<HomePage />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
