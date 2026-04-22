import { Tag } from 'antd';
import { formatStatus, getStatusColor } from '@/utils/formatters';

interface StatusBadgeProps {
  status: string | null | undefined;
  size?: 'small' | 'default';
}

export default function StatusBadge({ status, size }: StatusBadgeProps) {
  if (!status) return <Tag>-</Tag>;
  
  const color = getStatusColor(status);
  const label = formatStatus(status);
  
  const colorMap: Record<string, string> = {
    success: 'green',
    warning: 'orange', 
    error: 'red',
    processing: 'blue',
    default: 'default',
  };
  
  return (
    <Tag color={colorMap[color] || 'default'} style={size === 'small' ? { fontSize: 11 } : undefined}>
      {label}
    </Tag>
  );
}
