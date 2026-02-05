// src/lib/better-auth.ts
import { createAuthClient } from "better-auth/react";

// Create the auth client
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000",
  // Add any additional configuration options here
});