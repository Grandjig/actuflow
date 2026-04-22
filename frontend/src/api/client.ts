import axios, { AxiosError, AxiosRequestConfig } from 'axios';

// For GitHub Pages deployment, API URL must be absolute
// Set VITE_API_URL in your environment or GitHub repository variables
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
 baseURL: `${API_BASE_URL}/api/v1`,
 headers: {
 'Content-Type': 'application/json',
 },
 timeout: 30000,
});

// Request interceptor for auth token
apiClient.interceptors.request.use(
 (config) => {
 const token = localStorage.getItem('access_token');
 if (token) {
 config.headers.Authorization = `Bearer ${token}`;
 }
 return config;
 },
 (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
 (response) => response,
 async (error: AxiosError) => {
 const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };

 // Handle 401 - try refresh token
 if (error.response?.status === 401 && !originalRequest._retry) {
 originalRequest._retry = true;

 const refreshToken = localStorage.getItem('refresh_token');
 if (refreshToken) {
 try {
 const response = await axios.post(`${API_BASE_URL}/api/v1/auth/refresh`, {
 refresh_token: refreshToken,
 });

 const { access_token, refresh_token: newRefreshToken } = response.data;
 localStorage.setItem('access_token', access_token);
 localStorage.setItem('refresh_token', newRefreshToken);

 if (originalRequest.headers) {
 originalRequest.headers.Authorization = `Bearer ${access_token}`;
 }
 return apiClient(originalRequest);
 } catch (refreshError) {
 // Refresh failed - clear tokens and redirect to login
 localStorage.removeItem('access_token');
 localStorage.removeItem('refresh_token');
 window.location.href = '/login';
 return Promise.reject(refreshError);
 }
 }

 // No refresh token - redirect to login
 window.location.href = '/login';
 }

 return Promise.reject(error);
 }
);

// Helper functions
export const get = <T>(url: string, params?: Record<string, any>) =>
 apiClient.get<T>(url, { params }).then((res) => res.data);

export const post = <T>(url: string, data?: any) =>
 apiClient.post<T>(url, data).then((res) => res.data);

export const put = <T>(url: string, data?: any) =>
 apiClient.put<T>(url, data).then((res) => res.data);

export const patch = <T>(url: string, data?: any) =>
 apiClient.patch<T>(url, data).then((res) => res.data);

export const del = <T>(url: string) =>
 apiClient.delete<T>(url).then((res) => res.data);

export default apiClient;
