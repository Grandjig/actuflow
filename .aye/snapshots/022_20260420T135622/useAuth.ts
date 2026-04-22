import { useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';

export function useAuth() {
  const navigate = useNavigate();
  const {
    user,
    token,
    isAuthenticated,
    isLoggingIn,
    error,
    login: storeLogin,
    logout: storeLogout,
    clearError,
  } = useAuthStore();

  const login = useCallback(
    async (credentials: { email: string; password: string }) => {
      await storeLogin(credentials);
    },
    [storeLogin]
  );

  const logout = useCallback(() => {
    storeLogout();
    navigate('/login');
  }, [storeLogout, navigate]);

  const hasPermission = useCallback(
    (resource: string, action: string = 'read'): boolean => {
      if (!user?.role?.permissions) return false;
      
      const permission = `${resource}:${action}`;
      return user.role.permissions.includes(permission) || 
             user.role.permissions.includes(`${resource}:admin`) ||
             user.is_superuser === true;
    },
    [user]
  );

  const hasAnyPermission = useCallback(
    (permissions: string[]): boolean => {
      return permissions.some((p) => {
        const [resource, action] = p.split(':');
        return hasPermission(resource, action);
      });
    },
    [hasPermission]
  );

  const hasRole = useCallback(
    (roleName: string): boolean => {
      return user?.role?.name === roleName || user?.is_superuser === true;
    },
    [user]
  );

  return {
    user,
    token,
    isAuthenticated,
    isLoggingIn,
    error,
    login,
    logout,
    clearError,
    hasPermission,
    hasAnyPermission,
    hasRole,
  };
}

export default useAuth;
