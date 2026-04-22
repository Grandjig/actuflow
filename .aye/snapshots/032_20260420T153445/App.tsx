import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider, App as AntApp, theme } from 'antd';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

import { useAuthStore } from '@/stores/authStore';
import { useUIStore } from '@/stores/uiStore';
import MainLayout from '@/components/layout/MainLayout';
import AuthLayout from '@/components/layout/AuthLayout';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import ProtectedRoute from '@/components/auth/ProtectedRoute';

// Pages
import Login from '@/pages/auth/Login';
import Dashboard from '@/pages/Dashboard';
import PolicyList from '@/pages/policies/PolicyList';
import PolicyDetail from '@/pages/policies/PolicyDetail';
import PolicyCreate from '@/pages/policies/PolicyCreate';
import ClaimList from '@/pages/claims/ClaimList';
import ClaimDetail from '@/pages/claims/ClaimDetail';
import AssumptionSetList from '@/pages/assumptions/AssumptionSetList';
import AssumptionSetDetail from '@/pages/assumptions/AssumptionSetDetail';
import AssumptionSetCreate from '@/pages/assumptions/AssumptionSetCreate';
import CalculationList from '@/pages/calculations/CalculationList';
import CalculationDetail from '@/pages/calculations/CalculationDetail';
import CalculationCreate from '@/pages/calculations/CalculationCreate';
import ImportWizard from '@/pages/imports/ImportWizard';
import Settings from '@/pages/settings/Settings';
import NotFound from '@/pages/NotFound';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function AppRoutes() {
  const { isAuthenticated, isLoading, initAuth } = useAuthStore();

  useEffect(() => {
    initAuth();
  }, [initAuth]);

  if (isLoading) {
    return <LoadingSpinner fullScreen tip="Loading..." />;
  }

  return (
    <Routes>
      {/* Auth routes */}
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<Login />} />
      </Route>

      {/* Protected routes */}
      <Route
        element={
          <ProtectedRoute>
            <MainLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />

        {/* Policies */}
        <Route path="/policies" element={<PolicyList />} />
        <Route path="/policies/new" element={<PolicyCreate />} />
        <Route path="/policies/:id" element={<PolicyDetail />} />
        <Route path="/policies/:id/edit" element={<PolicyCreate />} />

        {/* Claims */}
        <Route path="/claims" element={<ClaimList />} />
        <Route path="/claims/:id" element={<ClaimDetail />} />

        {/* Assumptions */}
        <Route path="/assumptions" element={<AssumptionSetList />} />
        <Route path="/assumptions/new" element={<AssumptionSetCreate />} />
        <Route path="/assumptions/:id" element={<AssumptionSetDetail />} />

        {/* Calculations */}
        <Route path="/calculations" element={<CalculationList />} />
        <Route path="/calculations/new" element={<CalculationCreate />} />
        <Route path="/calculations/:id" element={<CalculationDetail />} />

        {/* Imports */}
        <Route path="/imports" element={<ImportWizard />} />
        <Route path="/imports/new" element={<ImportWizard />} />

        {/* Settings */}
        <Route path="/settings" element={<Settings />} />
        <Route path="/settings/*" element={<Settings />} />

        {/* 404 */}
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default function App() {
  const { theme: appTheme } = useUIStore();

  return (
    <QueryClientProvider client={queryClient}>
      <ConfigProvider
        theme={{
          algorithm: appTheme === 'dark' ? theme.darkAlgorithm : theme.defaultAlgorithm,
          token: {
            colorPrimary: '#2563eb',
            borderRadius: 6,
          },
        }}
      >
        <AntApp>
          <BrowserRouter>
            <AppRoutes />
          </BrowserRouter>
        </AntApp>
      </ConfigProvider>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
