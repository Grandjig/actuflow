import { Card, Alert, List, Tag, Progress, Typography, Space } from 'antd';
import {
  WarningOutlined,
  ExclamationCircleOutlined,
  CheckCircleOutlined,
  InfoCircleOutlined,
} from '@ant-design/icons';
import type { DataQualityIssue } from '@/types/ai';

const { Text } = Typography;

interface DataQualityPanelProps {
  issues: DataQualityIssue[];
  qualityScore?: number;
  recommendations?: string[];
  loading?: boolean;
}

const issueIcons: Record<string, React.ReactNode> = {
  missing: <WarningOutlined style={{ color: '#faad14' }} />,
  invalid_format: <ExclamationCircleOutlined style={{ color: '#ff4d4f' }} />,
  outlier: <InfoCircleOutlined style={{ color: '#1890ff' }} />,
  inconsistent: <WarningOutlined style={{ color: '#faad14' }} />,
  duplicate: <InfoCircleOutlined style={{ color: '#1890ff' }} />,
};

const issueColors: Record<string, string> = {
  missing: 'orange',
  invalid_format: 'red',
  outlier: 'blue',
  inconsistent: 'orange',
  duplicate: 'default',
};

export default function DataQualityPanel({
  issues,
  qualityScore,
  recommendations,
  loading,
}: DataQualityPanelProps) {
  const getScoreStatus = (score: number) => {
    if (score >= 0.9) return { color: '#52c41a', text: 'Excellent' };
    if (score >= 0.7) return { color: '#1890ff', text: 'Good' };
    if (score >= 0.5) return { color: '#faad14', text: 'Fair' };
    return { color: '#ff4d4f', text: 'Poor' };
  };

  return (
    <Card
      title={
        <Space>
          <CheckCircleOutlined />
          Data Quality Analysis
          <Tag color="purple" style={{ fontSize: 10 }}>AI</Tag>
        </Space>
      }
      loading={loading}
      style={{ marginBottom: 16 }}
    >
      {qualityScore !== undefined && (
        <div style={{ marginBottom: 24 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
            <Text>Quality Score</Text>
            <Text strong style={{ color: getScoreStatus(qualityScore).color }}>
              {getScoreStatus(qualityScore).text} ({(qualityScore * 100).toFixed(0)}%)
            </Text>
          </div>
          <Progress
            percent={qualityScore * 100}
            strokeColor={getScoreStatus(qualityScore).color}
            showInfo={false}
          />
        </div>
      )}

      {issues.length === 0 ? (
        <Alert
          message="No data quality issues detected"
          type="success"
          showIcon
        />
      ) : (
        <>
          <Alert
            message={`${issues.length} potential issue${issues.length > 1 ? 's' : ''} detected`}
            type="warning"
            showIcon
            style={{ marginBottom: 16 }}
          />
          <List
            size="small"
            dataSource={issues}
            renderItem={(issue) => (
              <List.Item>
                <List.Item.Meta
                  avatar={issueIcons[issue.issue_type]}
                  title={
                    <Space>
                      <Text strong>{issue.column}</Text>
                      <Tag color={issueColors[issue.issue_type]}>
                        {issue.issue_type.replace('_', ' ')}
                      </Tag>
                      {issue.row && (
                        <Text type="secondary" style={{ fontSize: 12 }}>
                          Row {issue.row}
                        </Text>
                      )}
                    </Space>
                  }
                  description={
                    <div>
                      <div>{issue.description}</div>
                      {issue.suggested_fix && (
                        <Text type="secondary" style={{ fontSize: 12 }}>
                          Suggested: {issue.suggested_fix}
                        </Text>
                      )}
                    </div>
                  }
                />
              </List.Item>
            )}
          />
        </>
      )}

      {recommendations && recommendations.length > 0 && (
        <div style={{ marginTop: 16 }}>
          <Text strong>Recommendations:</Text>
          <ul style={{ marginTop: 8, paddingLeft: 20 }}>
            {recommendations.map((rec, i) => (
              <li key={i}>
                <Text type="secondary">{rec}</Text>
              </li>
            ))}
          </ul>
        </div>
      )}
    </Card>
  );
}
