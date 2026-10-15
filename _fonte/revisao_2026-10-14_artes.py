"""Revisão 14/10/2026 (noite): fotos do clube saem, artes da campanha entram. Hero e fecho só com o pássaro.
Roda a partir da raiz do site: python _fonte/revisao_2026-10-14_artes.py
"""
import re, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

def sub(p, old, new, count=1):
    s = open(p, encoding="utf-8").read()
    assert s.count(old) == count, (p, old[:60], s.count(old))
    open(p, "w", encoding="utf-8").write(s.replace(old, new))

# ---- prep_assets: artes no lugar das fotos
s = open("_fonte/prep_assets.py", encoding="utf-8").read()
start = s.index("# ---------- fotos ----------"); end = s.index("# hero no celular")
new_block = '''# ---------- artes da campanha ----------
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

'''
s = s[:start] + new_block + s[end:]
a = s.index("# hero no celular"); b = s.index("# Leaflet:")
s = s[:a] + s[b:]
s = s.replace("- Fotos selecionadas -> public/img/fotos/*.webp (1600 e 800 de largura)", "- Artes da campanha -> public/img/artes/*.webp (1080, 800 e 480 de largura)")
open("_fonte/prep_assets.py", "w", encoding="utf-8").write(s)

# ---- Hero: sem foto, pássaro em traço branco
sub("src/components/Hero.astro", "import fotos from '../data/fotos.json';\n", "")
sub("src/components/Hero.astro", "const f = fotos.hero;\n", "")
s = open("src/components/Hero.astro", encoding="utf-8").read()
s = re.sub(r"  <picture>.*?</picture>\n  <div class=\"veil\" aria-hidden=\"true\"></div>", '  <img class="bird" src="/img/passaro-branco-640.png" width="576" height="879" alt="" fetchpriority="high" decoding="async" />', s, flags=re.S)
s = re.sub(r"  \.hero picture \{ display: contents; \}\n  \.bg \{[^\n]*\n  \.veil \{[^\n]*\n[^\n]*\n", "  .bird { position: absolute; right: -6%; top: 8%; height: 46%; width: auto; opacity: .85; z-index: -1; }\n", s)
s = re.sub(r"  @media \(min-width: 820px\) \{ \.content \{ padding-block: 140px 88px; \} \.veil \{[^\n]*\n", "  @media (min-width: 820px) { .content { padding-block: 140px 88px; } .bird { right: 6%; top: 12%; height: 76%; opacity: .95; } }\n", s)
assert ".bird {" in s and ".veil" not in s and "<picture>" not in s, "hero"
open("src/components/Hero.astro", "w", encoding="utf-8").write(s)

# ---- Ideia, Kit, Programação: artes
def swap_img(p, old_var, new_var, old_src_re, new_src):
    s = open(p, encoding="utf-8").read()
    assert old_var in s, (p, old_var)
    s = s.replace(old_var, new_var)
    s, n = re.subn(old_src_re, new_src, s)
    assert n == 1, (p, old_src_re, n)
    s = s.replace("  .ph { margin: 0; border-radius: 16px; overflow: hidden; aspect-ratio: 4 / 5; }", "  .ph { margin: 0; border-radius: 16px; overflow: hidden; aspect-ratio: 4 / 5; border: 1px solid var(--color-line); }")
    open(p, "w", encoding="utf-8").write(s)

def srcset(name):
    return f'src="/img/artes/{name}-800.webp" srcset="/img/artes/{name}-480.webp 480w, /img/artes/{name}-800.webp 800w, /img/artes/{name}-1080.webp 1080w"'

swap_img("src/components/Ideia.astro", "const a = fotos.igreja, b = fotos.noite;", "const a = fotos.arte_mesa, b = fotos.arte_ritual;",
         r'src="/img/fotos/igreja-480\.webp" srcset=\{`[^`]*`\}', srcset("arte_mesa"))
s = open("src/components/Ideia.astro", encoding="utf-8").read()
s, n = re.subn(r'src="/img/fotos/noite-480\.webp" srcset=\{`[^`]*`\}', srcset("arte_ritual"), s); assert n == 1
open("src/components/Ideia.astro", "w", encoding="utf-8").write(s)
swap_img("src/components/Kit.astro", "const f = fotos.dupla;", "const f = fotos.arte_kit;", r'src="/img/fotos/dupla-800\.webp" srcset=\{`[^`]*`\}', srcset("arte_kit"))
sub("src/components/Kit.astro", "object-fit: cover; object-position: 50% 30%;", "object-fit: cover;")
swap_img("src/components/Programacao.astro", "const f = fotos.amigos;", "const f = fotos.arte_brinde;", r'src="/img/fotos/amigos-800\.webp" srcset=\{`[^`]*`\}', srcset("arte_brinde"))

# ---- Fecho: sem foto, pássaro grande à direita no desktop
sub("src/components/Fecho.astro", "import fotos from '../data/fotos.json';\n", "")
sub("src/components/Fecho.astro", "const f = fotos.portico;\n", "")
s = open("src/components/Fecho.astro", encoding="utf-8").read()
s, n = re.subn(r'  <img class="bg"[^\n]*\n  <div class="veil" aria-hidden="true"></div>\n', "", s); assert n == 1
s, n = re.subn(r"  \.bg \{[^\n]*\n  \.veil \{[^\n]*\n", "  .fecho { background: radial-gradient(120% 90% at 85% 30%, #17213B 0%, #0B1F3A 60%); }\n", s); assert n == 1
s = s.replace("  .bird { width: 120px; height: auto; opacity: .9; }", "  .bird { width: 120px; height: auto; opacity: .9; }\n  @media (min-width: 820px) { .fecho .bird { position: absolute; right: 8%; top: 50%; transform: translateY(-50%); width: 260px; opacity: .55; } }")
open("src/components/Fecho.astro", "w", encoding="utf-8").write(s)

# ---- crédito
sub("src/data/event.json", '"photosCredit": "Fotos: atletas do The Hybrid Club, com autorização"', '"photosCredit": "Artes: campanha de lançamento da prova"')
print("revisao ok")
