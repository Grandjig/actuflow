import { useNavigate } from 'react-router-dom';
import { Card, List, Typography, Tag, Button, Space } from 'antd';
import { CalculatorOutlined, ClockCircleOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import { useCalculations } from '@/hooks/useCalculations';
import StatusBadge from '../common/StatusBadge';
import { formatDuration } from '@/utils/formatters';

export default function RecentCalculationsWidget() {
  const navigate = useNavigate();
  const { data, isLoading } = useCalculations({ page_size: 5 });

  return (
    <Card
      title={
        <Space>
          <CalculatorOutlined />
          Recent Calculations
        </Space>
      }
      extra={
        <Button type="link" onClick={() => navigate('/calculations')}>
          View all
        </Button>
      }
      loading={isLoading}
    >
      <List
        dataSource={data?.items || []}
        renderItem={(item) => (
          <List.Item
            style={{ cursor: 'pointer' }}
            onClick={() => navigate(`/calculations/${item.id}`)}
          >
            <List.Item.Meta
              title={item.run_name}
              description={
                <Space size="small">
                  <Typography.Text type="secondary">
                    <ClockCircleOutlined /> {dayjs(item.created_at).fromNow()}
                  </Typography.Text>
                  {item.duration_seconds && (
                    <Typography.Text type="secondary">
                      • {formatDuration(item.duration_seconds)}
                    </Typography.Text>
                  )}
                </Space>
              }
            />
            <StatusBadge status={item.status} size="small" />
          </List.Item>
        )}
        locale={{ emptyText: 'No recent calculations' }}
      />
    </Card>
  );
}
