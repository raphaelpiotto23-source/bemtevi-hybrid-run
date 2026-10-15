# Bem Te Vi Hybrid Run · comprar o domínio e publicar o site

Passo a passo de 15/10/2026. O site já está no ar em endereço provisório; falta só o domínio próprio.

| O quê | Onde |
|---|---|
| Site hoje (provisório) | https://raphaelpiotto23-source.github.io/bemtevi-hybrid-run/ |
| Repositório | https://github.com/raphaelpiotto23-source/bemtevi-hybrid-run (branch `main`) |
| Pasta no computador | `Desktop/03_HYBRID_CLUB/02_Hybrid_Run_BemTeVi/06_Site/2026-10-14_site_thehybridrun` |
| Publicação | Automática: cada `git push` na `main` publica em 1 a 2 minutos (GitHub Actions) |

---

## 1. O domínio

**thehybriderun.com.br** (com o "e" depois de "hybrid"). Decisão do Raphael em 15/10/2026. Livre no Registro.br nesse dia; thehybriderun.com também estava livre.

Cuidado com a grafia: thehybridrun.com.br (sem o "e") é de outra pessoa até 05/2027. Em locução, story e material impresso, soletrar o endereço ou usar o link direto, para ninguém cair no domínio errado.

## 2. Comprar no Registro.br

1. Entrar em https://registro.br e fazer login (ou criar conta com CPF ou CNPJ do The Hybrid Club).
2. Buscar `thehybriderun.com.br` → **Registrar**. Conferir a grafia antes de pagar: t-h-e-h-y-b-r-i-d-e-r-u-n.
3. Titular: CPF seu ou CNPJ do clube. Prazo: 1 ano já basta (dá para renovar).
4. Pagar (Pix ou boleto). Com Pix, o domínio fica ativo em minutos; com boleto, depois da compensação.
5. Não precisa contratar hospedagem nem e-mail: o site fica no GitHub, de graça.

## 3. Apontar o domínio para o GitHub (DNS)

No Registro.br, abrir o domínio → **DNS** → **Editar zona** (usar os servidores DNS do próprio Registro.br, que é o padrão).

Criar estes registros, exatamente assim:

| Tipo | Nome | Valor |
|---|---|---|
| A | (deixar vazio, é o domínio raiz) | 185.199.108.153 |
| A | (vazio) | 185.199.109.153 |
| A | (vazio) | 185.199.110.153 |
| A | (vazio) | 185.199.111.153 |
| CNAME | www | raphaelpiotto23-source.github.io |

Salvar. A propagação leva de 10 minutos a algumas horas (no .br costuma ser rápido).

## 4. Ligar o domínio no GitHub

1. Abrir https://github.com/raphaelpiotto23-source/bemtevi-hybrid-run/settings/pages
2. Em **Custom domain**, digitar `thehybriderun.com.br` e clicar **Save**. O GitHub checa o DNS; quando aparecer o selo verde "DNS check successful", seguir.
3. Abrir https://github.com/raphaelpiotto23-source/bemtevi-hybrid-run/settings/variables/actions e **apagar a variável `BASE_PATH`**. Ela só existe porque hoje o site vive em `/bemtevi-hybrid-run/`; com domínio próprio ele vive na raiz, e se a variável ficar as imagens quebram.
4. Voltar em Settings → Pages e marcar **Enforce HTTPS** (pode levar até 1 hora para a opção liberar, enquanto o GitHub emite o certificado).

## 5. Ajustes no código (eu faço, é só me chamar)

Quando o domínio estiver comprado, me passa o nome e eu faço tudo isto num commit só:

- [ ] Criar `public/CNAME` com o domínio (garante que o GitHub não perca a configuração a cada deploy)
- [ ] `src/data/event.json` → `siteUrl`: `https://thehybriderun.com.br`
- [ ] `astro.config.mjs` → `site: 'https://thehybriderun.com.br'`
- [ ] `public/robots.txt` e `public/sitemap.xml`: trocar `DOMINIO` pelo domínio
- [ ] Rodar o workflow de deploy de novo e conferir que imagens, mapa, fontes e countdown carregam no domínio novo
- [ ] Testar a prévia de link no WhatsApp (imagem de compartilhamento 1200x630)

Se preferir fazer sozinho: editar esses arquivos, depois na pasta do site rodar `git add -A`, `git commit -m "domínio"` e `git push`.

## 6. Depois de publicar

- [ ] **Bio do Instagram** (@thehybridclube e @bemtevi.confraria): trocar o link da Ticket Sports pelo domínio. O site leva para a Ticket Sports com UTM, e assim dá para medir quem veio do Instagram.
- [ ] **Google Search Console** (https://search.google.com/search-console): adicionar o domínio e enviar `https://thehybriderun.com.br/sitemap.xml`.
- [ ] **GA4 e Meta Pixel**: criar e me passar os IDs (formato `G-XXXXXXX` e um número de 15 a 16 dígitos). Entram em `event.json` → `analytics`; sem ID, nada é carregado.

## 7. Pendências de conteúdo que continuam abertas

| Item | Situação |
|---|---|
| Regulamento v1.1 | Não linkado. A v1.0 tem dados antigos e não pode entrar |
| Estacionamento | FAQ mostra `[PREENCHER: estacionamento e acesso]` até definir com o Bem Te Vi |
| Logo da Superação Eventos | Aparece só o nome; pedir o arquivo |
| Logos de Gonçalves e Boa Vista Seguros | Só o símbolo, tirado do post do treinão; pedir o vetor original para peças grandes |
| Voucher do kit | Aparece "Voucher dos parceiros"; confirmar de que é o voucher |
| Ponto do Lions / Bedrock no mapa | Aproximado (altura do nº 3484); conferir na vistoria do DTS |
| Anexo Técnico na prefeitura | Ainda descreve o retorno no Anglo; o site descreve Brutal + Lions em duas voltas |
| Preço do lote vigente | Conferir com a Ticket Sports no dia da virada (18/10). Se o 1º lote esgotar antes, colocar `"loteOverride": 2` no `event.json` |

## Contas e acessos

- GitHub: `raphaelpiotto23-source` (já logado no Chrome; a senha do git já está salva no Windows).
- Registro.br: a sua conta (CPF ou CNPJ).
- Nada do site depende de servidor pago. Custo total: só o domínio.
