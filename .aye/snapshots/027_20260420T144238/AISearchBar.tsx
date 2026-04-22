import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Modal, Input, List, Tag, Typography, Spin, Empty, Divider } from 'antd';
import {
  SearchOutlined,
  RobotOutlined,
  FileTextOutlined,
  CalculatorOutlined,
  TeamOutlined,
  HistoryOutlined,
  ArrowRightOutlined,
} from '@ant-design/icons';
import { useNaturalLanguageQuery } from '@/hooks/useAI';
import { useAIStore } from '@/stores/aiStore';

const { Text, Paragraph } = Typography;

interface AISearchBarProps {
  open: boolean;
  onClose: () => void;
}

interface SearchResult {
  type: string;
  title: string;
  description?: string;
  path: string;
  icon: React.ReactNode;
}

const typeIcons: Record<string, React.ReactNode> = {
  policy: <FileTextOutlined />,
  calculation: <CalculatorOutlined />,
  policyholder: <TeamOutlined />,
  assumption: <FileTextOutlined />,
};

export default function AISearchBar({ open, onClose }: AISearchBarProps) {
  const navigate = useNavigate();
  const inputRef = useRef<any>(null);
  const [query, setQuery] = useState('');
  const [showResults, setShowResults] = useState(false);

  const { queryHistory } = useAIStore();
  const nlQuery = useNaturalLanguageQuery();

  // Focus input when modal opens
  useEffect(() => {
    if (open) {
      setTimeout(() => inputRef.current?.focus(), 100);
    } else {
      setQuery('');
      setShowResults(false);
    }
  }, [open]);

  // Keyboard shortcut
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (!open) {
          // Would need to call parent to open
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [open]);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setShowResults(true);
    await nlQuery.mutateAsync({ query });
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
    if (e.key === 'Escape') {
      onClose();
    }
  };

  const handleResultClick = (result: any) => {
    if (result.suggested_action) {
      // Navigate based on action
      const { action, parameters } = result.suggested_action;
      if (action === 'navigate' && parameters.path) {
        navigate(parameters.path);
      } else if (action === 'filter') {
        // Apply filters to list page
        navigate(`/policies?${new URLSearchParams(parameters).toString()}`);
      }
    }
    onClose();
  };

  const recentQueries = queryHistory.slice(0, 5);

  return (
    <Modal
      open={open}
      onCancel={onClose}
      footer={null}
      closable={false}
      width={600}
      style={{ top: 100 }}
      styles={{ body: { padding: 0 } }}
    >
      <div style={{ padding: '16px 16px 0' }}>
        <Input
          ref={inputRef}
          size="large"
          placeholder="Ask anything... e.g., 'Show lapsed policies from 2024'"
          prefix={<SearchOutlined style={{ color: '#bfbfbf' }} />}
          suffix={
            <Tag color="blue" style={{ margin: 0 }}>
              <RobotOutlined /> AI
            </Tag>
          }
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          bordered={false}
          style={{ fontSize: 16 }}
        />
      </div>

      <Divider style={{ margin: '8px 0' }} />

      <div style={{ maxHeight: 400, overflow: 'auto', padding: '0 8px 16px' }}>
        {nlQuery.isPending && (
          <div style={{ textAlign: 'center', padding: 32 }}>
            <Spin tip="Analyzing your query..." />
          </div>
        )}

        {nlQuery.data && showResults && (
          <div style={{ padding: '0 8px' }}>
            <Text type="secondary" style={{ fontSize: 12, textTransform: 'uppercase' }}>
              AI Interpretation
            </Text>
            <div
              style={{
                background: '#f6ffed',
                border: '1px solid #b7eb8f',
                borderRadius: 8,
                padding: 16,
                marginTop: 8,
                cursor: 'pointer',
              }}
              onClick={() => handleResultClick(nlQuery.data)}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <Tag color="blue">{nlQuery.data.parsed_intent?.type}</Tag>
                  <Paragraph style={{ margin: '8px 0 0' }}>
                    {nlQuery.data.explanation}
                  </Paragraph>
                  {nlQuery.data.result_count !== undefined && (
                    <Text type="secondary">
                      Found {nlQuery.data.result_count} matching records
                    </Text>
                  )}
                </div>
                <ArrowRightOutlined style={{ fontSize: 20, color: '#52c41a' }} />
              </div>
            </div>
          </div>
        )}

        {!showResults && recentQueries.length > 0 && (
          <div style={{ padding: '0 8px' }}>
            <Text type="secondary" style={{ fontSize: 12, textTransform: 'uppercase' }}>
              <HistoryOutlined /> Recent Queries
            </Text>
            <List
              dataSource={recentQueries}
              renderItem={(q) => (
                <List.Item
                  style={{ cursor: 'pointer', padding: '8px 0' }}
                  onClick={() => {
                    setQuery(q);
                    // Could auto-search
                  }}
                >
                  <Text>{q}</Text>
                </List.Item>
              )}
            />
          </div>
        )}

        {!showResults && !nlQuery.isPending && recentQueries.length === 0 && (
          <Empty
            image={Empty.PRESENTED_IMAGE_SIMPLE}
            description={
              <span>
                Ask questions in natural language
                <br />
                <Text type="secondary" style={{ fontSize: 12 }}>
                  e.g., "Show policies with premium over $1000"
                </Text>
              </span>
            }
          />
        )}
      </div>

      <div
        style={{
          borderTop: '1px solid #f0f0f0',
          padding: '8px 16px',
          display: 'flex',
          justifyContent: 'space-between',
          fontSize: 12,
          color: '#8c8c8c',
        }}
      >
        <span>
          <Tag>Enter</Tag> to search
          <Tag style={{ marginLeft: 8 }}>Esc</Tag> to close
        </span>
        <span>Powered by AI</span>
      </div>
    </Modal>
  );
}
