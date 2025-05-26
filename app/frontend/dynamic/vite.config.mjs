import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import path from 'path';
import { fileURLToPath } from 'url';

// __dirname workaround for ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default defineConfig({
  root: './',
  build: {
    rollupOptions: {
      input: {
        heatmap: path.resolve(__dirname, 'index.html'),
      }
    },
    outDir: '../static/dist',
    emptyOutDir: true
  },
  plugins: [svelte()]
});
