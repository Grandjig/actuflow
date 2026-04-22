/**
 * Authentication hook.
 */

import { useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useAuthStore } from '@/stores/authStore';
import { login as apiLogin, logout as apiLogout, getCurrentUser } from '@/api/auth';
import type { User } from '@/types/models';

export function useAuth() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const {
    user,
    isAuthenticated,
    isLoading,
    error,
    setUser,
    setTokens,
    setLoading,
    setError,
    logout: storeLogout,
    hasPermission,
  } = useAuthStore();

  // Fetch current user on mount if we have a token
  const { isLoading: isLoadingUser } = useQuery({
    queryKey: ['currentUser'],
    queryFn: async () => {
      const token = localStorage.getItem('access_token');
      if (!token) return null;
      
      try {
        const userData = await getCurrentUser();
        setUser(userData);
        return userData;
      } catch {
        storeLogout();
        return null;
      }
    },
    enabled: !user && !!localStorage.getItem('access_token'),
    retry: false,
  });

  // Login mutation
  const loginMutation = useMutation({
    mutationFn: async ({ email, password }: { email: string; password: string }) => {
      setLoading(true);
      setError(null);
      const response = await apiLogin(email, password);
      return response;
    },
    onSuccess: (data) => {
      setTokens(data.access_token, data.refresh_token);
      setUser(data.user);
      setLoading(false);
      navigate('/');
    },
    onError: (err: Error) => {
      setError(err.message || 'Login failed');
      setLoading(false);
    },
  });

  // Logout
  const logout = useCallback(async () => {
    try {
      await apiLogout();
    } catch {
      // Ignore logout API errors
    } finally {
      storeLogout();
      queryClient.clear();
      navigate('/login');
    }
  }, [storeLogout, queryClient, navigate]);

  return {
    user,
    isAuthenticated,
    isLoading: isLoading || isLoadingUser,
    error,
    login: loginMutation.mutate,
    logout,
    hasPermission,
  };
}
