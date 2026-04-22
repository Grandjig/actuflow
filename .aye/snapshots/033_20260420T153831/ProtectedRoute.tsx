import { ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { Spin } from 'antd';
import { useAuthStore } from '@/stores/authStore';

interface ProtectedRouteProps {
  children: ReactNode;
  requiredPermission?: { resource: string; action: string };
}

export default function ProtectedRoute({
  children,
  requiredPermission,
}: ProtectedRouteProps) {
  const location = useLocation();
  const { isAuthenticated, isLoading, user } = useAuthStore();

  if (isLoading) {
    return (
      <div
        style={{
          height: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Spin size="large" tip="Loading..." />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (requiredPermission && user?.role?.permissions) {
    const hasPermission = user.role.permissions.some(
      (p) =>
        p.resource === requiredPermission.resource &&
        p.action === requiredPermission.action
    );

    if (!hasPermission && !user.is_superuser) {
      return <Navigate to="/" replace />;
    }
  }

  return <>{children}</>;
}
