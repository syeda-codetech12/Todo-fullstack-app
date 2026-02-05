'use client';

import React from 'react';
import ResponsiveNav from '@/components/navigation/ResponsiveNav';

interface AppShellProps {
  children: React.ReactNode;
}

/**
 * AppShell wraps all pages with the global navigation/header.
 * This ensures the navbar appears consistently on every page
 * while keeping the root layout as a server component.
 */
export default function AppShell({ children }: AppShellProps) {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <ResponsiveNav />
      <main className="flex-grow">
        {children}
      </main>
    </div>
  );
}

