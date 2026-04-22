import { Card, Statistic, Typography } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';
import type { ReactNode } from 'react';

const { Text } = Typography;

interface StatCardProps {
  title: string;
  value: string | number;
  change?: number;
  changeType?: 'increase' | 'decrease';
  icon?: ReactNode;
  color?: string;
  loading?: boolean;
  suffix?: string;
  prefix?: string;
}

export default function StatCard({
  title,
  value,
  change,
  changeType,
  icon,
  color = '#1890ff',
  loading = false,
  suffix,
  prefix,
}: StatCardProps) {
  const isIncrease = changeType === 'increase';
  const changeColor = isIncrease ? '#52c41a' : '#ff4d4f';

  return (
    <Card loading={loading}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <Text type="secondary" style={{ fontSize: 14 }}>
            {title}
          </Text>
          <div style={{ fontSize: 28, fontWeight: 600, marginTop: 4 }}>
            {prefix}{value}{suffix}
          </div>
          {change !== undefined && (
            <div style={{ marginTop: 4 }}>
              <span style={{ color: changeColor }}>
                {isIncrease ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
                {' '}{Math.abs(change)}%
              </span>
              <Text type="secondary" style={{ marginLeft: 8, fontSize: 12 }}>
                vs last period
              </Text>
            </div>
          )}
        </div>
        {icon && (
          <div
            style={{
              width: 48,
              height: 48,
              borderRadius: 8,
              background: `${color}15`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: color,
              fontSize: 24,
            }}
          >
            {icon}
          </div>
        )}
      </div>
    </Card>
  );
}
