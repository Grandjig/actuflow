import { Spin } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';

interface LoadingSpinnerProps {
  size?: 'small' | 'default' | 'large';
  tip?: string;
  fullScreen?: boolean;
}

export default function LoadingSpinner({
  size = 'default',
  tip,
  fullScreen = false,
}: LoadingSpinnerProps) {
  const spinner = (
    <Spin
      indicator={<LoadingOutlined spin />}
      size={size}
      tip={tip}
    />
  );

  if (fullScreen) {
    return (
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '100vh',
          width: '100%',
        }}
      >
        {spinner}
      </div>
    );
  }

  return spinner;
}
