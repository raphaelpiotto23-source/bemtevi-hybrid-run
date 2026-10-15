"""Prepara os ativos do site a partir do que já existe na pasta do projeto. 14/10/2026.

- Artes da campanha -> public/img/artes/*.webp (1080, 800 e 480 de largura)
- Pássaro do selo (PNG base64 dentro de selo_oficial.html) -> public/img/passaro.png
- Rotas: 5 km do DTS (29/09) e o eixo do KML (22/09) viram GPX em public/route/;
  o reconhecimento do 10 km (Strava 11/07) vira GPX com elevação, como referência.
Rode: python _fonte/prep_assets.py  (a partir da raiz do site)
"""
import base64, json, math, os, re, sys
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ = os.path.abspath(os.path.join(ROOT, "..", ".."))          # 02_Hybrid_Run_BemTeVi
DESK = os.path.abspath(os.path.join(PROJ, "..", ".."))          # Desktop
FOTOS = os.path.join(PROJ, "01_Marca", "Ativos", "Fotos")

def out(*p):
    d = os.path.join(ROOT, *p); os.makedirs(os.path.dirname(d), exist_ok=True); return d

# ---------- artes da campanha ----------
# 14/10, pedido do Raphael: nada de foto do clube; usar as peças da campanha da corrida (navy, pássaro, ondas).
# Só peças sem horário ou preço impresso: esses dados mudaram desde agosto e moram no event.json.
ARTES = os.path.join(PROJ, "02_Campanha", "01_Artes")
SEL = {
    "arte_mesa":   (os.path.join(ARTES, "2026-07-14_Lancamento", "Card2_AMesa.png"), "Arte da campanha: a única corrida onde a linha de chegada é a mesa"),
    "arte_ritual": (os.path.join(ARTES, "2026-07-14_Lancamento", "Card3_RitualDoPouso.png"), "Arte da campanha: cruzou a linha? Agora começa o pouso, em cinco passos"),
    "arte_kit":    (os.path.join(ARTES, "2026-08-26_Corrida", "P13_kit_c1.png"), "Arte da campanha: o que chega na tua mão antes da largada"),
    "arte_brinde": (os.path.join(ARTES, "2026-08-26_Corrida", "P12_mesa_c4.png"), "Arte da campanha: o brinde do bando, todo mundo junto de uma vez só"),
}
manifest = {}
for name, (src, alt) in SEL.items():
    im = Image.open(src).convert("RGB")
    w, h = im.size
    sizes = {}
    for target in (1080, 800, 480):
        r = min(1, target / w)
        im2 = im.resize((round(w * r), round(h * r)), Image.LANCZOS)
        p = out("public", "img", "artes", f"{name}-{target}.webp")
        im2.save(p, "WEBP", quality=82, method=6)
        sizes[target] = {"w": im2.width, "h": im2.height, "kb": os.path.getsize(p) // 1024}
    manifest[name] = {"alt": alt, "src": os.path.relpath(src, DESK), "sizes": sizes}
    print(name, sizes)
json.dump(manifest, open(out("src", "data", "fotos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# Leaflet: CSS e ícones servidos de public/, carregados só quando o mapa nasce
import shutil
os.makedirs(out("public", "leaflet", "x"), exist_ok=True)
shutil.copy(os.path.join(ROOT, "node_modules", "leaflet", "dist", "leaflet.css"), out("public", "leaflet", "leaflet.css"))
shutil.copytree(os.path.join(ROOT, "node_modules", "leaflet", "dist", "images"), out("public", "leaflet", "images"), dirs_exist_ok=True)

# ---------- pássaro ----------
html = open(os.path.join(PROJ, "02_Campanha", "03_Fontes", "assets", "selo_oficial.html"), encoding="utf-8").read()
m = re.search(r'data:image/png;base64,([A-Za-z0-9+/=]+)', html)
if m:
    raw = base64.b64decode(m.group(1))
    p = out("public", "img", "passaro.png"); open(p, "wb").write(raw)
    im = Image.open(p); print("passaro", im.size, im.mode, os.path.getsize(p) // 1024, "KB")
    # recorte do conteúdo não transparente + versão pequena
    if im.mode == "RGBA":
        bb = im.getbbox(); im = im.crop(bb)
        im.save(out("public", "img", "passaro.png"))
        s = im.copy(); s.thumbnail((640, 640)); s.save(out("public", "img", "passaro-640.png"), optimize=True)
        print("passaro recortado", im.size, "640:", os.path.getsize(out("public","img","passaro-640.png")) // 1024, "KB")

# ---------- rotas ----------
def hav(a, b):
    R = 6371000; la1, lo1 = map(math.radians, a); la2, lo2 = map(math.radians, b)
    d = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(d))

def write_gpx(path, name, pts, ele=None):
    seg = []
    for i, (la, lo) in enumerate(pts):
        e = f"<ele>{ele[i]}</ele>" if ele else ""
        seg.append(f'<trkpt lat="{la:.6f}" lon="{lo:.6f}">{e}</trkpt>')
    gpx = ('<?xml version="1.0" encoding="UTF-8"?>\n<gpx version="1.1" creator="The Hybrid Club" '
           'xmlns="http://www.topografix.com/GPX/1/1">\n<metadata><name>%s</name></metadata>\n<trk><name>%s</name><trkseg>\n%s\n</trkseg></trk></gpx>\n'
           % (name, name, "\n".join(seg)))
    open(path, "w", encoding="utf-8").write(gpx)
    L = sum(hav(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
    print(os.path.basename(path), len(pts), "pts", round(L), "m")

# 5 km: GPX do DTS (29/09), reamostrado a cada ~15 m para ficar leve
g = open(os.path.join(PROJ, "05_Operacao", "BemTeVi_Hybrid_Run_5km_DTS.gpx"), encoding="utf-8").read()
pts = [(float(a), float(b)) for a, b in re.findall(r'lat="([-\d.]+)" lon="([-\d.]+)"', g)]
keep = [pts[0]]; acc = 0
for i in range(1, len(pts)):
    acc += hav(pts[i - 1], pts[i])
    if acc >= 15: keep.append(pts[i]); acc = 0
if keep[-1] != pts[-1]: keep.append(pts[-1])
write_gpx(out("public", "route", "5k.gpx"), "The Hybrid Run - 5 km (DTS 29/09/2026)", keep)

# 10 km: eixo do KML de 22/09 (BTV -> Anglo -> BTV -> retorno leste -> BTV), sem elevação
k = open(os.path.join(PROJ, "05_Operacao", "BemTeVi_Hybrid_Run_tracado.kml"), encoding="utf-8").read()
segs = re.findall(r'<Placemark><name>(\d)\. [^<]+</name>.*?<coordinates>([^<]+)</coordinates>', k, re.S)
axis = []
for n, coords in sorted(segs):
    for c in coords.split():
        lo, la, _ = c.split(","); axis.append((float(la), float(lo)))
write_gpx(out("public", "route", "10k.gpx"), "The Hybrid Run - 10 km (eixo, em homologacao)", axis)

# referência de campo: Strava 11/07, com elevação
s = json.load(open(os.path.join(ROOT, "_fonte", "strava_19269541648.json"), encoding="utf-8"))
write_gpx(out("public", "route", "10k_ref_strava_2026-07-11.gpx"), "Reconhecimento 10 km - Strava 11/07/2026", [tuple(p) for p in s["location"]], s["altitude"])
