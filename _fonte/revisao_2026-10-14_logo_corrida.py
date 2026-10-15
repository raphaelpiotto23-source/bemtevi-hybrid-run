"""Revisão 14/10 (noite, 4): logo da corrida no lugar do do clube (cabeçalho, favicon, OG), ondas fora,
hero com a foto de dia, parceiros alinhados. Roda da raiz do site."""
import os, re, json
from PIL import Image, ImageOps, ImageDraw, ImageFont
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

def sub(p, old, new, count=1):
    s = open(p, encoding="utf-8").read()
    assert s.count(old) == count, (p, old[:60], s.count(old))
    open(p, "w", encoding="utf-8").write(s.replace(old, new))

# ---- cabeçalho: selo da corrida no lugar das ondas
s = open("src/components/Header.astro", encoding="utf-8").read()
s = re.sub(r'      <svg viewBox="0 0 60 44".*?</svg>\n', '      <img class="selo" src="/img/logo-corrida-160.png" width="36" height="36" alt="" />\n', s, flags=re.S)
s = s.replace("  .brand { display: inline-flex; align-items: center; gap: 12px;", "  .selo { width: 36px; height: 36px; border-radius: 50%; }\n  .brand { display: inline-flex; align-items: center; gap: 12px;")
assert ".selo" in s and "<svg" not in s
open("src/components/Header.astro", "w", encoding="utf-8").write(s)

# ---- ondas fora da página
s = open("src/pages/index.astro", encoding="utf-8").read()
s = s.replace("import Waves from '../components/Waves.astro';\n", "")
s = re.sub(r'    <Waves[^\n]*\n', '', s)
assert "Waves" not in s
open("src/pages/index.astro", "w", encoding="utf-8").write(s)

# ---- favicon e ícones a partir do selo
lg = Image.open("public/img/logo-corrida-512.png").convert("RGBA")
for n, size in [("favicon-32.png", 32), ("favicon-48.png", 48), ("apple-touch-icon.png", 180)]:
    im = lg.resize((size, size), Image.LANCZOS)
    if n == "apple-touch-icon.png":  # iOS não aceita transparência: fundo branco
        bg = Image.new("RGBA", im.size, (253, 251, 247, 255)); bg.alpha_composite(im); im = bg
    im.save(f"public/{n}", optimize=True)
lg.resize((48, 48), Image.LANCZOS).save("public/favicon.ico")
# favicon.svg vira o selo embutido
import base64
b64 = base64.b64encode(open("public/favicon-48.png", "rb").read()).decode()
open("public/favicon.svg", "w", encoding="utf-8").write(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 48 48"><image width="48" height="48" xlink:href="data:image/png;base64,{b64}"/></svg>')

# ---- OG: selo da corrida no lugar das ondas
F = "C:/Users/rapha/AppData/Local/Microsoft/Windows/Fonts/"
W, H = 1200, 630
og = Image.new("RGB", (W, H), (11, 31, 58)); d = ImageDraw.Draw(og)
f_ey = ImageFont.truetype(F + "Poppins-SemiBold.ttf", 22); f_t = ImageFont.truetype(F + "Poppins-ExtraBold.ttf", 118)
f_h = ImageFont.truetype(F + "Poppins-Medium.ttf", 36); f_m = ImageFont.truetype(F + "Poppins-SemiBold.ttf", 26)
x = 80
d.text((x, 80), "THE HYBRID CLUB × BEM TE VI  ·  ETAPA DE ABERTURA DO CIRCUITO HYBRID", font=f_ey, fill=(42, 191, 204))
d.text((x, 122), "The Hybrid", font=f_t, fill=(253, 251, 247)); d.text((x, 240), "Run", font=f_t, fill=(253, 251, 247))
d.text((x, 392), "A única corrida da região onde", font=f_h, fill=(253, 251, 247)); d.text((x, 436), "a linha de chegada é a mesa.", font=f_h, fill=(253, 251, 247))
d.text((x, 540), "29.11.2026  ·  07H30  ·  SÃO JOÃO DA BOA VISTA  ·  BEM TE VI", font=f_m, fill=(42, 191, 204))
selo = lg.resize((300, 300), Image.LANCZOS); og.paste(selo, (W - 80 - 300, 200), selo)
og.save("public/og-image.png", optimize=True)

# ---- hero: foto de dia (placa com céu azul), sem a sobreposição do Strava
SRC = os.path.join("..", "..", "02_Campanha", "Corrida_assets", "WhatsApp Image 2026-10-07 at 11.02.59.jpeg")
im = ImageOps.exif_transpose(Image.open(SRC)).convert("RGB"); w, h = im.size
top = im.crop((0, 0, w, int(h * 0.60)))  # abaixo disso entram a linha laranja e a caixa do Strava
sizes = {}
for t in (1600, 800, 480):
    r = min(1, t / top.width); im2 = top.resize((round(top.width * r), round(top.height * r)), Image.LANCZOS)
    p = f"public/img/fotos/dia-{t}.webp"; im2.save(p, "WEBP", quality=80, method=6); sizes[t] = {"w": im2.width, "h": im2.height, "kb": os.path.getsize(p) // 1024}
mob = top.crop((int(w * 0.18), 0, int(w * 0.82), top.height)); mob = mob.resize((640, int(640 * mob.height / mob.width)), Image.LANCZOS)
mob.save("public/img/fotos/dia-m-640.webp", "WEBP", quality=76, method=6)
f = json.load(open("src/data/fotos2.json", encoding="utf-8"))
f["dia"] = {"alt": "Placa da Confraria Bem Te Vi de dia, céu azul, árvores da avenida", "src": "02_Campanha/Corrida_assets/WhatsApp Image 2026-10-07 at 11.02.59.jpeg", "sizes": sizes, "mobile": {"w": mob.width, "h": mob.height}}
json.dump(f, open("src/data/fotos2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("dia", sizes, "mob", mob.size)
s = open("src/components/Hero.astro", encoding="utf-8").read()
s = s.replace("const f = fotos.fachada;", "const f = fotos.dia;")
s = s.replace('<source media="(max-width: 819px)" srcset="/img/fotos/fachada-m-640.webp" width="640" height="779" />', f'<source media="(max-width: 819px)" srcset="/img/fotos/dia-m-640.webp" width="{mob.width}" height="{mob.height}" />')
s = s.replace('src="/img/fotos/fachada-800.webp" srcset={`/img/fotos/fachada-800.webp 800w, /img/fotos/fachada-1600.webp ${f.sizes[\'1600\'].w}w`}', 'src="/img/fotos/dia-800.webp" srcset={`/img/fotos/dia-800.webp 800w, /img/fotos/dia-1600.webp ${f.sizes[\'1600\'].w}w`}')
assert "dia-800" in s and "dia-m-640" in s
# véu mais leve: a foto é clara, o texto precisa de navy só embaixo e à esquerda
s = s.replace("background: linear-gradient(180deg, rgba(11,31,58,.55) 0%, rgba(11,31,58,.35) 30%, rgba(11,31,58,.92) 62%, #0B1F3A 100%); }", "background: linear-gradient(180deg, rgba(11,31,58,.35) 0%, rgba(11,31,58,.3) 28%, rgba(11,31,58,.9) 60%, #0B1F3A 100%); }")
s = s.replace(".bg { object-position: 70% 30%; } .veil { background: linear-gradient(90deg, rgba(11,31,58,.95) 0%, rgba(11,31,58,.8) 40%, rgba(11,31,58,.3) 100%), linear-gradient(180deg, rgba(11,31,58,0) 60%, #0B1F3A 100%); }", ".bg { object-position: 60% 35%; } .veil { background: linear-gradient(90deg, rgba(11,31,58,.92) 0%, rgba(11,31,58,.72) 42%, rgba(11,31,58,.15) 100%), linear-gradient(180deg, rgba(11,31,58,0) 65%, #0B1F3A 100%); }")
open("src/components/Hero.astro", "w", encoding="utf-8").write(s)

# ---- parceiros alinhados: colunas que se ajustam ao número de parceiros
sub("src/components/Bando.astro", "    .parts { display: grid; grid-template-columns: repeat(6, 1fr); }", "    .parts { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); }")
print("revisao ok")
