"""Revisão 14/10 (noite, 7): LBE patrocinadora, Superação Eventos parceira, fotos de dia em tudo, percurso homologado.
Roda da raiz do site."""
import os, re, json
from PIL import Image, ImageOps
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SRC = os.path.join("..", "..", "02_Campanha", "Corrida_assets")

def sub(p, old, new, count=1):
    s = open(p, encoding="utf-8").read()
    assert s.count(old) == count, (p, old[:70], s.count(old))
    open(p, "w", encoding="utf-8").write(s.replace(old, new))

# ---- fotos de dia
def make(name, file, crop, alt, out_sizes=(1600, 800, 480), q=80):
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, file))).convert("RGB"); w, h = im.size
    if crop: im = im.crop((int(w * crop[0]), int(h * crop[1]), int(w * crop[2]), int(h * crop[3])))
    sizes = {}
    for t in out_sizes:
        r = min(1, t / im.width); im2 = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
        p = f"public/img/fotos/{name}-{t}.webp"; im2.save(p, "WEBP", quality=q, method=6); sizes[t] = {"w": im2.width, "h": im2.height, "kb": os.path.getsize(p) // 1024}
    print(name, sizes); return {"alt": alt, "src": file, "sizes": sizes}
f = json.load(open("src/data/fotos2.json", encoding="utf-8"))
f["avenida"] = make("avenida", "WhatsApp Image 2026-10-07 at 11.03.50.jpeg", (0, 0.05, 1, 0.62), "Av. Dr. Durval Nicolau de manhã, canteiro arborizado e céu azul")
f["verde"] = make("verde", "WhatsApp Image 2026-10-07 at 11.21.19.jpeg", None, "Corredor sorrindo de braços abertos numa prova de rua, céu azul")
f["roxo"] = make("roxo", "WhatsApp Image 2026-10-07 at 11.14.58.jpeg", None, "Corredor com número de peito numa rua de São João da Boa Vista, de dia")
f["placa_dia"] = make("placa_dia", "WhatsApp Image 2026-10-07 at 11.02.59.jpeg", (0.05, 0.14, 0.95, 0.66), "Placa da Confraria Bem Te Vi sob o céu azul de manhã")
json.dump(f, open("src/data/fotos2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def swap(p, var_old, var_new, src_old_re, name, sizes_attr=None):
    s = open(p, encoding="utf-8").read(); assert var_old in s, (p, var_old); s = s.replace(var_old, var_new)
    s, n = re.subn(src_old_re, f'src="/img/fotos/{name}-800.webp" srcset="/img/fotos/{name}-480.webp 480w, /img/fotos/{name}-800.webp 800w, /img/fotos/{name}-1600.webp 1600w"', s); assert n == 1, (p, src_old_re, n)
    open(p, "w", encoding="utf-8").write(s)
# Ideia: avenida + corredor
swap("src/components/Ideia.astro", "const a = fotos.fachada, b = fotos.placa;", "const a = fotos.avenida, b = fotos.verde;", r'src="/img/fotos/fachada-800\.webp" srcset="[^"]*"', "avenida")
s = open("src/components/Ideia.astro", encoding="utf-8").read()
s, n = re.subn(r'src="/img/fotos/placa-480\.webp" srcset="[^"]*"', 'src="/img/fotos/verde-800.webp" srcset="/img/fotos/verde-480.webp 480w, /img/fotos/verde-800.webp 800w, /img/fotos/verde-1600.webp 1600w"', s); assert n == 1
s = s.replace("import artes from '../data/fotos.json';\n", "")
open("src/components/Ideia.astro", "w", encoding="utf-8").write(s)
# Kit: corredor roxo no lugar da arte navy
s = open("src/components/Kit.astro", encoding="utf-8").read()
s = s.replace("import fotos from '../data/fotos.json';", "import fotos from '../data/fotos2.json';").replace("const f = fotos.arte_kit;", "const f = fotos.roxo;")
s, n = re.subn(r'src="/img/artes/arte_kit-800\.webp" srcset="[^"]*"', 'src="/img/fotos/roxo-800.webp" srcset="/img/fotos/roxo-480.webp 480w, /img/fotos/roxo-800.webp 800w, /img/fotos/roxo-1600.webp 1600w"', s); assert n == 1
s = s.replace("  .ph img { width: 100%; height: 100%; object-fit: cover; display: block; }", "  .ph img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 20%; display: block; }")
open("src/components/Kit.astro", "w", encoding="utf-8").write(s)
# Programação: placa de dia no lugar da arte navy
s = open("src/components/Programacao.astro", encoding="utf-8").read()
s = s.replace("import fotos from '../data/fotos.json';", "import fotos from '../data/fotos2.json';").replace("const f = fotos.arte_brinde;", "const f = fotos.placa_dia;")
s, n = re.subn(r'src="/img/artes/arte_brinde-800\.webp" srcset="[^"]*"', 'src="/img/fotos/placa_dia-800.webp" srcset="/img/fotos/placa_dia-480.webp 480w, /img/fotos/placa_dia-800.webp 800w, /img/fotos/placa_dia-1600.webp 1600w"', s); assert n == 1
open("src/components/Programacao.astro", "w", encoding="utf-8").write(s)

# ---- event.json: LBE patrocinadora, Superação parceira, percurso homologado
e = json.load(open("src/data/event.json", encoding="utf-8"))
lbe = next(p for p in e["partners"] if p["name"] == "LBE"); e["partners"].remove(lbe)
lbe["name"] = "LBE"; lbe["role"] = "Branding"
e["sponsors"].append(lbe)
e["partners"].append({"name": "Superação Eventos", "role": "Estrutura do evento", "logo": "TODO", "logoWhite": "TODO", "logoTodo": "Sem logo nos PDFs de orçamento; pedir"})
e["route"]["status"] = "Percurso homologado"
for d in e["distances"]:
    if "gpxStatus" in d: d["gpxStatus"] = d["gpxStatus"].replace("em homologação", "homologado em 14/10 pelo Raphael; falta burocracia interna")
e["photosCredit"] = "Fotos: Confraria Bem Te Vi e corredores de São João da Boa Vista, com autorização"
json.dump(e, open("src/data/event.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
sub("src/components/Percurso.astro", '<svg class="static" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Traçado do percurso: linha ao longo da avenida, com largada e chegada no Bem Te Vi">', '<svg class="static" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Traçado do percurso: linha ao longo da avenida, com largada e chegada na Confraria Bem Te Vi">')
print("revisao ok")
