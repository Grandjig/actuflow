import { get, post } from './client';
import type { LoginRequest, LoginResponse, RefreshTokenResponse, SuccessResponse } from '@/types/api';
import type { User } from '@/types/models';

export const authApi = {
  login: (data: LoginRequest) => 
    post<LoginResponse>('/auth/login', data),

  refresh: (refreshToken: string) =>
    post<RefreshTokenResponse>('/auth/refresh', { refresh_token: refreshToken }),

  logout: () => 
    post<SuccessResponse>('/auth/logout'),

  me: () => 
    get<User>('/auth/me'),

  changePassword: (currentPassword: string, newPassword: string) =>
    post<SuccessResponse>('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    }),
};
