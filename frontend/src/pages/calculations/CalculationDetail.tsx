/**
 * Calculation detail page.
 */

import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Descriptions,
  Button,
  Space,
  Tag,
  Tabs,
  Progress,
  Spin,
  Typography,
  Divider,
  Statistic,
  Row,
  Col,
} from 'antd';
import {
  ArrowLeftOutlined,
  StopOutlined,
  ReloadOutlined,
  DownloadOutlined,
  PlayCircleOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  LoadingOutlined,
} from '@ant-design/icons';
import {
  useCalculationRun,
  useCalculationProgress,
  useCalculationSummary,
  useCancelCalculationRun,
} from '@/hooks/useCalculations';
import type { CalculationStatus } from '@/types/models';
import { formatDateTime, formatCurrency } from '@/utils/helpers';

const { Title, Paragraph } = Typography;

const statusConfig: Record<CalculationStatus, { icon: React.ReactNode; color: string }> = {
  queued: { icon: <PlayCircleOutlined />, color: 'default' },
  running: { icon: <LoadingOutlined />, color: 'processing' },
  completed: { icon: <CheckCircleOutlined />, color: 'success' },
  failed: { icon: <CloseCircleOutlined />, color: 'error' },
  cancelled: { icon: <CloseCircleOutlined />, color: 'default' },
};

export default function CalculationDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: calculation, isLoading } = useCalculationRun(id!);
  const { data: progress } = useCalculationProgress(id!);
  const { data: summary } = useCalculationSummary(id!);
  const cancelMutation = useCancelCalculationRun();

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: 100 }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!calculation) {
    return <div>Calculation not found</div>;
  }

  const config = statusConfig[calculation.status];
  const isRunning = calculation.status === 'running' || calculation.status === 'queued';

  const handleCancel = () => {
    if (id) {
      cancelMutation.mutate(id);
    }
  };

  const tabItems = [
    {
      key: 'summary',
      label: 'Summary',
      children: (
        <div>
          {summary && (
            <Row gutter={16}>
              <Col span={6}>
                <Statistic
                  title="Total Reserve"
                  value={formatCurrency(summary.total_reserve as number)}
                />
              </Col>
              <Col span={6}>
                <Statistic
                  title="Policies Processed"
                  value={calculation.policies_count || 0}
                />
              </Col>
              <Col span={6}>
                <Statistic
                  title="Duration"
                  value={calculation.duration_seconds || 0}
                  suffix="seconds"
                />
              </Col>
              <Col span={6}>
                <Statistic
                  title="Anomalies"
                  value={summary.anomaly_count as number || 0}
                />
              </Col>
            </Row>
          )}
        </div>
      ),
    },
    {
      key: 'results',
      label: 'Results',
      children: <div>Detailed results table will go here</div>,
    },
    {
      key: 'narrative',
      label: 'AI Narrative',
      children: (
        <div>
          {calculation.ai_narrative ? (
            <Paragraph>{calculation.ai_narrative}</Paragraph>
          ) : (
            <Paragraph type="secondary">No AI narrative generated for this run.</Paragraph>
          )}
        </div>
      ),
    },
    {
      key: 'anomalies',
      label: 'Anomalies',
      children: <div>Anomaly list will go here</div>,
    },
  ];

  return (
    <div>
      <Space style={{ marginBottom: 16 }}>
        <Button
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate('/calculations')}
        >
          Back
        </Button>
      </Space>

      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div>
            <Title level={3} style={{ marginBottom: 8 }}>
              {calculation.run_name}
            </Title>
            <Space>
              <Tag icon={config.icon} color={config.color}>
                {calculation.status.toUpperCase()}
              </Tag>
              <span>{calculation.trigger_type}</span>
            </Space>
          </div>
          <Space>
            {isRunning && (
              <Button
                icon={<StopOutlined />}
                danger
                onClick={handleCancel}
                loading={cancelMutation.isPending}
              >
                Cancel
              </Button>
            )}
            {calculation.status === 'completed' && (
              <Button icon={<DownloadOutlined />}>Export Results</Button>
            )}
            <Button icon={<ReloadOutlined />}>Rerun</Button>
          </Space>
        </div>

        {isRunning && progress && (
          <div style={{ marginTop: 16 }}>
            <Progress
              percent={progress.progress_percent}
              status="active"
              format={() =>
                `${progress.policies_processed} / ${progress.policies_total} policies`
              }
            />
            {progress.current_step && (
              <Paragraph type="secondary">{progress.current_step}</Paragraph>
            )}
          </div>
        )}

        <Divider />

        <Descriptions column={3}>
          <Descriptions.Item label="Model">
            {calculation.model_definition?.name || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Assumption Set">
            {calculation.assumption_set?.name || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Triggered By">
            {calculation.triggered_by}
          </Descriptions.Item>
          <Descriptions.Item label="Started">
            {formatDateTime(calculation.started_at)}
          </Descriptions.Item>
          <Descriptions.Item label="Completed">
            {formatDateTime(calculation.completed_at)}
          </Descriptions.Item>
          <Descriptions.Item label="Duration">
            {calculation.duration_seconds ? `${calculation.duration_seconds}s` : '-'}
          </Descriptions.Item>
        </Descriptions>

        {calculation.error_message && (
          <>
            <Divider orientation="left">Error</Divider>
            <Paragraph type="danger">{calculation.error_message}</Paragraph>
          </>
        )}

        <Divider />

        <Tabs items={tabItems} />
      </Card>
    </div>
  );
}
