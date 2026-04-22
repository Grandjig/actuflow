import { Card, Form, Input, Select, DatePicker, Button, Space, Row, Col } from 'antd';
import { FilterOutlined, ClearOutlined } from '@ant-design/icons';
import type { FilterConfig } from '@/types/ui';

const { RangePicker } = DatePicker;

interface FilterPanelProps {
  filters?: FilterConfig[];
  config?: FilterConfig[]; // Alias
  values: Record<string, unknown>;
  onChange: (values: Record<string, unknown>) => void;
  onReset: () => void;
  loading?: boolean;
}

export default function FilterPanel({
  filters,
  config,
  values,
  onChange,
  onReset,
  loading,
}: FilterPanelProps) {
  const filterConfigs = filters || config || [];
  const [form] = Form.useForm();

  const handleValuesChange = (_: unknown, allValues: Record<string, unknown>) => {
    // Handle date range conversion
    const processedValues: Record<string, unknown> = {};
    Object.entries(allValues).forEach(([key, value]) => {
      if (Array.isArray(value) && value[0]?.format) {
        // It's a date range
        processedValues[`${key}_from`] = value[0].format('YYYY-MM-DD');
        processedValues[`${key}_to`] = value[1].format('YYYY-MM-DD');
      } else if (value !== undefined && value !== '') {
        processedValues[key] = value;
      }
    });
    onChange(processedValues);
  };

  const handleReset = () => {
    form.resetFields();
    onReset();
  };

  const renderFilterInput = (filter: FilterConfig) => {
    switch (filter.type) {
      case 'select':
        return (
          <Select
            placeholder={filter.placeholder || `Select ${filter.label}`}
            options={filter.options}
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
            allowClear
            style={{ width: '100%' }}
          />
        );
      case 'date':
        return (
          <DatePicker
            placeholder={filter.placeholder}
            style={{ width: '100%' }}
          />
        );
      case 'dateRange':
        return <RangePicker style={{ width: '100%' }} />;
      case 'number':
        return (
          <Input
            type="number"
            placeholder={filter.placeholder}
          />
        );
      default:
        return (
          <Input
            placeholder={filter.placeholder || `Enter ${filter.label}`}
          />
        );
    }
  };

  return (
    <Card size="small" style={{ marginBottom: 16 }}>
      <Form
        form={form}
        layout="vertical"
        initialValues={values}
        onValuesChange={handleValuesChange}
      >
        <Row gutter={16}>
          {filterConfigs.map((filter) => (
            <Col key={filter.key} xs={24} sm={12} md={8} lg={6} xl={4}>
              <Form.Item
                name={filter.key}
                label={filter.label}
                style={{ marginBottom: 12 }}
              >
                {renderFilterInput(filter)}
              </Form.Item>
            </Col>
          ))}
          <Col xs={24} sm={12} md={8} lg={6} xl={4}>
            <Form.Item label=" " style={{ marginBottom: 12 }}>
              <Space>
                <Button
                  icon={<ClearOutlined />}
                  onClick={handleReset}
                >
                  Reset
                </Button>
              </Space>
            </Form.Item>
          </Col>
        </Row>
      </Form>
    </Card>
  );
}
