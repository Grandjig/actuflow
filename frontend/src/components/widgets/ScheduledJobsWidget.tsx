/**
 * Scheduled jobs dashboard widget.
 */

import { Card, List, Tag, Typography, Space, Button, Empty, Tooltip } from 'antd';
import {
  ClockCircleOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  RightOutlined,
  PlayCircleOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useScheduledJobs, useTriggerJobNow } from '@/hooks/useAutomation';
import type { ScheduledJob } from '@/types/models';
import { formatDateTime } from '@/utils/helpers';

const { Text } = Typography;

const jobTypeColors: Record<string, string> = {
  calculation: 'blue',
  report: 'green',
  import: 'orange',
  data_check: 'purple',
};

export default function ScheduledJobsWidget() {
  const navigate = useNavigate();
  const { data, isLoading } = useScheduledJobs({ page_size: 5, is_active: true });
  const triggerMutation = useTriggerJobNow();

  const handleViewAll = () => {
    navigate('/automation/jobs');
  };

  const handleTriggerNow = (e: React.MouseEvent, jobId: string) => {
    e.stopPropagation();
    triggerMutation.mutate(jobId);
  };

  return (
    <Card
      title="Scheduled Jobs"
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
          description="No scheduled jobs"
        />
      ) : (
        <List
          dataSource={data.items}
          renderItem={(item: ScheduledJob) => {
            const lastRunStatus = item.last_run_status;

            return (
              <List.Item
                onClick={() => navigate(`/automation/jobs/${item.id}`)}
                style={{ cursor: 'pointer' }}
                actions={[
                  <Tooltip title="Run Now" key="run">
                    <Button
                      type="text"
                      icon={<PlayCircleOutlined />}
                      size="small"
                      onClick={(e) => handleTriggerNow(e, item.id)}
                      loading={triggerMutation.isPending}
                    />
                  </Tooltip>,
                ]}
              >
                <List.Item.Meta
                  title={
                    <Space>
                      <Tag color={jobTypeColors[item.job_type] || 'default'}>
                        {item.job_type.toUpperCase()}
                      </Tag>
                      <span>{item.name}</span>
                      {lastRunStatus && (
                        lastRunStatus === 'completed' ? (
                          <CheckCircleOutlined style={{ color: '#52c41a' }} />
                        ) : (
                          <CloseCircleOutlined style={{ color: '#ff4d4f' }} />
                        )
                      )}
                    </Space>
                  }
                  description={
                    <Space direction="vertical" size={0}>
                      <Space>
                        <ClockCircleOutlined />
                        <Text type="secondary" style={{ fontSize: 12 }}>
                          Next: {item.next_run ? formatDateTime(item.next_run) : 'Not scheduled'}
                        </Text>
                      </Space>
                      {item.last_run && (
                        <Text type="secondary" style={{ fontSize: 12 }}>
                          Last: {formatDateTime(item.last_run)}
                        </Text>
                      )}
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
