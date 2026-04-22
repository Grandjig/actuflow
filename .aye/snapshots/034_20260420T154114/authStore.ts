import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User } from '@/types/models';

interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // Actions
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshAuth: () => Promise<void>;
  initAuth: () => Promise<void>;
  hasPermission: (resource: string, action: string) => boolean;
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: true,
      error: null,

      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null });

        try {
          const response = await fetch(`${API_URL}/api/v1/auth/login/json`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
          });

          if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Login failed');
          }

          const data = await response.json();

          // Fetch user info
          const userResponse = await fetch(`${API_URL}/api/v1/auth/me`, {
            headers: { Authorization: `Bearer ${data.access_token}` },
          });

          if (!userResponse.ok) {
            throw new Error('Failed to fetch user info');
          }

          const user = await userResponse.json();

          set({
            token: data.access_token,
            refreshToken: data.refresh_token,
            user,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.message,
            isAuthenticated: false,
          });
          throw error;
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          refreshToken: null,
          isAuthenticated: false,
          error: null,
        });
      },

      refreshAuth: async () => {
        const { refreshToken } = get();
        if (!refreshToken) {
          throw new Error('No refresh token');
        }

        const response = await fetch(`${API_URL}/api/v1/auth/refresh`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refresh_token: refreshToken }),
        });

        if (!response.ok) {
          throw new Error('Failed to refresh token');
        }

        const data = await response.json();

        set({
          token: data.access_token,
          refreshToken: data.refresh_token,
        });
      },

      initAuth: async () => {
        const { token } = get();

        if (!token) {
          set({ isLoading: false, isAuthenticated: false });
          return;
        }

        try {
          const response = await fetch(`${API_URL}/api/v1/auth/me`, {
            headers: { Authorization: `Bearer ${token}` },
          });

          if (!response.ok) {
            // Try to refresh
            await get().refreshAuth();
            const newToken = get().token;
            const retryResponse = await fetch(`${API_URL}/api/v1/auth/me`, {
              headers: { Authorization: `Bearer ${newToken}` },
            });

            if (!retryResponse.ok) {
              throw new Error('Session expired');
            }

            const user = await retryResponse.json();
            set({ user, isAuthenticated: true, isLoading: false });
          } else {
            const user = await response.json();
            set({ user, isAuthenticated: true, isLoading: false });
          }
        } catch (error) {
          set({
            user: null,
            token: null,
            refreshToken: null,
            isAuthenticated: false,
            isLoading: false,
          });
        }
      },

      hasPermission: (resource: string, action: string) => {
        const { user } = get();
        if (!user) return false;
        if (user.is_superuser) return true;

        const permissions = user.role?.permissions || [];
        return permissions.some(
          (p) => p.resource === resource && p.action === action
        );
      },
    }),
    {
      name: 'actuflow-auth',
      partialize: (state) => ({
        token: state.token,
        refreshToken: state.refreshToken,
        user: state.user,
      }),
    }
  )
);
