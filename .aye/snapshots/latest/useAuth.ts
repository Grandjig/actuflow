import { useCallback } from 'react';
import { useAuthStore } from '@/stores/authStore';

export function useAuth() {
  const {
    user,
    token,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    hasPermission,
  } = useAuthStore();

  const hasAnyPermission = useCallback(
    (permissions: string[]) => {
      return permissions.some((p) => {
        const [resource, action] = p.split(':');
        return hasPermission(resource, action);
      });
    },
    [hasPermission]
  );

  const hasAllPermissions = useCallback(
    (permissions: string[]) => {
      return permissions.every((p) => {
        const [resource, action] = p.split(':');
        return hasPermission(resource, action);
      });
    },
    [hasPermission]
  );

  return {
    user,
    token,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
  };
}
