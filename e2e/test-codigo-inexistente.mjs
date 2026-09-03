// código inexistente: aviso + corregir con las letras precargadas; recuperación sola si aparece el proyector
import { chromium } from 'playwright-core';
const EXE = process.env.CHROME || ((process.env.LOCALAPPDATA || '').split(String.fromCharCode(92)).join('/') + '/ms-playwright/chromium-1228/chrome-win64/chrome.exe');
const URL = process.env.URL || 'http://127.0.0.1:8765/index.html', OUT = process.env.OUT || '.';
let checks = 0, fails = 0;
const ok = (c, m) => { checks++; if (!c) { fails++; console.log('  ✗ ' + m); } else console.log('  ✓ ' + m); };
const click = (p, s) => p.evaluate(s => document.querySelector(s).click(), s);
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch({ executablePath: EXE, headless: true });
const mk = async vp => { const p = await (await b.newContext({ viewport: vp })).newPage(); p.on('pageerror', e => console.log('PAGEERROR', e.message)); await p.goto(URL); await p.waitForTimeout(500); return p; };
const A = await mk({ width: 390, height: 844 }), P = await mk({ width: 1366, height: 768 });
// un código que nadie creó (con vocal: imposible que lo genere el proyector)
const falso = 'AXYZ';
await click(A, '#btnEntrar'); await A.keyboard.type(falso); await A.keyboard.press('Enter');
await A.waitForSelector('#lobby.on');
await A.waitForFunction(() => document.querySelector('#lobbyVacia').style.display !== 'none', null, { timeout: 15000 });
ok(/NO HAY NINGUNA PARTIDA CON EL CÓDIGO AXYZ/.test(await A.$eval('#lobbyEstado', e => e.textContent)), 'aviso de partida inexistente a los ~2,5 s');
ok(await A.evaluate(() => document.querySelector('#avGrid').style.display === 'none' && document.querySelector('#lobbyBtns').style.display === 'none'), 'la grilla de equipos y LISTOS quedan escondidos');
await A.screenshot({ path: `${OUT}/e2e-mob-vacia.png` });
await A.evaluate(() => cambiarCodigo()); await sleep(300);
ok(await A.evaluate(() => document.querySelector('#sala').classList.contains('on') && [...document.querySelectorAll('#slotsCode .slot')].map(s => s.textContent).join('') === 'AXYZ'), 'Corregir el código vuelve a la pantalla de código con las letras precargadas');
// ahora un código real: el proyector lo crea y el equipo entra bien
await click(P, '#btnCrear'); await P.waitForFunction(() => /ESPERANDO EQUIPOS/.test(document.querySelector('#espEstado').textContent), null, { timeout: 20000 });
const code = await P.$eval('#espInvCode', e => e.textContent.trim());
await A.keyboard.press('Backspace'); await A.keyboard.press('Backspace'); await A.keyboard.press('Backspace'); await A.keyboard.press('Backspace');
await A.keyboard.type(code); await A.keyboard.press('Enter');
await A.waitForFunction(() => document.querySelector('#btnArrancar').style.display !== 'none', null, { timeout: 20000 });
await sleep(3500);
ok(await A.evaluate(() => document.querySelector('#lobbyVacia').style.display === 'none' && document.querySelector('#avGrid').style.display !== 'none'), 'con el código del proyector no aparece el aviso');
// recuperación: equipo entra a un código antes de que exista el proyector, y el proyector aparece después
const C2 = await b.newContext({ viewport: { width: 1366, height: 768 } }); const P2 = await C2.newPage(); await P2.goto(URL); await P2.waitForTimeout(400);
const B = await mk({ width: 1024, height: 768 });
const pre = 'BCDF';
await click(B, '#btnEntrar'); await B.keyboard.type(pre); await B.keyboard.press('Enter');
await B.waitForFunction(() => document.querySelector('#lobbyVacia').style.display !== 'none', null, { timeout: 15000 });
await click(P2, '#btnEntrar'); await P2.keyboard.type(pre); await click(P2, '#btnProyector');
await P2.waitForFunction(() => /ESPERANDO EQUIPOS|LISTOS/.test(document.querySelector('#espEstado').textContent), null, { timeout: 20000 });
await B.waitForFunction(() => document.querySelector('#lobbyVacia').style.display === 'none' && document.querySelector('#avGrid').style.display !== 'none', null, { timeout: 15000 });
ok(true, 'si el proyector aparece después con ese código, el lobby se recupera solo');
await B.evaluate(() => document.querySelectorAll('.avBtn')[2].click()); await sleep(1200);
ok(await P2.evaluate(() => /PULPOS/.test(document.querySelector('#espInvList').textContent)), 'y el proyector ve al equipo');
console.log(`\n${checks - fails}/${checks} checks OK`);
await b.close(); process.exit(fails ? 1 : 0);
