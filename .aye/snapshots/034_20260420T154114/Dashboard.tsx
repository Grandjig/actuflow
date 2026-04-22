import { Row, Col, Card, Statistic, Typography, Space, Button, List, Tag } from 'antd';
import {
  FileTextOutlined,
  CalculatorOutlined,
  AlertOutlined,
  ClockCircleOutlined,
  RiseOutlined,
  FallOutlined,
  RobotOutlined,
  CheckCircleOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';

import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';
import PieChart from '@/components/charts/PieChart';
import LineChart from '@/components/charts/LineChart';
import { usePolicyStats } from '@/hooks/usePolicies';
import { useClaimStats, useClaimAnomalies } from '@/hooks/useClaims';
import { useCalculations } from '@/hooks/useCalculations';
import { useAuthStore } from '@/stores/authStore';
import { formatCurrency, formatCompact, formatRelativeTime } from '@/utils/formatters';

const { Text, Title } = Typography;

export default function Dashboard() {
  const navigate = useNavigate();
  const { user } = useAuthStore();

  const { data: policyStats } = usePolicyStats();
  const { data: claimStats } = useClaimStats();
  const { data: anomalies } = useClaimAnomalies(5);
  const { data: recentCalculations } = useCalculations({ page: 1, page_size: 5 });

  // Mock trend data
  const trendData = [
    { month: 'Jan', reserves: 125000000, premiums: 15000000 },
    { month: 'Feb', reserves: 128000000, premiums: 15500000 },
    { month: 'Mar', reserves: 132000000, premiums: 16000000 },
    { month: 'Apr', reserves: 130000000, premiums: 15800000 },
    { month: 'May', reserves: 135000000, premiums: 16200000 },
    { month: 'Jun', reserves: 140000000, premiums: 16800000 },
  ];

  const policyByStatus = policyStats?.by_status
    ? Object.entries(policyStats.by_status).map(([name, value]) => ({ name, value }))
    : [];

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
              value={policyStats?.active_policies || 0}
              prefix={<FileTextOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
            <div style={{ marginTop: 8 }}>
              <Text type="secondary">
                {formatCompact(policyStats?.total_policies || 0)} total
              </Text>
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card hoverable onClick={() => navigate('/calculations')}>
            <Statistic
              title="Total Premium"
              value={policyStats?.total_premium || 0}
              prefix="$"
              formatter={(v) => formatCompact(Number(v))}
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
              value={claimStats?.open_claims || 0}
              prefix={<AlertOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
            <div style={{ marginTop: 8 }}>
              <Text type="secondary">
                {formatCurrency(claimStats?.total_claimed || 0)} pending
              </Text>
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Claims Ratio"
              value={claimStats?.total_claimed && claimStats?.total_settled
                ? ((claimStats.total_settled / claimStats.total_claimed) * 100).toFixed(1)
                : 0
              }
              suffix="%"
              prefix={<CalculatorOutlined />}
              valueStyle={{ color: '#722ed1' }}
            />
            <div style={{ marginTop: 8 }}>
              <Text type="secondary">Settlement rate</Text>
            </div>
          </Card>
        </Col>
      </Row>

      {/* Charts Row */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} lg={16}>
          <Card title="Reserve & Premium Trends">
            <LineChart
              data={trendData}
              xDataKey="month"
              lines={[
                { dataKey: 'reserves', name: 'Reserves', color: '#1890ff' },
                { dataKey: 'premiums', name: 'Premiums', color: '#52c41a' },
              ]}
              height={300}
            />
          </Card>
        </Col>
        <Col xs={24} lg={8}>
          <Card title="Policies by Status">
            <PieChart
              data={policyByStatus}
              height={300}
              innerRadius={60}
            />
          </Card>
        </Col>
      </Row>

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
              dataSource={recentCalculations?.items || []}
              renderItem={(calc) => (
                <List.Item
                  style={{ cursor: 'pointer' }}
                  onClick={() => navigate(`/calculations/${calc.id}`)}
                >
                  <List.Item.Meta
                    avatar={<CalculatorOutlined style={{ fontSize: 20, color: '#1890ff' }} />}
                    title={calc.run_name}
                    description={formatRelativeTime(calc.created_at)}
                  />
                  <StatusBadge status={calc.status} />
                </List.Item>
              )}
              locale={{ emptyText: 'No recent calculations' }}
            />
          </Card>
        </Col>

        <Col xs={24} lg={12}>
          <Card
            title={
              <Space>
                <RobotOutlined />
                AI Anomaly Alerts
              </Space>
            }
            extra={
              <Button type="link" onClick={() => navigate('/claims?anomaly_only=true')}>
                View All
              </Button>
            }
          >
            {anomalies && anomalies.length > 0 ? (
              <List
                dataSource={anomalies}
                renderItem={(claim: any) => (
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
