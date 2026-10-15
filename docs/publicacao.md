# Publicação · site The Hybrid Run

Construído em 14/10/2026 a partir do brief `SITE · The Hybrid Run_Bem te vi`. Fonte de verdade dos dados: `src/data/event.json`. Nenhuma página tem número escrito à mão.

## O que está na pasta

```
2026-10-14_site_thehybridrun/
  src/data/event.json        todos os dados (lotes, preços, horários, patrocinadores, FAQ, contatos)
  src/data/fotos.json        manifesto das fotos (gerado por _fonte/prep_assets.py)
  src/lib/lotes.js           lógica de data: lote vigente, selo, countdown, camiseta, programação
  src/lib/route.js           leitura de GPX no build: mapa estático e perfil de elevação
  src/components/*.astro     uma seção por arquivo, na ordem do brief
  src/scripts/dinamico.js    countdown, lote, toggle 60+/PCD, CTA fixo, analytics (ilha única)
  src/scripts/mapa.js        Leaflet + OSM escurecido por filtro CSS (os tiles dark da CARTO exigem chave desde 14/10), só no desktop e só quando a seção aparece
  public/fonts/              Poppins 400/600/800 subsetadas (10 KB cada) e JetBrains Mono variável (31 KB)
  public/img/artes/          4 artes da campanha em WebP (480, 800 e 1080) + pássaro em traço branco
  public/route/              5k.gpx (DTS 29/09), 10k.gpx (eixo do KML 22/09), 10k_ref_strava_2026-07-11.gpx (com elevação)
  public/sponsors/           Batata Pura, Cimentolândia, Fotop e The Hybrid Club em SVG (original e branco); Fisio Cefe em PNG
  public/og-image.png        1200x630, navy, nome, hook e data
  _fonte/                    prep_assets.py (fotos, logos, rotas), test_lotes.mjs (viradas de lote), strava json
  docs/                      este arquivo, relatórios do Lighthouse
  dist/                      o site pronto (npm run build)
```

## Comandos

```bash
npm install
npm run build          # gera dist/
npm run check:lotes    # imprime o estado do site em 22 datas simuladas
python _fonte/prep_assets.py   # refaz fotos, logos e rotas a partir do projeto
```

Simular data no navegador: `?now=2026-11-29T07:00` (horário de São Paulo). Forçar lote: `loteOverride` no JSON.

## Lighthouse (14/10/2026, dist servido local, sem gzip)

| | Performance | Acessibilidade | Boas práticas | SEO |
|---|---|---|---|---|
| Celular | 87 a 90 | 100 | 100 | 100 |
| Desktop | 98 a 99 | 100 | 100 | 100 |

Duas rodadas limpas em sequência deram 90/99 e 87/98. Notas de celular oscilam 50 a 92 na mesma build quando o OneDrive está sincronizando a pasta. Medir com a pasta em repouso. Na Vercel ou Netlify, com brotli, o HTML de 87 KB cai para uns 18 KB e a nota sobe.

## Antes de publicar

- [ ] Domínio: definir e colocar em `event.json` (`siteUrl`) e `astro.config.mjs` (`site`). Trocar `DOMINIO` em `public/robots.txt` e `public/sitemap.xml`
- [ ] Conferir preço do lote vigente com a Ticket Sports no dia do deploy
- [ ] GA4 e Meta Pixel: IDs em `event.json` → `analytics`. Sem ID, nada é injetado
- [ ] Logos: Batata Pura e Cimentolândia em SVG (de `03_Comercial/Patrocinadores/*/03_Logo`, vetorizados 13/10), Fotop em SVG oficial do fotop.com, Fisio Cefe em PNG. **Gonçalves Imóveis e Boa Vista Seguros**: só o símbolo, traçado em 14/10 a partir do card 6 do post do treinão (83 e 46 px de origem, ampliados 8x e vetorizados com vtracer); o nome vai em texto ao lado. Para impressão grande, pedir o vetor original. Faltam Bem Te Vi (wordmark da LBE), Ticket Sports e Black Run Club
- [ ] Cimentolândia: o `00_CONTROLE_PATROCINIOS.md` (13/10) marca A CONFIRMAR; o brief de 14/10 lista como confirmado. Está no site. Tirar se não fechar
- [ ] Aprovação dos logos pelos patrocinadores
- [ ] Regulamento v1.1: `regulationUrl` no JSON. A v1.0 não entra (lotes antigos, 700 vagas, largada 7h00)
- [ ] Estacionamento: última pergunta do FAQ está `[PREENCHER: estacionamento e acesso, definir com o Bem Te Vi]`
- [ ] Foto do bar: não existe nenhuma na pasta. Se quiser uma foto real do Bem Te Vi no fecho, mandar e tratar em duotone navy para não quebrar a paleta
- [ ] GPX oficial: quando o DTS homologar, substituir `public/route/10k.gpx` e `5k.gpx` e tirar o selo "Percurso em homologação" (`route.status` no JSON)
- [ ] Link curto do Google Maps do Bem Te Vi em `venue.mapsUrl` (hoje é uma busca pelo endereço)

## Como hospedar

Vercel ou Netlify, projeto Astro detectado automaticamente (`npm run build`, saída `dist/`). Ou qualquer hospedagem estática: subir o conteúdo de `dist/`. Domínio próprio depois, no painel.

## Decisões: pedido original · o que foi feito · por quê

| Pedido | Feito | Por quê |
|---|---|---|
| Nome "The Hybrid Run_Bem te vi" | "Bem Te Vi Hybrid Run" em tudo: cabeçalho, hero (Bem Te Vi em teal sobre Hybrid Run), title, OG, JSON-LD, rodapé, WhatsApp. `name` e `siteName` no event.json | Última decisão do Raphael em 14/10 à noite: "tem que ser padronizado, o correto é bem te vi hybrid run". Antes disso passou por "The Hybrid Run" e "The Hybrid Run Bem Te Vi". Grafia sem hífen, como ele escreveu; o CLAUDE.md de 26/08 pedia "Bem-Te-Vi" com hífen |
| Skill construir-site: um `index.html`, zero JS | Astro + Tailwind com três ilhas de JS, como no brief | O brief pede countdown, lote pela data, toggle e mapa. Decisão do Raphael em 14/10. O resto da skill vale: fontes locais, head completo, Lighthouse, texto novo no JSON |
| "Festa" era palavra banida no `CLAUDE.md` do projeto | "Festa de confraternização" na programação e na copy | Liberada pelo Raphael em 14/10. `CLAUDE.md` atualizado |
| Fotos só quando mandar | Fotos reais de `02_Campanha/Corrida_assets` (07/10): fachada do Bem Te Vi no hero, mesa e placa em A ideia, grupo de corredores em Capitães, corredor noturno no fecho. Logo oficial da prova (bem-te-vi de óculos) no hero e no rodapé. Artes da campanha seguem no Kit e na Programação | Pedido do Raphael em 14/10 à noite: "usar fotos do bar também, a corrida é em collab". Nenhuma foto de patrocinador ou logo além de Batata Pura e Fisio Cefe existe no computador nem no e-mail (busca em 14/10) |
| Marcos do percurso com km pela numeração (Anglo em 3,77) | Marcos com km na ida, na lista, no SVG do celular e como pontos clicáveis no Leaflet | O KML de 22/09 e o GPX do DTS medem 1,7 km do Bem Te Vi ao Anglo (bate com a numeração 1705 → 90). Raphael confirmou 1,7 em 14/10; os outros km do brief foram escalados na mesma proporção (`kmBrief` → `km` no JSON) e posicionados sobre o eixo |
| GPX que o Raphael vai exportar do Strava | 10 km: eixo do KML de 22/09 (8,4 km, BTV → Anglo → BTV → leste → BTV). 5 km: GPX do DTS de 29/09. Perfil de elevação: Strava 11/07 (#19269541648) puxado pela API | Os três já estavam em `05_Operacao/`. Nada de traçado inventado. Selo "em homologação" fica até o DTS dar o aval |
| Perfil mostra "151 m de ganho" | Legenda usa o número do Strava | O cálculo bruto do stream dá 176 m (sem a suavização do Strava). Vale o número público do reconhecimento |
| Logos em SVG, versão branca | Batata Pura (do PDF) e Fisio Cefe (do PNG) em PNG, com versão branca pela máscara; os outros em texto | Não há SVG na pasta. `logoTodo` no JSON marca o que falta |
| Lighthouse 90+ em tudo no celular | 90 / 100 / 100 / 100 | Hero com recorte vertical de 43 KB, CSS do Leaflet fora da página, `content-visibility` nas seções, 3 pesos de Poppins. O que sobra é layout do HTML com os dois SVGs do percurso |
| Seção "Seja um capitão" (pedido de 14/10) | Seção Capitães do bando entre Preços e Percurso: 4 contrapartidas do programa (cortesia 1 a cada 10, troféu de equipe, post collab, link rastreável) e botão de WhatsApp | Copiado de `00_AGORA/2026-08-26_mkt_estrategia_ajustada_D-95.md`. A "mesa reservada no pouso" da peça P43 ficou fora porque está marcada como condição a fechar com o Rene. Custo do kit e CPA não aparecem |
| Patrocinadores "se mexendo" | Patrocinadores e parceiros em esteira contínua da esquerda para a direita, pausa no hover, lista duplicada para o loop; com `prefers-reduced-motion` vira rolagem manual | Pedido de 14/10 à noite |
| Patrocinadores com peso | Faixa "Com: Gonçalves Imóveis · Boa Vista Seguros · Batata Pura · Cimentolândia" logo abaixo do hero, mais a seção completa | Pedido de 14/10. Sem logo, o nome vai em Poppins 800 |
| Paleta navy no site inteiro (brief) | Site 100% claro (#FDFBF7 e areia #F0EDE8), navy só como texto e detalhe; nenhum fundo azul. Hero com a foto emoldurada ao lado do texto, fecho em areia com o pássaro navy, mapa com tiles claros, OG image clara. Logos em versão navy na faixa e na seção | Pedidos do Raphael em 14/10 à noite: "deixa o site mais pra branco com detalhes em azul" e depois "100% claro, nada de azul no fundo". Tema por variáveis CSS (`--bg`, `--fg`, `--fg2`, `--line`, `--accent`) com a classe `.dark` nos dois blocos escuros |
| Black Run Club como parceiro | Fora | Pedido de 14/10 |
| #SOMOS1PCT na assinatura | Fora; a frase "Para atletas que se constroem no processo" ficou | Pedido de 14/10 |
| Treinão de sábado | Seção própria depois de Capitães: 1º encontro 17/10 08h30 na porta do Bem Te Vi, 3 km ritmo de bando, progressão 3/3/5/5/7/7, bar às 10h e chopp a R$ 9,90 até meio-dia | Pedido de 14/10; dados do post do treinão (@thehybridclube, 14/10). `training` no event.json |
| Foto da mesa em A ideia | Trocada pela arte "A única corrida onde a linha de chegada é a mesa"; placa do bar fica | "Tem uma mesa nada a ver" (14/10) |
| Ondas do THC como divisor; ondas no cabeçalho e no favicon | Fora. Selo da corrida (bem-te-vi de óculos) no cabeçalho, no favicon, no apple-touch-icon e na OG image | Pedido de 14/10: "substitui tudo do logo do clube pro da corrida e até os verdes". O logo do THC segue só no card de parceiro, como realização |
| Foto do hero: fachada ao entardecer | Placa do Bem Te Vi de dia, céu azul (Corrida_assets 11.02.59, recorte dos 60% de cima para tirar a linha e a caixa do Strava) | "Vê se tem uma mais clara" (14/10) |
| "Casa Bem Te Vi" | "Confraria Bem Te Vi" na realização, na collab e no card de parceiro; assinatura "Feita para atletas híbridos: quem treina tendo trabalho e vida, e se constrói no processo, não na chegada" | Pedido de 14/10 à noite |
| "900 vagas" no hero, fecho, pitch e JSON-LD | Fora de tudo. `capacity` segue no JSON sem aparecer | "Nenhum dado interno" (14/10 à noite) |
| Esteira dos patrocinadores parada | O compilador do Astro transformava `.marq:hover .spons, .marq:hover .parts` em `.spons { paused }`: a primeira fileira nascia pausada. Regra virou `.marq:hover > ul` | Diagnóstico com dois quadros do Chrome headless em tempos diferentes |
| Início da página com "Prova comum dispersa em 40 minutos" | Primeiro bloco virou "Você cruza a linha. A mesa já está posta." (`ideia` no JSON). O texto de prova comum, a assinatura dos atletas híbridos e a realização foram para a seção Realização, no fim, antes de Seja patrocinador | "O começo do site precisa cativar; isso vai pro final em realização" |
| Retorno no Colégio Anglo (brief, KML e GPX do DTS) | Texto: retorno no Bedrock, no Lions Clube; o 10 km estende até a Brutal. Ponto do Bedrock no mapa = partida do reconhecimento de 11/07 (Strava, ~1,8 km a leste, altura do nº 3484, que o planejamento de julho chama de Lions). Brutal fica em frente à Drogal, no mesmo ponto do retorno do KML (rotatória do Anglo): coordenada mantida, falta só o número. Marcos sem km | Correção do Raphael em 14/10 à noite. Nas conversas com a prefeitura (Anexo Técnico I v2, 22/09) o retorno oficial ainda é o Anglo, a 3,77 km: **o traçado protocolado e o site divergem; alinhar antes da vistoria do DTS** |
| Kit | Entraram "Brinde dos patrocinadores" e "Voucher dos parceiros" | Pedido de 14/10; de que voucher se trata está em `detailTodo` |
| Wisekey patrocinadora | Entrou na lista, com o wordmark de `01_WISEKEY/.../04_Tipografia/Logo_04-8.png` em navy e branco | Pedido de 14/10 |
| Hero com a frase "A única corrida da região onde a linha de chegada é a mesa" | Hero explica a prova (distâncias, avenida, largada e chegada na Confraria, kit, pouso); a frase de efeito foi para Realização, no fim. Bloco seguinte "Como funciona" com horários e o dia | "Hero tá um bosta, precisa explicar, o começo precisa cativar" (14/10, repetido). `heroLede` e `ideia` no JSON |
| Faixa de patrocinadores sob o hero parada | Esteira da esquerda para a direita, como a seção | Pedido de 14/10 |
| Percurso em linha reta com dois retornos | Texto: sai da Confraria, contorna na Brutal (em frente à Drogal), vai até o Lions Clube (Bedrock) e volta; 5 km é uma volta, 10 km são duas | Pedido de 14/10 à noite. Pontos no mapa: Brutal = coordenada do KML, Lions = partida do Strava |
| LBE (Ladislau Branding Estúdio) como parceiro | Entrou com o logo do site lbestrategy.com (navy e branco); papel "Branding da Confraria Bem Te Vi" | Pedido de 14/10; o Instagram do estúdio é @lbe.strategy, o pessoal é @oladislau_ |
| Notas sob os preços (taxa 12%, 60+/PCD, grupos, prazos, balcão, cupom) | Fora da seção de preços. As regras seguem no FAQ e na Ticket Sports | "Tira isso" (14/10 à noite) |
| Fotos do entardecer e artes navy | Só fotos de dia: avenida, corredores, placa de dia; artes da campanha saíram do Kit e da Programação | "Muda as fotos, deixar de dia claro, foco nisso" |
| "Percurso em homologação" | "Percurso homologado" | Raphael, 14/10: já foi homologado, só falta burocracia interna |
| LBE parceiro | LBE patrocinador (nas duas esteiras); Superação Eventos parceira (estrutura), sem logo | Pedido de 14/10 |
| Camiseta "sujeita à grade" depois de 30/10 | Texto muda sozinho nos dois lugares (preços e kit) | `shirtState` em `lotes.js` |
| Contador de inscritos | Não existe; só "900 vagas" | Como o brief pede |

## Testado

- `npm run check:lotes`: 22 datas, todas as viradas (18/10, 08/11, 23/11, 24 a 26/11 balcão fechado, 27 e 28/11 balcão, 29/11 "É HOJE", 30/11 "Obrigado, bando"), urgência a 3 dias, camiseta em 31/10, bloco atual da programação no dia
- Link da Ticket Sports com UTM responde 200 (14/10)
- Nenhum travessão no HTML gerado (`grep` no `dist/index.html`)
- Captura de página inteira, celular e desktop, lida fatia por fatia
