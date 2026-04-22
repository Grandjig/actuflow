import { ReactNode } from 'react';
import { Empty, Button } from 'antd';
import { PlusOutlined } from '@ant-design/icons';

interface EmptyStateProps {
  title?: string;
  description?: string;
  icon?: ReactNode;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export default function EmptyState({
  title = 'No Data',
  description = 'No records found',
  icon,
  action,
}: EmptyStateProps) {
  return (
    <div
      style={{
        padding: 60,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <Empty
        image={icon || Empty.PRESENTED_IMAGE_SIMPLE}
        description={
          <>
            <div style={{ fontWeight: 500, marginBottom: 4 }}>{title}</div>
            <div style={{ color: '#8c8c8c' }}>{description}</div>
          </>
        }
      >
        {action && (
          <Button type="primary" icon={<PlusOutlined />} onClick={action.onClick}>
            {action.label}
          </Button>
        )}
      </Empty>
    </div>
  );
}
