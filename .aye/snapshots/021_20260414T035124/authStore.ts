import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User, Role, Permission } from '@/types/models';
import { authApi } from '@/api/auth';

interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isInitialized: boolean;
  isLoggingIn: boolean;
  error: string | null;

  // Actions
  initAuth: () => Promise<void>;
  login: (credentials: { email: string; password: string }) => Promise<void>;
  logout: () => void;
  refreshAuth: () => Promise<void>;
  setUser: (user: User) => void;
  clearError: () => void;

  // Permission helpers
  hasPermission: (resource: string, action: string) => boolean;
  hasRole: (roleName: string) => boolean;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      refreshToken: null,
      isAuthenticated: false,
      isInitialized: false,
      isLoggingIn: false,
      error: null,

      initAuth: async () => {
        const { token, refreshToken } = get();
        
        if (!token) {
          set({ isInitialized: true });
          return;
        }

        try {
          // Verify token and get user info
          const user = await authApi.me();
          set({ 
            user, 
            isAuthenticated: true, 
            isInitialized: true 
          });
        } catch (error) {
          // Token invalid, try refresh
          if (refreshToken) {
            try {
              const response = await authApi.refresh(refreshToken);
              const user = await authApi.me();
              set({
                token: response.access_token,
                refreshToken: response.refresh_token,
                user,
                isAuthenticated: true,
                isInitialized: true,
              });
            } catch {
              // Refresh failed, logout
              set({
                user: null,
                token: null,
                refreshToken: null,
                isAuthenticated: false,
                isInitialized: true,
              });
            }
          } else {
            set({
              user: null,
              token: null,
              refreshToken: null,
              isAuthenticated: false,
              isInitialized: true,
            });
          }
        }
      },

      login: async (credentials) => {
        set({ isLoggingIn: true, error: null });
        
        try {
          const response = await authApi.login(
            credentials.email,
            credentials.password
          );
          
          const user = await authApi.me();
          
          set({
            token: response.access_token,
            refreshToken: response.refresh_token,
            user,
            isAuthenticated: true,
            isLoggingIn: false,
            error: null,
          });
        } catch (error: any) {
          set({
            isLoggingIn: false,
            error: error.message || 'Login failed',
          });
          throw error;
        }
      },

      logout: () => {
        authApi.logout().catch(() => {});
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
          get().logout();
          return;
        }

        try {
          const response = await authApi.refresh(refreshToken);
          set({
            token: response.access_token,
            refreshToken: response.refresh_token,
          });
        } catch {
          get().logout();
        }
      },

      setUser: (user) => {
        set({ user });
      },

      clearError: () => {
        set({ error: null });
      },

      hasPermission: (resource: string, action: string) => {
        const { user } = get();
        if (!user) return false;
        if (user.is_superuser) return true;
        
        const permissions = user.role?.permissions || [];
        return permissions.some(
          (p: Permission) => p.resource === resource && p.action === action
        );
      },

      hasRole: (roleName: string) => {
        const { user } = get();
        if (!user) return false;
        if (user.is_superuser) return true;
        return user.role?.name === roleName;
      },
    }),
    {
      name: 'actuflow-auth',
      partialize: (state) => ({
        token: state.token,
        refreshToken: state.refreshToken,
      }),
    }
  )
);
