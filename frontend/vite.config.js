import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path'; // Windows path resolution ke liye essential framework

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  },
  test: {
    globals: true,
    environment: 'jsdom',
    // Path Fixed: Using path.resolve to force cross-platform absolute mapping
    setupFiles: path.resolve(__dirname, './src/test/setup.js'),
  },
});