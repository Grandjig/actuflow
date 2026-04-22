/**
 * Data quality issues panel for import wizard.
 */

import { Alert, List, Tag, Typography, Space, Button } from 'antd';
import {
  WarningOutlined,
  ExclamationCircleOutlined,
  InfoCircleOutlined,
  CheckOutlined,
} from '@ant-design/icons';
import type { DataQualityIssue } from '@/types/models';

const { Text } = Typography;

interface DataQualityPanelProps {
  issues: DataQualityIssue[];
  onApplyFix?: (issue: DataQualityIssue) => void;
}

const severityConfig = {
  error: {
    color: 'red',
    icon: <ExclamationCircleOutlined />,
    label: 'Error',
  },
  warning: {
    color: 'orange',
    icon: <WarningOutlined />,
    label: 'Warning',
  },
  info: {
    color: 'blue',
    icon: <InfoCircleOutlined />,
    label: 'Info',
  },
};

export default function DataQualityPanel({
  issues,
  onApplyFix,
}: DataQualityPanelProps) {
  if (issues.length === 0) {
    return (
      <Alert
        type="success"
        icon={<CheckOutlined />}
        message="No data quality issues detected"
        description="Your data passed all quality checks."
      />
    );
  }

  const errorCount = issues.filter((i) => i.severity === 'error').length;
  const warningCount = issues.filter((i) => i.severity === 'warning').length;

  return (
    <div>
      <Alert
        type={errorCount > 0 ? 'error' : warningCount > 0 ? 'warning' : 'info'}
        message="Data Quality Issues Detected"
        description={
          <Space>
            {errorCount > 0 && (
              <Tag color="red">{errorCount} errors</Tag>
            )}
            {warningCount > 0 && (
              <Tag color="orange">{warningCount} warnings</Tag>
            )}
            <Text type="secondary">
              Review and fix issues before importing.
            </Text>
          </Space>
        }
        style={{ marginBottom: 16 }}
      />

      <List
        dataSource={issues}
        renderItem={(issue) => {
          const config = severityConfig[issue.severity];
          const rowInfo = issue.row ?? (issue.rows?.[0]);
          const suggestedFix = issue.suggested_fix ?? issue.suggestion;
          
          return (
            <List.Item
              actions={
                suggestedFix && onApplyFix
                  ? [
                      <Button
                        key="fix"
                        size="small"
                        onClick={() => onApplyFix(issue)}
                      >
                        Apply Fix
                      </Button>,
                    ]
                  : undefined
              }
            >
              <List.Item.Meta
                avatar={
                  <Tag color={config.color} icon={config.icon}>
                    {config.label}
                  </Tag>
                }
                title={
                  <Space>
                    <Text strong>{issue.column}</Text>
                    <Text type="secondary">({issue.issue_type})</Text>
                    <Text type="secondary">
                      {issue.count} occurrence{issue.count !== 1 ? 's' : ''}
                    </Text>
                  </Space>
                }
                description={
                  <Space direction="vertical" size="small">
                    <Text>{issue.message}</Text>
                    {rowInfo !== undefined && (
                      <Text type="secondary">Row: {rowInfo}</Text>
                    )}
                    {suggestedFix && (
                      <Text type="success">Suggestion: {suggestedFix}</Text>
                    )}
                  </Space>
                }
              />
            </List.Item>
          );
        }}
      />
    </div>
  );
}
