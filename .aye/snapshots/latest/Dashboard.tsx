import { Row, Col, Card, Statistic, Typography, Space, Button, List, Tag, Empty } from 'antd';
import {
  FileTextOutlined,
  CalculatorOutlined,
  AlertOutlined,
  TeamOutlined,
  RiseOutlined,
  RobotOutlined,
  CheckCircleOutlined,
  SettingOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';

import PageHeader from '@/components/common/PageHeader';
import { useAuthStore } from '@/stores/authStore';
import { formatCurrency } from '@/utils/formatters';

const { Text } = Typography;

// Mock data for demo - replace with real API calls later
const mockStats = {
  activePolicies: 1234,
  totalPremium: 15600000,
  openClaims: 45,
  policyholders: 892,
};

const mockRecentCalculations = [
  { id: '1', run_name: 'Monthly Valuation - April 2026', status: 'completed', created_at: '2026-04-15' },
  { id: '2', run_name: 'Quarterly Reserve - Q1 2026', status: 'completed', created_at: '2026-04-01' },
  { id: '3', run_name: 'Ad-hoc Analysis', status: 'running', created_at: '2026-04-20' },
];

const mockAnomalies = [
  { id: '1', claim_number: 'CLM-2024-000015', anomaly_score: 0.89, claimed_amount: 450000 },
  { id: '2', claim_number: 'CLM-2024-000023', anomaly_score: 0.72, claimed_amount: 125000 },
];

export default function Dashboard() {
  const navigate = useNavigate();
  const { user } = useAuthStore();

  return (
    <>
      <PageHeader
        title={`Welcome back, ${user?.full_name?.split(' ')[0] || 'User'}`}
        subtitle="Here's what's happening with your actuarial operations"
      />

      {/* Key Metrics Row */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card hoverable onClick={() => navigate('/policies')}>
            <Statistic
              title="Active Policies"
              value={mockStats.activePolicies}
              prefix={<FileTextOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
            <div style={{ marginTop: 8 }}>
              <Text type="secondary">Click to manage policies</Text>
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card hoverable onClick={() => navigate('/calculations')}>
            <Statistic
              title="Total Premium"
              value={mockStats.totalPremium}
              prefix="$"
              formatter={(v) => Number(v).toLocaleString()}
              valueStyle={{ color: '#52c41a' }}
            />
            <div style={{ marginTop: 8 }}>
              <RiseOutlined style={{ color: '#52c41a' }} />
              <Text type="secondary"> +4.2% vs last month</Text>
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card hoverable onClick={() => navigate('/claims')}>
            <Statistic
              title="Open Claims"
              value={mockStats.openClaims}
              prefix={<AlertOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
            <div style={{ marginTop: 8 }}>
              <Text type="secondary">Requires attention</Text>
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card hoverable onClick={() => navigate('/policyholders')}>
            <Statistic
              title="Policyholders"
              value={mockStats.policyholders}
              prefix={<TeamOutlined />}
              valueStyle={{ color: '#722ed1' }}
            />
            <div style={{ marginTop: 8 }}>
              <Text type="secondary">Total customers</Text>
            </div>
          </Card>
        </Col>
      </Row>

      {/* Quick Actions */}
      <Card title="Quick Actions" style={{ marginBottom: 24 }}>
        <Space wrap>
          <Button type="primary" icon={<CalculatorOutlined />} onClick={() => navigate('/calculations/new')}>
            New Calculation
          </Button>
          <Button icon={<FileTextOutlined />} onClick={() => navigate('/policies/new')}>
            Add Policy
          </Button>
          <Button icon={<AlertOutlined />} onClick={() => navigate('/claims/new')}>
            File Claim
          </Button>
          <Button icon={<SettingOutlined />} onClick={() => navigate('/assumptions')}>
            Manage Assumptions
          </Button>
        </Space>
      </Card>

      {/* Activity Row */}
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <Card
            title={
              <Space>
                <CalculatorOutlined />
                Recent Calculations
              </Space>
            }
            extra={
              <Button type="link" onClick={() => navigate('/calculations')}>
                View All
              </Button>
            }
          >
            <List
              dataSource={mockRecentCalculations}
              renderItem={(calc) => (
                <List.Item
                  style={{ cursor: 'pointer' }}
                  onClick={() => navigate(`/calculations/${calc.id}`)}
                >
                  <List.Item.Meta
                    avatar={<CalculatorOutlined style={{ fontSize: 20, color: '#1890ff' }} />}
                    title={calc.run_name}
                    description={calc.created_at}
                  />
                  <Tag color={calc.status === 'completed' ? 'green' : 'processing'}>
                    {calc.status}
                  </Tag>
                </List.Item>
              )}
            />
          </Card>
        </Col>

        <Col xs={24} lg={12}>
          <Card
            title={
              <Space>
                <RobotOutlined />
                AI Anomaly Alerts
                <Tag color="purple" style={{ fontSize: 10 }}>AI</Tag>
              </Space>
            }
            extra={
              <Button type="link" onClick={() => navigate('/claims')}>
                View All
              </Button>
            }
          >
            {mockAnomalies.length > 0 ? (
              <List
                dataSource={mockAnomalies}
                renderItem={(claim) => (
                  <List.Item
                    style={{ cursor: 'pointer' }}
                    onClick={() => navigate(`/claims/${claim.id}`)}
                  >
                    <List.Item.Meta
                      avatar={<AlertOutlined style={{ fontSize: 20, color: '#ff4d4f' }} />}
                      title={claim.claim_number}
                      description={`Risk score: ${(claim.anomaly_score * 100).toFixed(0)}%`}
                    />
                    <Tag color="red">{formatCurrency(claim.claimed_amount)}</Tag>
                  </List.Item>
                )}
              />
            ) : (
              <div style={{ textAlign: 'center', padding: 40, color: '#999' }}>
                <CheckCircleOutlined style={{ fontSize: 32, marginBottom: 8 }} />
                <div>No anomalies detected</div>
              </div>
            )}
          </Card>
        </Col>
      </Row>
    </>
  );
}
