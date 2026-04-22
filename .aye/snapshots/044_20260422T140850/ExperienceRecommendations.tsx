import { Card, List, Tag, Button, Typography, Space, Progress, Tooltip } from 'antd';
import { BulbOutlined, ArrowUpOutlined, ArrowDownOutlined, CheckOutlined } from '@ant-design/icons';
import type { ExperienceRecommendation } from '@/types/models';
import { formatPercent, formatNumber } from '@/utils/formatters';

const { Text } = Typography;

interface ExperienceRecommendationsProps {
  recommendations: ExperienceRecommendation[];
  onApply?: (recommendation: ExperienceRecommendation) => void;
  loading?: boolean;
}

export default function ExperienceRecommendations({
  recommendations,
  onApply,
  loading,
}: ExperienceRecommendationsProps) {
  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return '#52c41a';
    if (confidence >= 0.6) return '#faad14';
    return '#ff4d4f';
  };

  const getChangeDirection = (current: number, recommended: number) => {
    if (recommended > current) {
      return { icon: <ArrowUpOutlined />, color: '#ff4d4f', text: 'Increase' };
    }
    if (recommended < current) {
      return { icon: <ArrowDownOutlined />, color: '#52c41a', text: 'Decrease' };
    }
    return { icon: null, color: '#666', text: 'No change' };
  };

  if (recommendations.length === 0) {
    return (
      <Card>
        <div style={{ textAlign: 'center', padding: 40, color: '#666' }}>
          <BulbOutlined style={{ fontSize: 40, marginBottom: 16 }} />
          <div>No recommendations available</div>
          <Text type="secondary">
            Run an experience analysis to generate AI recommendations
          </Text>
        </div>
      </Card>
    );
  }

  return (
    <Card
      title={
        <Space>
          <BulbOutlined />
          AI Experience Recommendations
          <Tag color="purple">Based on actual vs expected analysis</Tag>
        </Space>
      }
      loading={loading}
    >
      <List
        dataSource={recommendations}
        renderItem={(rec) => {
          const direction = getChangeDirection(rec.current_value, rec.recommended_value);
          const changePercent = ((rec.recommended_value - rec.current_value) / rec.current_value) * 100;

          return (
            <List.Item
              actions={
                onApply
                  ? [
                      <Button
                        key="apply"
                        type="primary"
                        size="small"
                        icon={<CheckOutlined />}
                        onClick={() => onApply(rec)}
                      >
                        Apply
                      </Button>,
                    ]
                  : undefined
              }
            >
              <List.Item.Meta
                title={
                  <Space>
                    <Text strong>{rec.assumption_type}</Text>
                    {rec.segment && <Tag>{rec.segment}</Tag>}
                  </Space>
                }
                description={
                  <div>
                    <Space style={{ marginBottom: 8 }}>
                      <Text>Current: {formatPercent(rec.current_value, 4)}</Text>
                      <span style={{ color: direction.color }}>
                        {direction.icon} {direction.text} to{' '}
                        {formatPercent(rec.recommended_value, 4)}
                        <Text type="secondary"> ({changePercent > 0 ? '+' : ''}{changePercent.toFixed(1)}%)</Text>
                      </span>
                    </Space>
                    <div>
                      <Text type="secondary">{rec.rationale}</Text>
                    </div>
                    <div style={{ marginTop: 8 }}>
                      <Space>
                        <Tooltip title="Confidence level based on data quality and volume">
                          <span>
                            Confidence:
                            <Progress
                              percent={rec.confidence * 100}
                              size="small"
                              strokeColor={getConfidenceColor(rec.confidence)}
                              style={{ width: 80, marginLeft: 8 }}
                              format={() => `${(rec.confidence * 100).toFixed(0)}%`}
                            />
                          </span>
                        </Tooltip>
                        <Text type="secondary">
                          Sample size: {formatNumber(rec.sample_size)}
                        </Text>
                      </Space>
                    </div>
                    {rec.impact && (
                      <div style={{ marginTop: 4 }}>
                        <Text type="secondary">
                          Reserve impact:{' '}
                          <span style={{ color: rec.impact.direction === 'increase' ? '#ff4d4f' : '#52c41a' }}>
                            {rec.impact.direction === 'increase' ? '+' : '-'}$
                            {Math.abs(rec.impact.reserve_change).toLocaleString()}
                          </span>
                        </Text>
                      </div>
                    )}
                  </div>
                }
              />
            </List.Item>
          );
        }}
      />
    </Card>
  );
}
