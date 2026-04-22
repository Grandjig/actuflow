/**
 * Authentication hook.
 */

import { useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';

export function useAuth() {
  const navigate = useNavigate();
  const {
    user,
    isAuthenticated,
    isLoading,
    error,
    login: storeLogin,
    logout: storeLogout,
    fetchUser,
    hasPermission,
  } = useAuthStore();

  // Fetch user on mount if we have a token but no user
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token && !user && !isLoading) {
      fetchUser();
    }
  }, [user, isLoading, fetchUser]);

  const login = useCallback(
    async (credentials: { email: string; password: string }) => {
      try {
        await storeLogin(credentials.email, credentials.password);
        navigate('/');
      } catch {
        // Error is already set in store
      }
    },
    [storeLogin, navigate]
  );

  const logout = useCallback(async () => {
    await storeLogout();
    navigate('/login');
  }, [storeLogout, navigate]);

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    hasPermission,
  };
}
