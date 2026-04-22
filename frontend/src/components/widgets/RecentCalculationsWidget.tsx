/**
 * Recent calculations dashboard widget.
 */

import { Card, List, Tag, Typography, Space, Button, Empty } from 'antd';
import {
  PlayCircleOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  LoadingOutlined,
  RightOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useCalculationRuns } from '@/hooks/useCalculations';
import type { CalculationRun, CalculationStatus } from '@/types/models';
import { formatDateTime } from '@/utils/helpers';

const { Text } = Typography;

const statusConfig: Record<
  CalculationStatus,
  { icon: React.ReactNode; color: string }
> = {
  queued: { icon: <PlayCircleOutlined />, color: 'default' },
  running: { icon: <LoadingOutlined />, color: 'processing' },
  completed: { icon: <CheckCircleOutlined />, color: 'success' },
  failed: { icon: <CloseCircleOutlined />, color: 'error' },
  cancelled: { icon: <CloseCircleOutlined />, color: 'default' },
};

export default function RecentCalculationsWidget() {
  const navigate = useNavigate();
  const { data, isLoading } = useCalculationRuns({ page_size: 5 });

  const handleViewAll = () => {
    navigate('/calculations');
  };

  return (
    <Card
      title="Recent Calculations"
      extra={
        <Button type="link" onClick={handleViewAll}>
          View All <RightOutlined />
        </Button>
      }
      loading={isLoading}
    >
      {!data?.items || data.items.length === 0 ? (
        <Empty
          image={Empty.PRESENTED_IMAGE_SIMPLE}
          description="No calculations yet"
        />
      ) : (
        <List
          dataSource={data.items}
          renderItem={(item: CalculationRun) => {
            const config = statusConfig[item.status];

            return (
              <List.Item
                onClick={() => navigate(`/calculations/${item.id}`)}
                style={{ cursor: 'pointer' }}
              >
                <List.Item.Meta
                  title={
                    <Space>
                      <Tag icon={config.icon} color={config.color}>
                        {item.status.toUpperCase()}
                      </Tag>
                      <span>{item.run_name}</span>
                    </Space>
                  }
                  description={
                    <Space direction="vertical" size={0}>
                      <Text type="secondary">
                        {item.model_definition?.name || 'Unknown Model'}
                      </Text>
                      <Text type="secondary" style={{ fontSize: 12 }}>
                        {formatDateTime(item.started_at || item.created_at)}
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
