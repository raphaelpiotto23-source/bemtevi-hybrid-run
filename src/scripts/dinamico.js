// Tudo que depende da hora: countdown, lote, preços, camiseta, programação, CTA fixo, analytics.
// Simule com ?now=2026-11-29T07:00 (horário de São Paulo).
import event from '../data/event.json';
import { parseNow, loteState, badge, priceFor, brl, raceState, countdownParts, pad2, shirtState, currentScheduleIndex } from '../lib/lotes.js';

const offset = parseNow(location.search).getTime() - Date.now();
const now = () => new Date(Date.now() + offset);
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

// ---- countdown
const units = { d: $('[data-unit="d"]'), h: $('[data-unit="h"]'), m: $('[data-unit="m"]'), s: $('[data-unit="s"]') };
function setDigits(el, value) {
  const str = String(value).padStart(2, '0');
  while (el.children.length < str.length) { const sp = document.createElement('span'); sp.className = 'digit'; el.appendChild(sp); }
  while (el.children.length > str.length) el.lastChild.remove();
  [...str].forEach((ch, i) => {
    const d = el.children[i];
    if (d.textContent !== ch) {
      // nó novo reinicia a animação sem forçar layout
      const n = document.createElement('span'); n.className = reduced ? 'digit' : 'digit tick'; n.textContent = ch; d.replaceWith(n);
    }
  });
}
function tick() {
  const r = raceState(event, now());
  const box = $('[data-countdown]'); const msg = $('[data-count-msg]'); const u = $('[data-count-units]');
  if (!box) return;
  box.dataset.kind = r.kind;
  if (r.kind === 'hoje') { msg.textContent = 'É HOJE'; msg.hidden = false; u.hidden = true; return; }
  if (r.kind === 'depois') { msg.textContent = 'Obrigado, bando. Fotos na Fotop.'; msg.hidden = false; u.hidden = true; return; }
  msg.hidden = true; u.hidden = false;
  const c = countdownParts(r.ms);
  setDigits(units.d, c.d); setDigits(units.h, pad2(c.h)); setDigits(units.m, pad2(c.m)); setDigits(units.s, pad2(c.s));
}

// ---- lote, selo e preços
function renderLote() {
  const n = now();
  const st = loteState(event, n);
  const b = badge(st);
  const el = $('[data-badge]');
  if (el) { el.textContent = b.text; el.classList.toggle('urgent', b.urgent); }
  const half = $('[data-desc]')?.checked ?? false;
  $$('[data-dist]').forEach((card) => {
    const p = priceFor(event, st, card.dataset.dist, half);
    const price = $('[data-price]', card), next = $('[data-next]', card);
    price.textContent = p.current != null ? brl(p.current) : 'Encerrado';
    if (p.next) { next.hidden = false; next.innerHTML = `no ${p.next.label.toLowerCase()}: <span class="strike mono">${brl(p.next.price)}</span>`; }
    else next.hidden = true;
  });
  const lab = $('[data-lote-label]');
  if (lab) lab.textContent = st.kind === 'lote' ? `Preço do ${st.lote.label}${half ? ', com 50% de desconto' : ''}` : st.kind === 'encerrado' ? 'Inscrições encerradas' : priceFor(event, st, '5k').label;
  const sp = priceFor(event, st, '5k');
  const sl = $('[data-sticky-label]'), spr = $('[data-sticky-price]');
  if (sl) sl.textContent = st.kind === 'lote' ? st.lote.label : sp.label;
  if (spr) spr.textContent = sp.current != null ? `a partir de ${brl(sp.current)}` : '';
  const sh = shirtState(event, n);
  $$('[data-shirt]').forEach((e) => { e.textContent = sh.text; });
  const idx = currentScheduleIndex(event, n);
  $$('[data-schedule] .row').forEach((row, i) => row.classList.toggle('now', i === idx));
}
$('[data-desc]')?.addEventListener('change', renderLote);

// ---- entrada de seção e linha do tempo
const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -10% 0px' });
$$('.reveal, [data-timeline]').forEach((el) => io.observe(el));

// ---- CTA fixo no celular depois do hero
const hero = $('#inicio');
if (hero) new IntersectionObserver(([e]) => document.body.classList.toggle('past-hero', !e.isIntersecting), { threshold: 0.15 }).observe(hero);

// ---- analytics no clique de inscrição (IDs em event.json; sem ID os globais não existem)
document.addEventListener('click', (e) => {
  const a = e.target.closest('[data-cta]');
  if (!a) return;
  window.gtag?.('event', 'inscreva_se', { cta: a.dataset.cta });
  window.fbq?.('track', 'InitiateCheckout', { content_name: a.dataset.cta });
});

tick(); renderLote();
setInterval(tick, 1000);
setInterval(renderLote, 60000);
