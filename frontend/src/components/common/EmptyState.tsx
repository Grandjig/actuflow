import { Empty, Button, Typography } from 'antd';
import { PlusOutlined } from '@ant-design/icons';

interface EmptyStateProps {
  title?: string;
  description?: string;
  action?: {
    label: string;
    onClick: () => void;
    icon?: React.ReactNode;
  };
  image?: React.ReactNode;
}

export default function EmptyState({
  title = 'No Data',
  description = 'No items found',
  action,
  image,
}: EmptyStateProps) {
  return (
    <Empty
      image={image || Empty.PRESENTED_IMAGE_SIMPLE}
      description={
        <div>
          <Typography.Text strong style={{ display: 'block', marginBottom: 4 }}>
            {title}
          </Typography.Text>
          <Typography.Text type="secondary">{description}</Typography.Text>
        </div>
      }
    >
      {action && (
        <Button
          type="primary"
          icon={action.icon || <PlusOutlined />}
          onClick={action.onClick}
        >
          {action.label}
        </Button>
      )}
    </Empty>
  );
}
