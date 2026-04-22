import { Row, Col, Card, Typography } from 'antd';
import {
  FileTextOutlined,
  TeamOutlined,
  CalculatorOutlined,
  DollarOutlined,
} from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';
import StatCard from '@/components/widgets/StatCard';
import RecentCalculationsWidget from '@/components/widgets/RecentCalculationsWidget';
import AnomalyAlertWidget from '@/components/widgets/AnomalyAlertWidget';
import ScheduledJobsWidget from '@/components/widgets/ScheduledJobsWidget';
import LineChart from '@/components/charts/LineChart';
import PieChart from '@/components/charts/PieChart';
import { usePolicyStats } from '@/hooks/usePolicies';
import { formatCurrency, formatNumber } from '@/utils/formatters';

export default function Dashboard() {
  const { data: policyStats, isLoading: statsLoading } = usePolicyStats();

  // Mock data for charts - in real app, this comes from API
  const reserveTrendData = [
    { month: 'Jan', reserves: 12500000, premium: 2100000 },
    { month: 'Feb', reserves: 12800000, premium: 2150000 },
    { month: 'Mar', reserves: 13100000, premium: 2200000 },
    { month: 'Apr', reserves: 12900000, premium: 2180000 },
    { month: 'May', reserves: 13400000, premium: 2250000 },
    { month: 'Jun', reserves: 13800000, premium: 2300000 },
  ];

  const policyStatusData = [
    { name: 'Active', value: policyStats?.active_count || 8500 },
    { name: 'Lapsed', value: 450 },
    { name: 'Surrendered', value: 230 },
    { name: 'Matured', value: 180 },
    { name: 'Claimed', value: 95 },
  ];

  // Mock anomaly data - in real app, this comes from AI service
  const anomalyAlerts = [
    {
      record_id: 'claim-001',
      record_type: 'claim',
      score: 0.87,
      reasons: ['Unusually high claim amount', 'Filed within 30 days of policy issue'],
      detected_at: new Date().toISOString(),
    },
    {
      record_id: 'calc-result-002',
      record_type: 'calculation_result',
      score: 0.72,
      reasons: ['Reserve 35% higher than expected'],
      detected_at: new Date(Date.now() - 3600000).toISOString(),
    },
  ];

  // Mock scheduled jobs - in real app, this comes from API
  const scheduledJobs = [
    {
      id: 'job-1',
      name: 'Monthly Reserve Calculation',
      job_type: 'calculation',
      cron_expression: '0 2 1 * *',
      is_active: true,
      next_run: new Date(Date.now() + 86400000 * 5).toISOString(),
      last_run: new Date(Date.now() - 86400000 * 25).toISOString(),
      last_run_status: 'completed',
      config: {},
      created_at: '',
    },
    {
      id: 'job-2',
      name: 'Weekly Report Generation',
      job_type: 'report',
      cron_expression: '0 8 * * 1',
      is_active: true,
      next_run: new Date(Date.now() + 86400000 * 2).toISOString(),
      last_run: new Date(Date.now() - 86400000 * 5).toISOString(),
      last_run_status: 'completed',
      config: {},
      created_at: '',
    },
  ];

  return (
    <div>
      <PageHeader
        title="Dashboard"
        subtitle="Welcome back! Here's what's happening with your portfolio."
      />

      {/* Stats Row */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <StatCard
            title="Total Policies"
            value={formatNumber(policyStats?.total_count || 9455)}
            change={3.2}
            changeType="increase"
            icon={<FileTextOutlined />}
            color="#2563eb"
            loading={statsLoading}
          />
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <StatCard
            title="Active Policies"
            value={formatNumber(policyStats?.active_count || 8500)}
            change={1.8}
            changeType="increase"
            icon={<TeamOutlined />}
            color="#16a34a"
            loading={statsLoading}
          />
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <StatCard
            title="Total Sum Assured"
            value={formatCurrency(policyStats?.total_sum_assured || 2500000000, 'USD', 0)}
            change={5.4}
            changeType="increase"
            icon={<DollarOutlined />}
            color="#ca8a04"
            loading={statsLoading}
          />
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <StatCard
            title="Annual Premium"
            value={formatCurrency(policyStats?.total_premium || 45000000, 'USD', 0)}
            change={2.1}
            changeType="increase"
            icon={<CalculatorOutlined />}
            color="#9333ea"
            loading={statsLoading}
          />
        </Col>
      </Row>

      {/* Charts Row */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} lg={16}>
          <Card title="Reserve & Premium Trend">
            <LineChart
              data={reserveTrendData}
              xDataKey="month"
              lines={[
                { dataKey: 'reserves', name: 'Reserves', color: '#2563eb' },
                { dataKey: 'premium', name: 'Premium', color: '#16a34a' },
              ]}
              height={300}
            />
          </Card>
        </Col>
        <Col xs={24} lg={8}>
          <Card title="Policy Status Distribution">
            <PieChart data={policyStatusData} height={300} innerRadius={50} />
          </Card>
        </Col>
      </Row>

      {/* Widgets Row */}
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={8}>
          <RecentCalculationsWidget />
        </Col>
        <Col xs={24} lg={8}>
          <AnomalyAlertWidget alerts={anomalyAlerts} />
        </Col>
        <Col xs={24} lg={8}>
          <ScheduledJobsWidget jobs={scheduledJobs} />
        </Col>
      </Row>
    </div>
  );
}
