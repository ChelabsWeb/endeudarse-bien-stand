# Endeudarse bien — Stand BCU (Taller 3, edición 2026)

Materiales del taller **"Endeudarse bien"** para el stand del BCU (*Central para Vos*).

## 🎮 El juego: 12 Meses

**[▶ Jugar ahora](https://chelabsweb.github.io/endeudarse-bien-stand/)** — un año en la piel de Joaquín, 12 decisiones (~5 min solo, ~15 min en equipos debatiendo).

Un solo archivo HTML, funciona **offline** en cualquier tablet o compu (también sirve `Joaquin_12_Meses.html` descargado). Modo kiosco, ranking del día, sonido sintetizado, cero dependencias.

- **Modo Duelo**: 2 jugadores pasa-la-tablet, mismos eventos, corona para el ganador.
- **Modo Sala**: varias máquinas compiten a la vez (1 vs 1 vs 1) con nombres de equipo. Todas ponen el mismo código de 4 letras → mismos eventos para todos, ranking en vivo mes a mes, timer de decisión de 45 s y podio final. Requiere internet (Supabase Realtime); ideal para talleres con grupos y pocas máquinas: se juega por tandas o por equipos alrededor de cada pantalla.
- **Modo Proyector**: una máquina extra entra a la sala en "solo mirar" (botón *Proyector* tras poner el código) y muestra el tablero gigante para todo el grupo: equipos, puntajes, progreso del año y huella en vivo. El facilitador arranca la partida (y la revancha) desde ahí.
- **QR "llevate el juego"** en la constancia final: los participantes lo escanean y se llevan el juego al celular.
- **Rejugable**: pool de 8 eventos de decisión (salen 3) + 8 "chequeos rápidos" con datos reales del BCU (salen 2, en los meses 4 y 11) + el shock del Mes 7.
- **Análisis en el proyector**: al terminar todos los equipos, el tablero muestra "dónde más nos clavamos" — los errores más repetidos entre equipos con su explicación ("la posta").
- **PWA**: abierta una vez desde la URL, queda cacheada y funciona sin internet.
- **Estadísticas del stand**: 5 toques en el membrete de la portada abren el panel del día (partidas, promedio, % huella limpia).

## 📦 Contenido

| Archivo | Qué es |
|---|---|
| `index.html` / `Joaquin_12_Meses.html` | El juego para las tablets del stand |
| `Taller3_Endeudarse_Bien_Stand_v3.pptx` | Mazo de 28 slides (diseño 2026) |
| `Guia_Facilitador_Taller3_Stand_v3.pdf` | Guía del facilitador |
| `Prompt_IA_Asesora_v2.md` | Prompt de "Valentina" (actividad con IA) |
| `stand_bcu.html` | Mini-web del stand (Valentina + calculadora + puntaje 1–7) |
| `Tarjeta_Takeaway.pdf` | Tarjetas para repartir (4 por hoja A4) |
