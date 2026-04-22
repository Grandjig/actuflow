/**
 * Application routes configuration.
 */

import { lazy, Suspense } from 'react';
import { createBrowserRouter, Navigate } from 'react-router-dom';
import { Spin } from 'antd';

// Layouts
import MainLayout from './layouts/MainLayout';

// Lazy load pages
const Login = lazy(() => import('./pages/auth/Login'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const PolicyList = lazy(() => import('./pages/policies/PolicyList'));
const PolicyDetail = lazy(() => import('./pages/policies/PolicyDetail'));
const ClaimList = lazy(() => import('./pages/claims/ClaimList'));
const ClaimDetail = lazy(() => import('./pages/claims/ClaimDetail'));
const CalculationList = lazy(() => import('./pages/calculations/CalculationList'));
const CalculationDetail = lazy(() => import('./pages/calculations/CalculationDetail'));
const CalculationCreate = lazy(() => import('./pages/calculations/CalculationCreate'));
const AssumptionSetList = lazy(() => import('./pages/assumptions/AssumptionSetList'));
const AssumptionSetDetail = lazy(() => import('./pages/assumptions/AssumptionSetDetail'));
const ProfileSettings = lazy(() => import('./pages/settings/ProfileSettings'));
const NotFound = lazy(() => import('./pages/NotFound'));

// Report pages - inline to avoid module resolution issues
const GeneratedReportList = lazy(() => 
  Promise.resolve({
    default: () => {
      const { useState } = require('react');
      const { Card, Table, Button, Space, Input, Typography, Tooltip } = require('antd');
      const { SearchOutlined, DownloadOutlined, EyeOutlined, SyncOutlined, CheckCircleOutlined, CloseCircleOutlined } = require('@ant-design/icons');
      const { useQuery } = require('@tanstack/react-query');
      const { getGeneratedReports } = require('./api/reports');
      const { formatDate, formatDateTime } = require('./utils/helpers');
      
      const { Title } = Typography;
      const [search, setSearch] = useState('');
      const [page, setPage] = useState(1);
      const [pageSize, setPageSize] = useState(20);
      
      const { data, isLoading } = useQuery({
        queryKey: ['generatedReports', { search, page, pageSize }],
        queryFn: () => getGeneratedReports({ search, page, page_size: pageSize }),
      });
      
      const statusIcons: Record<string, React.ReactNode> = {
        generating: <SyncOutlined spin style={{ color: '#1890ff' }} />,
        completed: <CheckCircleOutlined style={{ color: '#52c41a' }} />,
        failed: <CloseCircleOutlined style={{ color: '#ff4d4f' }} />,
      };
      
      const columns = [
        { key: 'name', title: 'Report Name', dataIndex: 'name' },
        { key: 'template', title: 'Template', dataIndex: ['report_template', 'name'], render: (v: string) => v || '-' },
        { key: 'period', title: 'Period', render: (_: unknown, r: any) => `${formatDate(r.reporting_period_start)} - ${formatDate(r.reporting_period_end)}` },
        { key: 'status', title: 'Status', dataIndex: 'status', render: (s: string) => <Space>{statusIcons[s]}<span>{s.toUpperCase()}</span></Space> },
        { key: 'generated_at', title: 'Generated', dataIndex: 'generated_at', render: (v: string) => formatDateTime(v) },
        { key: 'actions', title: 'Actions', width: 120, render: (_: unknown, r: any) => (
          <Space>
            <Tooltip title="View"><Button type="text" icon={<EyeOutlined />} disabled={r.status !== 'completed'} /></Tooltip>
            <Tooltip title="Download"><Button type="text" icon={<DownloadOutlined />} disabled={r.status !== 'completed'} /></Tooltip>
          </Space>
        )},
      ];
      
      return (
        <div>
          <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
            <Title level={2}>Generated Reports</Title>
          </div>
          <Card>
            <Space style={{ marginBottom: 16 }}>
              <Input placeholder="Search reports..." prefix={<SearchOutlined />} value={search} onChange={(e: any) => setSearch(e.target.value)} style={{ width: 250 }} />
            </Space>
            <Table columns={columns} dataSource={data?.items || []} rowKey="id" loading={isLoading} pagination={{ current: page, pageSize, total: data?.total || 0, showSizeChanger: true, showTotal: (t: number) => `Total ${t} reports`, onChange: (p: number, ps: number) => { setPage(p); setPageSize(ps); } }} />
          </Card>
        </div>
      );
    }
  })
);

const ReportTemplateList = lazy(() =>
  Promise.resolve({
    default: () => {
      const { useState } = require('react');
      const { useNavigate } = require('react-router-dom');
      const { Card, Table, Button, Space, Input, Tag, Typography, Tooltip } = require('antd');
      const { PlusOutlined, SearchOutlined, EditOutlined, PlayCircleOutlined } = require('@ant-design/icons');
      const { useQuery } = require('@tanstack/react-query');
      const { getReportTemplates } = require('./api/reports');
      
      const { Title } = Typography;
      const navigate = useNavigate();
      const [search, setSearch] = useState('');
      const [page, setPage] = useState(1);
      const [pageSize, setPageSize] = useState(20);
      
      const { data, isLoading } = useQuery({
        queryKey: ['reportTemplates', { search, page, pageSize }],
        queryFn: () => getReportTemplates({ search, page, page_size: pageSize }),
      });
      
      const typeColors: Record<string, string> = { regulatory: 'red', internal: 'blue', adhoc: 'green' };
      
      const columns = [
        { key: 'name', title: 'Template Name', dataIndex: 'name' },
        { key: 'report_type', title: 'Type', dataIndex: 'report_type', render: (t: string) => <Tag color={typeColors[t]}>{t.toUpperCase()}</Tag> },
        { key: 'regulatory_standard', title: 'Standard', dataIndex: 'regulatory_standard', render: (v: string) => v || '-' },
        { key: 'output_format', title: 'Format', dataIndex: 'output_format', render: (v: string) => <Tag>{v}</Tag> },
        { key: 'is_system', title: 'System', dataIndex: 'is_system_template', render: (v: boolean) => v ? <Tag color="purple">System</Tag> : '-' },
        { key: 'actions', title: 'Actions', width: 120, render: (_: unknown, r: any) => (
          <Space>
            <Tooltip title="Generate Report"><Button type="text" icon={<PlayCircleOutlined />} onClick={() => navigate(`/reports/generate?template=${r.id}`)} /></Tooltip>
            <Tooltip title="Edit"><Button type="text" icon={<EditOutlined />} disabled={r.is_system_template} onClick={() => navigate(`/reports/templates/${r.id}/edit`)} /></Tooltip>
          </Space>
        )},
      ];
      
      return (
        <div>
          <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
            <Title level={2}>Report Templates</Title>
            <Button type="primary" icon={<PlusOutlined />} onClick={() => navigate('/reports/templates/new')}>New Template</Button>
          </div>
          <Card>
            <Space style={{ marginBottom: 16 }}>
              <Input placeholder="Search templates..." prefix={<SearchOutlined />} value={search} onChange={(e: any) => setSearch(e.target.value)} style={{ width: 250 }} />
            </Space>
            <Table columns={columns} dataSource={data?.items || []} rowKey="id" loading={isLoading} pagination={{ current: page, pageSize, total: data?.total || 0, showSizeChanger: true, showTotal: (t: number) => `Total ${t} templates`, onChange: (p: number, ps: number) => { setPage(p); setPageSize(ps); } }} />
          </Card>
        </div>
      );
    }
  })
);

// Loading fallback
const PageLoader = () => (
  <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
    <Spin size="large" />
  </div>
);

// Wrap lazy components with Suspense
const withSuspense = (Component: React.ComponentType) => (
  <Suspense fallback={<PageLoader />}>
    <Component />
  </Suspense>
);

export const router = createBrowserRouter([
  {
    path: '/login',
    element: withSuspense(Login),
  },
  {
    path: '/',
    element: <MainLayout />,
    children: [
      {
        index: true,
        element: withSuspense(Dashboard),
      },
      {
        path: 'policies',
        children: [
          {
            index: true,
            element: withSuspense(PolicyList),
          },
          {
            path: ':id',
            element: withSuspense(PolicyDetail),
          },
        ],
      },
      {
        path: 'claims',
        children: [
          {
            index: true,
            element: withSuspense(ClaimList),
          },
          {
            path: ':id',
            element: withSuspense(ClaimDetail),
          },
        ],
      },
      {
        path: 'calculations',
        children: [
          {
            index: true,
            element: withSuspense(CalculationList),
          },
          {
            path: 'new',
            element: withSuspense(CalculationCreate),
          },
          {
            path: ':id',
            element: withSuspense(CalculationDetail),
          },
        ],
      },
      {
        path: 'assumptions',
        children: [
          {
            index: true,
            element: withSuspense(AssumptionSetList),
          },
          {
            path: ':id',
            element: withSuspense(AssumptionSetDetail),
          },
        ],
      },
      {
        path: 'reports',
        children: [
          {
            index: true,
            element: <Navigate to="/reports/generated" replace />,
          },
          {
            path: 'generated',
            element: withSuspense(GeneratedReportList),
          },
          {
            path: 'templates',
            element: withSuspense(ReportTemplateList),
          },
        ],
      },
      {
        path: 'settings',
        children: [
          {
            path: 'profile',
            element: withSuspense(ProfileSettings),
          },
        ],
      },
      {
        path: '*',
        element: withSuspense(NotFound),
      },
    ],
  },
]);
