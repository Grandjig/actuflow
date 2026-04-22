/**
 * Main dashboard page.
 */

import { Row, Col, Card, Statistic, Typography } from 'antd';
import {
  FileTextOutlined,
  TeamOutlined,
  CalculatorOutlined,
  AlertOutlined,
} from '@ant-design/icons';
import { useQuery } from '@tanstack/react-query';
import { getPolicyStats } from '@/api/policies';
import { getClaimStats } from '@/api/claims';
import RecentCalculationsWidget from '@/components/widgets/RecentCalculationsWidget';
import ScheduledJobsWidget from '@/components/widgets/ScheduledJobsWidget';

const { Title } = Typography;

interface PolicyStats {
  active_count?: number;
  policyholder_count?: number;
  calculations_this_month?: number;
}

interface ClaimStats {
  open_count?: number;
}

export default function Dashboard() {
  const { data: policyStats } = useQuery<PolicyStats>({
    queryKey: ['policyStats'],
    queryFn: getPolicyStats,
  });

  const { data: claimStats } = useQuery<ClaimStats>({
    queryKey: ['claimStats'],
    queryFn: getClaimStats,
  });

  return (
    <div>
      <Title level={2}>Dashboard</Title>

      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Active Policies"
              value={policyStats?.active_count ?? 0}
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Total Policyholders"
              value={policyStats?.policyholder_count ?? 0}
              prefix={<TeamOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Open Claims"
              value={claimStats?.open_count ?? 0}
              prefix={<AlertOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Calculations This Month"
              value={policyStats?.calculations_this_month ?? 0}
              prefix={<CalculatorOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={24} lg={12}>
          <RecentCalculationsWidget />
        </Col>
        <Col xs={24} lg={12}>
          <ScheduledJobsWidget />
        </Col>
      </Row>
    </div>
  );
}
