import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Vite configuration
// See https://vitejs.dev/guide/ for more details.

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true,
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
});