#!/usr/bin/env node
// Cross-platform script to set environment variables and run Next.js dev server

const { spawn } = require('child_process');
const os = require('os');

// Set environment variable to disable Turbopack
process.env.NEXT_PUBLIC_TURBOPACK = '0';

// Determine the command based on the OS
const isWindows = os.platform() === 'win32';
const command = isWindows ? 'npx.cmd' : 'npx';
const args = ['next', 'dev', '--port', '3001'];

// Spawn the next dev process with shell option for Windows compatibility
const devServer = spawn(command, args, {
  stdio: 'inherit',
  env: process.env,
  shell: isWindows  // Use shell on Windows for better compatibility
});

devServer.on('error', (err) => {
  console.error('Failed to start dev server:', err.message);
  process.exit(1);
});

devServer.on('close', (code) => {
  console.log(`Dev server exited with code ${code}`);
  process.exit(code);
});