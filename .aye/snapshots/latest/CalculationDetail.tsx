import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Descriptions,
  Button,
  Space,
  Tag,
  Row,
  Col,
  Statistic,
  Progress,
  Tabs,
  Table,
  Alert,
  Typography,
} from 'antd';
import {
  StopOutlined,
  DownloadOutlined,
  RobotOutlined,
  ReloadOutlined,
} from '@ant-design/icons';

import PageHeader from '@/components/common/PageHeader';
import StatusBadge from '@/components/common/StatusBadge';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import LineChart from '@/components/charts/LineChart';
import {
  useCalculation,
  useCalculationProgress,
  useCalculationSummary,
  useCancelCalculation,
} from '@/hooks/useCalculations';
import { useAuthStore } from '@/stores/authStore';
import { formatCurrency, formatDate, formatDuration } from '@/utils/formatters';

const { Paragraph } = Typography;

export default function CalculationDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { hasPermission } = useAuthStore();

  const { data: calculation, isLoading, refetch } = useCalculation(id!);
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
          <Button onClick={() => navigate('/calculations')}>Back</Button>
        </div>
      </Card>
    );
  }

  const isRunning = calculation.status === 'running' || calculation.status === 'queued';
  const isCompleted = calculation.status === 'completed';
  const isFailed = calculation.status === 'failed';

  const handleCancel = async () => {
    await cancelMutation.mutateAsync(id!);
    refetch();
  };

  return (
    <>
      <PageHeader
        title={calculation.run_name}
        subtitle={calculation.model_name || 'Calculation Run'}
        backUrl="/calculations"
        breadcrumbs={[
          { title: 'Calculations', path: '/calculations' },
          { title: calculation.run_name },
        ]}
        tags={[<StatusBadge key="status" status={calculation.status} />]}
        extra={
          <Space>
            {isRunning && hasPermission('calculation', 'update') && (
              <Button
                icon={<StopOutlined />}
                danger
                onClick={handleCancel}
                loading={cancelMutation.isPending}
              >
                Cancel
              </Button>
            )}
            {isCompleted && (
              <Button icon={<DownloadOutlined />}>Export Results</Button>
            )}
          </Space>
        }
      />

      {isFailed && calculation.error_message && (
        <Alert
          type="error"
          message="Calculation Failed"
          description={calculation.error_message}
          style={{ marginBottom: 24 }}
          showIcon
        />
      )}

      {/* Progress Section */}
      {isRunning && progress && (
        <Card style={{ marginBottom: 24 }}>
          <div style={{ textAlign: 'center' }}>
            <Progress
              type="circle"
              percent={progress.progress_percent}
              status={calculation.status === 'running' ? 'active' : undefined}
            />
            <div style={{ marginTop: 16 }}>
              <div>{progress.progress_message}</div>
              <div style={{ color: '#666', marginTop: 8 }}>
                {progress.policies_processed.toLocaleString()} / {progress.policies_total.toLocaleString()} policies
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* Stats Cards */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Policies Processed"
              value={calculation.policies_count || 0}
              suffix="policies"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Duration"
              value={formatDuration(calculation.duration_seconds)}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Reserves"
              value={summary?.total_reserves ? formatCurrency(summary.total_reserves) : '-'}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Anomalies"
              value={summary?.anomaly_count || 0}
              valueStyle={{ color: summary?.anomaly_count ? '#ff4d4f' : undefined }}
            />
          </Card>
        </Col>
      </Row>

      {/* Details and Results Tabs */}
      <Card>
        <Tabs
          items={[
            {
              key: 'details',
              label: 'Details',
              children: (
                <Descriptions bordered column={2}>
                  <Descriptions.Item label="Run Name">{calculation.run_name}</Descriptions.Item>
                  <Descriptions.Item label="Status">
                    <StatusBadge status={calculation.status} />
                  </Descriptions.Item>
                  <Descriptions.Item label="Model">
                    {calculation.model_name || '-'}
                  </Descriptions.Item>
                  <Descriptions.Item label="Assumption Set">
                    {calculation.assumption_set_name || '-'}
                  </Descriptions.Item>
                  <Descriptions.Item label="Trigger Type">
                    <Tag>{calculation.trigger_type}</Tag>
                  </Descriptions.Item>
                  <Descriptions.Item label="Policies">
                    {calculation.policies_count?.toLocaleString() || '-'}
                  </Descriptions.Item>
                  <Descriptions.Item label="Started">
                    {calculation.started_at ? formatDate(calculation.started_at) : '-'}
                  </Descriptions.Item>
                  <Descriptions.Item label="Completed">
                    {calculation.completed_at ? formatDate(calculation.completed_at) : '-'}
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
              key: 'narrative',
              label: (
                <Space>
                  <RobotOutlined />
                  AI Summary
                </Space>
              ),
              disabled: !isCompleted,
              children: calculation.ai_narrative ? (
                <div>
                  <Paragraph>{calculation.ai_narrative}</Paragraph>
                </div>
              ) : (
                <div style={{ textAlign: 'center', padding: 40, color: '#666' }}>
                  AI summary will be generated after calculation completes.
                </div>
              ),
            },
            {
              key: 'results',
              label: 'Results',
              disabled: !isCompleted,
              children: (
                <div>
                  <p>Results will be displayed here when available.</p>
                </div>
              ),
            },
          ]}
        />
      </Card>
    </>
  );
}
