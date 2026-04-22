import { Tag, Badge } from 'antd';
import { STATUS_COLORS } from '@/utils/constants';
import { formatStatus } from '@/utils/formatters';

interface StatusBadgeProps {
  status: string;
  type?: 'tag' | 'badge' | 'dot';
  size?: 'small' | 'default';
}

export default function StatusBadge({
  status,
  type = 'tag',
  size = 'default',
}: StatusBadgeProps) {
  const color = STATUS_COLORS[status] || 'default';
  const text = formatStatus(status);

  if (type === 'badge') {
    return <Badge status={color as any} text={text} />;
  }

  if (type === 'dot') {
    return <Badge status={color as any} />;
  }

  return (
    <Tag color={color} style={size === 'small' ? { fontSize: 11 } : undefined}>
      {text}
    </Tag>
  );
}
