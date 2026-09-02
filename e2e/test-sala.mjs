// E2E de la sala v2: proyector + 2 equipos, partida entera de 15 paradas.
// Verifica: equipos con nombre fijo, mismas letras en todas las pantallas, pregunta en vivo en el
// proyector con "quién respondió", reveal de decisiones antes de la tabla, podio final.
import { chromium } from 'playwright-core';
/* Chromium: CHROME=ruta/a/chrome.exe (por defecto el que instala Playwright en Windows) */
const EXE = process.env.CHROME || ((process.env.LOCALAPPDATA || '').split(String.fromCharCode(92)).join('/') + '/ms-playwright/chromium-1228/chrome-win64/chrome.exe');
const URL = process.env.URL || 'http://127.0.0.1:8765/index.html';
const OUT = process.env.OUT || '.';
let checks = 0, fails = 0;
const ok = (cond, msg) => { checks++; if (!cond) { fails++; console.log('  ✗ ' + msg); } else console.log('  ✓ ' + msg); };
const click = (p, sel) => p.evaluate(s => { const el = document.querySelector(s); if (!el) throw new Error('no ' + s); el.click(); }, sel);
const sleep = ms => new Promise(r => setTimeout(r, ms));

const browser = await chromium.launch({ executablePath: EXE, headless: true });
const mk = async (vp) => { const c = await browser.newContext({ viewport: vp }); const p = await c.newPage(); p.on('pageerror', e => console.log('PAGEERROR', e.message)); await p.goto(URL); await p.waitForTimeout(500); return p; };
const P = await mk({ width: 1366, height: 768 });
const A = await mk({ width: 1024, height: 768 });
const B = await mk({ width: 390, height: 844 });

console.log('1. proyector crea la partida');
await click(P, '#btnCrear');
await P.waitForSelector('#espInvCode', { timeout: 20000 });
await P.waitForFunction(() => /ESPERANDO EQUIPOS/.test(document.querySelector('#espEstado').textContent), null, { timeout: 20000 });
const code = await P.$eval('#espInvCode', e => e.textContent.trim());
ok(/^[A-Z]{4}$/.test(code), 'código de 4 letras: ' + code);

console.log('2. equipos entran con el código y eligen equipo (sin teclado de nombre)');
for (const [p, idx] of [[A, 3], [B, 0]]) {
  await click(p, '#btnEntrar');
  await p.waitForSelector('#sala.on');
  await p.keyboard.type(code);
  await p.keyboard.press('Enter');
  await p.waitForSelector('#lobby.on');
  await p.waitForFunction(() => document.querySelector('#btnArrancar').style.display !== 'none', null, { timeout: 20000 });
  // LISTOS sin equipo → rechazado
  await click(p, '#btnArrancar'); await sleep(150);
  ok(await p.evaluate(() => SALA.listo === false && !document.querySelector('.lobJ.yo .okTag')), 'LISTOS sin equipo rebota (no queda listo)');
  await p.evaluate(i => document.querySelectorAll('.avBtn')[i].click(), idx);
  await sleep(400);
}
await sleep(1500);
const nomA = await A.$eval('.lobJ.yo span', e => e.textContent);
const nomB = await B.$eval('.lobJ.yo span', e => e.textContent);
ok(/TIBURONES/.test(nomA) && /CHANCHOS/.test(nomB), `nombres = equipo elegido (${nomA} / ${nomB})`);
await A.waitForFunction(() => document.querySelectorAll('.avBtn.off').length === 1, null, { timeout: 10000 }).then(() => ok(true, 'el equipo del otro queda bloqueado en la grilla'), () => ok(false, 'el equipo del otro queda bloqueado en la grilla'));
await B.screenshot({ path: `${OUT}/e2e-mob-lobby.png` });
await click(A, '#btnArrancar'); await click(B, '#btnArrancar');
await P.waitForFunction(() => /Arrancar/.test(document.querySelector('#espArrancar').textContent), null, { timeout: 20000 });
ok(true, 'proyector ve a todos LISTOS');
await P.screenshot({ path: `${OUT}/e2e-proj-invite.png` });

console.log('3. arranca la partida');
await click(P, '#espArrancar');
await A.waitForSelector('#goOv.on', { timeout: 10000 });
await A.waitForSelector('#juego.on .op', { timeout: 15000 });
ok(true, 'ronda 0 abierta en las máquinas');

let revealVisto = 0, letrasOk = 0, pregVisto = 0, quienRespondio = 0;
for (let n = 0; n < 15; n++) {
  console.log('   parada', n + 1);
  const esBocha = await A.evaluate(() => document.querySelector('#bocha').classList.contains('on'));
  if (n === 8) {
    await A.waitForSelector('#bocha.on', { timeout: 20000 }); await B.waitForSelector('#bocha.on', { timeout: 20000 });
    await sleep(1800);
    const pb = await P.evaluate(() => !!document.querySelector('#espPreg.on .pBocha'));
    ok(pb, 'parada 9 (bocha): el proyector muestra la bocha');
    await click(A, '#bochaBtn'); await click(B, '#bochaBtn');
    await A.waitForSelector('#juego.on .op', { timeout: 20000 });
    continue;
  }
  await A.waitForFunction(i => document.querySelector('#juego').classList.contains('on') && document.querySelectorAll('#evOps .op').length === 3 && !document.querySelector('#mkOv').classList.contains('on'), n, { timeout: 30000 });
  const fresco = () => document.querySelector('#juego').classList.contains('on') && [...document.querySelectorAll('#evOps .op')].length === 3 && [...document.querySelectorAll('#evOps .op')].every(o => o.style.pointerEvents !== 'none') && !document.querySelector('#mkOv').classList.contains('on');
  await B.waitForFunction(fresco, null, { timeout: 30000 });
  await A.waitForFunction(fresco, null, { timeout: 30000 });
  await sleep(600);
  // proyector: pregunta en vivo con las mismas letras
  const pOps = await P.$$eval('#espPreg.on .pOp b', els => els.map(e => e.textContent.trim()));
  const aOps = await A.$$eval('#evOps .op b', els => els.map(e => e.textContent.trim()));
  const bOps = await B.$$eval('#evOps .op b', els => els.map(e => e.textContent.trim()));
  if (pOps.length === 3) pregVisto++;
  if (JSON.stringify(aOps) === JSON.stringify(bOps) && JSON.stringify(aOps) === JSON.stringify(pOps)) letrasOk++;
  if (n === 0) { await P.screenshot({ path: `${OUT}/e2e-proj-pregunta.png` }); await A.screenshot({ path: `${OUT}/e2e-desk-ronda.png` }); }
  // A responde la primera opción disponible; el proyector debe marcarlo
  await A.evaluate(() => { const b = [...document.querySelectorAll('#evOps .op:not(.off)')][0]; b.click(); });
  await sleep(900);
  const okA = await P.evaluate(() => document.querySelectorAll('#espPreg .pEq.ok').length);
  if (okA === 1) quienRespondio++;
  if (n === 0) await P.screenshot({ path: `${OUT}/e2e-proj-pregunta-1resp.png` });
  await B.evaluate(() => { const ops = [...document.querySelectorAll('#evOps .op:not(.off)')]; ops[ops.length - 1].click(); });
  if (n === 14) break; /* la última parada no tiene marcador: va directo a la constancia y al podio */
  // marcador: primero el reveal, después la tabla
  try { await P.waitForSelector('#mkOv.on', { timeout: 30000 }); }
  catch (e) {
    const dump = async (p, nm) => console.log(nm, JSON.stringify(await p.evaluate(() => ({ rFase: SALA.rFase, fase: SALA.fase, rn: SALA.rn, host: SALA.esHost, Si: S && S.i, resp: S && S.respondida, prog: Object.fromEntries(Object.entries(SALA.prog).map(([k, v]) => [k, { mes: v.mes, rn: v.rn, resp: v.resp, op: v.op, fin: v.fin }])) }))));
    await dump(P, 'P'); await dump(A, 'A'); await dump(B, 'B');
    throw e;
  }
  await sleep(700);
  const rv = await P.evaluate(() => ({ on: document.querySelector('#mkReveal').classList.contains('on'), rows: document.querySelectorAll('#mkReveal .rvRow').length, chips: document.querySelectorAll('#mkReveal .rvAv').length, tabla: document.querySelector('#mkRows').style.display }));
  if (rv.on && rv.rows >= 3 && rv.chips === 2 && rv.tabla === 'none') revealVisto++;
  if (n === 0) { await P.screenshot({ path: `${OUT}/e2e-proj-reveal.png` }); await A.screenshot({ path: `${OUT}/e2e-desk-reveal.png` }); await B.screenshot({ path: `${OUT}/e2e-mob-reveal.png` }); }
  if (n === 1) { await sleep(3800); await P.screenshot({ path: `${OUT}/e2e-proj-tabla.png` }); await B.screenshot({ path: `${OUT}/e2e-mob-tabla.png` }); }
  await P.waitForFunction(() => !document.querySelector('#mkOv').classList.contains('on'), null, { timeout: 30000 });
}
ok(pregVisto >= 13, `el proyector mostró la pregunta en vivo en ${pregVisto}/14 paradas`);
ok(letrasOk >= 13, `mismas letras en máquinas y proyector en ${letrasOk}/14 paradas`);
ok(quienRespondio >= 12, `el proyector marcó quién respondió en ${quienRespondio}/14 paradas`);
ok(revealVisto >= 12, `reveal de decisiones antes de la tabla en ${revealVisto}/13 paradas con marcador`);

console.log('4. cierre');
await A.waitForSelector('#final.on', { timeout: 30000 });
await B.waitForSelector('#final.on', { timeout: 30000 });
ok(true, 'las máquinas llegan a la constancia');
await P.waitForSelector('#espCols.podio', { timeout: 30000 });
await sleep(6000);
const podio = await P.$$eval('#espCols.podio .eCol .nom', els => els.map(e => e.textContent));
ok(podio.length === 2 && podio.every(x => /TIBURONES|CHANCHOS/.test(x)), 'podio del proyector con los dos equipos: ' + podio.join(' / '));
await P.screenshot({ path: `${OUT}/e2e-proj-podio.png`, fullPage: true });
await A.screenshot({ path: `${OUT}/e2e-desk-final.png` });
await A.evaluate(() => document.querySelector('#recibo').scrollIntoView()); await sleep(400);
await A.screenshot({ path: `${OUT}/e2e-desk-final-recibo.png` });
const errA = await A.evaluate(() => window.__err || 0);
console.log(`\n${checks - fails}/${checks} checks OK`);
await browser.close();
process.exit(fails ? 1 : 0);
