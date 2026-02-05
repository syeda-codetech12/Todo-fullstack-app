// src/app/tasks/create/page.tsx
'use client';

import { useAuth } from '@/hooks/useAuth';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import TaskForm from '@/components/tasks/TaskForm';
import { useTasks } from '@/hooks/useTasks';

export default function CreateTaskPage() {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const { createTask } = useTasks();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.replace('/signin');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Redirect happens in effect
  }

  const handleSubmit = async (formData: any) => {
    try {
      // Format the dueDate to ISO string if it exists
      const formattedData = {
        ...formData,
        dueDate: formData.dueDate ? new Date(formData.dueDate).toISOString() : undefined
      };
      await createTask(formattedData);
      router.push('/dashboard');
    } catch (error) {
      console.error('Failed to create task:', error);
      // In a real app, you'd want to show an error message to the user
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <main>
        <div className="max-w-3xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
              <h3 className="text-lg leading-6 font-medium text-gray-900">Create New Task</h3>
              <p className="mt-1 text-sm text-gray-500">Fill in the details for your new task</p>
            </div>
            <div className="px-4 py-5 sm:p-6">
              <TaskForm onSubmit={handleSubmit} submitLabel="Create Task" />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
