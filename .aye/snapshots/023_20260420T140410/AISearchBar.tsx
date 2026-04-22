import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Modal,
  Input,
  List,
  Typography,
  Tag,
  Spin,
  Button,
  Space,
  message,
} from 'antd';
import {
  SearchOutlined,
  RobotOutlined,
  HistoryOutlined,
  ThunderboltOutlined,
  LikeOutlined,
  DislikeOutlined,
} from '@ant-design/icons';
import { useNaturalLanguageQuery, useQueryFeedback } from '@/hooks/useAI';
import { useAIStore } from '@/stores/aiStore';

interface AISearchBarProps {
  open: boolean;
  onClose: () => void;
}

export default function AISearchBar({ open, onClose }: AISearchBarProps) {
  const navigate = useNavigate();
  const inputRef = useRef<any>(null);
  const [query, setQuery] = useState('');
  const { lastResponse, queryHistory, isPending, error } = useAIStore();
  const nlQuery = useNaturalLanguageQuery();
  const feedback = useQueryFeedback();

  useEffect(() => {
    if (open && inputRef.current) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [open]);

  // Keyboard shortcut
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (!open) {
          // Open handled by parent
        }
      }
      if (e.key === 'Escape' && open) {
        onClose();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [open, onClose]);

  const handleSearch = () => {
    if (!query.trim()) return;
    nlQuery.mutate({ query: query.trim() });
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSearch();
    }
  };

  const handleExecuteAction = () => {
    if (lastResponse?.suggested_api_call) {
      const apiCall = lastResponse.suggested_api_call;
      // Navigate based on endpoint
      const endpoint = apiCall.endpoint;
      if (endpoint.includes('/policies')) {
        navigate('/policies', { state: { filters: apiCall.params } });
      } else if (endpoint.includes('/claims')) {
        navigate('/claims', { state: { filters: apiCall.params } });
      } else if (endpoint.includes('/calculations')) {
        navigate('/calculations', { state: { filters: apiCall.params } });
      }
      onClose();
    }
  };

  const handleFeedback = (wasHelpful: boolean) => {
    // In a real app, we'd have a query ID to reference
    message.success(wasHelpful ? 'Thanks for the feedback!' : 'We\'ll work on improving this.');
  };

  const recentQueries = queryHistory.slice(0, 5);

  return (
    <Modal
      open={open}
      onCancel={onClose}
      footer={null}
      width={700}
      closable={false}
      centered
      styles={{
        body: { padding: 0 },
      }}
    >
      <div style={{ padding: '16px 24px', borderBottom: '1px solid #f0f0f0' }}>
        <Input
          ref={inputRef}
          size="large"
          placeholder="Ask a question in plain English... (e.g., 'Show all lapsed policies from 2024')"
          prefix={<RobotOutlined style={{ color: '#8c8c8c' }} />}
          suffix={
            <Button
              type="primary"
              size="small"
              onClick={handleSearch}
              loading={isPending}
            >
              Ask
            </Button>
          }
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          bordered={false}
          style={{ fontSize: 16 }}
        />
      </div>

      <div style={{ maxHeight: 400, overflow: 'auto' }}>
        {isPending && (
          <div style={{ padding: 40, textAlign: 'center' }}>
            <Spin tip="Thinking..." />
          </div>
        )}

        {error && (
          <div style={{ padding: 24, color: '#ff4d4f' }}>
            <Typography.Text type="danger">{error}</Typography.Text>
          </div>
        )}

        {lastResponse && !isPending && (
          <div style={{ padding: 24 }}>
            <div style={{ marginBottom: 16 }}>
              <Tag color="purple" icon={<RobotOutlined />}>
                AI Interpretation
              </Tag>
            </div>

            <Typography.Paragraph>
              <strong>I understood:</strong> {lastResponse.explanation}
            </Typography.Paragraph>

            {lastResponse.parsed_intent.clarification_needed && (
              <Typography.Paragraph type="warning">
                {lastResponse.parsed_intent.clarification_question}
              </Typography.Paragraph>
            )}

            {lastResponse.suggested_api_call && (
              <div style={{ marginTop: 16 }}>
                <Button
                  type="primary"
                  icon={<ThunderboltOutlined />}
                  onClick={handleExecuteAction}
                >
                  Go to Results
                </Button>
              </div>
            )}

            <div style={{ marginTop: 16, paddingTop: 16, borderTop: '1px solid #f0f0f0' }}>
              <Typography.Text type="secondary">Was this helpful?</Typography.Text>
              <Space style={{ marginLeft: 8 }}>
                <Button
                  size="small"
                  icon={<LikeOutlined />}
                  onClick={() => handleFeedback(true)}
                />
                <Button
                  size="small"
                  icon={<DislikeOutlined />}
                  onClick={() => handleFeedback(false)}
                />
              </Space>
            </div>
          </div>
        )}

        {!lastResponse && !isPending && recentQueries.length > 0 && (
          <div style={{ padding: 16 }}>
            <Typography.Text type="secondary" style={{ padding: '0 8px' }}>
              <HistoryOutlined /> Recent queries
            </Typography.Text>
            <List
              size="small"
              dataSource={recentQueries}
              renderItem={(item) => (
                <List.Item
                  style={{ cursor: 'pointer', padding: '8px 16px' }}
                  onClick={() => setQuery(item.query)}
                >
                  <Typography.Text>{item.query}</Typography.Text>
                </List.Item>
              )}
            />
          </div>
        )}

        {!lastResponse && !isPending && recentQueries.length === 0 && (
          <div style={{ padding: 40, textAlign: 'center', color: '#8c8c8c' }}>
            <RobotOutlined style={{ fontSize: 40, marginBottom: 16 }} />
            <div>Ask me anything about your data</div>
            <div style={{ fontSize: 12, marginTop: 8 }}>
              Try: "Show me all active policies with sum assured over $1M"
            </div>
          </div>
        )}
      </div>

      <div
        style={{
          padding: '8px 24px',
          borderTop: '1px solid #f0f0f0',
          background: '#fafafa',
          fontSize: 12,
          color: '#8c8c8c',
        }}
      >
        Press <Tag>Enter</Tag> to search • <Tag>Esc</Tag> to close
      </div>
    </Modal>
  );
}
