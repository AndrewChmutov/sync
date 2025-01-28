import { fileURLToPath, URL } from 'node:url'
import fs from "fs";

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  server: {
    port: 7777,
    https: {
      key: fs.readFileSync('../cert/key.pem', "utf-8"),
      cert: fs.readFileSync('../cert/cert.pem', "utf-8"),
    },
    proxy: {
      '/api': {
        target: 'https://localhost:8000',
        secure: true,
        changeOrigin: true,
      },
      '/socket.io': {
        target: 'wss://localhost:8000',
        ws: true,
        secure: true,
        changeOrigin: true,
      },
    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
