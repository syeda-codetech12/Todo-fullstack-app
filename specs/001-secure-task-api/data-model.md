# Data Model: Secure Task API with User-Specific Data

## Overview
This document defines the data models for the secure task API, including entities, relationships, and validation rules.

## Entities

### User Entity
Represents an authenticated user of the system.

**Fields**:
- `id` (UUID, Primary Key): Unique identifier for the user
- `email` (String, Required, Unique): User's email address
- `hashed_password` (String, Required): BCrypt hashed password
- `first_name` (String, Optional): User's first name
- `last_name` (String, Optional): User's last name
- `created_at` (DateTime, Required): Timestamp when user was created
- `updated_at` (DateTime, Required): Timestamp when user was last updated
- `is_active` (Boolean, Default: True): Whether the user account is active

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Password must meet minimum complexity requirements (handled during registration)
- First and last names must not exceed 50 characters each

### Task Entity
Represents a user's task with properties like title, description, status, creation date, and modification date, linked to a specific user.

**Fields**:
- `id` (UUID, Primary Key): Unique identifier for the task
- `title` (String, Required): Title of the task (max 200 characters)
- `description` (Text, Optional): Detailed description of the task
- `status` (String, Required, Default: "pending"): Current status of the task (values: "pending", "in_progress", "completed")
- `priority` (String, Optional, Default: "medium"): Priority level (values: "low", "medium", "high")
- `due_date` (DateTime, Optional): Deadline for completing the task
- `user_id` (UUID, Foreign Key): Reference to the user who owns this task
- `created_at` (DateTime, Required): Timestamp when task was created
- `updated_at` (DateTime, Required): Timestamp when task was last updated
- `completed_at` (DateTime, Optional): Timestamp when task was marked as completed
- `deleted_at` (DateTime, Optional): Timestamp when task was soft-deleted (null if not deleted)

**Validation Rules**:
- Title must be between 1 and 200 characters
- Description must not exceed 1000 characters
- Status must be one of the allowed values: "pending", "in_progress", "completed"
- Priority must be one of the allowed values: "low", "medium", "high"
- Due date must be in the future if provided
- User ID must reference an existing user

## Relationships

### User to Tasks
- One-to-Many relationship
- A user can have many tasks
- Tasks are soft-deleted when the owning user is deleted (set deleted_at timestamp)

**Relationship Definition**:
```
User.tasks (relationship field pointing to Task.user_id)
```

## Indexes

### User Entity
- Index on `email` field for fast lookup during authentication
- Index on `is_active` field for filtering active users

### Task Entity
- Index on `user_id` field for efficient retrieval of user-specific tasks
- Index on `status` field for filtering tasks by status
- Index on `due_date` field for sorting and filtering by deadline
- Index on `deleted_at` field for excluding soft-deleted records
- Composite index on (`user_id`, `status`) for efficient queries of user tasks by status

## State Transitions

### Task Status Transitions
Tasks can transition between statuses based on user actions:

1. `pending` → `in_progress`: When user starts working on the task
2. `in_progress` → `completed`: When user finishes the task
3. `completed` → `in_progress`: When user needs to reopen a completed task
4. `in_progress` → `pending`: When user decides to defer the task
5. `completed` → `pending`: When user wants to restart a completed task

## Constraints

### Data Integrity
- All timestamps are stored in UTC
- Task titles must be unique per user (users can't have duplicate task titles)
- Completed tasks must have a `completed_at` timestamp
- Uncompleted tasks must not have a `completed_at` timestamp
- Soft-deleted tasks must have a `deleted_at` timestamp
- Non-deleted tasks must have a NULL `deleted_at` timestamp

### Business Logic
- Users can only modify tasks they own
- Users can only view tasks they own
- Tasks cannot be created with a past due date
- When a task status changes to "completed", the `completed_at` field is automatically set
- When a task status changes from "completed" to any other status, the `completed_at` field is cleared
- When a task is soft-deleted, the `deleted_at` field is set to the current timestamp
- When a task is restored, the `deleted_at` field is set to NULL