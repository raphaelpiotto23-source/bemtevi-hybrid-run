import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// site: TODO (domínio a definir). Quando existir, colocar aqui e no event.json (siteUrl).
export default defineConfig({
  vite: { plugins: [tailwindcss()] },
  build: { inlineStylesheets: 'always' },
  compressHTML: true,
  server: { host: '127.0.0.1', port: 4321 },
});
