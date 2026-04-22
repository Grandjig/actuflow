import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Descriptions,
  Tag,
  Button,
  Space,
  Tabs,
  Progress,
  Spin,
  Row,
  Col,
  Statistic,
} from 'antd';
import {
  DownloadOutlined,
  ReloadOutlined,
  StopOutlined,
  WarningOutlined,
} from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';
import EmptyState from '@/components/common/EmptyState';
import NarrativeSummary from '@/components/ai/NarrativeSummary';
import AnomalyAlertWidget from '@/components/widgets/AnomalyAlertWidget';
import LineChart from '@/components/charts/LineChart';
import {
  useCalculation,
  useCalculationProgress,
  useCalculationSummary,
  useCalculationAnomalies,
  useCancelCalculation,
} from '@/hooks/useCalculations';
import { formatDate, formatDuration, formatCurrency, formatNumber } from '@/utils/formatters';

export default function CalculationDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: calculation, isLoading, error } = useCalculation(id!);
  const { data: progress } = useCalculationProgress(
    id!,
    calculation?.status === 'running' || calculation?.status === 'queued'
  );
  const { data: summary } = useCalculationSummary(id!);
  const { data: anomalies } = useCalculationAnomalies(id!);
  const cancelCalculation = useCancelCalculation();

  if (isLoading) {
    return (
      <div style={{ padding: 100, textAlign: 'center' }}>
        <Spin size="large" />
      </div>
    );
  }

  if (error || !calculation) {
    return (
      <EmptyState
        title="Calculation Not Found"
        description="The calculation run you're looking for doesn't exist."
        action={{ label: 'Back to Calculations', onClick: () => navigate('/calculations') }}
      />
    );
  }

  const isRunning = calculation.status === 'running' || calculation.status === 'queued';

  // Mock cashflow data for chart
  const cashflowData = Array.from({ length: 24 }, (_, i) => ({
    month: i + 1,
    premium: Math.max(0, 100000 - i * 2000 + Math.random() * 10000),
    claims: Math.max(0, 20000 + i * 1500 + Math.random() * 5000),
    net: Math.max(0, 80000 - i * 3500 + Math.random() * 15000),
  }));

  const tabItems = [
    {
      key: 'summary',
      label: 'Summary',
      children: (
        <Row gutter={[24, 24]}>
          {calculation.ai_narrative && (
            <Col xs={24}>
              <NarrativeSummary
                text={calculation.ai_narrative}
                title="Executive Summary"
              />
            </Col>
          )}
          <Col xs={24} md={6}>
            <Card>
              <Statistic
                title="Policies Processed"
                value={summary?.total_policies || calculation.policy_count || 0}
              />
            </Card>
          </Col>
          <Col xs={24} md={6}>
            <Card>
              <Statistic
                title="Total Reserve"
                value={formatCurrency(summary?.total_reserve || 0)}
              />
            </Card>
          </Col>
          <Col xs={24} md={6}>
            <Card>
              <Statistic
                title="Total Premium"
                value={formatCurrency(summary?.total_premium || 0)}
              />
            </Card>
          </Col>
          <Col xs={24} md={6}>
            <Card>
              <Statistic
                title="Anomalies"
                value={anomalies?.length || 0}
                prefix={anomalies?.length ? <WarningOutlined style={{ color: '#faad14' }} /> : null}
              />
            </Card>
          </Col>
          <Col xs={24}>
            <Card title="Projected Cash Flows">
              <LineChart
                data={cashflowData}
                xDataKey="month"
                lines={[
                  { dataKey: 'premium', name: 'Premium', color: '#16a34a' },
                  { dataKey: 'claims', name: 'Claims', color: '#dc2626' },
                  { dataKey: 'net', name: 'Net', color: '#2563eb' },
                ]}
                height={300}
              />
            </Card>
          </Col>
        </Row>
      ),
    },
    {
      key: 'results',
      label: 'Results',
      children: <EmptyState title="Results" description="Detailed results would be displayed here." />,
    },
    {
      key: 'anomalies',
      label: (
        <span>
          Anomalies
          {anomalies && anomalies.length > 0 && (
            <Tag color="red" style={{ marginLeft: 8 }}>
              {anomalies.length}
            </Tag>
          )}
        </span>
      ),
      children: (
        <AnomalyAlertWidget
          alerts={anomalies || []}
        />
      ),
    },
    {
      key: 'parameters',
      label: 'Parameters',
      children: (
        <Card>
          <Descriptions column={2}>
            <Descriptions.Item label="Model">
              {calculation.model_definition?.name || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="Assumption Set">
              {calculation.assumption_set?.name || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="Trigger Type">
              <Tag>{calculation.trigger_type}</Tag>
            </Descriptions.Item>
            <Descriptions.Item label="Triggered By">
              {calculation.triggered_by?.full_name || 'System'}
            </Descriptions.Item>
            <Descriptions.Item label="Policy Filter" span={2}>
              <pre style={{ margin: 0, fontSize: 12 }}>
                {JSON.stringify(calculation.policy_filter || {}, null, 2)}
              </pre>
            </Descriptions.Item>
            <Descriptions.Item label="Parameters" span={2}>
              <pre style={{ margin: 0, fontSize: 12 }}>
                {JSON.stringify(calculation.parameters || {}, null, 2)}
              </pre>
            </Descriptions.Item>
          </Descriptions>
        </Card>
      ),
    },
  ];

  return (
    <div>
      <PageHeader
        title={calculation.run_name}
        subtitle={`Run #${calculation.run_number}`}
        backUrl="/calculations"
        breadcrumb={[
          { title: 'Home', path: '/' },
          { title: 'Calculations', path: '/calculations' },
          { title: calculation.run_name },
        ]}
        extra={
          <Space>
            {isRunning && (
              <Button
                icon={<StopOutlined />}
                danger
                onClick={() => cancelCalculation.mutate(calculation.id)}
              >
                Cancel
              </Button>
            )}
            {calculation.status === 'completed' && (
              <>
                <Button icon={<DownloadOutlined />}>Export Results</Button>
                <Button icon={<ReloadOutlined />}>Rerun</Button>
              </>
            )}
          </Space>
        }
      />

      <Card style={{ marginBottom: 24 }}>
        <Row gutter={24} align="middle">
          <Col flex="auto">
            <Descriptions>
              <Descriptions.Item label="Status">
                <StatusBadge status={calculation.status} />
              </Descriptions.Item>
              <Descriptions.Item label="Started">
                {calculation.started_at ? formatDate(calculation.started_at, 'MMM D, YYYY HH:mm') : '-'}
              </Descriptions.Item>
              <Descriptions.Item label="Duration">
                {calculation.duration_seconds ? formatDuration(calculation.duration_seconds) : '-'}
              </Descriptions.Item>
              <Descriptions.Item label="Policies">
                {formatNumber(calculation.policy_count || 0)}
              </Descriptions.Item>
            </Descriptions>
          </Col>
          {isRunning && progress && (
            <Col>
              <Progress
                type="circle"
                percent={progress.progress_percent}
                size={80}
              />
            </Col>
          )}
        </Row>
        {progress?.progress_message && (
          <div style={{ marginTop: 8, color: '#8c8c8c' }}>
            {progress.progress_message}
          </div>
        )}
      </Card>

      <Tabs items={tabItems} />
    </div>
  );
}
