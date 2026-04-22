import type { ThemeConfig } from 'antd';

export const theme: ThemeConfig = {
  token: {
    colorPrimary: '#2563eb',
    colorSuccess: '#16a34a',
    colorWarning: '#d97706',
    colorError: '#dc2626',
    colorInfo: '#0891b2',
    colorTextBase: '#1f2937',
    colorBgBase: '#ffffff',
    borderRadius: 6,
    fontFamily: 'Inter, system-ui, sans-serif',
    fontSize: 14,
  },
  components: {
    Layout: {
      headerBg: '#ffffff',
      siderBg: '#ffffff',
      bodyBg: '#f9fafb',
    },
    Menu: {
      itemBg: 'transparent',
      itemSelectedBg: '#eff6ff',
      itemSelectedColor: '#2563eb',
    },
    Table: {
      headerBg: '#f9fafb',
      borderColor: '#e5e7eb',
    },
    Card: {
      paddingLG: 20,
    },
    Button: {
      borderRadius: 6,
    },
    Input: {
      borderRadius: 6,
    },
    Select: {
      borderRadius: 6,
    },
  },
};

export const statusColors = {
  active: '#16a34a',
  lapsed: '#dc2626',
  surrendered: '#d97706',
  matured: '#0891b2',
  claimed: '#7c3aed',
  pending: '#f59e0b',
  approved: '#16a34a',
  rejected: '#dc2626',
  draft: '#6b7280',
  queued: '#3b82f6',
  running: '#f59e0b',
  completed: '#16a34a',
  failed: '#dc2626',
  cancelled: '#6b7280',
};

export const priorityColors = {
  low: '#6b7280',
  medium: '#f59e0b',
  high: '#dc2626',
  critical: '#7c3aed',
};
