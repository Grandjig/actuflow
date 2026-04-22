// UI-related types

import type { ReactNode } from 'react';

export interface BreadcrumbItem {
  title: string;
  path?: string;
}

export interface MenuItem {
  key: string;
  label: string;
  icon?: ReactNode;
  path?: string;
  children?: MenuItem[];
  permission?: string;
}

export interface FilterConfig {
  key: string;
  label: string;
  type: 'text' | 'select' | 'multiSelect' | 'date' | 'dateRange' | 'number' | 'boolean';
  options?: { label: string; value: string | number | boolean }[];
  placeholder?: string;
  defaultValue?: unknown;
}

export interface TableColumn<T = unknown> {
  key: string;
  title: string;
  dataIndex?: string | string[];
  render?: (value: unknown, record: T, index: number) => ReactNode;
  sorter?: boolean;
  width?: number | string;
  align?: 'left' | 'center' | 'right';
  ellipsis?: boolean;
  fixed?: 'left' | 'right';
}

export interface ChartConfig {
  type: 'line' | 'bar' | 'pie' | 'doughnut' | 'area';
  title?: string;
  xAxis?: string;
  yAxis?: string;
  colors?: string[];
  stacked?: boolean;
  showLegend?: boolean;
}

export interface WidgetConfig {
  id: string;
  type: string;
  title: string;
  size: 'small' | 'medium' | 'large';
  position: { x: number; y: number; w: number; h: number };
  config?: Record<string, unknown>;
}

export interface FormField {
  name: string;
  label: string;
  type: 'text' | 'number' | 'select' | 'date' | 'textarea' | 'checkbox' | 'radio';
  required?: boolean;
  placeholder?: string;
  options?: { label: string; value: string | number }[];
  rules?: unknown[];
  dependencies?: string[];
}

export interface ModalConfig {
  title: string;
  width?: number;
  closable?: boolean;
  maskClosable?: boolean;
  footer?: ReactNode | null;
}

export interface ToastMessage {
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  description?: string;
  duration?: number;
}
