// src/components/tasks/TaskItem.tsx
import Link from 'next/link';
import { Task } from '@/lib/types';
import { useTasks } from '@/hooks/useTasks';

interface TaskItemProps {
  task: Task;
}

export default function TaskItem({ task }: TaskItemProps) {
  const { toggleTaskCompletion, deleteTask } = useTasks();

  const handleToggleCompletion = async () => {
    await toggleTaskCompletion(task.id);
  };

  const handleDelete = async () => {
    if (confirm('Are you sure you want to delete this task?')) {
      await deleteTask(task.id);
    }
  };

  // Determine the class for the task based on completion status
  const taskClass = task.completed
    ? 'bg-green-50 border-l-4 border-green-500'
    : 'bg-white border-l-4 border-yellow-500';

  return (
    <li className={`px-4 py-5 sm:px-6 ${taskClass}`}>
      <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between">
        <div className="flex items-start">
          <input
            id={`task-${task.id}`}
            name={`task-${task.id}`}
            type="checkbox"
            checked={task.completed}
            onChange={handleToggleCompletion}
            className="h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded mt-0.5"
          />
          <div className="ml-3 flex-1 min-w-0">
            <label htmlFor={`task-${task.id}`} className={`text-sm font-medium ${task.completed ? 'text-green-800 line-through' : 'text-gray-900'}`}>
              {task.title}
            </label>
            {task.description && (
              <p className={`mt-1 text-sm ${task.completed ? 'text-green-700' : 'text-gray-500'}`}>
                {task.description}
              </p>
            )}
            <div className="mt-2 flex items-center">
              {task.dueDate && (
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${task.completed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                  <svg className="-ml-0.5 mr-1.5 h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" />
                  </svg>
                  {new Date(task.dueDate).toLocaleDateString()}
                </span>
              )}
              {task.completed && (
                <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Completed
                </span>
              )}
            </div>
          </div>
        </div>
        <div className="mt-4 sm:mt-0 sm:ml-4 flex flex-shrink-0">
          <Link
            href={`/tasks/${task.id}`}
            className="inline-flex items-center px-3 py-1 border border-transparent text-sm leading-4 font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            View
          </Link>
          <button
            onClick={handleDelete}
            className="ml-2 inline-flex items-center px-3 py-1 border border-transparent text-sm leading-4 font-medium rounded-md text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            Delete
          </button>
        </div>
      </div>
    </li>
  );
}