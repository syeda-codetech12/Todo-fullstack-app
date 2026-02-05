// src/hooks/useTasks.ts
import { useState, useEffect } from 'react';
import apiClient from '@/lib/api';
import { Task } from '@/lib/types';
import { useAuth } from './useAuth';

interface TasksState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  fetchTasks: (userId?: string) => Promise<void>;
  createTask: (taskData: Omit<Task, 'id' | 'userId' | 'createdAt' | 'updatedAt'>) => Promise<void>;
  updateTask: (id: string, taskData: Partial<Omit<Task, 'id' | 'userId' | 'createdAt' | 'updatedAt'>>) => Promise<void>;
  deleteTask: (id: string) => Promise<void>;
  toggleTaskCompletion: (id: string) => Promise<void>;
}

export const useTasks = (): TasksState => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth(); // Get current user from auth context

  const fetchTasks = async (userId?: string) => {
    const targetUserId = userId || user?.id;
    if (!targetUserId) {
      setError('User not authenticated'); return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await apiClient.get(`/users/${targetUserId}/tasks/`);
      setTasks(response.data.tasks || []);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  const createTask = async (taskData: Omit<Task, 'id' | 'userId' | 'createdAt' | 'updatedAt'>) => {
    if (!user?.id) {
      setError('User not authenticated'); return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await apiClient.post(`/users/${user.id}/tasks/`, taskData);
      setTasks([...tasks, response.data.data]);
    } catch (err: any) {
      setError(err.message || 'Failed to create task');
    } finally {
      setLoading(false);
    }
  };

  const updateTask = async (id: string, taskData: Partial<Omit<Task, 'id' | 'userId' | 'createdAt' | 'updatedAt'>>) => {
    if (!user?.id) {
      setError('User not authenticated'); return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await apiClient.put(`/users/${user.id}/tasks/${id}`, taskData);
      setTasks(tasks.map(task => task.id === id ? response.data.data : task));
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
    } finally {
      setLoading(false);
    }
  };

  const deleteTask = async (id: string) => {
    if (!user?.id) {
      setError('User not authenticated'); return;
    }

    setLoading(true);
    setError(null);

    try {
      await apiClient.delete(`/users/${user.id}/tasks/${id}`);
      setTasks(tasks.filter(task => task.id !== id));
    } catch (err: any) {
      setError(err.message || 'Failed to delete task');
    } finally {
      setLoading(false);
    }
  };

  const toggleTaskCompletion = async (id: string) => {
    if (!user?.id) {
      setError('User not authenticated'); return;
    }

    const task = tasks.find(t => t.id === id);
    if (!task) return;

    setLoading(true);
    setError(null);

    try {
      // Determine the new status based on current status
      const newStatus = task.status === 'completed' ? 'pending' : 'completed';
      const response = await apiClient.put(`/users/${user.id}/tasks/${id}`, {
        ...task,
        status: newStatus
      });
      setTasks(tasks.map(t => t.id === id ? response.data.data : t));
    } catch (err: any) {
      setError(err.message || 'Failed to update task completion');
    } finally {
      setLoading(false);
    }
  };

  // Fetch tasks when the hook is first used
  useEffect(() => {
    if (user?.id) {
      fetchTasks(user.id);
    }
  }, [user?.id]);

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
  };
};
