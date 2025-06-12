import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  root: 'src',
  resolve: {
    alias: {
      '@': new URL('./src', import.meta.url).pathname
    }
  },
  server: {
    port: 5173,
    proxy: {
      '/users':      'http://localhost:8000',
      '/ressources': 'http://localhost:8000',
      '/emprunts':   'http://localhost:8000'
    },
    // SPA fallback to index.html on refresh
    historyApiFallback: true
  },
  build: { outDir: '../dist', emptyOutDir: true }
})
