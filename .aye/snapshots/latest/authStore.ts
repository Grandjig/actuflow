import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: string;
  email: string;
  full_name: string;
  role?: {
    id: string;
    name: string;
    permissions: string[];
  };
  department?: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  setUser: (user: User) => void;
  hasPermission: (resource: string, action: string) => boolean;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      refreshToken: null,
      isAuthenticated: false,

      login: async (email: string, password: string) => {
        // For demo purposes, simulate login
        // In production, this would call the real API
        try {
          const response = await fetch('http://localhost:8000/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
          });

          if (!response.ok) {
            // If API fails, use mock login for demo
            if (email === 'admin@actuflow.com' && password === 'admin123') {
              set({
                user: {
                  id: '1',
                  email: 'admin@actuflow.com',
                  full_name: 'System Administrator',
                  role: { id: '1', name: 'admin', permissions: ['*'] },
                  department: 'IT',
                },
                token: 'demo-token',
                refreshToken: 'demo-refresh',
                isAuthenticated: true,
              });
              return;
            }
            throw new Error('Invalid credentials');
          }

          const data = await response.json();
          
          // Fetch user profile
          const profileResponse = await fetch('http://localhost:8000/api/v1/auth/me', {
            headers: { Authorization: `Bearer ${data.access_token}` },
          });
          
          const user = profileResponse.ok ? await profileResponse.json() : {
            id: '1',
            email,
            full_name: email.split('@')[0],
            role: { id: '1', name: 'user', permissions: [] },
          };

          set({
            user,
            token: data.access_token,
            refreshToken: data.refresh_token,
            isAuthenticated: true,
          });
        } catch (error) {
          // Fallback for demo
          if (email === 'admin@actuflow.com' && password === 'admin123') {
            set({
              user: {
                id: '1',
                email: 'admin@actuflow.com',
                full_name: 'System Administrator',
                role: { id: '1', name: 'admin', permissions: ['*'] },
                department: 'IT',
              },
              token: 'demo-token',
              refreshToken: 'demo-refresh',
              isAuthenticated: true,
            });
            return;
          }
          throw error;
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          refreshToken: null,
          isAuthenticated: false,
        });
      },

      setUser: (user: User) => {
        set({ user });
      },

      hasPermission: (resource: string, action: string) => {
        const { user } = get();
        if (!user?.role?.permissions) return false;
        if (user.role.permissions.includes('*')) return true;
        return user.role.permissions.includes(`${resource}:${action}`);
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);
