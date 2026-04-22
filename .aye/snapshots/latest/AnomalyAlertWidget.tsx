import { useNavigate } from 'react-router-dom';
import { Card, List, Typography, Tag, Button, Space, Empty } from 'antd';
import { WarningOutlined, ExclamationCircleOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import type { AnomalyAlert } from '@/types/ai';

interface AnomalyAlertWidgetProps {
  alerts: AnomalyAlert[];
  loading?: boolean;
}

export default function AnomalyAlertWidget({ alerts, loading = false }: AnomalyAlertWidgetProps) {
  const navigate = useNavigate();

  const getSeverityColor = (score: number) => {
    if (score > 0.8) return 'red';
    if (score > 0.5) return 'orange';
    return 'gold';
  };

  const handleClick = (alert: AnomalyAlert) => {
    const routes: Record<string, string> = {
      claim: '/claims',
      calculation_result: '/calculations',
      policy: '/policies',
    };
    const basePath = routes[alert.record_type] || '/';
    navigate(`${basePath}/${alert.record_id}`);
  };

  return (
    <Card
      title={
        <Space>
          <WarningOutlined style={{ color: '#faad14' }} />
          Anomaly Alerts
          {alerts.length > 0 && (
            <Tag color="red">{alerts.length}</Tag>
          )}
        </Space>
      }
      extra={
        <Tag color="purple" style={{ fontSize: 10 }}>
          AI Powered
        </Tag>
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
          renderItem={(alert) => (
            <List.Item
              style={{ cursor: 'pointer' }}
              onClick={() => handleClick(alert)}
            >
              <List.Item.Meta
                avatar={
                  <ExclamationCircleOutlined
                    style={{ fontSize: 20, color: getSeverityColor(alert.score) }}
                  />
                }
                title={
                  <Space>
                    <Typography.Text>{alert.record_type}</Typography.Text>
                    <Tag color={getSeverityColor(alert.score)}>
                      {(alert.score * 100).toFixed(0)}%
                    </Tag>
                  </Space>
                }
                description={
                  <>
                    <div>{alert.reasons[0]}</div>
                    <Typography.Text type="secondary" style={{ fontSize: 11 }}>
                      {dayjs(alert.detected_at).fromNow()}
                    </Typography.Text>
                  </>
                }
              />
            </List.Item>
          )}
        />
      )}
    </Card>
  );
}
