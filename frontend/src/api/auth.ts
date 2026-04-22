/**
 * Authentication API functions.
 */

import { apiClient } from './client';
import type { User } from '@/types/models';

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export interface TokenRefreshResponse {
  access_token: string;
  refresh_token: string;
}

/**
 * Login with email and password.
 */
export async function login(email: string, password: string): Promise<LoginResponse> {
  const response = await apiClient.post<LoginResponse>('/auth/login', {
    email,
    password,
  });
  return response.data;
}

/**
 * Logout current user.
 */
export async function logout(): Promise<void> {
  try {
    await apiClient.post('/auth/logout');
  } catch {
    // Ignore logout errors
  }
}

/**
 * Refresh access token.
 */
export async function refreshToken(refresh_token: string): Promise<TokenRefreshResponse> {
  const response = await apiClient.post<TokenRefreshResponse>('/auth/refresh', {
    refresh_token,
  });
  return response.data;
}

/**
 * Get current user profile.
 */
export async function getCurrentUser(): Promise<User> {
  const response = await apiClient.get<User>('/auth/me');
  return response.data;
}

/**
 * Update current user's password.
 */
export async function updatePassword(
  currentPassword: string,
  newPassword: string
): Promise<void> {
  await apiClient.post('/auth/change-password', {
    current_password: currentPassword,
    new_password: newPassword,
  });
}
