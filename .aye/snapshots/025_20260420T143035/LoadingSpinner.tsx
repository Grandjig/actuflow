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
  const icon = <LoadingOutlined style={{ fontSize: size === 'large' ? 48 : size === 'small' ? 16 : 24 }} spin />;

  if (fullScreen) {
    return (
      <div
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'rgba(255, 255, 255, 0.8)',
          zIndex: 1000,
        }}
      >
        <Spin indicator={icon} tip={tip} size={size} />
      </div>
    );
  }

  return (
    <div style={{ textAlign: 'center', padding: 48 }}>
      <Spin indicator={icon} tip={tip} size={size} />
    </div>
  );
}
