/**
 * Experience-based assumption recommendations component.
 */

import {
  Card,
  List,
  Tag,
  Typography,
  Space,
  Progress,
  Button,
  Tooltip,
  Statistic,
  Row,
  Col,
} from 'antd';
import {
  ArrowUpOutlined,
  ArrowDownOutlined,
  QuestionCircleOutlined,
} from '@ant-design/icons';
import type { ExperienceRecommendation } from '@/types/models';
import { formatCurrency, formatPercent } from '@/utils/helpers';

const { Text, Title } = Typography;

interface ExperienceRecommendationsProps {
  recommendations: ExperienceRecommendation[];
  onApply?: (recommendation: ExperienceRecommendation) => void;
  onDismiss?: (recommendation: ExperienceRecommendation) => void;
}

const confidenceColors = {
  low: 'orange',
  medium: 'blue',
  high: 'green',
};

export default function ExperienceRecommendations({
  recommendations,
  onApply,
  onDismiss,
}: ExperienceRecommendationsProps) {
  if (recommendations.length === 0) {
    return (
      <Card>
        <Text type="secondary">
          No recommendations available. Run an experience analysis to generate
          assumption update suggestions.
        </Text>
      </Card>
    );
  }

  return (
    <List
      dataSource={recommendations}
      renderItem={(rec) => {
        const rateDiff = rec.suggested_rate - rec.current_rate;
        const rateChangePercent = (rateDiff / rec.current_rate) * 100;
        const isIncrease = rateDiff > 0;

        return (
          <List.Item>
            <Card style={{ width: '100%' }}>
              <Row gutter={24}>
                <Col span={6}>
                  <Space direction="vertical" size="small">
                    <Text type="secondary">Assumption Type</Text>
                    <Text strong style={{ fontSize: 16 }}>
                      {rec.assumption_type}
                    </Text>
                    <Tag>{rec.segment}</Tag>
                  </Space>
                </Col>

                <Col span={6}>
                  <Space direction="vertical" size="small">
                    <Text type="secondary">Rate Comparison</Text>
                    <Space>
                      <Statistic
                        title="Current"
                        value={formatPercent(rec.current_rate)}
                        valueStyle={{ fontSize: 14 }}
                      />
                      <Text>→</Text>
                      <Statistic
                        title="Suggested"
                        value={formatPercent(rec.suggested_rate)}
                        valueStyle={{
                          fontSize: 14,
                          color: isIncrease ? '#cf1322' : '#3f8600',
                        }}
                        prefix={
                          isIncrease ? (
                            <ArrowUpOutlined />
                          ) : (
                            <ArrowDownOutlined />
                          )
                        }
                      />
                    </Space>
                  </Space>
                </Col>

                <Col span={6}>
                  <Space direction="vertical" size="small">
                    <Text type="secondary">
                      Credibility
                      <Tooltip title="Based on data volume and statistical significance">
                        <QuestionCircleOutlined style={{ marginLeft: 4 }} />
                      </Tooltip>
                    </Text>
                    <Progress
                      percent={Math.round(rec.credibility * 100)}
                      size="small"
                      status={
                        rec.credibility > 0.7
                          ? 'success'
                          : rec.credibility > 0.4
                          ? 'normal'
                          : 'exception'
                      }
                    />
                    <Space>
                      <Tag color={confidenceColors[rec.confidence]}>
                        {rec.confidence.toUpperCase()} confidence
                      </Tag>
                      <Text type="secondary">
                        {rec.data_points.toLocaleString()} data points
                      </Text>
                    </Space>
                  </Space>
                </Col>

                <Col span={6}>
                  <Space direction="vertical" size="small">
                    {rec.impact && (
                      <>
                        <Text type="secondary">Reserve Impact</Text>
                        <Statistic
                          value={formatCurrency(Math.abs(rec.impact.reserve_change))}
                          valueStyle={{
                            fontSize: 14,
                            color:
                              rec.impact.direction === 'increase'
                                ? '#cf1322'
                                : '#3f8600',
                          }}
                          prefix={
                            rec.impact.direction === 'increase' ? '+' : '-'
                          }
                        />
                      </>
                    )}
                    <Space>
                      {onApply && (
                        <Button
                          type="primary"
                          size="small"
                          onClick={() => onApply(rec)}
                        >
                          Apply
                        </Button>
                      )}
                      {onDismiss && (
                        <Button size="small" onClick={() => onDismiss(rec)}>
                          Dismiss
                        </Button>
                      )}
                    </Space>
                  </Space>
                </Col>
              </Row>
            </Card>
          </List.Item>
        );
      }}
    />
  );
}
