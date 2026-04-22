import type { ThemeConfig } from 'antd';

export const theme: ThemeConfig = {
  token: {
    // Colors
    colorPrimary: '#2563eb',
    colorSuccess: '#10b981',
    colorWarning: '#f59e0b',
    colorError: '#ef4444',
    colorInfo: '#3b82f6',

    // Border
    borderRadius: 6,
    borderRadiusLG: 8,
    borderRadiusSM: 4,

    // Font
    fontFamily:
      "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif",
    fontSize: 14,
    fontSizeHeading1: 38,
    fontSizeHeading2: 30,
    fontSizeHeading3: 24,
    fontSizeHeading4: 20,
    fontSizeHeading5: 16,

    // Spacing
    padding: 16,
    paddingLG: 24,
    paddingSM: 12,
    paddingXS: 8,
    margin: 16,
    marginLG: 24,
    marginSM: 12,
    marginXS: 8,

    // Layout
    controlHeight: 36,
    controlHeightLG: 40,
    controlHeightSM: 28,

    // Shadows
    boxShadow:
      '0 1px 2px 0 rgba(0, 0, 0, 0.03), 0 1px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px 0 rgba(0, 0, 0, 0.02)',
    boxShadowSecondary:
      '0 6px 16px 0 rgba(0, 0, 0, 0.08), 0 3px 6px -4px rgba(0, 0, 0, 0.12), 0 9px 28px 8px rgba(0, 0, 0, 0.05)',
  },
  components: {
    Layout: {
      bodyBg: '#f5f5f5',
      headerBg: '#ffffff',
      siderBg: '#001529',
    },
    Menu: {
      darkItemBg: '#001529',
      darkSubMenuItemBg: '#000c17',
    },
    Card: {
      paddingLG: 24,
    },
    Table: {
      headerBg: '#fafafa',
      borderColor: '#f0f0f0',
    },
    Button: {
      primaryShadow: '0 2px 0 rgba(37, 99, 235, 0.1)',
    },
    Input: {
      activeBorderColor: '#2563eb',
      hoverBorderColor: '#93c5fd',
    },
    Select: {
      optionSelectedBg: '#eff6ff',
    },
  },
};

export default theme;
