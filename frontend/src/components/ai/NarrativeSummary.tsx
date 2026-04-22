import { useState } from 'react';
import { Card, Typography, Button, Input, Space, Tag, Tooltip } from 'antd';
import {
  RobotOutlined,
  EditOutlined,
  SaveOutlined,
  CloseOutlined,
  CopyOutlined,
} from '@ant-design/icons';
import { message } from 'antd';
import { copyToClipboard } from '@/utils/helpers';

const { TextArea } = Input;
const { Paragraph } = Typography;

interface NarrativeSummaryProps {
  text: string;
  onSave?: (newText: string) => void;
  editable?: boolean;
  loading?: boolean;
  title?: string;
}

export default function NarrativeSummary({
  text,
  onSave,
  editable = true,
  loading = false,
  title = 'AI Summary',
}: NarrativeSummaryProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedText, setEditedText] = useState(text);

  const handleSave = () => {
    if (onSave) {
      onSave(editedText);
    }
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditedText(text);
    setIsEditing(false);
  };

  const handleCopy = async () => {
    const success = await copyToClipboard(text);
    if (success) {
      message.success('Copied to clipboard');
    }
  };

  return (
    <Card
      size="small"
      title={
        <Space>
          <RobotOutlined style={{ color: '#722ed1' }} />
          {title}
          <Tag color="purple" style={{ marginLeft: 8 }}>
            AI Generated
          </Tag>
        </Space>
      }
      extra={
        <Space>
          {!isEditing && (
            <>
              <Tooltip title="Copy to clipboard">
                <Button icon={<CopyOutlined />} size="small" onClick={handleCopy} />
              </Tooltip>
              {editable && (
                <Tooltip title="Edit">
                  <Button
                    icon={<EditOutlined />}
                    size="small"
                    onClick={() => setIsEditing(true)}
                  />
                </Tooltip>
              )}
            </>
          )}
          {isEditing && (
            <>
              <Button
                icon={<SaveOutlined />}
                size="small"
                type="primary"
                onClick={handleSave}
              >
                Save
              </Button>
              <Button icon={<CloseOutlined />} size="small" onClick={handleCancel}>
                Cancel
              </Button>
            </>
          )}
        </Space>
      }
      loading={loading}
      style={{ backgroundColor: '#faf5ff' }}
    >
      {isEditing ? (
        <TextArea
          value={editedText}
          onChange={(e) => setEditedText(e.target.value)}
          autoSize={{ minRows: 3, maxRows: 10 }}
        />
      ) : (
        <Paragraph style={{ marginBottom: 0, whiteSpace: 'pre-wrap' }}>{text}</Paragraph>
      )}
    </Card>
  );
}
