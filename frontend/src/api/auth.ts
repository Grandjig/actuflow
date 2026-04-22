import { post, get } from './client';
import type { TokenResponse } from '@/types/api';
import type { User } from '@/types/models';

export const authApi = {
  login: async (email: string, password: string): Promise<TokenResponse> => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    const response = await fetch(
      `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/auth/login`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      }
    );

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }

    return response.json();
  },

  refresh: (refreshToken: string): Promise<TokenResponse> =>
    post<TokenResponse>('/auth/refresh', { refresh_token: refreshToken }),

  logout: (): Promise<void> =>
    post<void>('/auth/logout').catch(() => {}),

  me: (): Promise<User> =>
    get<User>('/auth/me'),
};
