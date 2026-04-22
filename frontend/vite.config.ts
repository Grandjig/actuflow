import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig(({ mode }) => {
 const env = loadEnv(mode, process.cwd(), '');
 
 // For GitHub Pages, base should be '/repo-name/'
 // For other deployments, use '/'
 const base = process.env.GITHUB_PAGES === 'true' ? '/actuflow/' : '/';

 return {
 plugins: [react()],
 base,
 resolve: {
 alias: {
 '@': path.resolve(__dirname, './src'),
 },
 },
 define: {
 // Make env variables available
 'import.meta.env.VITE_API_URL': JSON.stringify(
 env.VITE_API_URL || 'http://localhost:8000'
 ),
 },
 server: {
 port: 3000,
 host: true,
 proxy: {
 '/api': {
 target: env.VITE_API_URL || 'http://localhost:8000',
 changeOrigin: true,
 },
 '/ws': {
 target: env.VITE_WS_URL || 'ws://localhost:8000',
 ws: true,
 },
 },
 },
 build: {
 outDir: 'dist',
 sourcemap: false,
 rollupOptions: {
 output: {
 manualChunks: {
 vendor: ['react', 'react-dom', 'react-router-dom'],
 ui: ['antd', '@ant-design/icons'],
 charts: ['recharts'],
 },
 },
 },
 },
 };
});
