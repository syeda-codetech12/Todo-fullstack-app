# Quickstart Guide: Todo Full-Stack Web App – Frontend Interface

## Prerequisites

- Node.js 18.x or later
- npm or yarn package manager
- Access to the backend API (running on http://localhost:8000 or your deployed URL)

## Setup Instructions

### 1. Clone and Navigate to Project Directory
```bash
# If the frontend directory doesn't exist yet
mkdir frontend
cd frontend
```

### 2. Initialize Next.js Application
```bash
npx create-next-app@latest .
# Select the following options:
# - Yes for TypeScript
# - Yes for ESLint
# - Yes for Tailwind CSS
# - Yes for src directory
# - App Router: Yes
# - Strict Mode: Yes
# - Bundle Analyzer: No
```

### 3. Install Additional Dependencies
```bash
npm install better-auth @better-auth/react
# Additional dependencies as needed
npm install @hookform/resolvers zod react-hook-form
npm install axios
npm install @types/node --save-dev
```

### 4. Environment Configuration
Create a .env.local file in the frontend directory with the following:

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_JWT_SECRET=your_jwt_secret_here
AUTH_SECRET=your_auth_secret_here
```

### 5. Project Structure Setup
After initialization, your project structure should look like:

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router structure
│   │   ├── (auth)/          # Authentication routes (signup, signin)
│   │   │   ├── signup/
│   │   │   └── signin/
│   │   ├── dashboard/       # Protected route for task management
│   │   ├── tasks/           # Task-related pages
│   │   │   ├── create/
│   │   │   ├── [id]/        # Individual task view/edit
│   │   │   └── layout.tsx   # Shared task layout
│   │   ├── globals.css      # Global styles
│   │   ├── layout.tsx       # Root layout
│   │   └── page.tsx         # Home page
│   ├── components/          # Reusable UI components
│   │   ├── ui/              # Base UI components (buttons, inputs, etc.)
│   │   ├── auth/            # Authentication components
│   │   ├── tasks/           # Task-specific components
│   │   └── navigation/      # Navigation components
│   ├── hooks/               # Custom React hooks
│   │   ├── useAuth.ts       # Authentication state management
│   │   └── useTasks.ts      # Task management hooks
│   ├── lib/                 # Utility functions
│   │   ├── auth.ts          # Authentication utilities
│   │   ├── api.ts           # API client and utilities
│   │   └── types.ts         # TypeScript type definitions
│   ├── providers/           # React context providers
│   │   └── AuthProvider.tsx # Authentication context
│   └── middleware.ts        # Next.js middleware for protected routes
├── public/                  # Static assets
├── package.json
├── next.config.js
├── tailwind.config.js       # Or other styling configuration
├── tsconfig.json
└── README.md
```

## Running the Application

### Development Mode
```bash
npm run dev
```

The application will be available at http://localhost:3000

### Production Build
```bash
npm run build
npm run start
```

## Testing Procedures

### Unit Tests
```bash
npm run test
```

### Linting
```bash
npm run lint
```

### Type Checking
```bash
npm run type-check
```

## Key Features Implementation

### 1. Better Auth Integration
- Configure Better Auth in lib/auth.ts
- Set up authentication context in providers/AuthProvider.tsx
- Implement login/signup pages in app/(auth)/

### 2. Protected Routes
- Create middleware to protect routes requiring authentication
- Implement redirect logic for unauthorized access

### 3. Task Management Components
- Create task list component in components/tasks/TaskList.tsx
- Create task form component in components/tasks/TaskForm.tsx
- Implement CRUD operations using API client

### 4. API Client with JWT
- Create API client in lib/api.ts with interceptors
- Automatically attach Authorization header with JWT token
- Handle token expiration and refresh

### 5. Responsive Design
- Use Tailwind CSS utility classes for responsive layouts
- Implement mobile-first design approach
- Test on various screen sizes
