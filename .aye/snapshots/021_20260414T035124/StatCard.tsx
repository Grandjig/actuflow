import { Card, Statistic, Typography } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';
import type { StatCardData } from '@/types/ui';

interface StatCardProps extends StatCardData {
  loading?: boolean;
  onClick?: () => void;
}

export default function StatCard({
  title,
  value,
  change,
  changeType,
  icon,
  color,
  loading = false,
  onClick,
}: StatCardProps) {
  return (
    <Card
      className="stat-card"
      hoverable={!!onClick}
      onClick={onClick}
      loading={loading}
      style={{ cursor: onClick ? 'pointer' : 'default' }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <Statistic
          title={title}
          value={value}
          valueStyle={{ color: color || '#1677ff' }}
        />
        {icon && (
          <div
            style={{
              fontSize: 24,
              color: color || '#1677ff',
              opacity: 0.8,
            }}
          >
            {icon}
          </div>
        )}
      </div>

      {change !== undefined && (
        <div style={{ marginTop: 8 }}>
          <Typography.Text
            type={changeType === 'increase' ? 'success' : 'danger'}
            style={{ fontSize: 12 }}
          >
            {changeType === 'increase' ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
            {Math.abs(change)}%
          </Typography.Text>
          <Typography.Text type="secondary" style={{ fontSize: 12, marginLeft: 8 }}>
            vs last period
          </Typography.Text>
        </div>
      )}
    </Card>
  );
}
