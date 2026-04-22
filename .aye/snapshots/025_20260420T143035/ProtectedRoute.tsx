import { ReactNode, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Spin } from 'antd';
import { useAuthStore } from '@/stores/authStore';

interface ProtectedRouteProps {
  children: ReactNode;
  permission?: string;
  roles?: string[];
}

export default function ProtectedRoute({
  children,
  permission,
  roles,
}: ProtectedRouteProps) {
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated, isLoading, user, hasPermission, hasRole } = useAuthStore();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      navigate('/login', { state: { from: location }, replace: true });
    }
  }, [isAuthenticated, isLoading, navigate, location]);

  // Show loading while checking auth
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

  // Not authenticated
  if (!isAuthenticated) {
    return null;
  }

  // Check permission if specified
  if (permission) {
    const [resource, action] = permission.split(':');
    if (!hasPermission(resource, action)) {
      return (
        <div style={{ padding: 48, textAlign: 'center' }}>
          <h2>Access Denied</h2>
          <p>You don't have permission to access this page.</p>
        </div>
      );
    }
  }

  // Check roles if specified
  if (roles && roles.length > 0) {
    if (!hasRole(...roles)) {
      return (
        <div style={{ padding: 48, textAlign: 'center' }}>
          <h2>Access Denied</h2>
          <p>You don't have the required role to access this page.</p>
        </div>
      );
    }
  }

  return <>{children}</>;
}
