import type { ReactNode } from 'react';

// Breadcrumb types
export interface BreadcrumbItem {
  title: string;
  path?: string;
}

// Filter types
export interface FilterConfig {
  key: string;
  label: string;
  type: 'text' | 'select' | 'date' | 'dateRange' | 'number';
  placeholder?: string;
  options?: Array<{ label: string; value: string | number | boolean }>;
}

// Table types
export interface TableColumn<T> {
  key: string;
  title: string;
  dataIndex?: keyof T | string[];
  render?: (value: unknown, record: T, index: number) => ReactNode;
  sorter?: boolean;
  width?: number | string;
  align?: 'left' | 'center' | 'right';
  fixed?: 'left' | 'right';
  ellipsis?: boolean;
}

// Widget types
export interface StatCardData {
  title: string;
  value: string | number;
  change?: number;
  changeType?: 'increase' | 'decrease' | 'neutral';
  icon?: ReactNode;
  color?: string;
}

// Chart types
export interface ChartDataPoint {
  name: string;
  value: number;
  [key: string]: string | number;
}

export interface LineChartConfig {
  data: ChartDataPoint[];
  xAxisKey: string;
  lines: Array<{
    dataKey: string;
    name: string;
    color?: string;
  }>;
}

export interface BarChartConfig {
  data: ChartDataPoint[];
  xAxisKey: string;
  bars: Array<{
    dataKey: string;
    name: string;
    color?: string;
    stackId?: string;
  }>;
}

export interface PieChartConfig {
  data: Array<{
    name: string;
    value: number;
    color?: string;
  }>;
}

// Form types
export interface FormFieldConfig {
  name: string;
  label: string;
  type: 'text' | 'number' | 'select' | 'date' | 'textarea' | 'switch' | 'radio';
  placeholder?: string;
  required?: boolean;
  rules?: Array<{
    required?: boolean;
    message?: string;
    pattern?: RegExp;
    min?: number;
    max?: number;
  }>;
  options?: Array<{ label: string; value: string | number }>;
  span?: number;
}

// Modal types
export interface ConfirmModalConfig {
  title: string;
  content: string;
  okText?: string;
  cancelText?: string;
  danger?: boolean;
  onOk: () => void | Promise<void>;
  onCancel?: () => void;
}

// Menu types
export interface MenuItem {
  key: string;
  label: string;
  icon?: ReactNode;
  path?: string;
  children?: MenuItem[];
  permission?: { resource: string; action: string };
}

// Action types
export interface ActionItem {
  key: string;
  label: string;
  icon?: ReactNode;
  onClick: () => void;
  danger?: boolean;
  disabled?: boolean;
}
