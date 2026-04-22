// UI-related types

import type { ReactNode } from 'react';

export interface MenuItem {
  key: string;
  label: string;
  icon?: ReactNode;
  path?: string;
  children?: MenuItem[];
  permission?: string;
}

export interface BreadcrumbItem {
  title: string;
  path?: string;
}

export interface TableColumn<T> {
  key: string;
  title: string;
  dataIndex?: keyof T | string[];
  width?: number | string;
  fixed?: 'left' | 'right';
  sortable?: boolean;
  filterable?: boolean;
  render?: (value: unknown, record: T, index: number) => ReactNode;
}

export interface FilterOption {
  label: string;
  value: string | number | boolean;
}

export interface SelectOption {
  label: string;
  value: string | number;
  disabled?: boolean;
}

export interface ChartDataPoint {
  name: string;
  value: number;
  [key: string]: unknown;
}

export interface DashboardWidget {
  id: string;
  type: 'chart' | 'metric' | 'table' | 'list';
  title: string;
  config: WidgetConfigUI;
  position: GridPosition;
}

export interface WidgetConfigUI {
  dataSource: string;
  chartType?: 'line' | 'bar' | 'pie' | 'area';
  metrics?: string[];
  dimensions?: string[];
  filters?: Record<string, unknown>;
  refreshInterval?: number;
}

export interface GridPosition {
  x: number;
  y: number;
  w: number;
  h: number;
  minW?: number;
  minH?: number;
  maxW?: number;
  maxH?: number;
}

export interface ToastMessage {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message?: string;
  duration?: number;
}

export interface ModalProps {
  open: boolean;
  onClose: () => void;
  title?: string;
  width?: number | string;
  footer?: ReactNode;
}

export interface ConfirmOptions {
  title: string;
  content: string;
  okText?: string;
  cancelText?: string;
  type?: 'warning' | 'danger' | 'info';
}

export interface FileUploadState {
  file: File | null;
  uploading: boolean;
  progress: number;
  error?: string;
}

export interface FormFieldError {
  field: string;
  message: string;
}
