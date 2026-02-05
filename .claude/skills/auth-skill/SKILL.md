---
name: auth-skill
description: Handle authentication flows including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Auth Skill – Signup, Signin, JWT & Better Auth

## Instructions
Implement secure and scalable authentication systems with the following features:

1. **User Signup**
   - Validate user input (email, password, etc.)
   - Hash passwords before storing in database
   - Prevent duplicate accounts

2. **User Signin**
   - Verify user credentials
   - Compare hashed passwords securely
   - Return authentication token on success

3. **Password Hashing**
   - Use bcrypt or argon2 for hashing
   - Apply proper salt rounds
   - Never store plain text passwords

4. **JWT Token Handling**
   - Generate access tokens on login
   - Verify tokens for protected routes
   - Handle token expiration properly

5. **Better Auth Integration**
   - Configure Better Auth provider
   - Use built-in session management
   - Support social login if required