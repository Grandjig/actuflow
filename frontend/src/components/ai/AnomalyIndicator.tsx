import { Tooltip, Tag, Space } from 'antd';
import { WarningOutlined, ExclamationCircleOutlined } from '@ant-design/icons';

interface AnomalyIndicatorProps {
  score: number;
  reasons?: string[];
  size?: 'small' | 'default';
}

export default function AnomalyIndicator({
  score,
  reasons = [],
  size = 'default',
}: AnomalyIndicatorProps) {
  const severity = score > 0.8 ? 'high' : score > 0.5 ? 'medium' : 'low';
  const color = severity === 'high' ? '#ff4d4f' : severity === 'medium' ? '#faad14' : '#52c41a';

  const tooltipContent = (
    <div>
      <div style={{ fontWeight: 'bold', marginBottom: 4 }}>
        Anomaly Score: {(score * 100).toFixed(0)}%
      </div>
      {reasons.length > 0 && (
        <ul style={{ margin: 0, paddingLeft: 16 }}>
          {reasons.map((reason, index) => (
            <li key={index}>{reason}</li>
          ))}
        </ul>
      )}
    </div>
  );

  return (
    <Tooltip title={tooltipContent}>
      <Tag
        color={severity === 'high' ? 'error' : severity === 'medium' ? 'warning' : 'success'}
        icon={severity === 'high' ? <ExclamationCircleOutlined /> : <WarningOutlined />}
        style={size === 'small' ? { fontSize: 11 } : undefined}
      >
        {severity === 'high' ? 'High Risk' : severity === 'medium' ? 'Review' : 'Normal'}
      </Tag>
    </Tooltip>
  );
}
