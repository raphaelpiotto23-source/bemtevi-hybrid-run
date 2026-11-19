// Testa as viradas de lote e do countdown com datas simuladas. node _fonte/test_lotes.mjs
import event from '../src/data/event.json' with { type: 'json' };
import { loteState, badge, priceFor, raceState, shirtState, currentScheduleIndex, brl, parseNow } from '../src/lib/lotes.js';

const cases = [
  '2026-11-19T12:00', '2027-01-11T23:59', '2027-01-12T00:00', '2027-01-17T06:00', '2027-01-17T09:50', '2027-01-18T08:00',
];
for (const c of cases) {
  const now = parseNow('?now=' + c);
  const st = loteState(event, now);
  const b = badge(st);
  const p = priceFor(event, st, '10k');
  const r = raceState(event, now);
  const sh = shirtState(event, now);
  console.log(
    c.padEnd(17), st.kind.padEnd(9), b.text.padEnd(44), (b.urgent ? 'URG' : '   '),
    ('10k ' + brl(p.current) + (p.next ? ' > ' + brl(p.next.price) + ' (' + p.next.label + ')' : '')).padEnd(34),
    r.kind.padEnd(6), sh.guaranteed ? 'tam.ok' : 'grade ', 'prog#' + currentScheduleIndex(event, now),
  );
}
