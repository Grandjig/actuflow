import { Modal, Typography } from 'antd';
import { ExclamationCircleOutlined } from '@ant-design/icons';

interface ConfirmModalProps {
  open: boolean;
  title: string;
  content: string;
  onConfirm: () => void | Promise<void>;
  onCancel: () => void;
  confirmText?: string;
  cancelText?: string;
  danger?: boolean;
  loading?: boolean;
}

export default function ConfirmModal({
  open,
  title,
  content,
  onConfirm,
  onCancel,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  danger = false,
  loading = false,
}: ConfirmModalProps) {
  return (
    <Modal
      open={open}
      title={
        <span>
          <ExclamationCircleOutlined
            style={{ color: danger ? '#ff4d4f' : '#faad14', marginRight: 8 }}
          />
          {title}
        </span>
      }
      onOk={onConfirm}
      onCancel={onCancel}
      okText={confirmText}
      cancelText={cancelText}
      okButtonProps={{ danger, loading }}
      centered
    >
      <Typography.Paragraph>{content}</Typography.Paragraph>
    </Modal>
  );
}
