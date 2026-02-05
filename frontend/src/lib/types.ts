// src/lib/types.ts
export interface User {
  id: string;
  email: string;
  name?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface SessionState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  dueDate?: Date;
  createdAt: Date;
  updatedAt: Date;
  userId: string; // Owner of the task
}

export interface TaskFormData {
  title: string;
  description?: string;
  dueDate?: Date;
}

export interface LoginResponse {
  user: User;
  token: string;
  refreshToken: string;
}

export interface RegisterResponse {
  user: User;
  token: string;
  refreshToken: string;
}

export interface TaskApiResponse {
  data: Task[];
  pagination?: {
    currentPage: number;
    totalPages: number;
    totalCount: number;
  };
}

export interface SingleTaskApiResponse {
  data: Task;
}

export interface ErrorResponse {
  error: string;
  message: string;
  statusCode: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name?: string;
}

export interface TaskRequest {
  title: string;
  description?: string;
  dueDate?: Date;
}