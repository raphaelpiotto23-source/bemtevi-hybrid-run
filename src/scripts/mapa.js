// Mapa interativo (Leaflet + OSM escurecido por CSS), só no desktop e só quando a seção aparece.
// Os tiles dark da CARTO passaram a exigir chave de API (visto em 14/10/2026); OSM com filtro não precisa.
// No celular fica o SVG estático renderizado no build. O toggle 5 km / 10 km vale para os dois.
import event from '../data/event.json';

const wrap = document.querySelector('[data-route]');
const buttons = Array.from(document.querySelectorAll('[data-show]'));
let map = null, layers = {};

function setActive(id) {
  wrap.dataset.active = id;
  buttons.forEach((b) => { const on = b.dataset.show === id; b.classList.toggle('on', on); b.setAttribute('aria-pressed', String(on)); });
  if (map) {
    Object.entries(layers).forEach(([k, g]) => { if (k === id) g.addTo(map); else map.removeLayer(g); });
    map.fitBounds(layers[id].getBounds(), { padding: [24, 24] });
  }
}
buttons.forEach((b) => b.addEventListener('click', () => setActive(b.dataset.show)));

function parseGpx(txt) {
  const re = /<trkpt lat="([-\d.]+)" lon="([-\d.]+)"/g; const pts = []; let m;
  while ((m = re.exec(txt))) pts.push([+m[1], +m[2]]);
  return pts;
}

async function boot() {
  const L = (await import('leaflet')).default;
  // CSS do Leaflet só quando o mapa nasce (copiado de node_modules para public/leaflet no prep_assets.py)
  await new Promise((ok) => { const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = '/leaflet/leaflet.css'; l.onload = ok; l.onerror = ok; document.head.appendChild(l); });
  map = L.map('mapa', { scrollWheelZoom: false, attributionControl: true });
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>', maxZoom: 19,
  }).addTo(map);
  const colors = { '10k': '#0B1F3A', '5k': '#1B7A8C' };
  for (const d of event.distances.filter((x) => x.gpx !== 'TODO')) {
    const pts = parseGpx(await (await fetch(d.gpx)).text());
    const g = L.featureGroup();
    L.polyline(pts, { color: colors[d.id], weight: 5, opacity: 0.95, lineJoin: 'round' }).addTo(g);
    event.route.points.filter((p) => p.dists.includes(d.id)).forEach((p) => {
      L.circleMarker([p.lat, p.lon], { radius: 8, color: '#0B1F3A', weight: 3, fillColor: '#FDFBF7', fillOpacity: 1 })
        .bindPopup(`<strong>${p.label}</strong><br>${p.detail}`).addTo(g);
    });
    // marcos do caminho, clicáveis, nas duas distâncias
    (JSON.parse(wrap.dataset.landmarks || '[]')).forEach((m) => {
      L.circleMarker([m.lat, m.lon], { radius: 5, color: '#0B1F3A', weight: 2, fillColor: '#2ABFCC', fillOpacity: 1 })
        .bindPopup(`<strong>km ${m.km.toLocaleString('pt-BR')}</strong><br>${m.name}`).addTo(g);
    });
    layers[d.id] = g;
  }
  setActive(wrap.dataset.active || '10k');
}

if (matchMedia('(min-width: 820px)').matches && document.getElementById('mapa')) {
  const io = new IntersectionObserver(([e]) => { if (e.isIntersecting) { io.disconnect(); boot(); } }, { rootMargin: '200px' });
  io.observe(wrap);
}
