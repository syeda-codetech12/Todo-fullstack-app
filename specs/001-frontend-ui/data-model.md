# Data Model: Todo Full-Stack Web App – Frontend Interface

## User Entity Representation

### User Interface
```typescript
interface User {
  id: string;
  email: string;
  name?: string;
  createdAt: Date;
  updatedAt: Date;
}
```

### Session State
```typescript
interface SessionState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}
```

## Task Entity Structure

### Task Interface
```typescript
interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  dueDate?: Date;
  createdAt: Date;
  updatedAt: Date;
  userId: string; // Owner of the task
}
```

### Task Form Data
```typescript
interface TaskFormData {
  title: string;
  description?: string;
  dueDate?: Date;
}
```

## State Management Patterns

### Authentication State Management
- Use React Context to maintain authentication state across the application
- Store user information and authentication tokens in the context
- Provide helper functions to update authentication state
- Implement loading states for authentication operations

### Task State Management
- Use React Context for shared task state across components
- Implement optimistic updates for better user experience
- Handle loading states for task operations
- Manage filtering and sorting of tasks

## API Response Types

### Authentication Responses
```typescript
interface LoginResponse {
  user: User;
  token: string;
  refreshToken: string;
}

interface RegisterResponse {
  user: User;
  token: string;
  refreshToken: string;
}
```

### Task API Responses
```typescript
interface TaskApiResponse {
  data: Task[];
  pagination?: {
    currentPage: number;
    totalPages: number;
    totalCount: number;
  };
}

interface SingleTaskApiResponse {
  data: Task;
}
```

### Error Response
```typescript
interface ErrorResponse {
  error: string;
  message: string;
  statusCode: number;
}
```

## Form Validation Schema

### Login Form Validation
- Email: Required, valid email format
- Password: Required, minimum length 8 characters

### Registration Form Validation
- Email: Required, valid email format
- Password: Required, minimum length 8 characters, includes special character
- Name: Optional, maximum length 100 characters

### Task Form Validation
- Title: Required, maximum length 200 characters
- Description: Optional, maximum length 1000 characters
- Due Date: Optional, must be a valid date in the future

## UI State Models

### Loading States
- Global loading indicator
- Per-component loading states
- Skeleton loading for task lists

### Error States
- Form validation errors
- API error messages
- Network error handling
- Unauthorized access handling

### Success States
- Confirmation messages
- Toast notifications
- Optimistic UI updates

## Responsive Design States

### Screen Size Breakpoints
- Mobile: 320px - 768px
- Tablet: 768px - 1024px
- Desktop: 1024px+

### Component Adaptations
- Collapsible navigation on mobile
- Stacked vs side-by-side layouts
- Touch-friendly controls
- Font size adjustments

