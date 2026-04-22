import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { authApi } from '@/api/auth';
import type { User } from '@/types/models';

interface AuthState {
  token: string | null;
  refreshToken: string | null;
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // Actions
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshAuth: () => Promise<void>;
  initAuth: () => Promise<void>;
  setUser: (user: User) => void;
  hasPermission: (resource: string, action: string) => boolean;
  hasRole: (...roles: string[]) => boolean;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      token: null,
      refreshToken: null,
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null });
        try {
          const response = await authApi.login(email, password);
          set({
            token: response.access_token,
            refreshToken: response.refresh_token,
            isAuthenticated: true,
            isLoading: false,
          });

          // Fetch user info
          const user = await authApi.me();
          set({ user });
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.message || 'Login failed',
            isAuthenticated: false,
            token: null,
            refreshToken: null,
            user: null,
          });
          throw error;
        }
      },

      logout: () => {
        authApi.logout().catch(() => {});
        set({
          token: null,
          refreshToken: null,
          user: null,
          isAuthenticated: false,
          error: null,
        });
      },

      refreshAuth: async () => {
        const { refreshToken } = get();
        if (!refreshToken) {
          throw new Error('No refresh token');
        }

        try {
          const response = await authApi.refresh(refreshToken);
          set({
            token: response.access_token,
            refreshToken: response.refresh_token,
          });
        } catch (error) {
          get().logout();
          throw error;
        }
      },

      initAuth: async () => {
        const { token } = get();
        if (!token) return;

        set({ isLoading: true });
        try {
          const user = await authApi.me();
          set({ user, isAuthenticated: true, isLoading: false });
        } catch (error) {
          // Token might be expired, try refresh
          try {
            await get().refreshAuth();
            const user = await authApi.me();
            set({ user, isAuthenticated: true, isLoading: false });
          } catch {
            get().logout();
            set({ isLoading: false });
          }
        }
      },

      setUser: (user: User) => set({ user }),

      hasPermission: (resource: string, action: string) => {
        const { user } = get();
        if (!user) return false;
        if (user.is_superuser) return true;
        if (!user.role?.permissions) return false;

        return user.role.permissions.some(
          (p) =>
            (p.resource === resource && p.action === action) ||
            (p.resource === resource && p.action === 'admin')
        );
      },

      hasRole: (...roles: string[]) => {
        const { user } = get();
        if (!user) return false;
        if (user.is_superuser) return true;
        if (!user.role) return false;
        return roles.includes(user.role.name);
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
