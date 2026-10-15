"""Revisão 14/10 (noite, 3): site claro com azul de detalhe; navy só no hero e no fecho.
Tira Black Run Club e #SOMOS1PCT; seção do treinão de sábado; foto da mesa sai.
Roda da raiz do site."""
import json, os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

def sub(p, old, new, count=1):
    s = open(p, encoding="utf-8").read()
    assert s.count(old) == count, (p, old[:60], s.count(old))
    open(p, "w", encoding="utf-8").write(s.replace(old, new))

def edit(p, fn):
    s = open(p, encoding="utf-8").read(); n = fn(s); assert n != s, p; open(p, "w", encoding="utf-8").write(n)

# ---------- event.json
e = json.load(open("src/data/event.json", encoding="utf-8"))
e["partners"] = [p for p in e["partners"] if p["name"] != "Black Run Club"]
e["hashtag"] = ""
e["training"] = {
    "eyebrow": "Treinão de sábado",
    "title": "Todo sábado tem treino. E tem chegada.",
    "lede": "Treino de corrida saindo do Bem Te Vi e terminando no Bem Te Vi. Aberto, de graça, para qualquer ritmo. Não precisa estar inscrito na prova para ir.",
    "firstLabel": "Primeiro encontro",
    "firstDate": "17.10",
    "time": "08h30",
    "where": "Na porta do Bem Te Vi, Av. Dr. Durval Nicolau, 1705. Depois, todo sábado até 29/11.",
    "facts": [
        {"title": "3 km, ritmo de bando", "detail": "Quem quer puxar, puxa. Quem quer trotar, trota. Ninguém fica para trás."},
        {"title": "Vai subindo", "detail": "3, 3, 5, 5, 7, 7 km. Os 10 km só no dia 29."},
        {"title": "O treino acaba na mesa", "detail": "O bar abre às 10h e o chopp sai a R$ 9,90 até meio-dia para quem treinou."},
        {"title": "Chama a turma", "detail": "Da corrida, da academia, do trabalho. Quem nunca correu também vem."}
    ],
    "note": "Cerveja merecida, como todo atleta híbrido. Chopp só para maiores de 18."
}
# logos em navy para fundo claro
for s in e["sponsors"] + e["partners"]:
    if s.get("logoWhite") and s["logoWhite"] != "TODO":
        s["logoNavy"] = s["logoWhite"].replace("-branco", "-navy")
json.dump(e, open("src/data/event.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# ---------- global.css: variáveis de tema
sub("src/styles/global.css", "Cor: branco quebrado #FDFBF7 sobre navy #0B1F3A · navy BTV #17213B como segundo fundo · papel #FDFBF7 em dois blocos claros",
    "Cor: navy #0B1F3A sobre branco quebrado #FDFBF7 · areia #F0EDE8 como segundo fundo claro · navy só no hero e no fecho (classe .dark)")
sub("src/styles/global.css", "@layer base {\n", """@layer base {
  :root { --bg: var(--color-paper); --fg: var(--color-navy); --fg2: var(--color-ink2); --line: var(--color-line-ink); --accent: var(--color-teal); }
  .dark { --bg: var(--color-navy); --fg: var(--color-paper); --fg2: var(--color-mute); --line: var(--color-line); --accent: var(--color-aqua); background: var(--bg); color: var(--fg); }
""")
sub("src/styles/global.css", "  body { background: var(--color-navy); color: var(--color-paper);", "  body { background: var(--bg); color: var(--fg);")
sub("src/styles/global.css", "  :focus-visible { outline: 3px solid var(--color-aqua); outline-offset: 3px; }", "  :focus-visible { outline: 3px solid var(--accent); outline-offset: 3px; }")
sub("src/styles/global.css", "  .lede { font-size: clamp(18px, 1.6vw, 22px); color: var(--color-mute); max-width: 680px; }\n  .paper .lede { color: var(--color-ink2); }", "  .lede { font-size: clamp(18px, 1.6vw, 22px); color: var(--fg2); max-width: 680px; }")
sub("src/styles/global.css", "  .eyebrow { font-family: var(--font-mono); font-size: 13px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: var(--color-aqua); }\n  .paper .eyebrow { color: var(--color-teal); }", "  .eyebrow { font-family: var(--font-mono); font-size: 13px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: var(--accent); }")
sub("src/styles/global.css", "  .label { font-family: var(--font-mono); font-size: 13px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--color-mute); }\n  .paper .label { color: var(--color-ink2); }\n  .paper { background: var(--color-paper); color: var(--color-navy); }\n  .navy2 { background: var(--color-navy2); }",
    "  .label { font-family: var(--font-mono); font-size: 13px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--fg2); }\n  .sand { background: var(--color-sand); }")
sub("src/styles/global.css", "  .btn-ghost { border: 2px solid var(--color-line); color: var(--color-paper); }\n  .btn-ghost:hover { border-color: var(--color-aqua); }\n  .paper .btn-ghost { border-color: var(--color-line-ink); color: var(--color-navy); }\n  .paper .btn-ghost:hover { border-color: var(--color-navy); }",
    "  .btn-ghost { border: 2px solid var(--line); color: var(--fg); }\n  .btn-ghost:hover { border-color: var(--accent); }")
sub("src/styles/global.css", "text-transform: uppercase; padding: 8px 14px; border-radius: 999px; border: 1px solid var(--color-aqua); color: var(--color-aqua); }", "text-transform: uppercase; padding: 8px 14px; border-radius: 999px; border: 1px solid var(--accent); color: var(--accent); }")
sub("src/styles/global.css", "  .card { border: 1px solid var(--color-line); border-radius: 20px; padding: 28px; }\n  .paper .card { border-color: var(--color-line-ink); }", "  .card { border: 1px solid var(--line); border-radius: 20px; padding: 28px; background: var(--color-paper); }")

# ---------- componentes: tokens -> variáveis de tema
def themify(s):
    s = s.replace("color: var(--color-mute)", "color: var(--fg2)").replace("var(--color-line)", "var(--line)").replace("color: var(--color-paper)", "color: var(--fg)")
    s = s.replace("color: var(--color-ink2)", "color: var(--fg2)").replace("var(--color-line-ink)", "var(--line)")
    return s
for f in ["Ideia", "Modalidades", "Capitaes", "Percurso", "Kit", "Programacao", "Retirada", "Bando", "Faq", "Fecho", "Footer", "Header", "StickyCta", "Faixa"]:
    p = f"src/components/{f}.astro"; s = open(p, encoding="utf-8").read(); open(p, "w", encoding="utf-8").write(themify(s))

# seções: claro por padrão, areia alternando
sub("src/components/Ideia.astro", '<section id="ideia" class="sec navy2">', '<section id="ideia" class="sec">')
sub("src/components/Modalidades.astro", '<section id="precos" class="sec paper">', '<section id="precos" class="sec sand">')
sub("src/components/Capitaes.astro", '<section id="capitaes" class="sec navy2">', '<section id="capitaes" class="sec">')
sub("src/components/Kit.astro", '<section id="kit" class="sec navy2">', '<section id="kit" class="sec">')
sub("src/components/Retirada.astro", '<section id="retirada" class="sec paper">', '<section id="retirada" class="sec sand">')
sub("src/components/Bando.astro", '<section id="bando" class="sec navy2">', '<section id="bando" class="sec">')
sub("src/components/Faq.astro", '<section id="faq" class="sec">', '<section id="faq" class="sec sand">')
sub("src/components/Fecho.astro", '<section id="fecho" class="fecho">', '<section id="fecho" class="fecho dark">')
sub("src/components/Fecho.astro", '<section id="patrocinio" class="sec navy2">', '<section id="patrocinio" class="sec">')
sub("src/components/Hero.astro", '<section id="inicio" class="hero">', '<section id="inicio" class="hero dark">')

# Ideia: foto da mesa sai (arte da campanha no lugar), hashtag sai
edit("src/components/Ideia.astro", lambda s: s.replace("import fotos from '../data/fotos2.json';", "import fotos from '../data/fotos2.json';\nimport artes from '../data/fotos.json';").replace("const a = fotos.mesa, b = fotos.placa;", "const a = artes.arte_mesa, b = fotos.placa;"))
edit("src/components/Ideia.astro", lambda s: re.sub(r'src="/img/fotos/mesa-480\.webp" srcset="[^"]*"', 'src="/img/artes/arte_mesa-800.webp" srcset="/img/artes/arte_mesa-480.webp 480w, /img/artes/arte_mesa-800.webp 800w, /img/artes/arte_mesa-1080.webp 1080w"', s))
sub("src/components/Ideia.astro", '        <p class="mono tag">{event.hashtag}</p>\n', '')
sub("src/components/Ideia.astro", "  .tag { color: var(--color-aqua); font-weight: 600; letter-spacing: 0.1em; }\n", "")
sub("src/components/Ideia.astro", "  .dot { width: 16px; height: 16px; border-radius: 50%; background: var(--color-navy2); border: 3px solid var(--color-aqua); }", "  .dot { width: 16px; height: 16px; border-radius: 50%; background: var(--color-paper); border: 3px solid var(--accent); }")
sub("src/components/Ideia.astro", "  .tl::after { content: \"\"; position: absolute; left: 0; top: 7px; height: 2px; width: 100%; background: var(--color-aqua);", "  .tl::after { content: \"\"; position: absolute; left: 0; top: 7px; height: 2px; width: 100%; background: var(--accent);")
sub("src/components/Ideia.astro", "  .t { font-weight: 600; color: var(--color-aqua); font-size: 15px; letter-spacing: 0.06em; }", "  .t { font-weight: 600; color: var(--accent); font-size: 15px; letter-spacing: 0.06em; }")
sub("src/components/Ideia.astro", "  .ph { margin: 0; border-radius: 16px; overflow: hidden; aspect-ratio: 4 / 5; }", "  .ph { margin: 0; border-radius: 16px; overflow: hidden; aspect-ratio: 4 / 5; border: 1px solid var(--line); }")
sub("src/components/Footer.astro", '    <p class="small">{event.photosCredit}. <span class="mono">{event.hashtag}</span></p>', '    <p class="small">{event.photosCredit}.</p>')

# Header, sticky, footer, faixa claros
sub("src/components/Header.astro", "  .top { position: sticky; top: 0; z-index: 40; background: rgba(11, 31, 58, 0.88); backdrop-filter: blur(10px); border-bottom: 1px solid var(--line); }", "  .top { position: sticky; top: 0; z-index: 40; background: rgba(253, 251, 247, 0.9); backdrop-filter: blur(10px); border-bottom: 1px solid var(--line); }")
sub("src/components/Header.astro", "  .menu a:hover { color: var(--fg); }", "  .menu a:hover { color: var(--accent); }")
sub("src/components/StickyCta.astro", "background: rgba(11,31,58,.92); backdrop-filter: blur(10px);", "background: rgba(253,251,247,.94); backdrop-filter: blur(10px);")
sub("src/components/Footer.astro", "  .foot { background: var(--color-navy); border-top: 1px solid var(--line); padding-block: 56px 96px; }", "  .foot { background: var(--color-sand); border-top: 1px solid var(--line); padding-block: 56px 96px; }")
sub("src/components/Footer.astro", "  a:hover { color: var(--color-aqua); }", "  a:hover { color: var(--accent); }")
sub("src/components/Faixa.astro", "  .faixa { background: var(--color-navy); border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); }", "  .faixa { background: var(--color-paper); border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); }")
sub("src/components/Faixa.astro", "  .more { margin-left: auto; text-decoration: none; color: var(--color-aqua); }", "  .more { margin-left: auto; text-decoration: none; color: var(--accent); }")
sub("src/components/Faixa.astro", "const logo = (x) => (x.logoWhite && x.logoWhite !== 'TODO' ? x.logoWhite : null);", "const logo = (x) => (x.logoNavy ? x.logoNavy : null);")
sub("src/components/Bando.astro", "const logo = (x) => (x.logoWhite && x.logoWhite !== 'TODO' ? x.logoWhite : null);", "const logo = (x) => (x.logoNavy ? x.logoNavy : null);")

# Modalidades: toggle e preços em tema claro
sub("src/components/Modalidades.astro", "  .toggle input:checked + .sw { background: var(--color-teal); }", "  .toggle input:checked + .sw { background: var(--accent); }")
sub("src/components/Modalidades.astro", "  .toggle input:focus-visible + .sw { outline: 3px solid var(--color-teal); outline-offset: 3px; }", "  .toggle input:focus-visible + .sw { outline: 3px solid var(--accent); outline-offset: 3px; }")
sub("src/components/Modalidades.astro", "  .sw { width: 48px; height: 28px; border-radius: 999px; background: var(--line);", "  .sw { width: 48px; height: 28px; border-radius: 999px; background: rgba(11,31,58,.18);")

# Capitães, Kit, Programação, FAQ, Retirada: acentos
for f in ["Capitaes", "Kit", "Programacao", "Faq", "Percurso", "Retirada"]:
    p = f"src/components/{f}.astro"; s = open(p, encoding="utf-8").read()
    s = s.replace("color: var(--color-aqua)", "color: var(--accent)").replace("background: var(--color-aqua); border-radius: 2px", "background: var(--accent); border-radius: 2px")
    open(p, "w", encoding="utf-8").write(s)
sub("src/components/Kit.astro", "  .it { display: grid; grid-template-columns: 40px 1fr; gap: 4px 12px; padding: 18px 20px; border: 1px solid var(--line); border-radius: 16px;", "  .it { display: grid; grid-template-columns: 40px 1fr; gap: 4px 12px; padding: 18px 20px; border: 1px solid var(--line); border-radius: 16px; background: var(--color-sand);")
sub("src/components/Programacao.astro", "  .row.now { background: linear-gradient(90deg, rgba(42,191,204,.12), transparent);", "  .row.now { background: linear-gradient(90deg, rgba(27,122,140,.12), transparent);")
sub("src/components/Retirada.astro", "  .hours { font-size: 20px; font-weight: 600; color: var(--color-teal); }", "  .hours { font-size: 20px; font-weight: 600; color: var(--accent); }")

# Percurso: mapa continua escuro (detalhe em azul), perfil e textos no tema
sub("src/components/Percurso.astro", "  .seg { font: inherit; font-weight: 600; font-size: 15px; padding: 10px 18px; min-height: 44px; border-radius: 999px; border: 2px solid var(--line); background: none; color: var(--fg); cursor: pointer; }", "  .seg { font: inherit; font-weight: 600; font-size: 15px; padding: 10px 18px; min-height: 44px; border-radius: 999px; border: 2px solid var(--line); background: none; color: var(--fg); cursor: pointer; }\n  .seg.on { background: var(--color-navy); border-color: var(--color-navy); color: var(--color-paper); }")
edit("src/components/Percurso.astro", lambda s: s.replace("  .seg.on { background: var(--color-aqua); border-color: var(--color-aqua); color: var(--color-navy); }\n", ""))
edit("src/components/Percurso.astro", lambda s: s.replace('fill="#AFC0D6"', 'fill="#3A4A63"').replace('<path d={el.area} fill="#2ABFCC" opacity=".16" />', '<path d={el.area} fill="#1B7A8C" opacity=".14" />').replace('<path d={el.line} fill="none" stroke="#2ABFCC" stroke-width="2.5"', '<path d={el.line} fill="none" stroke="#1B7A8C" stroke-width="2.5"'))
sub("src/components/Percurso.astro", "  .map-wrap { position: relative; border-radius: 20px; overflow: hidden; border: 1px solid var(--line); background: var(--color-navy2); }", "  .map-wrap { position: relative; border-radius: 20px; overflow: hidden; border: 1px solid var(--line); background: var(--color-navy); }")
sub("src/components/Percurso.astro", "  .gmaps { position: absolute; left: 16px; bottom: 16px; min-height: 44px; font-size: 14px; padding: 8px 16px; background: var(--color-navy); }", "  .gmaps { position: absolute; left: 16px; bottom: 16px; min-height: 44px; font-size: 14px; padding: 8px 16px; background: var(--color-paper); color: var(--color-navy); border-color: var(--color-paper); }")
sub("src/components/Percurso.astro", "  .marks .k { color: var(--color-aqua); margin-right: 8px; }", "  .marks .k { color: var(--accent); margin-right: 8px; }")

# Fecho/patrocínio
sub("src/components/Fecho.astro", "  .veil { position: absolute; inset: 0; z-index: -1; background: linear-gradient(180deg, #0B1F3A 0%, rgba(11,31,58,.6) 40%, rgba(11,31,58,.7) 75%, #17213B 100%); }", "  .veil { position: absolute; inset: 0; z-index: -1; background: linear-gradient(180deg, #0B1F3A 0%, rgba(11,31,58,.6) 40%, rgba(11,31,58,.75) 80%, #0B1F3A 100%); }")

# Waves: cores de fundo por tema
sub("src/components/Waves.astro", "const bg = { navy: '#0B1F3A', navy2: '#17213B', paper: '#FDFBF7' };", "const bg = { navy: '#0B1F3A', navy2: '#17213B', paper: '#FDFBF7', sand: '#F0EDE8' };")

# index: ordem e temas
sub("src/pages/index.astro", "import Capitaes from '../components/Capitaes.astro';", "import Capitaes from '../components/Capitaes.astro';\nimport Treinao from '../components/Treinao.astro';")
sub("src/pages/index.astro", '    <Faixa />\n    <Waves from="navy" to="navy2" />\n    <Ideia />', '    <Faixa />\n    <Ideia />')
sub("src/pages/index.astro", '    <Capitaes />\n    <Percurso />\n    <Waves from="navy" to="navy2" />\n    <Kit />', '    <Capitaes />\n    <Treinao />\n    <Percurso />\n    <Waves from="paper" to="paper" />\n    <Kit />')
print("revisao ok")
