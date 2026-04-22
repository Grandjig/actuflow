import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Descriptions,
  Tag,
  Button,
  Space,
  Tabs,
  Progress,
  Statistic,
  Row,
  Col,
  Alert,
  Spin,
} from 'antd';
import {
  StopOutlined,
  ReloadOutlined,
  DownloadOutlined,
  RobotOutlined,
} from '@ant-design/icons';

import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import {
  useCalculation,
  useCalculationProgress,
  useCalculationSummary,
  useCancelCalculation,
} from '@/hooks/useCalculations';
import { formatDate, formatDuration, formatCurrency, formatNumber } from '@/utils/formatters';

export default function CalculationDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: calculation, isLoading } = useCalculation(id!);
  const { data: progress } = useCalculationProgress(id!);
  const { data: summary } = useCalculationSummary(id!);
  const cancelMutation = useCancelCalculation();

  if (isLoading) {
    return <LoadingSpinner fullScreen tip="Loading calculation..." />;
  }

  if (!calculation) {
    return (
      <Card>
        <div style={{ textAlign: 'center', padding: 48 }}>
          <h3>Calculation not found</h3>
          <Button onClick={() => navigate('/calculations')}>Back to Calculations</Button>
        </div>
      </Card>
    );
  }

  const isRunning = calculation.status === 'running' || calculation.status === 'queued';

  return (
    <>
      <PageHeader
        title={calculation.run_name}
        subtitle={calculation.model_name}
        backUrl="/calculations"
        breadcrumbs={[
          { title: 'Calculations', path: '/calculations' },
          { title: calculation.run_name },
        ]}
        tags={[<StatusBadge key="status" status={calculation.status} />]}
        extra={
          <Space>
            {isRunning && (
              <Button
                danger
                icon={<StopOutlined />}
                onClick={() => cancelMutation.mutate(id!)}
                loading={cancelMutation.isPending}
              >
                Cancel
              </Button>
            )}
            {calculation.status === 'completed' && (
              <Button icon={<DownloadOutlined />}>Export Results</Button>
            )}
          </Space>
        }
      />

      {/* Progress for running calculations */}
      {isRunning && progress && (
        <Card style={{ marginBottom: 24 }}>
          <Row align="middle" gutter={24}>
            <Col flex="auto">
              <Progress
                percent={progress.progress_percent}
                status={calculation.status === 'running' ? 'active' : undefined}
              />
              <div style={{ marginTop: 8, color: '#666' }}>
                {progress.progress_message} - {progress.policies_processed} of{' '}
                {progress.policies_total} policies processed
              </div>
            </Col>
          </Row>
        </Card>
      )}

      {/* Summary stats for completed */}
      {calculation.status === 'completed' && summary && (
        <Row gutter={16} style={{ marginBottom: 24 }}>
          <Col span={6}>
            <Card>
              <Statistic
                title="Policies Processed"
                value={formatNumber(summary.total_policies)}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Total Reserves"
                value={formatCurrency(summary.total_reserves)}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Total Premiums"
                value={formatCurrency(summary.total_premiums)}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Anomalies Flagged"
                value={summary.anomaly_count}
                valueStyle={{ color: summary.anomaly_count > 0 ? '#faad14' : '#52c41a' }}
              />
            </Card>
          </Col>
        </Row>
      )}

      {/* Error message for failed */}
      {calculation.status === 'failed' && calculation.error_message && (
        <Alert
          type="error"
          message="Calculation Failed"
          description={calculation.error_message}
          style={{ marginBottom: 24 }}
        />
      )}

      {/* AI Narrative */}
      {calculation.ai_narrative && (
        <Card
          title={
            <Space>
              <RobotOutlined />
              AI Summary
              <Tag color="purple">AI Generated</Tag>
            </Space>
          }
          style={{ marginBottom: 24 }}
        >
          <div style={{ whiteSpace: 'pre-wrap' }}>{calculation.ai_narrative}</div>
        </Card>
      )}

      {/* Details */}
      <Card>
        <Tabs
          items={[
            {
              key: 'details',
              label: 'Details',
              children: (
                <Descriptions bordered column={2}>
                  <Descriptions.Item label="Run Name">
                    {calculation.run_name}
                  </Descriptions.Item>
                  <Descriptions.Item label="Status">
                    <StatusBadge status={calculation.status} />
                  </Descriptions.Item>
                  <Descriptions.Item label="Model">
                    {calculation.model_name}
                  </Descriptions.Item>
                  <Descriptions.Item label="Assumption Set">
                    {calculation.assumption_set_name}
                  </Descriptions.Item>
                  <Descriptions.Item label="Trigger Type">
                    <Tag>{calculation.trigger_type}</Tag>
                  </Descriptions.Item>
                  <Descriptions.Item label="Policies Count">
                    {calculation.policies_count?.toLocaleString() || '-'}
                  </Descriptions.Item>
                  <Descriptions.Item label="Started At">
                    {formatDate(calculation.started_at)}
                  </Descriptions.Item>
                  <Descriptions.Item label="Completed At">
                    {formatDate(calculation.completed_at)}
                  </Descriptions.Item>
                  <Descriptions.Item label="Duration">
                    {formatDuration(calculation.duration_seconds)}
                  </Descriptions.Item>
                  <Descriptions.Item label="Created">
                    {formatDate(calculation.created_at)}
                  </Descriptions.Item>
                </Descriptions>
              ),
            },
            {
              key: 'results',
              label: 'Results',
              children: <div>Results table would go here</div>,
            },
            {
              key: 'parameters',
              label: 'Parameters',
              children: (
                <pre style={{ background: '#f5f5f5', padding: 16, borderRadius: 4 }}>
                  {JSON.stringify(calculation.parameters || {}, null, 2)}
                </pre>
              ),
            },
          ]}
        />
      </Card>
    </>
  );
}
