"""Parte 2 da revisão clara: o que ficou depois do assert que falhou em Percurso. Roda da raiz do site."""
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

def sub(p, old, new, count=1):
    s = open(p, encoding="utf-8").read()
    assert s.count(old) == count, (p, old[:60], s.count(old))
    open(p, "w", encoding="utf-8").write(s.replace(old, new))

P = "src/components/Percurso.astro"
sub(P, "  .seg.on { background: var(--color-aqua); border-color: var(--accent); color: var(--color-navy); }\n", "")
sub(P, 'fill="#AFC0D6"', 'fill="#3A4A63"', 4)
sub(P, '<path d={el.area} fill="#2ABFCC" opacity=".16" />', '<path d={el.area} fill="#1B7A8C" opacity=".14" />')
sub(P, '<path d={el.line} fill="none" stroke="#2ABFCC" stroke-width="2.5"', '<path d={el.line} fill="none" stroke="#1B7A8C" stroke-width="2.5"')
sub(P, "border: 1px solid var(--line); background: var(--color-navy2); }", "border: 1px solid var(--line); background: var(--color-navy); }")
sub(P, "padding: 8px 16px; background: var(--color-navy); }", "padding: 8px 16px; background: var(--color-paper); color: var(--color-navy); border-color: var(--color-paper); }")
sub("src/components/Fecho.astro", "rgba(11,31,58,.7) 75%, #17213B 100%); }", "rgba(11,31,58,.75) 80%, #0B1F3A 100%); }")
sub("src/components/Waves.astro", "const bg = { navy: '#0B1F3A', navy2: '#17213B', paper: '#FDFBF7' };", "const bg = { navy: '#0B1F3A', navy2: '#17213B', paper: '#FDFBF7', sand: '#F0EDE8' };")
I = "src/pages/index.astro"
sub(I, "import Capitaes from '../components/Capitaes.astro';", "import Capitaes from '../components/Capitaes.astro';\nimport Treinao from '../components/Treinao.astro';")
sub(I, '    <Faixa />\n    <Waves from="navy" to="navy2" />\n    <Ideia />', '    <Faixa />\n    <Ideia />')
sub(I, '    <Capitaes />\n    <Percurso />\n    <Waves from="navy" to="navy2" />\n    <Kit />', '    <Capitaes />\n    <Treinao />\n    <Percurso />\n    <Waves from="paper" to="paper" />\n    <Kit />')
print("parte 2 ok")
