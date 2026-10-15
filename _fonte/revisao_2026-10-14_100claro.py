"""Revisão 14/10 (noite, 5): site 100% claro, nenhum fundo navy. Hero com foto emoldurada, fecho em areia,
treinão claro, mapa com tiles claros. Roda da raiz do site."""
import os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

def sub(p, old, new, count=1):
    s = open(p, encoding="utf-8").read()
    assert s.count(old) == count, (p, old[:70], s.count(old))
    open(p, "w", encoding="utf-8").write(s.replace(old, new))

# ---- Hero: claro, foto emoldurada
H = "src/components/Hero.astro"
s = open(H, encoding="utf-8").read()
s = s.replace('<section id="inicio" class="hero dark">', '<section id="inicio" class="hero">')
s = re.sub(r'  <picture>.*?</picture>\n  <div class="veil" aria-hidden="true"></div>\n', '', s, flags=re.S)
s = s.replace('  <div class="wrap content">\n', '  <div class="wrap grid">\n  <div class="content">\n')
s = s.replace('    <p class="vagas label">{event.capacity} vagas · Corrida 10 km e 5 km · Caminhada 3 km</p>\n  </div>\n</section>',
 '''    <p class="vagas label">{event.capacity} vagas · Corrida 10 km e 5 km · Caminhada 3 km</p>
  </div>
  <figure class="ph">
    <picture>
      <source media="(max-width: 819px)" srcset="/img/fotos/dia-m-640.webp" />
      <img src="/img/fotos/dia-800.webp" srcset={`/img/fotos/dia-800.webp 800w, /img/fotos/dia-1600.webp ${f.sizes['1600'].w}w`} sizes="(min-width: 820px) 46vw, 100vw" width={f.sizes['800'].w} height={f.sizes['800'].h} alt={f.alt} fetchpriority="high" decoding="async" />
    </picture>
  </figure>
  </div>
</section>''')
# estilos
s = re.sub(r"<style>.*?</style>", """<style>
  .hero { background: var(--color-paper); overflow: hidden; }
  .grid { display: grid; gap: 28px; padding-block: 32px 56px; }
  .ph { margin: 0; border-radius: 20px; overflow: hidden; aspect-ratio: 4 / 3; order: -1; }
  .ph img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 30%; display: block; }
  .content { display: grid; gap: 20px; }
  .collab { display: flex; align-items: center; gap: 14px; }
  .selo { width: 64px; height: 64px; border-radius: 50%; box-shadow: 0 0 0 2px var(--line); }
  .when { font-size: clamp(14px, 1.6vw, 18px); letter-spacing: 0.16em; color: var(--accent); font-weight: 600; }
  .hook { font-size: clamp(20px, 2.4vw, 30px); font-weight: 400; max-width: 640px; line-height: 1.3; }
  .count { margin-top: 8px; }
  .units { display: flex; gap: 20px; flex-wrap: wrap; }
  .unit { display: grid; gap: 4px; }
  .num { font-size: clamp(40px, 7vw, 76px); font-weight: 600; line-height: 1; letter-spacing: -0.02em; perspective: 300px; }
  .count-msg { font-size: clamp(28px, 4.5vw, 52px); font-weight: 800; line-height: 1.1; }
  .actions { display: flex; flex-wrap: wrap; align-items: center; gap: 16px; margin-top: 8px; }
  .vagas { margin-top: 4px; }
  @media (min-width: 820px) {
    .grid { grid-template-columns: 1.1fr 1fr; align-items: center; gap: 56px; padding-block: 72px 96px; min-height: min(100svh, 880px); }
    .ph { order: 0; aspect-ratio: 5 / 4; }
    .selo { width: 80px; height: 80px; }
  }
</style>""", s, flags=re.S)
assert "veil" not in s and 'class="ph"' in s
open(H, "w", encoding="utf-8").write(s)

# ---- Fecho: areia, pássaro navy, sem foto
F = "src/components/Fecho.astro"
s = open(F, encoding="utf-8").read()
s = s.replace('<section id="fecho" class="fecho dark">', '<section id="fecho" class="fecho sand">')
s = re.sub(r'  <img class="bg"[^\n]*\n  <div class="veil" aria-hidden="true"></div>\n', '', s)
s = s.replace('<img class="bird" src="/img/passaro-branco-640.png"', '<img class="bird" src="/img/passaro-640.png"')
s = re.sub(r"  \.bg \{[^\n]*\n  \.veil \{[^\n]*\n", "", s)
s = s.replace("import fotos from '../data/fotos2.json';\n", "").replace("const f = fotos.noite;\n", "")
s = s.replace('<section id="patrocinio" class="sec">', '<section id="patrocinio" class="sec">')
assert "veil" not in s and "passaro-640" in s
open(F, "w", encoding="utf-8").write(s)

# ---- Treinão: card claro
T = "src/components/Treinao.astro"
sub(T, "  .big { display: grid; gap: 6px; align-content: start; padding: 28px; border-radius: 20px; background: var(--color-navy); color: var(--color-paper); }\n  .big .label { color: var(--color-mute); }",
       "  .big { display: grid; gap: 6px; align-content: start; padding: 28px; border-radius: 20px; background: var(--color-paper); border: 1px solid var(--line); }")
sub(T, "  .hour { font-size: clamp(28px, 3.6vw, 40px); font-weight: 600; color: var(--color-aqua); line-height: 1.1; }\n  .where { color: var(--color-mute); font-size: 15px; margin-top: 6px; }",
       "  .hour { font-size: clamp(28px, 3.6vw, 40px); font-weight: 600; color: var(--accent); line-height: 1.1; }\n  .where { color: var(--fg2); font-size: 15px; margin-top: 6px; }")

# ---- Percurso: mapa claro
P = "src/components/Percurso.astro"
sub(P, "  .mapa :global(.leaflet-tile-pane) { filter: invert(1) hue-rotate(190deg) brightness(.72) contrast(.9) saturate(.25); }\n", "  .mapa :global(.leaflet-tile-pane) { filter: saturate(.35) contrast(.95); }\n")
sub(P, "border: 1px solid var(--line); background: var(--color-navy); }", "border: 1px solid var(--line); background: var(--color-sand); }")
sub(P, '<path class="r r10" d={path10} fill="none" stroke="#3F839E"', '<path class="r r10" d={path10} fill="none" stroke="#0B1F3A"')
sub(P, '<path class="r r5" d={path5} fill="none" stroke="#2ABFCC"', '<path class="r r5" d={path5} fill="none" stroke="#1B7A8C"')
sub(P, '<circle class="mk" cx={m.x} cy={m.y} r="4" fill="#2ABFCC">', '<circle class="mk" cx={m.x} cy={m.y} r="4" fill="#2ABFCC" stroke="#0B1F3A" stroke-width="1">')
sub(P, '<circle cx={p.x} cy={p.y} r="9" fill="#0B1F3A" stroke="#FDFBF7" stroke-width="3" />', '<circle cx={p.x} cy={p.y} r="9" fill="#FDFBF7" stroke="#0B1F3A" stroke-width="3" />')
sub(P, 'font-size="13" font-weight="600" fill="#FDFBF7">{p.label}</text>', 'font-size="13" font-weight="600" fill="#0B1F3A">{p.label}</text>')
sub(P, "padding: 8px 16px; background: var(--color-paper); color: var(--color-navy); border-color: var(--color-paper); }", "padding: 8px 16px; background: var(--color-paper); color: var(--color-navy); border-color: var(--color-navy); }")
# Leaflet: linha do 10 km em navy e do 5 km em teal, marcadores claros
M = "src/scripts/mapa.js"
sub(M, "  const colors = { '10k': '#3F839E', '5k': '#2ABFCC' };", "  const colors = { '10k': '#0B1F3A', '5k': '#1B7A8C' };")
sub(M, "L.circleMarker([p.lat, p.lon], { radius: 8, color: '#FDFBF7', weight: 3, fillColor: '#0B1F3A', fillOpacity: 1 })", "L.circleMarker([p.lat, p.lon], { radius: 8, color: '#0B1F3A', weight: 3, fillColor: '#FDFBF7', fillOpacity: 1 })")
sub(M, "L.circleMarker([m.lat, m.lon], { radius: 5, color: '#2ABFCC', weight: 2, fillColor: '#0B1F3A', fillOpacity: 1 })", "L.circleMarker([m.lat, m.lon], { radius: 5, color: '#0B1F3A', weight: 2, fillColor: '#2ABFCC', fillOpacity: 1 })")

# ---- Ideia: fachada no lugar da arte navy
I = "src/components/Ideia.astro"
sub(I, "const a = artes.arte_mesa, b = fotos.placa;", "const a = fotos.fachada, b = fotos.placa;")
s = open(I, encoding="utf-8").read()
s = re.sub(r'src="/img/artes/arte_mesa-800\.webp" srcset="[^"]*"', 'src="/img/fotos/fachada-800.webp" srcset="/img/fotos/fachada-480.webp 480w, /img/fotos/fachada-800.webp 800w, /img/fotos/fachada-1600.webp 1313w"', s)
assert "fachada-800" in s
open(I, "w", encoding="utf-8").write(s)

# ---- theme-color e OG claros
sub("src/layouts/Base.astro", '<meta name="theme-color" content="#0B1F3A" />', '<meta name="theme-color" content="#FDFBF7" />')
print("revisao ok")
