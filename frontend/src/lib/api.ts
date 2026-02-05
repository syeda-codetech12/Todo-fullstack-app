// src/lib/api.ts
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import { getAuthToken, removeAuthToken, setAuthToken } from './auth';

// Base API configuration
const BACKEND_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: `${BACKEND_BASE_URL}/api`,
  timeout: 10000, // 10 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token
apiClient.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    const token = getAuthToken();
    if (token) {
      config.headers = {
        ...config.headers,
        Authorization: `Bearer ${token}`,
      };
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration and network errors
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };

    // Handle network connectivity issues
    if (!error.response) {
      console.error('Network error:', error.message);
      // In a real app, you might want to show a toast notification about network issues
      return Promise.reject(error);
    }

    // If token has expired and we haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      // Attempt to refresh token here if refresh token mechanism exists
      // For now, we'll just remove the token and redirect to login
      removeAuthToken();

      // Redirect to login page
      if (typeof window !== 'undefined') {
        window.location.href = '/signin';
      }

      return Promise.reject(error);
    }

    return Promise.reject(error);
  }
);

export default apiClient;