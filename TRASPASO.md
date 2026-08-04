# Traspaso — "Endeudarse bien" / juego 12 Meses (BCU · Pin!)

> Documento para retomar el proyecto. Última actualización: 2026-08-04.

## Qué es esto

Kit completo del **Taller 3 "Endeudarse bien"** del programa **Pin!** (INJU/MIDES + BCU + CAF, marca "Central para Vos"), para talleres con ~20 adolescentes. La pieza central es el juego **"12 Meses"**: un año en la piel de Joaquín ($32.000 de sueldo), una decisión financiera por mes. Ya fue presentado en el BCU y gustó; el formato del taller es **3 máquinas en equipos + 1 proyector**.

- **Juego en vivo**: https://chelabsweb.github.io/endeudarse-bien-stand/ (GitHub Pages; deploy automático al pushear a `main`)
- **Repo**: https://github.com/ChelabsWeb/endeudarse-bien-stand

## El juego (index.html — un solo archivo, cero dependencias)

- **Modos**: Jugar (solo, offline/PWA) · Duelo (2, pasa-la-tablet) · **Sala** (varias máquinas + proyector, necesita internet) · **Preguntas** (trivia relámpago de 10).
- **Partida**: 15 paradas ≈ 20 min en equipos → 12 meses de decisiones (5 fijos: UTE, tarjeta, auto, moto, aguinaldo · 5 sorteados de un pool de 12) + 3 "recreos" de quizzes (sorteados de un banco de 12, con datos reales del BCU) + shock del mes 7 + imprevisto del mes 8.
- **Modo Sala**: el código de 4 letras es a la vez semilla determinista (mismos eventos en todas las máquinas: `xmur3`+`mulberry32`, semilla = `CODIGO#ronda`) y canal de **Supabase Realtime** (broadcast + presence, canal `bcu12m:CODIGO`, sin tablas — solo canales). El proyector entra con "Proyector: solo mirar": tablero en vivo, arranque/revancha, reveal del ganador con redoble, y "DONDE MÁS NOS CLAVAMOS" (errores repetidos entre equipos con su explicación).
- **Robustez**: equipo desconectado → a los 20s queda "SE DESCONECTÓ" y la sala cierra igual; botón "Cerrar el año" de emergencia; Reintentar en errores de red; timer de 45s por decisión que presiona pero **no fuerza** la elección (decisión pedagógica).
- **Puntaje**: patrimonio + fondo×0,5 − intereses×1,5 − marcas×$8.000 (consultas de crédito: −$3.000 y NO bajan la categoría BCU) + rachas + medallas. ⚠️ `calcResumen` y `scoreParcial` deben mantenerse espejados o el podio no cuadra con la constancia.
- **Paleta oficial** Central para Vos (no cambiar): tinta `#003B8B`, violeta `#811DE6`, amarillo `#FBC504`, naranja `#F76025`, magenta `#DA1556` (negativo), lima `#74D526` (+`--verdeTxt #2E7D0F` para lima como texto).
- Supabase: proyecto "Sistema EDO by Chelabs" (`okywobvelfvyhnzvjycm`), solo Realtime, costo $0. URL y publishable key embebidas en el HTML (`SB_URL`/`SB_KEY`).

## Archivos del repo

| Archivo | Qué es |
|---|---|
| `index.html` = `Joaquin_12_Meses.html` | El juego (⚠️ al editar uno, `cp index.html Joaquin_12_Meses.html` antes de commitear) |
| `sw.js` | Service worker: red-primero para navegación (siempre sirve la última versión) |
| `Formacion_de_Formadores_Endeudarse_Bien_2026.pptx` | Mazo del taller (39 slides, estética Pin!, calcado al deck original con el juego como bloque central) |
| `gen_formadores_pptx.py` | Regenera el mazo: `python3 gen_formadores_pptx.py` (python-pptx; QRs opcionales en /tmp) |
| `Guia_Facilitador_Taller3_Stand_v3.pdf` · `Tarjeta_Takeaway.pdf` · `Prompt_IA_Asesora_v2.md` · `stand_bcu.html` | Materiales del stand (guía, tarjetas, IA asesora, mini-web) |

Fuentes oficiales de contenido: **Manual de tallerista Pin! 2025** (Taller 3, págs. 56-94) y la paleta (`paletadecolores.pdf`) — pedírselos a Feli si no los tenés.

## Cómo trabajar

1. Editar `index.html` → `cp index.html Joaquin_12_Meses.html` → commit → push → GitHub Pages actualiza en ~1 min.
2. Probar la sala: 3 pestañas del navegador (una entra como Proyector) con el mismo código.
3. Tests E2E usados hasta ahora: Playwright con varios contextos contra `python3 -m http.server` (ojo: el botón "Seguir" del feedback se habilita a los 1000ms — esperar ~1150ms antes de clickearlo en bots).

## Estado y pendientes

**Hecho y probado**: todo lo de arriba, incluida una pasada de un panel de diseño de 6 especialistas (15 mejoras aplicadas).

**Pendientes sugeridos** (en orden de valor):
1. **Modo Preguntas en la sala**: los 3 equipos respondiendo la misma trivia contra reloj en el proyector (hoy es solo local). Sirve de desempate.
2. Personajes ilustrados oficiales de la paleta (págs. 2-5 del PDF) en portada/constancia.
3. Modo "por rondas" en sala: esperar a todos cada mes y revelar qué eligió cada equipo (oro pedagógico, cambia el flujo de avance).
4. Renombrar variables CSS `--azul`/`--rosa` (hoy contienen violeta/naranja) — dejado a propósito para después del primer taller real.
5. Sellos de feedback propios para quizzes ("ZAFÁS" no calza al errar un dato).

**Regla de oro**: no romper la semilla determinista, el protocolo Realtime (start/prog/fin), el modo offline ni la paleta oficial.
