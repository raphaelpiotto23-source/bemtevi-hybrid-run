// Leitura de GPX no build: linha para o mapa estático (celular) e perfil de elevação.
import fs from 'node:fs';
import path from 'node:path';

export function readGpx(publicPath) {
  const file = path.join(process.cwd(), 'public', publicPath);
  const s = fs.readFileSync(file, 'utf8');
  const re = /<trkpt lat="([-\d.]+)" lon="([-\d.]+)">(?:<ele>([-\d.]+)<\/ele>)?/g;
  const pts = [];
  let m;
  while ((m = re.exec(s))) pts.push({ lat: +m[1], lon: +m[2], ele: m[3] != null ? +m[3] : null });
  return pts;
}

export function hav(a, b) {
  const R = 6371000;
  const toR = (x) => (x * Math.PI) / 180;
  const la1 = toR(a.lat), la2 = toR(b.lat);
  const d = Math.sin((la2 - la1) / 2) ** 2 + Math.cos(la1) * Math.cos(la2) * Math.sin(toR(b.lon - a.lon) / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(d));
}

export function cumulative(pts) {
  const out = [0];
  for (let i = 1; i < pts.length; i++) out.push(out[i - 1] + hav(pts[i - 1], pts[i]));
  return out;
}

// Ponto a d metros do início da linha (interpolação linear entre trkpts).
export function pointAt(pts, d) {
  const cum = cumulative(pts);
  if (d <= 0) return { lat: pts[0].lat, lon: pts[0].lon };
  for (let i = 1; i < pts.length; i++) {
    if (cum[i] >= d) {
      const t = (d - cum[i - 1]) / (cum[i] - cum[i - 1] || 1);
      return { lat: pts[i - 1].lat + (pts[i].lat - pts[i - 1].lat) * t, lon: pts[i - 1].lon + (pts[i].lon - pts[i - 1].lon) * t };
    }
  }
  return { lat: pts.at(-1).lat, lon: pts.at(-1).lon };
}

export function gain(pts) {
  let g = 0;
  for (let i = 1; i < pts.length; i++) {
    const d = (pts[i].ele ?? 0) - (pts[i - 1].ele ?? 0);
    if (d > 0) g += d;
  }
  return Math.round(g);
}

// Projeção equirretangular comum a várias rotas, para o SVG estático.
export function projector(routes, w, h, pad = 16) {
  const all = routes.flat();
  const lat0 = all.reduce((s, p) => s + p.lat, 0) / all.length;
  const k = Math.cos((lat0 * Math.PI) / 180);
  const xs = all.map((p) => p.lon * k), ys = all.map((p) => p.lat);
  const minX = Math.min(...xs), maxX = Math.max(...xs), minY = Math.min(...ys), maxY = Math.max(...ys);
  const sx = (w - 2 * pad) / (maxX - minX || 1), sy = (h - 2 * pad) / (maxY - minY || 1);
  const s = Math.min(sx, sy);
  const ox = (w - (maxX - minX) * s) / 2, oy = (h - (maxY - minY) * s) / 2;
  return (p) => ({ x: ox + (p.lon * k - minX) * s, y: h - (oy + (p.lat - minY) * s) });
}

export function toPath(pts, proj) {
  return pts.map((p, i) => { const q = proj(p); return `${i ? 'L' : 'M'}${q.x.toFixed(1)} ${q.y.toFixed(1)}`; }).join('');
}

// Perfil de elevação: polígono fechado (área) e linha, em coordenadas do SVG.
export function elevation(pts, w, h, pad = { l: 36, r: 12, t: 12, b: 24 }) {
  const dist = cumulative(pts);
  const total = dist[dist.length - 1];
  const eles = pts.map((p) => p.ele).filter((e) => e != null);
  const min = Math.floor(Math.min(...eles) / 10) * 10, max = Math.ceil(Math.max(...eles) / 10) * 10;
  const X = (d) => pad.l + (d / total) * (w - pad.l - pad.r);
  const Y = (e) => pad.t + (1 - (e - min) / (max - min || 1)) * (h - pad.t - pad.b);
  const line = pts.map((p, i) => `${i ? 'L' : 'M'}${X(dist[i]).toFixed(1)} ${Y(p.ele).toFixed(1)}`).join('');
  const area = `${line}L${X(total).toFixed(1)} ${(h - pad.b).toFixed(1)}L${pad.l} ${(h - pad.b).toFixed(1)}Z`;
  const kms = [];
  for (let k = 0; k <= Math.floor(total / 1000); k++) kms.push({ km: k, x: X(k * 1000) });
  return { line, area, min, max, total, gain: gain(pts), kms, yMin: Y(min), yMax: Y(max) };
}
