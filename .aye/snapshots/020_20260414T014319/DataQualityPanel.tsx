import { Card, Table, Tag, Typography, Alert, Collapse, Badge } from 'antd';
import { WarningOutlined, CheckCircleOutlined } from '@ant-design/icons';
import type { DataQualityIssue } from '@/types/ai';

interface DataQualityPanelProps {
  issues: DataQualityIssue[];
  qualityScore: number;
  recommendations?: string[];
}

export default function DataQualityPanel({
  issues,
  qualityScore,
  recommendations = [],
}: DataQualityPanelProps) {
  const issuesByType = issues.reduce(
    (acc, issue) => {
      acc[issue.issue_type] = (acc[issue.issue_type] || 0) + 1;
      return acc;
    },
    {} as Record<string, number>
  );

  const columns = [
    {
      title: 'Row',
      dataIndex: 'row',
      key: 'row',
      width: 80,
      render: (row: number | undefined) => row ?? '-',
    },
    {
      title: 'Column',
      dataIndex: 'column',
      key: 'column',
      width: 150,
    },
    {
      title: 'Issue',
      dataIndex: 'issue_type',
      key: 'issue_type',
      width: 120,
      render: (type: string) => {
        const colors: Record<string, string> = {
          missing: 'orange',
          invalid_format: 'red',
          outlier: 'purple',
          duplicate: 'blue',
        };
        return <Tag color={colors[type] || 'default'}>{type.replace('_', ' ')}</Tag>;
      },
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: 'Suggested Fix',
      dataIndex: 'suggested_fix',
      key: 'suggested_fix',
      render: (fix: string | undefined) =>
        fix ? (
          <Typography.Text type="success">{fix}</Typography.Text>
        ) : (
          '-'
        ),
    },
  ];

  const scoreColor =
    qualityScore >= 0.9
      ? '#52c41a'
      : qualityScore >= 0.7
        ? '#faad14'
        : '#ff4d4f';

  return (
    <Card
      title={
        <span>
          <WarningOutlined style={{ marginRight: 8 }} />
          Data Quality Analysis
        </span>
      }
      extra={
        <span>
          Quality Score:{' '}
          <Typography.Text strong style={{ color: scoreColor }}>
            {(qualityScore * 100).toFixed(0)}%
          </Typography.Text>
        </span>
      }
    >
      {qualityScore >= 0.95 ? (
        <Alert
          message="Excellent Data Quality"
          description="No significant issues detected in the uploaded data."
          type="success"
          showIcon
          icon={<CheckCircleOutlined />}
        />
      ) : (
        <>
          <div style={{ marginBottom: 16, display: 'flex', gap: 8 }}>
            {Object.entries(issuesByType).map(([type, count]) => (
              <Badge key={type} count={count} showZero>
                <Tag>{type.replace('_', ' ')}</Tag>
              </Badge>
            ))}
          </div>

          {recommendations.length > 0 && (
            <Alert
              message="Recommendations"
              description={
                <ul style={{ margin: 0, paddingLeft: 20 }}>
                  {recommendations.map((rec, index) => (
                    <li key={index}>{rec}</li>
                  ))}
                </ul>
              }
              type="info"
              showIcon
              style={{ marginBottom: 16 }}
            />
          )}

          <Collapse
            items={[
              {
                key: 'issues',
                label: `View ${issues.length} issues`,
                children: (
                  <Table
                    columns={columns}
                    dataSource={issues.slice(0, 50)}
                    rowKey={(_, index) => String(index)}
                    size="small"
                    pagination={false}
                    scroll={{ y: 300 }}
                  />
                ),
              },
            ]}
          />
        </>
      )}
    </Card>
  );
}
