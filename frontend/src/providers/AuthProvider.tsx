// src/providers/AuthProvider.tsx
'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { User, SessionState } from '@/lib/types';
import {
  getAuthToken,
  getRefreshToken,
  getUserInfo,
  isAuthenticated as checkAuthStatus,
  removeAuthToken,
  setAuthToken,
  setRefreshToken,
  setUserInfo
} from '@/lib/auth';
import apiClient from '@/lib/api';

interface AuthContextType extends SessionState {
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name?: string) => Promise<void>;
  logout: () => void;
  updateUser: (userData: Partial<User>) => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [sessionState, setSessionState] = useState<SessionState>({
    user: null,
    token: null,
    refreshToken: null,
    isAuthenticated: false,
    isLoading: true,
  });

  // Initialize auth state on mount
  useEffect(() => {
    const initAuth = async () => {
      const token = getAuthToken();
      const refreshToken = getRefreshToken();
      const user = getUserInfo();

      if (token && user && checkAuthStatus()) {
        setSessionState({
          user,
          token,
          refreshToken,
          isAuthenticated: true,
          isLoading: false,
        });
      } else {
        setSessionState(prev => ({
          ...prev,
          isLoading: false,
        }));
      }
    };

    initAuth();
  }, []);

  const login = async (email: string, password: string) => {
    setSessionState(prev => ({ ...prev, isLoading: true }));

    try {
      // Make API call to backend
      const response = await apiClient.post('/auth/login', { email, password });

      // Extract token from response (backend returns access_token and token_type)
      const { access_token: token, token_type } = response.data;

      // Store auth info FIRST before making subsequent API calls
      // This ensures the apiClient interceptor can pick up the token
      setAuthToken(token);
      // Note: Backend doesn't return refresh token, so we'll store null for now

      // Get user info after successful login - using apiClient for consistency
      // The apiClient interceptor will automatically add the Authorization header
      const userResponse = await apiClient.get('/auth/me');
      const user = userResponse.data;

      // Store user info
      setUserInfo(user);

      // Update state
      setSessionState({
        user,
        token,
        refreshToken: null, // Backend doesn't return refresh token
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error: any) {
      setSessionState(prev => ({
        ...prev,
        isLoading: false,
      }));
      // Better error handling - check for network errors
      if (error?.message === 'Network Error' || error?.code === 'ERR_NETWORK') {
        throw new Error('Unable to connect to the server. Please check if the backend is running.');
      }
      throw error?.response?.data?.detail || error?.message || error;
    }
  };

  const register = async (email: string, password: string, name?: string) => {
    setSessionState(prev => ({ ...prev, isLoading: true }));

    try {
      // Make API call to backend - in a real backend, registration would return user data and token
      // For now, we'll simulate by calling login after registration
      const registerResponse = await apiClient.post('/auth/register', {
        email,
        password,
        first_name: name?.split(' ')[0] || 'User',
        last_name: name?.split(' ').slice(1).join(' ') || ''
      });

      // After successful registration, log the user in to get the token
      const loginResponse = await apiClient.post('/auth/login', { email, password });
      const { access_token: token, token_type } = loginResponse.data;

      // Get user info after successful authentication
      const userResponse = await apiClient.get('/auth/me');
      const user = userResponse.data;

      // Store auth info
      setAuthToken(token);
      // Note: Backend doesn't return refresh token, so we'll store null for now
      setUserInfo(user);

      // Update state
      setSessionState({
        user,
        token,
        refreshToken: null, // Backend doesn't return refresh token
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error: any) {
      setSessionState(prev => ({
        ...prev,
        isLoading: false,
      }));
      throw error?.response?.data?.detail || error;
    }
  };

  const logout = () => {
    removeAuthToken();
    setSessionState({
      user: null,
      token: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: false,
    });
  };

  const updateUser = (userData: Partial<User>) => {
    if (sessionState.user) {
      const updatedUser = { ...sessionState.user, ...userData };
      setSessionState(prev => ({
        ...prev,
        user: updatedUser,
      }));
      setUserInfo(updatedUser);
    }
  };

  const value = {
    ...sessionState,
    login,
    register,
    logout,
    updateUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};