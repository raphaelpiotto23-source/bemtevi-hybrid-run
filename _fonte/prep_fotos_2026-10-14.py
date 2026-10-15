"""Fotos reais da corrida e do bar (02_Campanha/Corrida_assets, 07/10/2026) e o logo oficial da prova.
Gera public/img/fotos/*.webp e src/data/fotos2.json. Rode a partir da raiz do site.
"""
import json, os
from PIL import Image, ImageOps, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "..", "..", "02_Campanha", "Corrida_assets")
def out(*p):
    d = os.path.join(ROOT, *p); os.makedirs(os.path.dirname(d), exist_ok=True); return d

SEL = {
    "fachada": ("WhatsApp Image 2026-10-07 at 10.52.33.jpeg", "Fachada do Bem Te Vi ao entardecer, com o letreiro 'seu lugar de pouso'", None),
    "placa":   ("WhatsApp Image 2026-10-07 at 10.52.40.jpeg", "Placa da Confraria Bem Te Vi contra o céu do fim de tarde", None),
    "equipe":  ("WhatsApp Image 2026-10-07 at 11.22.12.jpeg", "Grupo de corredores com número de peito numa rua de São João da Boa Vista", None),
    "mesa":    ("WhatsApp Image 2026-10-07 at 11.33.38.jpeg", "Amigos à mesa no Bem Te Vi, à noite", (0, 0.11, 1, 0.86)),  # tira a moldura do Instagram
    "noite":   ("rhayla_spcity_lt1_0655.jpg.jpeg", "Corredor em prova noturna", None),
}
manifest = {}
for name, (f, alt, crop) in SEL.items():
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, f))).convert("RGB")
    if crop:
        w, h = im.size; im = im.crop((int(w * crop[0]), int(h * crop[1]), int(w * crop[2]), int(h * crop[3])))
    w, h = im.size; sizes = {}
    for target in (1600, 800, 480):
        r = min(1, target / w)
        im2 = im.resize((round(w * r), round(h * r)), Image.LANCZOS)
        p = out("public", "img", "fotos", f"{name}-{target}.webp")
        im2.save(p, "WEBP", quality=78, method=6)
        sizes[target] = {"w": im2.width, "h": im2.height, "kb": os.path.getsize(p) // 1024}
    manifest[name] = {"alt": alt, "src": f, "sizes": sizes}
    print(name, sizes)

# hero no celular: recorte 3:4 da fachada, foco no letreiro
im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, SEL["fachada"][0]))).convert("RGB")
w, h = im.size; ch = int(w * 4 / 3); crop = im.crop((0, 0, w, min(h, ch))).resize((640, int(640 * min(h, ch) / w)), Image.LANCZOS)
crop.save(out("public", "img", "fotos", "fachada-m-640.webp"), "WEBP", quality=74, method=6)
print("fachada-m", crop.size)

# logo oficial da corrida: círculo recortado com fundo transparente, 512 e 160
lg = Image.open(os.path.join(SRC, "Logo Corrida.jpeg")).convert("RGB")
s = min(lg.size); lg = lg.crop(((lg.width - s) // 2, (lg.height - s) // 2, (lg.width + s) // 2, (lg.height + s) // 2))
for size in (512, 160):
    l2 = lg.resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0); ImageDraw.Draw(mask).ellipse((1, 1, size - 2, size - 2), fill=255)
    rgba = l2.convert("RGBA"); rgba.putalpha(mask)
    rgba.save(out("public", "img", f"logo-corrida-{size}.png"), optimize=True)
    print("logo", size, os.path.getsize(out("public", "img", f"logo-corrida-{size}.png")) // 1024, "KB")
json.dump(manifest, open(out("src", "data", "fotos2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
