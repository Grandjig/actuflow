import { Tag, Badge } from 'antd';
import { STATUS_COLORS } from '@/utils/constants';
import { formatStatus } from '@/utils/formatters';

interface StatusBadgeProps {
  status: string;
  type?: 'tag' | 'badge';
  showDot?: boolean;
}

export default function StatusBadge({
  status,
  type = 'tag',
  showDot = false,
}: StatusBadgeProps) {
  const color = STATUS_COLORS[status] || 'default';
  const label = formatStatus(status);

  if (type === 'badge') {
    const badgeStatus = color === 'green' ? 'success' :
                        color === 'red' ? 'error' :
                        color === 'gold' || color === 'orange' ? 'warning' :
                        color === 'processing' ? 'processing' : 'default';
    
    return <Badge status={badgeStatus} text={label} />;
  }

  return <Tag color={color}>{label}</Tag>;
}
