"""Revisão 14/10 (noite, 6): sete ajustes do Raphael. Roda da raiz do site.
1 sem "900 vagas" · 2/7 esteira dos patrocinadores (bug: .marq:hover .spons virou .spons paused no build)
3 início cativante, "prova comum" vai para Realização no fim · 4 retorno no Bedrock / Lions Clube, marco Brutal
5 kit com brinde dos patrocinadores e voucher · 6 Wisekey patrocinadora"""
import os, re, json
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

def sub(p, old, new, count=1):
    s = open(p, encoding="utf-8").read()
    assert s.count(old) == count, (p, old[:70], s.count(old))
    open(p, "w", encoding="utf-8").write(s.replace(old, new))

e = json.load(open("src/data/event.json", encoding="utf-8"))
# 1 · nada de número interno
e["sponsorPitch"] = "Sua marca na porta da Confraria Bem Te Vi, na frente dos corredores e das famílias que ficam o domingo inteiro."
# 3 · início cativante (o pouso), o resto vai para Realização
e["ideia"] = {
    "eyebrow": "O pouso",
    "title": "Você cruza a linha. A mesa já está posta.",
    "lede": "Café, chopp, música e família na porta da Confraria Bem Te Vi. Quem corre fica. Quem veio junto também. E o domingo segue pela tarde, na festa que abre a temporada de dezembro."
}
# 4 · percurso: retorno no Bedrock (Lions Clube); marco Brutal
e["route"]["description"] = "Vai e volta no eixo Av. Dr. Durval Nicolau / Av. Dr. Octávio da Silva Bastos. Sai da Confraria Bem Te Vi, segue até o retorno no Bedrock, no Lions Clube, e volta. O 10 km tem uma extensão no sentido dos números maiores da avenida antes de fechar na chegada."
for p in e["route"]["points"]:
    if p["id"] == "anglo":
        p["id"] = "bedrock"; p["label"] = "Retorno"; p["detail"] = "Bedrock, no Lions Clube"
        p["coordsTodo"] = "Coordenada ainda é a do KML de 22/09 (rotatória do Anglo). Confirmar o ponto do Bedrock / Lions Clube e atualizar lat/lon"
    if p["id"] == "btv": p["detail"] = "Confraria Bem Te Vi, nº 1705"
for m in e["route"]["landmarks"]:
    if m["name"].startswith("Retorno Anglo"): m["name"] = "Brutal"
e["route"]["landmarks"].append({"name": "Retorno: Bedrock / Lions Clube", "km": e["route"]["landmarks"][-1]["km"]})
e["route"]["landmarksNote"] = "km na ida, da Confraria Bem Te Vi ao retorno. Base de 1,7 km confirmada em 14/10; em 14/10 à noite o Raphael corrigiu: o retorno é no Bedrock (Lions Clube), não no Anglo, e o marco do fim é a Brutal. Conferir os km com o traçado novo."
# 5 · kit
e["kit"].insert(6, {"id": "brinde", "label": "Brinde dos patrocinadores"})
e["kit"].insert(7, {"id": "voucher", "label": "Voucher dos parceiros", "detailTodo": "Confirmar com o Raphael de que voucher se trata"})
# 6 · Wisekey
e["sponsors"].append({"name": "Wisekey", "logo": "/sponsors/wisekey.png", "logoWhite": "/sponsors/wisekey-branco.png", "logoNavy": "/sponsors/wisekey-navy.png", "logoNote": "PNG de 01_WISEKEY/01_Wise_Core/05_Marca_e_Identidade/04_Tipografia"})
json.dump(e, open("src/data/event.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# 1 · hero e fecho sem vagas; JSON-LD sem capacidade
sub("src/components/Hero.astro", '    <p class="vagas label">{event.capacity} vagas · Corrida 10 km e 5 km · Caminhada 3 km</p>', '    <p class="vagas label">Corrida 10 km e 5 km · Caminhada 3 km · Chip, medalha e ficha de pouso</p>')
sub("src/components/Fecho.astro", '    <p class="lede">Chip, medalha e uma mesa esperando. {event.capacity} vagas.</p>', '    <p class="lede">Chip, medalha e uma mesa esperando.</p>')
sub("src/layouts/Base.astro", "  sport: 'Corrida de rua', maximumAttendeeCapacity: event.capacity,\n", "  sport: 'Corrida de rua',\n")

# 2/7 · esteira: regra de hover separada por filho direto (o compilador quebrou a lista de seletores)
sub("src/components/Bando.astro", "  .marq:hover .spons, .marq:hover .parts { animation-play-state: paused; }", "  .marq:hover > ul { animation-play-state: paused; }")

# 3 · Ideia: início cativante, sem o bloco de "prova comum"
I = "src/components/Ideia.astro"
s = open(I, encoding="utf-8").read()
s = s.replace('''      <p class="eyebrow">A ideia</p>
      <h2>Prova comum dispersa em 40 minutos. Aqui o público fica horas no mesmo lugar.</h2>
      <p class="lede">{event.support}</p>''', '''      <p class="eyebrow">{event.ideia.eyebrow}</p>
      <h2>{event.ideia.title}</h2>
      <p class="lede">{event.ideia.lede}</p>''')
s = re.sub(r'      <div class="sig reveal">.*?      </div>\n', '''      <div class="sig reveal">
        <p class="label">Largada e chegada no mesmo lugar</p>
        <p class="sig-t">A arena é a porta do bar. O pódio é a mesa.</p>
      </div>
''', s, flags=re.S)
assert "event.ideia" in s and "A arena é a porta" in s
open(I, "w", encoding="utf-8").write(s)
sub("src/pages/index.astro", "import Fecho from '../components/Fecho.astro';", "import Fecho from '../components/Fecho.astro';\nimport Realizacao from '../components/Realizacao.astro';")
sub("src/pages/index.astro", "    <Fecho />\n", "    <Fecho />\n    <Realizacao />\n")

# 4 · Percurso: texto do retorno
sub("src/components/Percurso.astro", '      <div><p class="label">Retorno</p><p>Em frente ao Colégio Anglo, na rotatória com a Av. Dr. Oscar Pirajá Martins.</p></div>', '      <div><p class="label">Retorno</p><p>No Bedrock, no Lions Clube. Vai e volta pela avenida.</p></div>')
sub("src/components/Percurso.astro", '      <div><p class="label">Largada e chegada</p><p>Mesmo lugar, na porta do Bem Te Vi.</p></div>', '      <div><p class="label">Largada e chegada</p><p>Mesmo lugar, na porta da Confraria Bem Te Vi.</p></div>')
print("revisao ok")
