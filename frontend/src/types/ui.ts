// UI-related types

export interface BreadcrumbItem {
  title: string;
  path?: string;
}

export interface MenuItem {
  key: string;
  label: string;
  icon?: React.ReactNode;
  path?: string;
  children?: MenuItem[];
  disabled?: boolean;
}

export interface FilterConfig {
  key: string;
  label: string;
  type: 'text' | 'select' | 'multiSelect' | 'date' | 'dateRange' | 'number';
  placeholder?: string;
  options?: { label: string; value: string | number }[];
  defaultValue?: any;
}

export interface TableColumn<T = any> {
  key: string;
  title: string;
  dataIndex?: string;
  render?: (value: any, record: T, index: number) => React.ReactNode;
  width?: number | string;
  align?: 'left' | 'center' | 'right';
  sorter?: boolean;
  fixed?: 'left' | 'right';
}

export interface ChartDataPoint {
  name: string;
  value: number;
  [key: string]: any;
}

export interface DashboardWidget {
  id: string;
  type: string;
  title: string;
  config: Record<string, any>;
  position: {
    x: number;
    y: number;
    w: number;
    h: number;
  };
}

export interface Notification {
  id: string;
  type: 'info' | 'success' | 'warning' | 'error';
  title: string;
  message: string;
  read: boolean;
  createdAt: string;
  resourceType?: string;
  resourceId?: string;
}

export interface ModalState {
  visible: boolean;
  data?: any;
  mode?: 'create' | 'edit' | 'view';
}

export type ThemeMode = 'light' | 'dark';
