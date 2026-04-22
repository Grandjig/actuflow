import type { ThemeConfig } from 'antd';

export const theme: ThemeConfig = {
  token: {
    // Primary color
    colorPrimary: '#2563eb',
    colorPrimaryHover: '#1d4ed8',
    colorPrimaryActive: '#1e40af',

    // Success
    colorSuccess: '#16a34a',

    // Warning
    colorWarning: '#ca8a04',

    // Error
    colorError: '#dc2626',

    // Info
    colorInfo: '#0891b2',

    // Border radius
    borderRadius: 6,
    borderRadiusLG: 8,
    borderRadiusSM: 4,

    // Font
    fontFamily:
      '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    fontSize: 14,

    // Layout
    colorBgContainer: '#ffffff',
    colorBgLayout: '#f5f5f5',
  },
  components: {
    Layout: {
      headerBg: '#ffffff',
      siderBg: '#ffffff',
    },
    Menu: {
      itemSelectedBg: '#eff6ff',
      itemSelectedColor: '#2563eb',
    },
    Card: {
      paddingLG: 24,
    },
    Table: {
      headerBg: '#fafafa',
    },
  },
};
