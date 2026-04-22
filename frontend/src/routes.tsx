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
const ProfileSettings = lazy(() => import('./pages/settings/ProfileSettings'));
const GeneratedReportList = lazy(() => import('./pages/reports/GeneratedReportList'));
const ReportTemplateList = lazy(() => import('./pages/reports/ReportTemplateList'));
const NotFound = lazy(() => import('./pages/NotFound'));

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
