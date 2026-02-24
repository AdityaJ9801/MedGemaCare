import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
      '/login': 'http://localhost:8000',
      '/patients': 'http://localhost:8000',
      '/prescriptions': 'http://localhost:8000',
      '/reports': 'http://localhost:8000',
      '/files': 'http://localhost:8000',
    },
  },
})
