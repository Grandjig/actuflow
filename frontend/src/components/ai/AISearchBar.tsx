import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Modal, Input, List, Space, Tag, Typography, Spin } from 'antd';
import {
  SearchOutlined,
  RobotOutlined,
  FileTextOutlined,
  CalculatorOutlined,
  TeamOutlined,
  HistoryOutlined,
} from '@ant-design/icons';

import { useNaturalLanguageQuery } from '@/hooks/useAI';
import { useAIStore } from '@/stores/aiStore';
import { getResourceUrl } from '@/utils/helpers';

const { Text } = Typography;

interface AISearchBarProps {
  open: boolean;
  onClose: () => void;
}

export default function AISearchBar({ open, onClose }: AISearchBarProps) {
  const navigate = useNavigate();
  const inputRef = useRef<any>(null);
  const [query, setQuery] = useState('');
  const { queryHistory } = useAIStore();
  const nlQuery = useNaturalLanguageQuery();

  useEffect(() => {
    if (open && inputRef.current) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [open]);

  useEffect(() => {
    if (!open) {
      setQuery('');
    }
  }, [open]);

  const handleSearch = async () => {
    if (!query.trim()) return;

    try {
      const result = await nlQuery.mutateAsync({ query });

      // Navigate based on result
      if (result.suggested_api_call) {
        const { endpoint, params } = result.suggested_api_call;
        const searchParams = new URLSearchParams();
        Object.entries(params || {}).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            searchParams.set(key, String(value));
          }
        });

        // Map endpoint to route
        const routeMap: Record<string, string> = {
          '/api/v1/policies': '/policies',
          '/api/v1/claims': '/claims',
          '/api/v1/calculations': '/calculations',
          '/api/v1/assumptions': '/assumptions',
        };

        const route = routeMap[endpoint] || '/policies';
        navigate(`${route}?${searchParams.toString()}`);
        onClose();
      }
    } catch (error) {
      // Error handled by mutation
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    } else if (e.key === 'Escape') {
      onClose();
    }
  };

  const handleHistoryClick = (historicQuery: string) => {
    setQuery(historicQuery);
  };

  const suggestions = [
    { icon: <FileTextOutlined />, text: 'Show all active policies', category: 'Policies' },
    { icon: <TeamOutlined />, text: 'Find claims over $100,000', category: 'Claims' },
    { icon: <CalculatorOutlined />, text: 'Recent calculation runs', category: 'Calculations' },
  ];

  return (
    <Modal
      open={open}
      onCancel={onClose}
      footer={null}
      closable={false}
      width={640}
      style={{ top: 100 }}
      styles={{ body: { padding: 0 } }}
    >
      <div style={{ padding: 16 }}>
        <Input
          ref={inputRef}
          size="large"
          placeholder="Ask a question or search... (e.g., 'Show lapsed policies from Q1')"
          prefix={<RobotOutlined style={{ color: '#722ed1' }} />}
          suffix={nlQuery.isPending ? <Spin size="small" /> : <SearchOutlined />}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          style={{ borderRadius: 8 }}
        />
      </div>

      {nlQuery.data && (
        <div style={{ padding: '0 16px 16px' }}>
          <div
            style={{
              background: '#f6ffed',
              border: '1px solid #b7eb8f',
              borderRadius: 8,
              padding: 12,
            }}
          >
            <Space direction="vertical" style={{ width: '100%' }}>
              <Text strong>Understood:</Text>
              <Text>{nlQuery.data.explanation}</Text>
              {nlQuery.data.result_count !== undefined && (
                <Text type="secondary">
                  Found {nlQuery.data.result_count} results
                </Text>
              )}
            </Space>
          </div>
        </div>
      )}

      {!query && !nlQuery.data && (
        <div style={{ padding: '0 16px 16px' }}>
          {queryHistory.length > 0 && (
            <>
              <Text type="secondary" style={{ fontSize: 12 }}>
                <HistoryOutlined /> Recent Searches
              </Text>
              <List
                size="small"
                dataSource={queryHistory.slice(0, 5)}
                renderItem={(item) => (
                  <List.Item
                    style={{ cursor: 'pointer', padding: '8px 0' }}
                    onClick={() => handleHistoryClick(item)}
                  >
                    <Text>{item}</Text>
                  </List.Item>
                )}
                style={{ marginBottom: 16 }}
              />
            </>
          )}

          <Text type="secondary" style={{ fontSize: 12 }}>
            Try asking:
          </Text>
          <List
            size="small"
            dataSource={suggestions}
            renderItem={(item) => (
              <List.Item
                style={{ cursor: 'pointer', padding: '8px 0' }}
                onClick={() => setQuery(item.text)}
              >
                <Space>
                  {item.icon}
                  <Text>{item.text}</Text>
                  <Tag>{item.category}</Tag>
                </Space>
              </List.Item>
            )}
          />
        </div>
      )}

      <div
        style={{
          padding: '8px 16px',
          borderTop: '1px solid #f0f0f0',
          background: '#fafafa',
          borderRadius: '0 0 8px 8px',
        }}
      >
        <Space>
          <Tag>Enter</Tag>
          <Text type="secondary">to search</Text>
          <Tag>Esc</Tag>
          <Text type="secondary">to close</Text>
        </Space>
      </div>
    </Modal>
  );
}
