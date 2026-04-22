/**
 * AI-powered search bar component.
 */

import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input, Modal, List, Typography, Tag, Space, Spin } from 'antd';
import { SearchOutlined, RobotOutlined } from '@ant-design/icons';
import { useMutation } from '@tanstack/react-query';
import { sendNaturalLanguageQuery } from '@/api/ai';
import { getResourceUrl } from '@/utils/helpers';

const { Text } = Typography;

interface SearchResult {
  type: string;
  id: string;
  title: string;
  description?: string;
  score?: number;
}

interface QueryResponse {
  intent: string;
  results: SearchResult[];
  message?: string;
}

export default function AISearchBar() {
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);

  const mutation = useMutation({
    mutationFn: sendNaturalLanguageQuery,
    onSuccess: (data: QueryResponse) => {
      setResults(data.results || []);
    },
  });

  const handleSearch = useCallback(() => {
    if (query.trim()) {
      mutation.mutate(query);
    }
  }, [query, mutation]);

  const handleResultClick = (result: SearchResult) => {
    const url = getResourceUrl(result.type, result.id);
    navigate(url);
    setIsOpen(false);
    setQuery('');
    setResults([]);
  };

  return (
    <>
      <Input
        placeholder="Search or ask a question..."
        prefix={<SearchOutlined />}
        suffix={<RobotOutlined style={{ color: '#1890ff' }} />}
        onClick={() => setIsOpen(true)}
        readOnly
        style={{ width: 300, cursor: 'pointer' }}
      />

      <Modal
        title={
          <Space>
            <RobotOutlined />
            <span>AI Search</span>
          </Space>
        }
        open={isOpen}
        onCancel={() => {
          setIsOpen(false);
          setQuery('');
          setResults([]);
        }}
        footer={null}
        width={600}
      >
        <Input.Search
          placeholder="Ask a question in plain English..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onSearch={handleSearch}
          loading={mutation.isPending}
          enterButton="Search"
          size="large"
          style={{ marginBottom: 16 }}
        />

        <Text type="secondary" style={{ display: 'block', marginBottom: 16 }}>
          Try: "Show me all lapsed policies from Q1" or "Find claims over $100k"
        </Text>

        {mutation.isPending && (
          <div style={{ textAlign: 'center', padding: 20 }}>
            <Spin />
            <Text style={{ marginLeft: 8 }}>Analyzing your query...</Text>
          </div>
        )}

        {results.length > 0 && (
          <List
            dataSource={results}
            renderItem={(item) => (
              <List.Item
                onClick={() => handleResultClick(item)}
                style={{ cursor: 'pointer' }}
              >
                <List.Item.Meta
                  title={
                    <Space>
                      <Tag>{item.type}</Tag>
                      <span>{item.title}</span>
                    </Space>
                  }
                  description={item.description}
                />
              </List.Item>
            )}
          />
        )}

        {mutation.isSuccess && results.length === 0 && (
          <Text type="secondary">No results found. Try a different query.</Text>
        )}
      </Modal>
    </>
  );
}
