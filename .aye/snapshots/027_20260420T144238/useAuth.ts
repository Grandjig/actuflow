import { useAuthStore } from '@/stores/authStore';

export function useAuth() {
  const {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    hasPermission,
    hasRole,
  } = useAuthStore();

  const hasAnyPermission = (permissions: string[]) => {
    return permissions.some((perm) => {
      const [resource, action] = perm.split(':');
      return hasPermission(resource, action);
    });
  };

  const hasAllPermissions = (permissions: string[]) => {
    return permissions.every((perm) => {
      const [resource, action] = perm.split(':');
      return hasPermission(resource, action);
    });
  };

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    hasPermission,
    hasRole,
    hasAnyPermission,
    hasAllPermissions,
    isSuperuser: user?.is_superuser || false,
  };
}

export default useAuth;
