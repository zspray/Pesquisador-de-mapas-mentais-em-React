import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/buscar': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/baixar_imagem': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
})
