import { Card, Table, Tag, Typography, Button, Space, Tooltip, Progress } from 'antd';
import { BulbOutlined, ArrowRightOutlined, InfoCircleOutlined } from '@ant-design/icons';
import type { ExperienceRecommendation } from '@/types/models';
import { formatPercent, formatNumber } from '@/utils/formatters';

interface ExperienceRecommendationsProps {
  recommendations: ExperienceRecommendation[];
  onApply?: (recommendation: ExperienceRecommendation) => void;
}

export default function ExperienceRecommendations({
  recommendations,
  onApply,
}: ExperienceRecommendationsProps) {
  const columns = [
    {
      title: 'Assumption',
      dataIndex: 'assumption_type',
      key: 'assumption_type',
      render: (type: string) => <Tag color="blue">{type}</Tag>,
    },
    {
      title: 'Current',
      dataIndex: 'current_value',
      key: 'current_value',
      render: (value: number) => formatPercent(value),
    },
    {
      title: '',
      key: 'arrow',
      width: 40,
      render: () => <ArrowRightOutlined style={{ color: '#8c8c8c' }} />,
    },
    {
      title: 'Recommended',
      dataIndex: 'recommended_value',
      key: 'recommended_value',
      render: (value: number, record: ExperienceRecommendation) => {
        const change = ((value - record.current_value) / record.current_value) * 100;
        const color = change > 0 ? '#ff4d4f' : '#52c41a';
        return (
          <span>
            {formatPercent(value)}
            <Typography.Text style={{ color, marginLeft: 8, fontSize: 12 }}>
              ({change > 0 ? '+' : ''}{change.toFixed(1)}%)
            </Typography.Text>
          </span>
        );
      },
    },
    {
      title: 'Confidence',
      dataIndex: 'confidence',
      key: 'confidence',
      render: (confidence: number) => (
        <Progress
          percent={Math.round(confidence * 100)}
          size="small"
          status={confidence >= 0.8 ? 'success' : confidence >= 0.5 ? 'normal' : 'exception'}
          style={{ width: 80 }}
        />
      ),
    },
    {
      title: 'Sample Size',
      dataIndex: 'sample_size',
      key: 'sample_size',
      render: (size: number) => formatNumber(size),
    },
    {
      title: 'Rationale',
      dataIndex: 'rationale',
      key: 'rationale',
      ellipsis: true,
      render: (text: string) => (
        <Tooltip title={text}>
          <Typography.Text ellipsis style={{ maxWidth: 200 }}>
            {text}
          </Typography.Text>
        </Tooltip>
      ),
    },
    {
      title: 'Action',
      key: 'action',
      render: (_: unknown, record: ExperienceRecommendation) =>
        onApply && (
          <Button size="small" type="link" onClick={() => onApply(record)}>
            Apply
          </Button>
        ),
    },
  ];

  return (
    <Card
      title={
        <Space>
          <BulbOutlined style={{ color: '#faad14' }} />
          AI Recommendations
          <Tag color="purple">Based on Experience Analysis</Tag>
        </Space>
      }
      extra={
        <Tooltip title="These recommendations are based on actual vs expected experience analysis. Review carefully before applying.">
          <InfoCircleOutlined style={{ color: '#8c8c8c' }} />
        </Tooltip>
      }
    >
      {recommendations.length === 0 ? (
        <Typography.Text type="secondary">
          No recommendations at this time. Assumptions appear aligned with recent experience.
        </Typography.Text>
      ) : (
        <Table
          columns={columns}
          dataSource={recommendations}
          rowKey={(_, index) => String(index)}
          pagination={false}
          size="small"
        />
      )}
    </Card>
  );
}
