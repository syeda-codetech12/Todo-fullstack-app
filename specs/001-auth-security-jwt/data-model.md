# Data Model: Todo Full-Stack Web App – Authentication & Security Focus

## User Entity
Represents a registered user with unique identifier, email, name, and account creation/update timestamps

**Fields**:
- id (UUID/string): Unique identifier for the user
- email (string): User's email address (unique, required)
- name (string): User's full name (required)
- hashed_password (string): BCrypt hashed password (required)
- created_at (timestamp): Account creation timestamp
- updated_at (timestamp): Last account update timestamp
- is_active (boolean): Whether the account is active (default: true)

**Validation rules**:
- Email must be a valid email format
- Email must be unique across all users
- Name must be 2-50 characters
- Password must be at least 8 characters with complexity requirements

## Task Entity
User-specific entity containing title, description, completion status, due date, and user relationship

**Fields**:
- id (UUID/string): Unique identifier for the task
- title (string): Task title (required, max 200 chars)
- description (string): Task description (optional, max 1000 chars)
- completed (boolean): Whether the task is completed (default: false)
- due_date (timestamp): Optional deadline for the task
- created_at (timestamp): Task creation timestamp
- updated_at (timestamp): Last task update timestamp
- user_id (UUID/string): Foreign key linking to the owning user

**Validation rules**:
- Title must be 1-200 characters
- Description must be <= 1000 characters if provided
- Due date must be in the future if provided
- User_id must reference an existing user

## JWT Token Entity (Conceptual)
Authentication token containing user identity, expiration time, and signed with secret key

**Fields**:
- token (string): The JWT token string
- user_id (UUID/string): Reference to the user the token belongs to
- issued_at (timestamp): When the token was issued
- expires_at (timestamp): When the token expires
- is_revoked (boolean): Whether the token has been revoked (for refresh tokens)

**Validation rules**:
- Token must be a valid JWT format
- Expires_at must be in the future
- User_id must reference an existing user

## Authentication Session Entity (Conceptual)
Temporary state representing an authenticated user's active session

**Fields**:
- id (UUID/string): Unique identifier for the session
- user_id (UUID/string): Reference to the user the session belongs to
- session_token (string): Session identifier (for httpOnly cookie)
- created_at (timestamp): Session creation timestamp
- expires_at (timestamp): Session expiration timestamp
- ip_address (string): IP address of the client (for security)
- user_agent (string): User agent string (for security)

**Validation rules**:
- Session token must be unique
- Expires_at must be in the future
- User_id must reference an existing user
