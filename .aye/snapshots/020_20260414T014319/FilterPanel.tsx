import { useState } from 'react';
import {
  Card,
  Form,
  Select,
  DatePicker,
  InputNumber,
  Input,
  Button,
  Space,
  Collapse,
} from 'antd';
import { FilterOutlined, ClearOutlined } from '@ant-design/icons';
import type { FilterConfig } from '@/types/ui';

const { RangePicker } = DatePicker;
const { Panel } = Collapse;

interface FilterPanelProps {
  filters: FilterConfig[];
  values: Record<string, unknown>;
  onChange: (values: Record<string, unknown>) => void;
  onReset: () => void;
  collapsed?: boolean;
}

export default function FilterPanel({
  filters,
  values,
  onChange,
  onReset,
  collapsed = true,
}: FilterPanelProps) {
  const [form] = Form.useForm();

  const handleValuesChange = (_: unknown, allValues: Record<string, unknown>) => {
    onChange(allValues);
  };

  const handleReset = () => {
    form.resetFields();
    onReset();
  };

  const renderFilterField = (filter: FilterConfig) => {
    switch (filter.type) {
      case 'select':
        return (
          <Select
            placeholder={filter.placeholder || `Select ${filter.label}`}
            options={filter.options}
            allowClear
            style={{ minWidth: 150 }}
          />
        );
      case 'date':
        return <DatePicker placeholder={filter.placeholder} style={{ width: '100%' }} />;
      case 'dateRange':
        return <RangePicker style={{ width: '100%' }} />;
      case 'number':
        return (
          <InputNumber
            placeholder={filter.placeholder}
            style={{ width: '100%' }}
          />
        );
      case 'text':
      default:
        return <Input placeholder={filter.placeholder} allowClear />;
    }
  };

  const content = (
    <Form
      form={form}
      layout="inline"
      initialValues={values}
      onValuesChange={handleValuesChange}
      style={{ flexWrap: 'wrap', gap: 8 }}
    >
      {filters.map((filter) => (
        <Form.Item key={filter.key} name={filter.key} label={filter.label}>
          {renderFilterField(filter)}
        </Form.Item>
      ))}
      <Form.Item>
        <Button icon={<ClearOutlined />} onClick={handleReset}>
          Clear
        </Button>
      </Form.Item>
    </Form>
  );

  if (collapsed) {
    return (
      <Collapse
        ghost
        items={[
          {
            key: 'filters',
            label: (
              <Space>
                <FilterOutlined />
                Filters
              </Space>
            ),
            children: content,
          },
        ]}
      />
    );
  }

  return <Card size="small">{content}</Card>;
}
