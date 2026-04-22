import { Tag } from 'antd';
import { STATUS_COLORS } from '@/utils/constants';
import { formatStatus } from '@/utils/formatters';

interface StatusBadgeProps {
  status: string;
  size?: 'small' | 'default';
}

export default function StatusBadge({ status, size = 'default' }: StatusBadgeProps) {
  const color = STATUS_COLORS[status] || 'default';
  const label = formatStatus(status);

  return (
    <Tag color={color} style={size === 'small' ? { fontSize: 11 } : undefined}>
      {label}
    </Tag>
  );
}
