import { useNavigate } from 'react-router-dom';
import { Card, List, Typography, Tag, Button, Space, Progress } from 'antd';
import { ClockCircleOutlined, PlayCircleOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import type { ScheduledJob } from '@/types/models';

interface ScheduledJobsWidgetProps {
  jobs: ScheduledJob[];
  loading?: boolean;
}

export default function ScheduledJobsWidget({ jobs, loading = false }: ScheduledJobsWidgetProps) {
  const navigate = useNavigate();

  const getStatusColor = (status: string | undefined) => {
    if (!status) return 'default';
    if (status === 'completed') return 'green';
    if (status === 'running') return 'blue';
    if (status === 'failed') return 'red';
    return 'default';
  };

  return (
    <Card
      title={
        <Space>
          <ClockCircleOutlined />
          Scheduled Jobs
        </Space>
      }
      extra={
        <Button type="link" onClick={() => navigate('/automation/jobs')}>
          Manage
        </Button>
      }
      loading={loading}
    >
      <List
        dataSource={jobs.slice(0, 5)}
        renderItem={(job) => (
          <List.Item
            style={{ cursor: 'pointer' }}
            onClick={() => navigate(`/automation/jobs/${job.id}`)}
          >
            <List.Item.Meta
              title={
                <Space>
                  {job.is_active ? (
                    <PlayCircleOutlined style={{ color: '#52c41a' }} />
                  ) : (
                    <PlayCircleOutlined style={{ color: '#8c8c8c' }} />
                  )}
                  {job.name}
                </Space>
              }
              description={
                <Space direction="vertical" size={0}>
                  <Typography.Text type="secondary" style={{ fontSize: 12 }}>
                    Next: {job.next_run ? dayjs(job.next_run).format('MMM D, HH:mm') : 'Not scheduled'}
                  </Typography.Text>
                  {job.last_run && (
                    <Typography.Text type="secondary" style={{ fontSize: 11 }}>
                      Last: {dayjs(job.last_run).fromNow()} -{' '}
                      <Tag color={getStatusColor(job.last_run_status)} style={{ fontSize: 10 }}>
                        {job.last_run_status}
                      </Tag>
                    </Typography.Text>
                  )}
                </Space>
              }
            />
          </List.Item>
        )}
        locale={{ emptyText: 'No scheduled jobs' }}
      />
    </Card>
  );
}
