// Toda a lógica de data do site. Roda no build (Astro) e no navegador (ilhas).
// Fuso: America/Sao_Paulo. As datas do event.json já trazem o offset -03:00.

const DAY = 86400000;
export const TZ = 'America/Sao_Paulo';

// ?now=2026-11-29T07:00 simula a data. Sem offset, lê como horário de São Paulo.
export function parseNow(search, fallback = new Date()) {
  const p = new URLSearchParams(search || '').get('now');
  if (!p) return fallback;
  const s = /([+-]\d\d:\d\d|Z)$/.test(p) ? p : p + '-03:00';
  const d = new Date(s);
  return Number.isNaN(d.getTime()) ? fallback : d;
}

// "2026-11-29" no fuso de São Paulo
export function dateKey(d) {
  return new Intl.DateTimeFormat('en-CA', { timeZone: TZ, year: 'numeric', month: '2-digit', day: '2-digit' }).format(d);
}

// "07:30" no fuso de São Paulo
export function timeKey(d) {
  return new Intl.DateTimeFormat('en-GB', { timeZone: TZ, hour: '2-digit', minute: '2-digit', hour12: false }).format(d);
}

export function daysLeft(ms) {
  return Math.max(1, Math.ceil(ms / DAY));
}

// Qual lote vale agora.
// kind: 'lote' (online aberto) · 'fechado' (24 a 26/11) · 'balcao' (27 e 28/11) · 'encerrado'
export function loteState(event, now) {
  const t = now.getTime();
  const lotes = event.lotes;
  const online = lotes.filter((l) => !l.from);
  const balcao = lotes.find((l) => l.from) || null;

  if (event.loteOverride) {
    const l = lotes.find((x) => x.id === event.loteOverride);
    if (l) {
      const i = online.indexOf(l);
      const next = l.from ? null : online[i + 1] || balcao;
      return { kind: l.from ? 'balcao' : 'lote', lote: l, next, msLeft: Date.parse(l.until) - t, forced: true };
    }
  }
  for (let i = 0; i < online.length; i++) {
    const l = online[i];
    if (t <= Date.parse(l.until)) {
      return { kind: 'lote', lote: l, next: online[i + 1] || balcao, msLeft: Date.parse(l.until) - t, last: i === online.length - 1 };
    }
  }
  if (balcao && t < Date.parse(balcao.from)) return { kind: 'fechado', lote: balcao, next: null, msLeft: Date.parse(balcao.from) - t };
  if (balcao && t <= Date.parse(balcao.until)) return { kind: 'balcao', lote: balcao, next: null, msLeft: Date.parse(balcao.until) - t };
  return { kind: 'encerrado', lote: null, next: null, msLeft: 0 };
}

// Selo do hero. urgent = faltando 3 dias ou menos para virar o lote.
export function badge(state) {
  if (state.kind === 'lote') {
    const n = daysLeft(state.msLeft);
    const label = state.lote.label.toUpperCase();
    const prazo = state.msLeft < DAY ? 'ACABA HOJE' : `ACABA EM ${n} DIAS`;
    const text = state.last ? `${label} · ÚLTIMO ONLINE · ${prazo}` : `${label} · ${prazo}`;
    return { text, urgent: n <= 3 };
  }
  if (state.kind === 'fechado') return { text: 'INSCRIÇÕES ONLINE ENCERRADAS · GARANTA NO BALCÃO', urgent: true };
  if (state.kind === 'balcao') return { text: 'BALCÃO ABERTO NA RETIRADA DO KIT', urgent: true };
  return { text: 'INSCRIÇÕES ENCERRADAS', urgent: false };
}

// Preço de uma modalidade no estado atual, com o do próximo lote para riscar.
export function priceFor(event, state, distId, half = false) {
  const f = half ? (event.discounts.senior60 ?? 0.5) : 1;
  const lote = state.lote;
  if (!lote) return { current: null, next: null, label: 'Inscrições encerradas' };
  const current = lote.prices[distId] * f;
  const next = state.next ? { label: state.next.label, price: state.next.prices[distId] * f } : null;
  const label = state.kind === 'fechado' ? 'No balcão, 27 e 28/11' : state.kind === 'balcao' ? 'Balcão, enquanto houver vaga' : lote.label;
  return { current, next, label };
}

export function brl(n) {
  if (n == null) return '';
  const frac = Math.round(n * 100) % 100 === 0 ? 0 : 2;
  return 'R$ ' + n.toLocaleString('pt-BR', { minimumFractionDigits: frac, maximumFractionDigits: frac });
}

// Countdown. kind: 'antes' · 'hoje' · 'depois'
export function raceState(event, now) {
  const start = new Date(event.raceStart);
  const ms = start.getTime() - now.getTime();
  if (dateKey(now) === dateKey(start)) return { kind: 'hoje', ms };
  if (ms < 0) return { kind: 'depois', ms };
  return { kind: 'antes', ms };
}

export function countdownParts(ms) {
  const s = Math.max(0, Math.floor(ms / 1000));
  return { d: Math.floor(s / 86400), h: Math.floor((s % 86400) / 3600), m: Math.floor((s % 3600) / 60), s: s % 60 };
}

export const pad2 = (n) => String(n).padStart(2, '0');

export function shirtState(event, now) {
  const ok = now.getTime() <= Date.parse(event.shirtSizeUntil);
  return { guaranteed: ok, text: ok ? 'Tamanho garantido até 30/10' : 'Camiseta sujeita à grade' };
}

export function transferState(event, now) {
  return now.getTime() <= Date.parse(event.transferUntil);
}

// Índice do bloco atual da programação, só no dia da prova. -1 fora do dia.
export function currentScheduleIndex(event, now) {
  if (raceState(event, now).kind !== 'hoje') return -1;
  const hm = timeKey(now);
  const times = event.schedule.map((s) => (s.time === 'Tarde' ? '12:00' : s.time));
  let idx = -1;
  times.forEach((t, i) => { if (hm >= t) idx = i; });
  return idx;
}

// URL de inscrição com UTM (testado em 14/10: a Ticket Sports responde 200 com a query).
export function registrationUrl(event, cta) {
  const sep = event.registrationUrl.includes('?') ? '&' : '?';
  return `${event.registrationUrl}${sep}${event.utm}${cta ? '&utm_content=' + cta : ''}`;
}

export function whatsappUrl(event, text) {
  return `https://wa.me/${event.contactWhatsapp}?text=${encodeURIComponent(text)}`;
}
