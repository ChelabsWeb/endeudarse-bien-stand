# Traspaso — "Endeudarse bien" / juego 12 Meses (BCU · Pin!)

> Documento para retomar el proyecto. Última actualización: 2026-08-04 (segunda edición: sala v2 tipo Kahoot).

## Qué es esto

Kit completo del **Taller 3 "Endeudarse bien"** del programa **Pin!** (INJU/MIDES + BCU + CAF, marca "Central para Vos"), para talleres con ~20 adolescentes. La pieza central es el juego **"12 Meses"**: un año en la piel de Joaquín ($32.000 de sueldo), una decisión financiera por mes. Ya fue presentado en el BCU y gustó; el formato del taller es **3 máquinas en equipos + 1 proyector**.

- **Juego en vivo**: https://chelabsweb.github.io/endeudarse-bien-stand/ (GitHub Pages; deploy automático al pushear a `main`)
- **Repo**: https://github.com/ChelabsWeb/endeudarse-bien-stand

## El juego (index.html — un solo archivo, cero dependencias)

- **Modos**: **Sala** (la principal: máquinas por equipos + proyector, tipo Kahoot, necesita internet) · Jugar solo (offline/PWA) · Duelo (2, pasa-la-tablet) · Preguntas (trivia relámpago de 10) — los tres últimos bajo "Más modos" en el home.
- **Partida**: 15 paradas ≈ 20-25 min en equipos → 12 meses de decisiones (5 fijos: UTE, tarjeta, auto, moto, aguinaldo · 5 sorteados de un pool de 12) + 3 "recreos" de quizzes (sorteados de un banco de 12, con datos reales del BCU) + shock del mes 7 + imprevisto del mes 8.
- **Modo Sala (v2, tipo Kahoot)**: "Crear partida" genera el código (4 letras sin confundibles) y deja esa máquina de **proyector-host** mostrando el código gigante; los equipos entran con "Entrar con código", eligen nombre y **personaje** (12 stickers SVG propios, lock en vivo por presence, auto-asignación determinista al que no elige). El código sigue siendo la semilla determinista (`xmur3`+`mulberry32`, semilla = `CODIGO#ronda`) y el canal Realtime pasa a **`bcu12m2:CODIGO`** (broadcast + presence, sin tablas).
  - **Rondas sincronizadas**: el host abre cada parada (`ronda {n,dur,tipo}`), la cierra cuando respondieron todos o vence SU reloj (los timers de las máquinas son cosméticos), y manda el **marcador ordenado** (`marcador {n,tabla,final}`): overlay de ~6s con FLIP de posiciones, count-up y flechas — grande en el proyector, con nota personal en las máquinas. El feedback pedagógico es la sala de espera (sin botón Seguir; 2,5s de lectura mínima). `prog` sale al decidir y lleva `rn/resp/av`. Ronda vencida = sin puntos + racha cortada. La bocha (índice 8, ver `BOCHA_IDX`) cierra al toque de todos sin marcador.
  - **Host resiliente**: proyector caído → releva la máquina de menor id; proyector nuevo a mitad de partida → adopta la ronda por heartbeats (5s, también mientras se decide) con 7s de gracia antes de poder cerrar por completitud; el host vigente encadena la ronda siguiente aunque el cierre lo haya mandado un host en retirada. "Saltar ronda" y "Cerrar el año" como palancas del facilitador.
- **Robustez**: **F5 revive** (identidad + snapshot en sessionStorage: la pestaña vuelve como el mismo equipo y re-abre la parada en curso si no la había respondido); equipo desconectado → a los 20s "SE DESCONECTÓ" y la sala sigue; Reintentar en errores de red.
- ⚠️ Al tocar el motor de sala, leer los comentarios de `hostChequearCierre`/`recibirRonda`/`recibirMarcador`: las trampas de host-jugador (rFase vs fase), eco de ronda (guard contra `S.i`), roster parcial y host en retirada ya están resueltas y documentadas ahí.
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

**Hecho y probado**: todo lo de arriba. La sala v2 completa (rondas sincronizadas + identidad + landing + marcador + podio) se verificó con Playwright multi-contexto: partida entera de 15 paradas con timeout de equipo, F5 a mitad de ronda, caída del proyector con relevo, proyector nuevo a mitad de partida, y los modos offline intactos (50 checks verdes). El test vive fuera del repo (pedirlo si hace falta; se rearma rápido con `python -m http.server` + playwright-core).

**Pendientes sugeridos** (en orden de valor):
1. **Modo Preguntas en la sala**: los equipos respondiendo la misma trivia contra reloj en el proyector (hoy es solo local). Sirve de desempate. El protocolo de rondas ya lo soporta casi entero (rondas tipo quiz existen como "recreos").
2. Revelar qué eligió cada equipo en el marcador de ronda (oro pedagógico; la infraestructura de rondas ya está — sumar `op` al prog y pintarlo en el overlay).
3. Renombrar variables CSS `--azul`/`--rosa` (hoy contienen violeta/naranja) — dejado a propósito para después del primer taller real.
4. Sellos de feedback propios para quizzes ("ZAFÁS" no calza al errar un dato).
5. Sonido de sala en el proyector (redoble/ticks ya existen; un "pum" al abrir cada parada sumaría).

**Regla de oro**: no romper la semilla determinista, el protocolo Realtime v2 (start/ronda/prog/marcador/fin en `bcu12m2:`), el modo offline, la paleta oficial, ni el espejo `calcResumen`/`scoreParcial` (el marcador muestra el parcial 14 veces por partida: si se corren, el podio no cuadra con lo que el salón vio). `BOCHA_IDX` está acoplado al orden de `armarPartida`.
