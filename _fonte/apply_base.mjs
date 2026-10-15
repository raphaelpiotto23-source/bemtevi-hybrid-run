// Reescreve os caminhos absolutos de dist/ para viver sob um subcaminho (GitHub Pages sem domínio próprio).
// BASE_PATH="/bemtevi-hybrid-run" → "/img/x.webp" vira "/bemtevi-hybrid-run/img/x.webp". Vazio: não faz nada.
import { readdirSync, readFileSync, writeFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const base = (process.env.BASE_PATH || '').replace(/\/$/, '');
if (!base) { console.log('apply_base: sem BASE_PATH, nada a fazer'); process.exit(0); }
const dirs = ['/img/', '/fonts/', '/route/', '/sponsors/', '/leaflet/', '/_astro/', '/og-image.png', '/favicon', '/apple-touch-icon.png', '/site.webmanifest'];
const re = new RegExp(`(["'(=,\\s])(${dirs.map((d) => d.replace(/[.*+?^${}()|[\]\\/]/g, '\\$&')).join('|')})`, 'g');

function walk(dir) {
  for (const f of readdirSync(dir)) {
    const p = join(dir, f);
    if (statSync(p).isDirectory()) { walk(p); continue; }
    if (!/\.(html|js|css|webmanifest|xml|txt)$/.test(f)) continue;
    const s = readFileSync(p, 'utf8');
    const n = s.replace(re, (m, pre, path) => `${pre}${base}${path}`);
    if (n !== s) { writeFileSync(p, n); console.log('base aplicada em', p); }
  }
}
walk('dist');
