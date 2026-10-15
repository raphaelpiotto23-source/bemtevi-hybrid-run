// Move o site de dist/ para dist/<SUBDIR>/ e deixa na raiz só CNAME, robots, sitemap e um redirect.
// Uso no deploy: SUBDIR=bemtevi node _fonte/subdir.mjs (rodar depois do apply_base com BASE_PATH=/bemtevi).
import { readdirSync, mkdirSync, renameSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const sub = (process.env.SUBDIR || '').replace(/^\/|\/$/g, '');
if (!sub) { console.log('subdir: sem SUBDIR, nada a fazer'); process.exit(0); }
const keep = new Set(['CNAME', 'robots.txt', 'sitemap.xml', sub]);
mkdirSync(join('dist', sub), { recursive: true });
for (const f of readdirSync('dist')) {
  if (keep.has(f)) continue;
  renameSync(join('dist', f), join('dist', sub, f));
}
const to = `/${sub}/`;
writeFileSync(join('dist', 'index.html'), `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Bem Te Vi Hybrid Run</title><meta http-equiv="refresh" content="0; url=${to}"><link rel="canonical" href="${to}"><script>location.replace('${to}'+location.search+location.hash)</script></head><body><a href="${to}">Bem Te Vi Hybrid Run</a></body></html>\n`);
writeFileSync(join('dist', '404.html'), `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Bem Te Vi Hybrid Run</title><meta http-equiv="refresh" content="0; url=${to}"><script>location.replace('${to}')</script></head><body><a href="${to}">Bem Te Vi Hybrid Run</a></body></html>\n`);
console.log(`subdir: site movido para /${sub}/ com redirect na raiz`);
