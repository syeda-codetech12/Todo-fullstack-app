// src/app/tasks/[id]/page.tsx
'use client';

import { useAuth } from '@/hooks/useAuth';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import TaskDetail from '@/components/tasks/TaskDetail';
import { Task } from '@/lib/types';
import { useTasks } from '@/hooks/useTasks';

interface Props {
  params: {
    id: string;
  };
}

export default function TaskDetailPage({ params }: Props) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const { tasks, loading } = useTasks();
  const [task, setTask] = useState<Task | null>(null);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/signin');
    }
  }, [isAuthenticated, isLoading, router]);

  useEffect(() => {
    if (tasks.length > 0) {
      const foundTask = tasks.find(t => t.id === params.id);
      if (foundTask) {
        setTask(foundTask);
      } else {
        // Task not found, redirect to dashboard
        router.push('/dashboard');
      }
    }
  }, [tasks, params.id, router]);

  if (isLoading || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Redirect happens in effect
  }

  if (!task) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-lg">Task not found</div>
      </div>
    );
  }

  const handleTaskUpdated = () => {
    // Refresh the task list by triggering a refetch
    // This would typically happen automatically with proper state management
  };

  const handleTaskDeleted = () => {
    // Redirect to dashboard after task deletion
    router.push('/dashboard');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Task Details</h1>
              <p className="mt-1 text-sm text-gray-500">View and manage your task</p>
            </div>
            <a
              href="/dashboard"
              className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Back to Dashboard
            </a>
          </div>
        </div>
      </header>
      <main>
        <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
          <TaskDetail
            task={task}
            onEditComplete={handleTaskUpdated}
            onDeleteComplete={handleTaskDeleted}
          />
        </div>
      </main>
    </div>
  );
}