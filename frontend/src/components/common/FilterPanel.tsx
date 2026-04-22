import { Card, Form, Select, DatePicker, Input, Button, Space, Row, Col } from 'antd';
import { FilterOutlined, ClearOutlined } from '@ant-design/icons';
import type { FilterConfig } from '@/types/ui';

const { RangePicker } = DatePicker;

interface FilterPanelProps {
  config: FilterConfig[];
  values: Record<string, unknown>;
  onChange: (values: Record<string, unknown>) => void;
  onReset: () => void;
}

export default function FilterPanel({
  config,
  values,
  onChange,
  onReset,
}: FilterPanelProps) {
  const handleChange = (key: string, value: unknown) => {
    onChange({ ...values, [key]: value });
  };

  const renderFilter = (filter: FilterConfig) => {
    switch (filter.type) {
      case 'select':
        return (
          <Select
            placeholder={filter.placeholder || `Select ${filter.label}`}
            options={filter.options}
            value={values[filter.key] as string}
            onChange={(value) => handleChange(filter.key, value)}
            allowClear
            style={{ width: '100%' }}
          />
        );
      case 'multiSelect':
        return (
          <Select
            mode="multiple"
            placeholder={filter.placeholder || `Select ${filter.label}`}
            options={filter.options}
            value={values[filter.key] as string[]}
            onChange={(value) => handleChange(filter.key, value)}
            allowClear
            style={{ width: '100%' }}
          />
        );
      case 'dateRange':
        return (
          <RangePicker
            style={{ width: '100%' }}
            onChange={(dates) => {
              if (dates) {
                handleChange(`${filter.key}_from`, dates[0]?.format('YYYY-MM-DD'));
                handleChange(`${filter.key}_to`, dates[1]?.format('YYYY-MM-DD'));
              } else {
                handleChange(`${filter.key}_from`, undefined);
                handleChange(`${filter.key}_to`, undefined);
              }
            }}
          />
        );
      case 'date':
        return (
          <DatePicker
            style={{ width: '100%' }}
            onChange={(date) => handleChange(filter.key, date?.format('YYYY-MM-DD'))}
          />
        );
      default:
        return (
          <Input
            placeholder={filter.placeholder || filter.label}
            value={values[filter.key] as string}
            onChange={(e) => handleChange(filter.key, e.target.value)}
            allowClear
          />
        );
    }
  };

  return (
    <Card size="small" style={{ marginBottom: 16 }}>
      <Row gutter={[16, 16]} align="middle">
        {config.map((filter) => (
          <Col key={filter.key} xs={24} sm={12} md={8} lg={6}>
            <Form.Item label={filter.label} style={{ marginBottom: 0 }}>
              {renderFilter(filter)}
            </Form.Item>
          </Col>
        ))}
        <Col>
          <Space>
            <Button icon={<ClearOutlined />} onClick={onReset}>
              Clear
            </Button>
          </Space>
        </Col>
      </Row>
    </Card>
  );
}
