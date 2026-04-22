import { useState } from 'react';
import { Input, Card, List, Tag, Typography, Spin, Empty } from 'antd';
import { SearchOutlined, RobotOutlined, ArrowRightOutlined } from '@ant-design/icons';
import type { NLQueryResponse } from '@/types/ai';
import { post } from '@/api/client';

const { Text, Paragraph } = Typography;
const { Search } = Input;

interface NaturalLanguageInputProps {
  onAction?: (action: { action: string; parameters: Record<string, unknown> }) => void;
  placeholder?: string;
  context?: Record<string, unknown>;
}

export default function NaturalLanguageInput({
  onAction,
  placeholder = 'Ask anything... e.g., "Show me lapsed policies from Q1"',
  context,
}: NaturalLanguageInputProps) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<NLQueryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (query: string) => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await post<NLQueryResponse>('/ai/query', {
        query,
        context,
      });
      setResult(response);
    } catch (err: any) {
      setError(err.message || 'Failed to process query');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const handleExecuteAction = () => {
    if (result?.suggested_action && onAction) {
      onAction({
        action: result.suggested_action.action,
        parameters: result.suggested_action.parameters,
      });
    }
  };

  return (
    <div>
      <Search
        placeholder={placeholder}
        enterButton={
          <span>
            <RobotOutlined /> Ask AI
          </span>
        }
        size="large"
        onSearch={handleSearch}
        loading={loading}
        allowClear
        style={{ marginBottom: 16 }}
      />

      {loading && (
        <Card>
          <div style={{ textAlign: 'center', padding: 24 }}>
            <Spin tip="Analyzing your query..." />
          </div>
        </Card>
      )}

      {error && (
        <Card>
          <Text type="danger">{error}</Text>
        </Card>
      )}

      {result && !loading && (
        <Card>
          <div style={{ marginBottom: 16 }}>
            <Text type="secondary">Interpreted as:</Text>
            <Paragraph style={{ marginTop: 4 }}>
              <Tag color="blue">{result.parsed_intent.type}</Tag>
              {result.explanation}
            </Paragraph>
          </div>

          {result.suggested_action && (
            <div
              style={{
                background: '#f6ffed',
                border: '1px solid #b7eb8f',
                borderRadius: 6,
                padding: 16,
                cursor: 'pointer',
              }}
              onClick={handleExecuteAction}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <Text strong>Suggested Action</Text>
                  <Paragraph style={{ margin: '4px 0' }}>
                    {result.suggested_action.explanation}
                  </Paragraph>
                  <Tag color="green">{result.suggested_action.action}</Tag>
                </div>
                <ArrowRightOutlined style={{ fontSize: 20, color: '#52c41a' }} />
              </div>
            </div>
          )}

          {result.result_count !== undefined && (
            <div style={{ marginTop: 12 }}>
              <Text type="secondary">
                Found {result.result_count} matching records
              </Text>
            </div>
          )}
        </Card>
      )}
    </div>
  );
}
