"""Revisão 14/10 (noite, 2): fotos do bar e da corrida (Corrida_assets), logo oficial da prova, seção Seja um capitão,
faixa de patrocinadores sob o hero, collab explícita. Roda da raiz do site.
"""
import json, os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

def sub(p, old, new, count=1):
    s = open(p, encoding="utf-8").read()
    assert s.count(old) == count, (p, old[:70], s.count(old))
    open(p, "w", encoding="utf-8").write(s.replace(old, new))

# ---- event.json: capitães, collab
e = json.load(open("src/data/event.json", encoding="utf-8"))
e["collab"] = "The Hybrid Club × Bem Te Vi"
e["captains"] = {
    "eyebrow": "Capitães do bando",
    "title": "Corre em grupo? Traz o grupo inteiro.",
    "lede": "Assessoria, academia, box, grupo de corrida ou empresa: quem traz a equipe vira capitão e corre com vantagem.",
    "perks": [
        {"title": "1 inscrição cortesia a cada 10 da equipe", "detail": "Conta no link do capitão, direto na Ticket Sports."},
        {"title": "Troféu de equipe com mais pousos", "detail": "Entregue na premiação, com o nome do grupo no palco."},
        {"title": "Post collab de apresentação da equipe", "detail": "Nos perfis da prova e do Bem Te Vi."},
        {"title": "Link ou cupom rastreável", "detail": "Para saber exatamente quem veio pelo seu grupo."}
    ],
    "cta": "Quero ser capitão",
    "who": "Vale para grupos de São João da Boa Vista e região",
    "whatsappText": "Olá! Quero ser capitão do bando na The Hybrid Run, 29/11. Meu grupo: "
}
e["photosCredit"] = "Fotos: Bem Te Vi e corredores de São João da Boa Vista, com autorização. Artes: campanha de lançamento da prova"
json.dump(e, open("src/data/event.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# ---- Hero: fachada do bar + logo oficial + collab
s = open("src/components/Hero.astro", encoding="utf-8").read()
s = s.replace("import { loteState", "import fotos from '../data/fotos2.json';\nimport { loteState")
s = s.replace("const units = [", "const f = fotos.fachada;\nconst units = [")
s = s.replace('  <img class="bird" src="/img/passaro-branco-640.png" width="576" height="879" alt="" fetchpriority="high" decoding="async" />',
 """  <picture>
    <source media="(max-width: 819px)" srcset="/img/fotos/fachada-m-640.webp" width="640" height="779" />
    <img class="bg" src="/img/fotos/fachada-800.webp" srcset={`/img/fotos/fachada-800.webp 800w, /img/fotos/fachada-1600.webp ${f.sizes['1600'].w}w`} sizes="100vw"
         width={f.sizes['1600'].w} height={f.sizes['1600'].h} alt="" fetchpriority="high" decoding="async" />
  </picture>
  <div class="veil" aria-hidden="true"></div>""")
s = s.replace('    <p class="eyebrow">{event.circuit} · {event.edition}</p>',
 """    <div class="collab">
      <img class="selo" src="/img/logo-corrida-160.png" width="80" height="80" alt="Selo da prova: bem-te-vi de óculos, São João da Boa Vista, 29.11.2026" fetchpriority="high" />
      <p class="eyebrow">{event.collab}<br />{event.circuit} · {event.edition}</p>
    </div>""")
s = re.sub(r"  \.bird \{[^\n]*\n", """  .hero picture { display: contents; }
  .bg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 50% 20%; z-index: -2; }
  .veil { position: absolute; inset: 0; z-index: -1; background: linear-gradient(180deg, rgba(11,31,58,.55) 0%, rgba(11,31,58,.35) 30%, rgba(11,31,58,.92) 62%, #0B1F3A 100%); }
  .collab { display: flex; align-items: center; gap: 14px; }
  .selo { width: 64px; height: 64px; border-radius: 50%; box-shadow: 0 0 0 2px rgba(253,251,247,.25); }
""", s)
s = s.replace("  @media (min-width: 820px) { .content { padding-block: 140px 88px; } .bird { right: 6%; top: 12%; height: 76%; opacity: .95; } }",
 "  @media (min-width: 820px) { .content { padding-block: 140px 88px; } .selo { width: 80px; height: 80px; } .bg { object-position: 70% 30%; } .veil { background: linear-gradient(90deg, rgba(11,31,58,.95) 0%, rgba(11,31,58,.8) 40%, rgba(11,31,58,.3) 100%), linear-gradient(180deg, rgba(11,31,58,0) 60%, #0B1F3A 100%); } }")
assert ".veil {" in s and ".selo" in s and "fachada" in s
open("src/components/Hero.astro", "w", encoding="utf-8").write(s)

# ---- faixa de patrocinadores sob o hero (componente novo)
open("src/components/Faixa.astro", "w", encoding="utf-8").write("""---
import event from '../data/event.json';
const logo = (x) => (x.logoWhite && x.logoWhite !== 'TODO' ? x.logoWhite : null);
---
<div class="faixa" aria-label="Patrocinadores">
  <div class="wrap row">
    <span class="label">Com</span>
    <ul>
      {event.sponsors.map((s) => <li>{logo(s) ? <img src={logo(s)} alt={s.name} height="28" loading="lazy" decoding="async" /> : <span>{s.name}</span>}</li>)}
    </ul>
    <a class="label more" href="#bando">Todos os parceiros</a>
  </div>
</div>
<style>
  .faixa { background: var(--color-navy); border-top: 1px solid var(--color-line); border-bottom: 1px solid var(--color-line); }
  .row { display: flex; align-items: center; gap: 20px; min-height: 64px; padding-block: 12px; flex-wrap: wrap; }
  ul { list-style: none; margin: 0; padding: 0; display: flex; align-items: center; gap: 12px 28px; flex-wrap: wrap; }
  li { font-weight: 800; font-size: 15px; letter-spacing: -0.01em; white-space: nowrap; }
  li img { height: 28px; width: auto; display: block; }
  .more { margin-left: auto; text-decoration: none; color: var(--color-aqua); }
  .more:hover { text-decoration: underline; }
</style>
""")
sub("src/pages/index.astro", "import Waves from '../components/Waves.astro';", "import Waves from '../components/Waves.astro';\nimport Faixa from '../components/Faixa.astro';\nimport Capitaes from '../components/Capitaes.astro';")
sub("src/pages/index.astro", "    <Hero />\n    <Waves from=\"navy\" to=\"navy2\" />", "    <Hero />\n    <Faixa />\n    <Waves from=\"navy\" to=\"navy2\" />")
sub("src/pages/index.astro", "    <Modalidades />\n    <Percurso />", "    <Modalidades />\n    <Capitaes />\n    <Percurso />")

# ---- Ideia: mesa + placa (fotos do bar), legenda
s = open("src/components/Ideia.astro", encoding="utf-8").read()
s = s.replace("import fotos from '../data/fotos.json';", "import fotos from '../data/fotos2.json';")
s = s.replace("const a = fotos.arte_mesa, b = fotos.arte_ritual;", "const a = fotos.mesa, b = fotos.placa;")
s = re.sub(r'src="/img/artes/arte_mesa-800\.webp" srcset="[^"]*"', 'src="/img/fotos/mesa-480.webp" srcset="/img/fotos/mesa-480.webp 480w, /img/fotos/mesa-800.webp 736w"', s)
s = re.sub(r'src="/img/artes/arte_ritual-800\.webp" srcset="[^"]*"', 'src="/img/fotos/placa-480.webp" srcset="/img/fotos/placa-480.webp 480w, /img/fotos/placa-800.webp 800w, /img/fotos/placa-1600.webp 1320w"', s)
assert "mesa-480" in s and "placa-480" in s
s = s.replace("  .ph { margin: 0; border-radius: 16px; overflow: hidden; aspect-ratio: 4 / 5; border: 1px solid var(--color-line); }", "  .ph { margin: 0; border-radius: 16px; overflow: hidden; aspect-ratio: 4 / 5; }")
open("src/components/Ideia.astro", "w", encoding="utf-8").write(s)

# ---- Fecho: corredor noturno ao fundo, pássaro fica
s = open("src/components/Fecho.astro", encoding="utf-8").read()
s = s.replace("import { registrationUrl", "import fotos from '../data/fotos2.json';\nimport { registrationUrl")
s = s.replace("const wa = whatsappUrl", "const f = fotos.noite;\nconst wa = whatsappUrl")
s = s.replace('<section id="fecho" class="fecho">\n', """<section id="fecho" class="fecho">
  <img class="bg" src="/img/fotos/noite-800.webp" srcset={`/img/fotos/noite-480.webp 480w, /img/fotos/noite-800.webp 800w, /img/fotos/noite-1600.webp ${f.sizes['1600'].w}w`} sizes="100vw" width={f.sizes['800'].w} height={f.sizes['800'].h} alt="" loading="lazy" decoding="async" />
  <div class="veil" aria-hidden="true"></div>
""")
s = s.replace("  .fecho { background: radial-gradient(120% 90% at 85% 30%, #17213B 0%, #0B1F3A 60%); }\n",
 "  .bg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 60% 40%; z-index: -2; }\n  .veil { position: absolute; inset: 0; z-index: -1; background: linear-gradient(180deg, #0B1F3A 0%, rgba(11,31,58,.6) 40%, rgba(11,31,58,.7) 75%, #17213B 100%); }\n")
assert ".bg {" in s
open("src/components/Fecho.astro", "w", encoding="utf-8").write(s)

# ---- Footer: logo oficial
sub("src/components/Footer.astro", '      <p class="label">Realização</p>', '      <img class="selo" src="/img/logo-corrida-160.png" width="72" height="72" alt="Selo da prova" loading="lazy" decoding="async" />\n      <p class="label">Realização</p>')
sub("src/components/Footer.astro", "  .big { font-weight: 800;", "  .selo { border-radius: 50%; margin-bottom: 16px; }\n  .big { font-weight: 800;")
sub("src/components/Footer.astro", "<p class=\"big\">The Hybrid Club<br />Casa Bem Te Vi</p>", "<p class=\"big\">{event.collab}</p>")
print("revisao ok")
