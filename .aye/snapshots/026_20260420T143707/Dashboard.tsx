import { Row, Col, Card, Statistic, Table, Tag, Typography, Space, Button } from 'antd';
import {
  FileTextOutlined,
  TeamOutlined,
  CalculatorOutlined,
  AlertOutlined,
  CheckSquareOutlined,
  RiseOutlined,
  FallOutlined,
  ClockCircleOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';

import PageHeader from '@/components/common/PageHeader';
import StatCard from '@/components/widgets/StatCard';
import LineChart from '@/components/charts/LineChart';
import PieChart from '@/components/charts/PieChart';
import AnomalyAlertWidget from '@/components/widgets/AnomalyAlertWidget';
import { usePolicyStats } from '@/hooks/usePolicies';
import { useClaimStats } from '@/hooks/useClaims';
import { useCalculations } from '@/hooks/useCalculations';
import { formatCurrency, formatDate, formatStatus } from '@/utils/formatters';
import { STATUS_COLORS } from '@/utils/constants';

const { Title, Text } = Typography;

export default function Dashboard() {
  const navigate = useNavigate();
  const { data: policyStats, isLoading: loadingPolicies } = usePolicyStats();
  const { data: claimStats, isLoading: loadingClaims } = useClaimStats();
  const { data: calculations, isLoading: loadingCalcs } = useCalculations({ page_size: 5 });

  // Mock data for charts
  const premiumTrend = [
    { month: 'Jan', premium: 1200000, claims: 450000 },
    { month: 'Feb', premium: 1350000, claims: 520000 },
    { month: 'Mar', premium: 1280000, claims: 380000 },
    { month: 'Apr', premium: 1420000, claims: 610000 },
    { month: 'May', premium: 1380000, claims: 490000 },
    { month: 'Jun', premium: 1510000, claims: 420000 },
  ];

  const productMix = policyStats?.by_product_type
    ? Object.entries(policyStats.by_product_type).map(([name, value]) => ({ name, value }))
    : [
        { name: 'Term Life', value: 45 },
        { name: 'Whole Life', value: 30 },
        { name: 'Universal Life', value: 15 },
        { name: 'Endowment', value: 10 },
      ];

  // Mock anomaly alerts
  const anomalyAlerts = [
    {
      id: '1',
      record_type: 'claim',
      record_id: 'claim-123',
      score: 0.85,
      reasons: ['Claim amount significantly higher than policy average', 'Multiple claims in short period'],
      detected_at: new Date().toISOString(),
    },
    {
      id: '2',
      record_type: 'calculation_result',
      record_id: 'calc-456',
      score: 0.72,
      reasons: ['Reserve movement outside expected range'],
      detected_at: new Date(Date.now() - 3600000).toISOString(),
    },
  ];

  const recentCalcColumns = [
    {
      title: 'Run Name',
      dataIndex: 'run_name',
      key: 'name',
      render: (text: string, record: any) => (
        <a onClick={() => navigate(`/calculations/${record.id}`)}>{text}</a>
      ),
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={STATUS_COLORS[status]}>{formatStatus(status)}</Tag>
      ),
    },
    {
      title: 'Policies',
      dataIndex: 'policies_count',
      key: 'policies',
      render: (v: number) => v?.toLocaleString() || '-',
    },
    {
      title: 'Date',
      dataIndex: 'created_at',
      key: 'date',
      render: formatDate,
    },
  ];

  return (
    <>
      <PageHeader
        title="Dashboard"
        subtitle="Overview of your actuarial operations"
        extra={
          <Space>
            <Button onClick={() => navigate('/calculations/new')} type="primary">
              New Calculation
            </Button>
          </Space>
        }
      />

      {/* Key Metrics */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <StatCard
            title="Active Policies"
            value={policyStats?.active_policies?.toLocaleString() || '0'}
            change={5.2}
            changeType="increase"
            icon={<FileTextOutlined />}
            color="#2563eb"
            loading={loadingPolicies}
          />
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <StatCard
            title="Total Premium"
            value={formatCurrency(policyStats?.total_premium || 0)}
            change={3.8}
            changeType="increase"
            icon={<RiseOutlined />}
            color="#16a34a"
            loading={loadingPolicies}
          />
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <StatCard
            title="Open Claims"
            value={claimStats?.open_claims?.toString() || '0'}
            change={-2.1}
            changeType="decrease"
            icon={<AlertOutlined />}
            color="#ca8a04"
            loading={loadingClaims}
          />
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <StatCard
            title="Pending Tasks"
            value="12"
            icon={<CheckSquareOutlined />}
            color="#9333ea"
          />
        </Col>
      </Row>

      {/* Charts Row */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} lg={16}>
          <Card title="Premium vs Claims Trend">
            <LineChart
              data={premiumTrend}
              xDataKey="month"
              lines={[
                { dataKey: 'premium', name: 'Premium', color: '#2563eb' },
                { dataKey: 'claims', name: 'Claims', color: '#dc2626' },
              ]}
              height={300}
            />
          </Card>
        </Col>
        <Col xs={24} lg={8}>
          <Card title="Product Mix">
            <PieChart data={productMix} height={300} innerRadius={50} />
          </Card>
        </Col>
      </Row>

      {/* Bottom Row */}
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={14}>
          <Card
            title="Recent Calculations"
            extra={<a onClick={() => navigate('/calculations')}>View All</a>}
          >
            <Table
              dataSource={calculations?.items || []}
              columns={recentCalcColumns}
              rowKey="id"
              pagination={false}
              loading={loadingCalcs}
              size="small"
            />
          </Card>
        </Col>
        <Col xs={24} lg={10}>
          <AnomalyAlertWidget alerts={anomalyAlerts} />
        </Col>
      </Row>
    </>
  );
}
