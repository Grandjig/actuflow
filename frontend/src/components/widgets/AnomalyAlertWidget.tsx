/**
 * Anomaly alerts dashboard widget.
 */

import { Card, List, Tag, Typography, Space, Button, Empty } from 'antd';
import {
  WarningOutlined,
  ExclamationCircleOutlined,
  RightOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import type { AnomalyAlert } from '@/types/models';
import { formatDateTime } from '@/utils/helpers';

const { Text } = Typography;

interface AnomalyAlertWidgetProps {
  alerts: AnomalyAlert[];
  loading?: boolean;
}

const severityConfig: Record<string, { color: string; icon: React.ReactNode }> = {
  low: {
    color: 'blue',
    icon: <WarningOutlined />,
  },
  medium: {
    color: 'orange',
    icon: <WarningOutlined />,
  },
  high: {
    color: 'red',
    icon: <ExclamationCircleOutlined />,
  },
};

export default function AnomalyAlertWidget({
  alerts,
  loading,
}: AnomalyAlertWidgetProps) {
  const navigate = useNavigate();

  const handleViewAll = () => {
    navigate('/anomalies');
  };

  const handleAlertClick = (alert: AnomalyAlert) => {
    // Navigate to the related resource
    if (alert.resource_type && alert.resource_id) {
      navigate(`/${alert.resource_type}s/${alert.resource_id}`);
    }
  };

  return (
    <Card
      title="Anomaly Alerts"
      extra={
        <Button type="link" onClick={handleViewAll}>
          View All <RightOutlined />
        </Button>
      }
      loading={loading}
    >
      {alerts.length === 0 ? (
        <Empty
          image={Empty.PRESENTED_IMAGE_SIMPLE}
          description="No anomalies detected"
        />
      ) : (
        <List
          dataSource={alerts.slice(0, 5)}
          renderItem={(alert) => {
            const config = severityConfig[alert.severity] || severityConfig.medium;

            return (
              <List.Item
                onClick={() => handleAlertClick(alert)}
                style={{ cursor: 'pointer' }}
              >
                <List.Item.Meta
                  avatar={
                    <Tag color={config.color} icon={config.icon}>
                      {alert.severity.toUpperCase()}
                    </Tag>
                  }
                  title={alert.description}
                  description={
                    <Space direction="vertical" size={0}>
                      <Text type="secondary">
                        {alert.resource_type}: {alert.resource_id}
                      </Text>
                      {alert.reasons && alert.reasons.length > 0 && (
                        <Text type="secondary" style={{ fontSize: 12 }}>
                          {alert.reasons[0]}
                          {alert.reasons.length > 1 && ` (+${alert.reasons.length - 1} more)`}
                        </Text>
                      )}
                      <Text type="secondary" style={{ fontSize: 12 }}>
                        {formatDateTime(alert.created_at)}
                      </Text>
                    </Space>
                  }
                />
              </List.Item>
            );
          }}
        />
      )}
    </Card>
  );
}
