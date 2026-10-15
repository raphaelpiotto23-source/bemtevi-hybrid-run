// Testa as viradas de lote e do countdown com datas simuladas. node _fonte/test_lotes.mjs
import event from '../src/data/event.json' with { type: 'json' };
import { loteState, badge, priceFor, raceState, shirtState, currentScheduleIndex, brl, parseNow } from '../src/lib/lotes.js';

const cases = [
  '2026-10-14T12:00', '2026-10-15T23:59', '2026-10-16T00:00', '2026-10-18T23:59', '2026-10-19T00:00',
  '2026-10-30T23:59', '2026-10-31T00:00', '2026-11-06T10:00', '2026-11-08T23:59', '2026-11-09T00:00',
  '2026-11-21T10:00', '2026-11-23T23:59', '2026-11-24T00:00', '2026-11-26T23:59', '2026-11-27T13:59',
  '2026-11-27T14:00', '2026-11-28T18:00', '2026-11-28T18:01', '2026-11-29T06:00', '2026-11-29T07:31',
  '2026-11-29T09:50', '2026-11-30T08:00',
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
