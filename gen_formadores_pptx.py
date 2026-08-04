# -*- coding: utf-8 -*-
"""Genera 'Formación de formadores — Endeudarse bien (edición juego 2026)'.

Uso:  python3 gen_formadores_pptx.py
Requiere: python-pptx. Opcional: /tmp/qr_juego.png y /tmp/qr_consulta.png
(se generan con `npx qrcode` o cualquier generador; si faltan, la slide
del ticket de salida sale sin imágenes).

Fuentes de contenido: Manual de tallerista Pin! 2025 (Taller 3, págs. 56-94)
+ el juego "12 Meses" (https://chelabsweb.github.io/endeudarse-bien-stand/).
Estética: risografía uruguaya del juego (papel/tinta/amarillo/rosa/azul).
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

PAPEL  = RGBColor(0xF3, 0xEE, 0xE2)
PAPEL2 = RGBColor(0xFB, 0xF8, 0xF0)
TINTA  = RGBColor(0x1B, 0x1F, 0x3A)
AMAR   = RGBColor(0xFF, 0xD5, 0x00)
ROSA   = RGBColor(0xFF, 0x48, 0xB0)
AZUL   = RGBColor(0x00, 0x78, 0xBF)
VERDE  = RGBColor(0x00, 0xA9, 0x5C)
ROJO   = RGBColor(0xF1, 0x50, 0x60)
MUTED  = RGBColor(0x6E, 0x66, 0x56)
BLANCO = RGBColor(0xFF, 0xFF, 0xFF)

DISP, BODY = 'Arial Black', 'Arial'

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
NPAG = [0]


def slide(bg=PAPEL):
    s = prs.slides.add_slide(BLANK)
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    r.fill.solid(); r.fill.fore_color.rgb = bg; r.line.fill.background()
    r.shadow.inherit = False
    NPAG[0] += 1
    return s


def box(s, x, y, w, h, fill=PAPEL2, line=TINTA, lw=2.5, off=0.08, shadow=True):
    if shadow:
        sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x + off), Inches(y + off), Inches(w), Inches(h))
        sh.fill.solid(); sh.fill.fore_color.rgb = TINTA; sh.line.fill.background(); sh.shadow.inherit = False
    b = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    b.fill.solid(); b.fill.fore_color.rgb = fill
    b.line.color.rgb = line; b.line.width = Pt(lw)
    b.shadow.inherit = False
    return b


def text(s, x, y, w, h, items, anchor=MSO_ANCHOR.TOP):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    first = True
    for it in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = it.get('al', PP_ALIGN.LEFT)
        p.space_after = Pt(it.get('sa', 4)); p.space_before = Pt(it.get('sb', 0))
        segs = it['segs'] if 'segs' in it else [it]
        for sg in segs:
            r = p.add_run(); r.text = sg['t']; f = r.font
            f.size = Pt(sg.get('s', it.get('s', 15)))
            f.bold = sg.get('b', it.get('b', False))
            f.name = sg.get('f', it.get('f', BODY))
            f.color.rgb = sg.get('c', it.get('c', TINTA))
    return tb


def head(s, kick, title, tc=TINTA):
    text(s, 0.55, 0.28, 12.3, 0.4, [{'t': kick, 's': 12.5, 'c': AZUL, 'b': True}])
    text(s, 0.5, 0.56, 12.4, 1.0, [{'t': title, 's': 33, 'c': tc, 'f': DISP}])


def footer(s, extra=''):
    text(s, 0.55, 7.08, 12.3, 0.35, [{'t': f'PIN! · BCU · CENTRAL PARA VOS · TALLER 3 ENDEUDARSE BIEN{extra}   ·   {NPAG[0]:02d}',
                                      's': 9, 'c': MUTED, 'b': True}])


def chip(s, x, y, w, txt, fill=AMAR, tc=TINTA, size=12, h=0.36):
    c = box(s, x, y, w, h, fill=fill, lw=2, off=0.05)
    tf = c.text_frame; tf.word_wrap = False
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.margin_top = tf.margin_bottom = Inches(0.01)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = txt
    r.font.size = Pt(size); r.font.bold = True; r.font.name = BODY; r.font.color.rgb = tc
    return c


def barra(s, x, y, w_total, frac, label, val, color=AZUL):
    text(s, x, y - 0.02, 3.15, 0.32, [{'t': label, 's': 12.5, 'b': True}])
    box(s, x + 3.2, y, w_total, 0.3, fill=PAPEL2, lw=2, off=0.05, shadow=False)
    if frac > 0:
        f = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x + 3.2), Inches(y), Inches(max(w_total * frac, 0.12)), Inches(0.3))
        f.fill.solid(); f.fill.fore_color.rgb = color; f.line.color.rgb = TINTA; f.line.width = Pt(2); f.shadow.inherit = False
    text(s, x + 3.2 + w_total + 0.12, y - 0.03, 0.9, 0.32, [{'t': str(val), 's': 14, 'b': True, 'f': DISP, 'c': color}])


# ---------------------------------------------------------------- 1 PORTADA
s = slide()
chip(s, 0.55, 0.6, 4.9, 'PIN! · INJU · BCU · CAF  —  CENTRAL PARA VOS', fill=PAPEL2)
text(s, 0.5, 1.35, 12.4, 2.6, [
    {'t': 'ENDEUDARSE', 's': 76, 'f': DISP, 'c': TINTA, 'sa': 0},
    {'t': 'BIEN', 's': 76, 'f': DISP, 'c': ROSA},
])
text(s, 0.55, 4.05, 12, 0.6, [{'t': 'Taller 3 · Decisiones financieras informadas', 's': 22, 'b': True}])
b = box(s, 0.55, 4.8, 7.6, 1.05, fill=AMAR)
tf = b.text_frame; tf.word_wrap = True; tf.margin_left = Inches(0.18); tf.margin_top = Inches(0.12)
p = tf.paragraphs[0]
r = p.add_run(); r.text = 'FORMACIÓN DE FORMADORES · EDICIÓN JUEGO 2026'
r.font.size = Pt(17); r.font.name = DISP; r.font.color.rgb = TINTA
p2 = tf.add_paragraph()
r = p2.add_run(); r.text = 'El taller ahora se juega: 3 máquinas en equipos + tablero en vivo'
r.font.size = Pt(14); r.font.bold = True; r.font.name = BODY; r.font.color.rgb = TINTA
for i, (cx, col) in enumerate([(0.55, AZUL), (2.15, ROSA), (3.75, VERDE)]):
    chip(s, cx, 6.15, 1.45, f'EQUIPO {i+1}', fill=col, tc=BLANCO)
chip(s, 5.35, 6.15, 2.3, 'PROYECTOR EN VIVO', fill=TINTA, tc=AMAR)
footer(s)

# ------------------------------------------------------- 2 QUÉ CAMBIÓ
s = slide(); head(s, 'LA EDICIÓN 2026', 'Qué cambió: el taller ahora se juega')
b = box(s, 0.55, 1.75, 5.9, 4.5, fill=PAPEL2)
text(s, 0.8, 1.95, 5.4, 4.1, [
    {'t': 'ANTES', 's': 18, 'f': DISP, 'c': MUTED, 'sa': 10},
    {'t': '• Slides con casos leídos en voz alta', 'sa': 8},
    {'t': '• Preguntas orales y anotación en pizarra', 'sa': 8},
    {'t': '• Kahoot como quiz aparte', 'sa': 8},
    {'t': '• Los datos del BCU contados, no vividos', 'sa': 8},
    {'t': '• Difícil con 20 participantes y pocas máquinas', 'sa': 8},
])
b = box(s, 6.85, 1.75, 5.9, 4.5, fill=AMAR)
text(s, 7.1, 1.95, 5.4, 4.1, [
    {'t': 'AHORA', 's': 18, 'f': DISP, 'c': TINTA, 'sa': 10},
    {'t': '• El juego "12 Meses": un año en la piel de Joaquín, 10 decisiones', 'b': True, 'sa': 8},
    {'t': '• 3 equipos juegan A LA VEZ, mismos eventos, ranking en vivo', 'b': True, 'sa': 8},
    {'t': '• Los datos del BCU aparecen DENTRO del juego como quizzes', 'b': True, 'sa': 8},
    {'t': '• El proyector es el tablero: toda la sala mira la carrera', 'b': True, 'sa': 8},
    {'t': '• Cada participante se lleva el juego en su celular (QR)', 'b': True, 'sa': 8},
])
text(s, 0.55, 6.45, 12.3, 0.5, [{'segs': [
    {'t': 'El juego, siempre listo en:  ', 's': 14, 'b': True, 'c': TINTA},
    {'t': 'chelabsweb.github.io/endeudarse-bien-stand', 's': 16, 'b': True, 'c': AZUL},
]}])
footer(s)

# ------------------------------------------------------- 3 OBJETIVO (fiel al manual)
s = slide(); head(s, 'PROPÓSITO DEL TALLER (MANUAL PIN! 2025)', 'Lo que el taller tiene que lograr')
objs = [
    ('REFLEXIÓN PRÁCTICA', 'Guiar una reflexión sobre el impacto del endeudamiento en la estabilidad financiera propia.', AZUL),
    ('OPCIONES REALES', 'Identificar las opciones de financiamiento disponibles en Uruguay con casos verosímiles.', VERDE),
    ('HUELLA FINANCIERA', 'Entender dónde queda registrada (BCU y Clearing de Informes) y cómo consultarla gratis.', ROSA),
    ('MODELO PAMY', 'Evaluar un préstamo en 4 pasos: ¿Preciso? ¿Ahorro? ¿Mejores? ¿Y después?', AMAR),
]
for i, (t, d, col) in enumerate(objs):
    x = 0.55 + (i % 2) * 6.3; y = 1.8 + (i // 2) * 2.15
    b = box(s, x, y, 5.95, 1.85, fill=PAPEL2)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(0.22), Inches(1.85))
    bar.fill.solid(); bar.fill.fore_color.rgb = col; bar.line.color.rgb = TINTA; bar.line.width = Pt(2); bar.shadow.inherit = False
    text(s, x + 0.42, y + 0.18, 5.3, 1.5, [
        {'t': t, 's': 16, 'f': DISP, 'sa': 6},
        {'t': d, 's': 13.5},
    ])
text(s, 0.55, 6.35, 12.3, 0.55, [{'t': 'Idea fuerza oficial: un préstamo debe verse como un COMPROMISO DE AHORRO, no como una solución inmediata.', 's': 14.5, 'b': True, 'c': ROJO}])
footer(s)

# ------------------------------------------------------- 4 ESTRUCTURA 90'
s = slide(); head(s, 'ESTRUCTURA · 90 MINUTOS', 'La agenda, con el juego en el centro')
rows = [
    ('5\'',  'Bienvenida y propósito', 'Endeudarse bien: decisiones informadas. Presentar equipos y máquinas.', TINTA),
    ('15\'', 'Parte I · Desafío financiero', 'Rompehielo "100 uruguayos dicen": las 2 preguntas oficiales definen los equipos.', AZUL),
    ('25\'', 'Parte II · La partida "12 Meses"', '3 equipos, mismos eventos, ranking en vivo en el proyector. PAMY y quizzes viven acá.', ROSA),
    ('15\'', 'Parte III · La huella', 'Leer el podio: intereses, marcas. Los dos espejos (BCU/Clearing) y ¿le prestarían a Joaquín?', VERDE),
    ('15\'', 'Parte IV · Decidir consciente', 'Interacción con la IA asesora en rol de Joaquín. Escala 1-7 antes y después.', AMAR),
    ('10\'', 'Cierre + ticket de salida', 'Minuto de oro por equipo + QR "llevate el juego" y consultá tu huella. (+5\' transiciones)', TINTA),
]
y = 1.72
for dur, tit, desc, col in rows:
    b = box(s, 0.55, y, 12.2, 0.76, fill=PAPEL2, off=0.06)
    c = box(s, 0.7, y + 0.14, 0.85, 0.48, fill=col, lw=2, off=0.04)
    tf = c.text_frame; p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = dur; r.font.size = Pt(15); r.font.name = DISP
    r.font.color.rgb = BLANCO if col in (TINTA, AZUL, ROSA, VERDE) else TINTA
    text(s, 1.75, y + 0.07, 3.6, 0.6, [{'t': tit, 's': 14.5, 'f': DISP}], anchor=MSO_ANCHOR.MIDDLE)
    text(s, 5.5, y + 0.07, 7.1, 0.6, [{'t': desc, 's': 12}], anchor=MSO_ANCHOR.MIDDLE)
    y += 0.86
footer(s)

# ------------------------------------------------------- 5 SETUP TÉCNICO
s = slide(); head(s, 'ANTES DE QUE LLEGUE EL GRUPO', 'Setup técnico: 10 minutos y listo')
b = box(s, 0.55, 1.7, 7.5, 4.9, fill=PAPEL2)
text(s, 0.85, 1.92, 7.0, 4.5, [
    {'t': 'CHECKLIST', 's': 15, 'f': DISP, 'c': AZUL, 'sa': 8},
    {'t': '1 · 3 máquinas o tablets con el juego abierto (la URL de abajo). Con abrirlo una vez, queda cacheado.', 'sa': 7, 's': 13.5},
    {'t': '2 · 1 computadora conectada al proyector, también con el juego.', 'sa': 7, 's': 13.5},
    {'t': '3 · Wifi para las 4 máquinas: el modo Sala lo necesita.', 'sa': 7, 's': 13.5},
    {'t': '4 · Elegí un código de sala de 4 letras (ej. MOTO) y anotalo grande en la pizarra.', 'sa': 7, 's': 13.5},
    {'t': '5 · En cada máquina: SALA → código → nombre del equipo (hasta 12 letras).', 'sa': 7, 's': 13.5},
    {'t': '6 · En el proyector: SALA → código → "PROYECTOR: SOLO MIRAR".', 'sa': 7, 's': 13.5},
    {'t': '7 · Desde el proyector se arranca la partida y la revancha. Vos tenés el control.', 'b': True, 'sa': 7, 's': 13.5},
])
b = box(s, 8.35, 1.7, 4.4, 3.0, fill=ROJO)
text(s, 8.6, 1.9, 3.9, 2.6, [
    {'t': 'PLAN B SIN WIFI', 's': 15, 'f': DISP, 'c': BLANCO, 'sa': 8},
    {'t': 'El juego funciona 100% offline en modo normal: cada equipo juega en su máquina y comparan puntajes con el Ranking del día.', 'c': BLANCO, 's': 13, 'b': True},
])
b = box(s, 8.35, 5.0, 4.4, 1.6, fill=AMAR)
text(s, 8.6, 5.18, 3.9, 1.3, [
    {'t': 'TIP DE STAND', 's': 13, 'f': DISP, 'sa': 5},
    {'t': '5 toques en el membrete de la portada abren las estadísticas del día.', 's': 12.5, 'b': True},
])
footer(s)

# ------------------------------------------------------- 6 EL JUEGO EN 30 SEGUNDOS
s = slide(); head(s, 'PARA EL FACILITADOR', 'El juego "12 Meses" en 30 segundos')
text(s, 0.55, 1.65, 12.2, 0.8, [{'segs': [
    {'t': 'Sos Joaquín: sueldo justo, deudas viejas y ganas de una moto. ', 's': 16, 'b': True},
    {'t': 'Un año en 10 decisiones (~3 minutos por partida).', 's': 16, 'b': True, 'c': AZUL},
]}])
hud = [
    ('BILLETERA', 'La plata del mes. Sube y baja con cada decisión.', VERDE),
    ('FONDO', 'El colchón de emergencia. Vale doble en el puntaje.', AZUL),
    ('INTERESES REGALADOS', 'Todo lo pagado de más por financiar. Resta fuerte.', ROJO),
    ('RACHA', '3+ decisiones buenas seguidas = bonus "cabeza fría".', ROSA),
    ('HUELLA', '5 puntos. Cada marca (Clearing) queda 5 años y resta $8.000.', TINTA),
]
y = 2.55
for t, d, col in hud:
    chip(s, 0.55, y, 3.1, t, fill=col, tc=BLANCO if col != AMAR else TINTA, size=11.5)
    text(s, 3.85, y - 0.04, 8.9, 0.45, [{'t': d, 's': 13}], anchor=MSO_ANCHOR.MIDDLE)
    y += 0.55
text(s, 0.55, 5.5, 12.2, 1.4, [
    {'t': 'Al final: constancia de huella fotografiable, puntaje desglosado en recibo, 8 medallas rioplatenses y ranking del día.', 's': 14, 'b': True, 'sa': 6},
    {'t': 'También existe el modo Duelo (2 jugadores pasa-la-tablet) para el stand.', 's': 12.5, 'c': MUTED},
])
footer(s)

# ------------------------------------------------------- 7 MODO SALA PASO A PASO
s = slide(); head(s, 'LA MECÁNICA DEL TALLER', 'Modo Sala: 3 máquinas, mismos eventos')
pasos = [
    ('1', 'CÓDIGO', 'Todas las máquinas ponen el MISMO código de 4 letras. Eso garantiza los mismos eventos para todos: la comparación es justa.'),
    ('2', 'EQUIPOS', 'Cada máquina escribe su nombre de equipo (hasta 12 letras). Se ven entre sí en el lobby.'),
    ('3', 'ARRANQUE', 'Desde el proyector: ¡Arrancar! Cuenta regresiva 3-2-1 en todas las pantallas a la vez.'),
    ('4', 'LA PARTIDA', 'Cada equipo decide a su ritmo con timer de 45 segundos por decisión. Ranking en vivo arriba de cada pantalla.'),
    ('5', 'EL PODIO', 'Al terminar: podio con corona, patrimonio, intereses regalados, categoría BCU y marcas de cada equipo.'),
    ('6', 'REVANCHA', 'Desde el proyector. El sorteo cambia: eventos nuevos garantizados.'),
]
for i, (n, t, d) in enumerate(pasos):
    x = 0.55 + (i % 3) * 4.18; y = 1.8 + (i // 3) * 2.4
    b = box(s, x, y, 3.9, 2.1, fill=PAPEL2)
    c = box(s, x + 0.18, y + 0.18, 0.55, 0.55, fill=AMAR, lw=2, off=0.05)
    tf = c.text_frame; p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = n; r.font.size = Pt(18); r.font.name = DISP; r.font.color.rgb = TINTA
    text(s, x + 0.9, y + 0.22, 2.9, 0.5, [{'t': t, 's': 15, 'f': DISP}])
    text(s, x + 0.2, y + 0.85, 3.5, 1.2, [{'t': d, 's': 11.8}])
footer(s)

# ------------------------------------------------------- 8 ROMPEHIELO
s = slide(); head(s, 'PARTE I · ROMPEHIELO (15\')', 'Desafío financiero: ¿cuántos ya debemos?')
b = box(s, 0.55, 1.75, 7.4, 2.5, fill=PAPEL2)
text(s, 0.85, 1.95, 6.9, 2.2, [
    {'t': 'LA PREGUNTA DE ARRANQUE', 's': 14, 'f': DISP, 'c': AZUL, 'sa': 8},
    {'t': 'En Uruguay hay unos 600.000 jóvenes de 18 a 30 años. ¿Cuántos creen que ya pidieron un préstamo a un banco o financiera?', 's': 15, 'b': True, 'sa': 8},
    {'t': 'Cada equipo grita su número. El que más se acerca elige nombre y máquina primero.', 's': 13, 'c': MUTED},
])
b = box(s, 8.25, 1.75, 4.5, 2.5, fill=TINTA)
text(s, 8.45, 2.0, 4.1, 2.1, [
    {'t': '297.329', 's': 44, 'f': DISP, 'c': AMAR, 'al': PP_ALIGN.CENTER, 'sa': 4},
    {'t': '1 DE CADA 2 JÓVENES', 's': 15, 'f': DISP, 'c': BLANCO, 'al': PP_ALIGN.CENTER, 'sa': 4},
    {'t': 'registrados en la Central de Riesgos del BCU', 's': 11.5, 'c': BLANCO, 'al': PP_ALIGN.CENTER, 'b': True},
])
text(s, 0.55, 4.5, 12.2, 1.9, [
    {'t': 'Cómo facilitarlo (manual Pin!):', 's': 14, 'b': True, 'c': AZUL, 'sa': 5},
    {'t': '• "Si fuéramos como el promedio de Uruguay, un equipo entero estaría endeudado y otro no."', 's': 13, 'sa': 4},
    {'t': '• Aclarar: estar registrado no significa no estar pagando. Preguntar: ¿les sorprende?', 's': 13, 'sa': 4},
    {'t': '• Conectar: "Todo lo que vimos acá lo van a VIVIR ahora en el juego."', 's': 13, 'b': True},
])
footer(s)

# ------------------------------------------------------- 9 PREGUNTA 1 MOTIVOS
s = slide(); head(s, 'PARTE I · PREGUNTA 1 (ESTILO "100 URUGUAYOS DICEN")', '¿Por qué se endeudan los hogares?')
text(s, 0.55, 1.6, 12.2, 0.45, [{'t': 'Los equipos se alternan; 30 segundos por respuesta y responde solo el vocero. Puntos = cuántos uruguayos están en cada situación.', 's': 12.5, 'b': True, 'c': MUTED}])
datos = [
    ('Gastos corrientes (comida, ropa, hogar)', 25, ROJO),
    ('Gastos mensuales (UTE, OSE, alquiler)', 18, AZUL),
    ('Cancelar una deuda previa', 17, ROSA),
    ('Bienes duraderos (auto, muebles)', 15, VERDE),
    ('Arreglo de la vivienda', 12, TINTA),
    ('Compra de vivienda', 5, MUTED),
    ('Inversión en un negocio', 3, MUTED),
    ('Vacaciones', 2, MUTED),
]
y = 2.25
for label, val, col in datos:
    barra(s, 0.7, y, 6.6, val / 25.0, label, val, col)
    y += 0.47
text(s, 0.55, 6.2, 12.2, 0.7, [{'segs': [
    {'t': 'El mensaje: ', 's': 14, 'b': True},
    {'t': 'la mayoría se endeuda para llegar a fin de mes, no por gustos. Si la deuda es para gastos corrientes, lo que se necesita es más ingresos o menos gastos — no deuda.', 's': 14, 'b': True, 'c': ROJO},
]}])
footer(s)

# ------------------------------------------------------- 10 PREGUNTA 2 CATEGORÍAS
s = slide(); head(s, 'PARTE I · PREGUNTA 2', 'La nota del BCU: ¿qué tan bien pagamos?')
cats = [
    ('1', 'Pago fuerte: al día o atraso < 10 días', 50, VERDE),
    ('2', 'Pago adecuado: atraso 10–60 días', 7, AZUL),
    ('3', 'Pago comprometido: 60–180 días', 3, AMAR),
    ('4', 'Varias deudas, una irrecuperable (>180)', 10, ROSA),
    ('5', 'TODAS las deudas irrecuperables', 30, ROJO),
]
text(s, 0.55, 1.62, 12.2, 0.4, [{'t': 'De cada 100 jóvenes deudores, ¿cuántos hay en cada categoría? (Central de Riesgos, BCU)', 's': 13, 'b': True, 'c': MUTED}])
y = 2.2
for n, label, val, col in cats:
    barra(s, 0.7, y, 6.2, val / 50.0, f'CAT {n} · {label}', val, col)
    y += 0.52
b = box(s, 0.55, 5.05, 12.2, 1.35, fill=ROJO)
text(s, 0.85, 5.22, 11.7, 1.05, [
    {'t': '1 DE CADA 3 JÓVENES DEUDORES YA TIENE TODO INCOBRABLE', 's': 19, 'f': DISP, 'c': BLANCO, 'sa': 4},
    {'t': 'La mitad paga impecable — y un tercio arrancó su vida financiera con la huella quemada 5 años. Esa diferencia se decide en jugadas como las del juego.', 's': 13, 'b': True, 'c': BLANCO},
])
footer(s)

# ------------------------------------------------------- 11 LA PARTIDA: FORMATO EQUIPOS
s = slide(); head(s, 'PARTE II · LA PARTIDA (25\')', 'Cómo se juega con ~20 y 3 máquinas')
b = box(s, 0.55, 1.75, 6.0, 4.6, fill=PAPEL2)
text(s, 0.85, 1.95, 5.5, 4.2, [
    {'t': 'FORMATO', 's': 15, 'f': DISP, 'c': AZUL, 'sa': 8},
    {'t': '• 3 equipos de ~6-7 alrededor de cada máquina.', 'sa': 7, 's': 13.5},
    {'t': '• Cada decisión se debate en el equipo: ahí está el aprendizaje.', 'sa': 7, 's': 13.5, 'b': True},
    {'t': '• Timer de 45 segundos por decisión: el debate es intenso pero corto.', 'sa': 7, 's': 13.5},
    {'t': '• El ranking en vivo mete presión sana: se ve quién va primero, mes a mes.', 'sa': 7, 's': 13.5},
    {'t': '• Una partida dura ~10 minutos. Da tiempo a revancha con eventos nuevos.', 'sa': 7, 's': 13.5},
])
roles = [
    ('VOCERO/A', 'El único que toca la pantalla. Rota cada 3 meses del juego.', AMAR, TINTA),
    ('CONTADOR/A', 'Obligado a hacer la cuenta EN VOZ ALTA: cuota × cuotas, antes de decidir.', AZUL, BLANCO),
    ('ABOGADO/A DEL DIABLO', 'Tiene que defender la opción tentadora. Si nadie tienta, no hay mérito en resistir.', ROSA, BLANCO),
]
y = 1.75
for t, d, col, tc in roles:
    b = box(s, 6.95, y, 5.8, 1.4, fill=col)
    text(s, 7.2, y + 0.15, 5.3, 1.1, [
        {'t': t, 's': 14, 'f': DISP, 'c': tc, 'sa': 4},
        {'t': d, 's': 12.5, 'b': True, 'c': tc},
    ])
    y += 1.62
footer(s)

# ------------------------------------------------------- 12 EL AÑO DE JOAQUÍN
s = slide(); head(s, 'PARTE II · EL RECORRIDO', 'El año de Joaquín: 10 decisiones')
meses = [
    ('M1', 'La factura de UTE atrasada', TINTA, 'FIJO'),
    ('M2', 'La tarjeta clavada en $10.000', TINTA, 'FIJO'),
    ('M3', 'Evento sorteado', AZUL, 'SORTEO'),
    ('M4', 'CHEQUEO RÁPIDO (quiz con datos reales)', ROSA, 'QUIZ'),
    ('M5', '¡Chau préstamo del auto!', TINTA, 'FIJO'),
    ('M6', 'Evento sorteado', AZUL, 'SORTEO'),
    ('M7', 'LA BOCHA: la vida no avisa', ROJO, 'SHOCK'),
    ('M8', 'Imprevisto (heladera o celular)', ROJO, 'SORTEO'),
    ('M9', 'La moto. El plan de siempre.', TINTA, 'FIJO'),
    ('M12', 'Diciembre: cae el aguinaldo', TINTA, 'FIJO'),
]
y = 1.78
for i, (m, t, col, tag) in enumerate(meses):
    x = 0.55 + (i % 2) * 6.25; yy = y + (i // 2) * 0.95
    b = box(s, x, yy, 5.95, 0.8, fill=PAPEL2, off=0.06)
    c = box(s, x + 0.12, yy + 0.14, 0.72, 0.52, fill=col, lw=2, off=0.04)
    tf = c.text_frame; p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = m; r.font.size = Pt(13); r.font.name = DISP; r.font.color.rgb = BLANCO if col != AMAR else TINTA
    text(s, x + 1.0, yy + 0.09, 3.9, 0.62, [{'t': t, 's': 12.3, 'b': True}], anchor=MSO_ANCHOR.MIDDLE)
    chip(s, x + 4.95, yy + 0.22, 0.88, tag, fill=PAPEL, tc=MUTED, size=8.5, h=0.3)
text(s, 0.55, 6.6, 12.2, 0.4, [{'t': 'Los sorteos y el quiz cambian en cada partida: la revancha nunca repite.', 's': 12.5, 'b': True, 'c': MUTED}])
footer(s)

# ------------------------------------------------------- 13 QUÉ ENSEÑA CADA MES FIJO
s = slide(); head(s, 'PARTE II · LOS 5 MOMENTOS FIJOS', 'Qué enseña cada mes (y cómo reforzarlo)')
lecciones = [
    ('M1 · UTE', 'La factura "inocente" va al Clearing y marca la huella 5 años. Deuda para tapar deuda: se muda y engorda.', TINTA),
    ('M2 · TARJETA', 'El pago mínimo es la deuda eterna: pagás y el saldo ni se entera. A la tarjeta se le gana con plan.', ROSA),
    ('M5 · SE LIBERA PLATA', 'Cobrate primero: débito automático al fondo. La plata sin nombre se gasta sola.', VERDE),
    ('M9 · LA MOTO', 'PAMY en acción. Con entrega ahorrada pedís menos: cada peso de entrega son dos que no regalás.', AZUL),
    ('M12 · AGUINALDO', 'No es premio: es la mejor herramienta financiera del año. El 50/50 decidido antes también es un plan.', AMAR),
]
y = 1.78
for t, d, col in lecciones:
    b = box(s, 0.55, y, 12.2, 0.85, fill=PAPEL2, off=0.06)
    c = box(s, 0.7, y + 0.14, 1.85, 0.56, fill=col, lw=2, off=0.04)
    tf = c.text_frame; p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = t; r.font.size = Pt(11.5); r.font.name = DISP
    r.font.color.rgb = TINTA if col in (AMAR,) else BLANCO
    text(s, 2.75, y + 0.1, 9.85, 0.68, [{'t': d, 's': 12.8, 'b': True}], anchor=MSO_ANCHOR.MIDDLE)
    y += 0.98
footer(s)

# ------------------------------------------------------- 14 LOS QUIZZES
s = slide(); head(s, 'PARTE II · LOS DATOS, DENTRO DEL JUEGO', 'Chequeos rápidos: 5 quizzes con datos reales')
text(s, 0.55, 1.62, 12.2, 0.45, [{'t': 'En el Mes 4 SIEMPRE cae uno, sorteado. Respuesta correcta: +$2.000 y camino a la medalla "Ojo de Halcón".', 's': 13, 'b': True, 'c': MUTED}])
quizzes = [
    ('¿Dónde aparece la UTE impaga?', 'En el Clearing (no en el BCU). Los dos espejos.'),
    ('¿Cuántos jóvenes ya pidieron préstamo?', '297.329 de 600.000: la mitad.'),
    ('¿Para qué nos endeudamos?', 'Motivo nº1: los gastos de todos los días (25 de 100).'),
    ('La temida categoría 5', '1 de cada 3 jóvenes deudores tiene todo incobrable.'),
    ('¿Cuántas cuotas son tuyas?', 'De 36 cuotas de $3.999: 20 para vos, 16 para la financiera.'),
]
y = 2.25
for t, d in quizzes:
    b = box(s, 0.55, y, 12.2, 0.72, fill=PAPEL2, off=0.06)
    text(s, 0.8, y + 0.05, 5.3, 0.6, [{'t': t, 's': 13, 'f': DISP}], anchor=MSO_ANCHOR.MIDDLE)
    text(s, 6.3, y + 0.05, 6.3, 0.6, [{'t': d, 's': 12.5, 'b': True, 'c': AZUL}], anchor=MSO_ANCHOR.MIDDLE)
    y += 0.84
text(s, 0.55, 6.55, 12.2, 0.45, [{'t': 'Consejo: cuando cae el quiz, frená la sala 60 segundos y comentá el dato con todo el grupo.', 's': 13, 'b': True, 'c': ROJO}])
footer(s)

# ------------------------------------------------------- 15 DISPARADORES
s = slide(); head(s, 'PARTE II · TU ROL DURANTE LA PARTIDA', 'Disparadores para frenar y preguntar')
disp = [
    ('EN CUALQUIER DECISIÓN', '"¿Por qué eligieron eso? ¿Quién estaba en contra?" — que el desacuerdo se escuche.'),
    ('ANTE CUOTAS', '"¿Quién hizo la cuenta? ¿Cuánto da cuota × cuotas?" — el contador del equipo responde.'),
    ('ANTE UN "YA MISMO"', '"¿Qué pasa si esperan un mes?" — un préstamo es una decisión de tiempo.'),
    ('ANTE UNA MARCA', '"¿Quién ve esa marca y por cuánto tiempo?" — el banco mira los dos espejos, 5 años.'),
    ('ANTE LA MOTO', '"¿El delivery paga la moto… si llueve dos semanas?" — deuda que genera ingreso vs. margen.'),
    ('EN EL FEEDBACK', 'Leé "La posta" en voz alta cuando un equipo se clave: es la lección en una frase.'),
]
for i, (t, d) in enumerate(disp):
    x = 0.55 + (i % 2) * 6.25; y = 1.8 + (i // 2) * 1.6
    b = box(s, x, y, 5.95, 1.35, fill=PAPEL2)
    text(s, x + 0.22, y + 0.13, 5.5, 1.1, [
        {'t': t, 's': 12.5, 'f': DISP, 'c': AZUL, 'sa': 4},
        {'t': d, 's': 12.3, 'b': True},
    ])
footer(s)

# ------------------------------------------------------- 16 PAMY
s = slide(); head(s, 'EL ENTREGABLE CONCEPTUAL', 'PAMY: la lista de cotejo antes de firmar')
pamy = [
    ('P', 'PRECISO', '¿Lo preciso de verdad… y lo preciso YA? Un préstamo es una decisión de tiempo: ¿qué pasa si espero?', AMAR, TINTA),
    ('A', 'AHORRO', 'Tomar un préstamo ES ahorrar (después y con intereses). Si puedo pagar la cuota, ¿por qué no ahorro antes y soy mi propio prestamista?', VERDE, BLANCO),
    ('M', 'MEJORES', 'Comparar TODAS las opciones por costo total: bancos (ojo BROU), financieras, casas de crédito, tarjetas, cooperativas. La TEA y la cuenta cuota × cuotas.', AZUL, BLANCO),
    ('Y', 'Y DESPUÉS', '¿De dónde sale la cuota? ¿Qué gasto comprimo? ¿Cuál es el plan para sostener el ahorro y cumplirlo?', ROSA, BLANCO),
]
for i, (l, t, d, col, tc) in enumerate(pamy):
    x = 0.55 + (i % 2) * 6.3; y = 1.78 + (i // 2) * 2.35
    b = box(s, x, y, 5.95, 2.05, fill=col)
    text(s, x + 0.25, y + 0.16, 1.0, 1.0, [{'t': l, 's': 40, 'f': DISP, 'c': tc}])
    text(s, x + 1.35, y + 0.2, 4.45, 1.75, [
        {'t': t, 's': 16, 'f': DISP, 'c': tc, 'sa': 5},
        {'t': d, 's': 11.8, 'b': True, 'c': tc},
    ])
footer(s)

# ------------------------------------------------------- 17 LA CUENTA QUE SALVA
s = slide(); head(s, 'EL REFLEJO QUE HAY QUE INSTALAR', 'La cuenta que salva: cuota × cuotas')
ej = [
    ('$15.000 en 6 cuotas de $2.999', '6 × $2.999 = $17.994', '5 cuotas para vos · 1 entera para la financiera', VERDE),
    ('$80.000 en 36 cuotas de $3.999', '36 × $3.999 = $143.964', '20 cuotas para vos · 16 enteras para la financiera', ROJO),
]
y = 1.85
for t, cta, rep, col in ej:
    b = box(s, 0.55, y, 12.2, 1.75, fill=PAPEL2)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.55), Inches(y), Inches(0.22), Inches(1.75))
    bar.fill.solid(); bar.fill.fore_color.rgb = col; bar.line.color.rgb = TINTA; bar.line.width = Pt(2); bar.shadow.inherit = False
    text(s, 1.0, y + 0.15, 11.5, 1.5, [
        {'t': t, 's': 15, 'b': True, 'sa': 4},
        {'t': cta, 's': 22, 'f': DISP, 'c': col, 'sa': 4},
        {'t': rep, 's': 14, 'b': True},
    ])
    y += 2.05
text(s, 0.55, 6.0, 12.2, 0.9, [
    {'t': 'La cuota chica esconde el total gigante. Antes de firmar: total a pagar vs. precio contado — y pedirlo POR ESCRITO.', 's': 15, 'b': True, 'c': ROJO},
])
footer(s)

# ------------------------------------------------------- 18 LOS DOS ESPEJOS
s = slide(); head(s, 'PARTE III · LA HUELLA (15\')', 'Los dos espejos: BCU y Clearing')
b = box(s, 0.55, 1.75, 6.0, 4.3, fill=AZUL)
text(s, 0.85, 1.95, 5.5, 3.9, [
    {'t': 'BCU · CENTRAL DE RIESGOS', 's': 15, 'f': DISP, 'c': BLANCO, 'sa': 8},
    {'t': '• Solo sistema financiero regulado: bancos, financieras, cooperativas.', 'c': BLANCO, 'sa': 6, 's': 12.8, 'b': True},
    {'t': '• Tu nota del 1 al 5 según días de atraso.', 'c': BLANCO, 'sa': 6, 's': 12.8, 'b': True},
    {'t': '• No borra la información, aunque canceles la deuda.', 'c': BLANCO, 'sa': 6, 's': 12.8, 'b': True},
    {'t': '• Gratis: consultadeuda.bcu.gub.uy', 'c': AMAR, 'sa': 6, 's': 13.5, 'b': True},
])
b = box(s, 6.85, 1.75, 5.9, 4.3, fill=ROSA)
text(s, 7.15, 1.95, 5.4, 3.9, [
    {'t': 'CLEARING DE INFORMES', 's': 15, 'f': DISP, 'c': BLANCO, 'sa': 8},
    {'t': '• Servicios (UTE, OSE), comercios, cheques rechazados, refinanciaciones.', 'c': BLANCO, 'sa': 6, 's': 12.8, 'b': True},
    {'t': '• Muestra QUIÉN te consultó en los últimos 6 meses.', 'c': BLANCO, 'sa': 6, 's': 12.8, 'b': True},
    {'t': '• Las marcas duran 5 años desde el registro.', 'c': BLANCO, 'sa': 6, 's': 12.8, 'b': True},
    {'t': '• clearing.com.uy/personas', 'c': AMAR, 'sa': 6, 's': 13.5, 'b': True},
])
text(s, 0.55, 6.25, 12.2, 0.6, [{'t': 'EL BANCO MIRA LOS DOS. Por eso en el juego la UTE impaga también marca la huella.', 's': 16, 'f': DISP, 'c': TINTA, 'al': PP_ALIGN.CENTER}])
footer(s)

# ------------------------------------------------------- 19 PODIO + JOAQUÍN
s = slide(); head(s, 'PARTE III · DEL PODIO AL CASO', 'Leer el podio… y decidir: ¿le prestarían?')
b = box(s, 0.55, 1.75, 6.0, 4.5, fill=PAPEL2)
text(s, 0.85, 1.95, 5.5, 4.1, [
    {'t': 'EL PODIO COMO CIERRE', 's': 14, 'f': DISP, 'c': AZUL, 'sa': 7},
    {'t': '• Intereses regalados = plata quemada: ¿cuánto regaló cada equipo?', 'sa': 6, 's': 13},
    {'t': '• Marcas = 5 años de huella: ¿cuáles se podían evitar?', 'sa': 6, 's': 13},
    {'t': '• Cada equipo cuenta su PEOR decisión y qué haría distinto (minuto de oro por equipo).', 'sa': 6, 's': 13, 'b': True},
    {'t': '• La categoría BCU del podio conecta directo con la pregunta 2 del rompehielo.', 'sa': 6, 's': 13},
])
b = box(s, 6.85, 1.75, 5.9, 4.5, fill=PAPEL2)
text(s, 7.15, 1.95, 5.4, 4.1, [
    {'t': '¿LE PRESTARÍAN A JOAQUÍN?', 's': 14, 'f': DISP, 'c': ROSA, 'sa': 7},
    {'t': 'Pide $60.000 para la moto (delivery: +$7.000/mes).', 'sa': 6, 's': 13, 'b': True},
    {'t': 'El BCU dice: tarjeta y préstamo al día → categoría 1. Parece que sí…', 'sa': 6, 's': 13},
    {'t': 'El Clearing dice: UTE 60 días, refinanciación, cheque rechazado, 6 consultas. Mmm…', 'sa': 6, 's': 13},
    {'t': 'Debate y votación: ¿pesa más la nota del BCU o el Clearing? ¿Importa que la moto genere ingresos?', 'sa': 6, 's': 13, 'b': True},
])
footer(s)

# ------------------------------------------------------- 20 IA
s = slide(); head(s, 'PARTE IV · DECIDIR CONSCIENTE (15\')', 'La IA asesora: introspección antes de firmar')
b = box(s, 0.55, 1.75, 6.0, 4.5, fill=PAPEL2)
text(s, 0.85, 1.95, 5.5, 4.1, [
    {'t': 'LA DINÁMICA', 's': 14, 'f': DISP, 'c': AZUL, 'sa': 7},
    {'t': '1 · Antes: cada uno anota su decisión (¿tomarían el préstamo?) y su convicción del 1 al 7.', 'sa': 6, 's': 13},
    {'t': '2 · En rol de Joaquín, conversan con la IA asesora (mini-web del stand).', 'sa': 6, 's': 13},
    {'t': '3 · Después: ¿mantienen la decisión? ¿Cambió el 1-7? ¿Qué apareció que no habían pensado?', 'sa': 6, 's': 13, 'b': True},
])
b = box(s, 6.85, 1.75, 5.9, 4.5, fill=TINTA)
text(s, 7.15, 1.95, 5.4, 4.1, [
    {'t': 'LO QUE PREGUNTA LA IA', 's': 14, 'f': DISP, 'c': AMAR, 'sa': 7},
    {'t': '"¿Por qué necesitás este préstamo?"', 'c': BLANCO, 'sa': 5, 's': 13, 'b': True},
    {'t': '"¿Cómo vas a cubrir las cuotas?"', 'c': BLANCO, 'sa': 5, 's': 13, 'b': True},
    {'t': '"¿Y si surge un imprevisto mientras pagás?"', 'c': BLANCO, 'sa': 5, 's': 13, 'b': True},
    {'t': '"Imaginate tu vida en un año con esta decisión."', 'c': BLANCO, 'sa': 5, 's': 13, 'b': True},
    {'t': 'La IA no juzga ni recomienda: guía la reflexión. Ese es el punto.', 'c': AMAR, 'sa': 5, 's': 12.5, 'b': True},
])
footer(s)

# ------------------------------------------------------- 21 CIERRE
s = slide(); head(s, 'CIERRE (10\')', 'Minuto de oro: decirlo es creerlo')
text(s, 0.55, 1.75, 12.2, 1.6, [
    {'t': 'Cada participante piensa UNA cosa del taller que no quiere olvidar… y se la dice a alguien.', 's': 17, 'b': True, 'sa': 6},
    {'t': 'Verbalizar el aprendizaje lo consolida (efecto "decirlo es creerlo", manual Pin!). Con equipos: un minuto de oro por equipo, a partir de su partida.', 's': 13.5, 'c': MUTED},
])
b = box(s, 0.55, 3.4, 12.2, 1.7, fill=AMAR)
text(s, 0.9, 3.62, 11.6, 1.3, [
    {'t': 'LA IDEA FUERZA', 's': 14, 'f': DISP, 'sa': 5},
    {'t': '"Pedir prestado es ahorrar: un préstamo es un compromiso de ahorro — para vos y para pagarle los intereses a quien te prestó — no una solución inmediata."', 's': 17, 'f': DISP},
])
text(s, 0.55, 5.4, 12.2, 1.2, [
    {'t': 'Y la huella queda: cada decisión del juego —y de la vida— construye la reputación financiera que abre o cierra puertas 5 años.', 's': 14.5, 'b': True},
])
footer(s)

# ------------------------------------------------------- 22 TICKET DE SALIDA
s = slide(); head(s, 'TICKET DE SALIDA', 'Se van con el juego en el bolsillo')
qr1, qr2 = '/tmp/qr_juego.png', '/tmp/qr_consulta.png'
b = box(s, 0.55, 1.8, 6.0, 4.4, fill=PAPEL2)
if os.path.exists(qr1):
    s.shapes.add_picture(qr1, Inches(0.95), Inches(2.15), Inches(2.2), Inches(2.2))
text(s, 3.35, 2.3, 3.0, 2.4, [
    {'t': 'LLEVATE EL JUEGO', 's': 15, 'f': DISP, 'c': AZUL, 'sa': 6},
    {'t': 'El QR está en la constancia final de cada partida. Abierto una vez, funciona sin internet.', 's': 12.5, 'b': True},
])
text(s, 0.95, 4.6, 5.2, 1.4, [{'t': 'chelabsweb.github.io/endeudarse-bien-stand', 's': 13, 'b': True, 'c': AZUL}])
b = box(s, 6.85, 1.8, 5.9, 4.4, fill=PAPEL2)
if os.path.exists(qr2):
    s.shapes.add_picture(qr2, Inches(7.25), Inches(2.15), Inches(2.2), Inches(2.2))
text(s, 9.65, 2.3, 2.9, 2.4, [
    {'t': 'TU HUELLA REAL, GRATIS', 's': 15, 'f': DISP, 'c': ROSA, 'sa': 6},
    {'t': 'Que cada uno consulte su huella de verdad al llegar a casa.', 's': 12.5, 'b': True},
])
text(s, 7.25, 4.6, 5.2, 1.4, [
    {'t': 'consultadeuda.bcu.gub.uy', 's': 13, 'b': True, 'c': ROSA, 'sa': 3},
    {'t': '+ Tarjeta takeaway impresa (4 por hoja A4) con las reglas de oro.', 's': 12, 'b': True, 'c': MUTED},
])
footer(s)

# ------------------------------------------------------- 23 FICHA TÉCNICA
s = slide(); head(s, 'ANEXO', 'Ficha técnica y solución de problemas')
text(s, 0.55, 1.75, 12.2, 4.8, [
    {'t': 'EL JUEGO', 's': 14, 'f': DISP, 'c': AZUL, 'sa': 5},
    {'t': '• URL: chelabsweb.github.io/endeudarse-bien-stand  ·  Un solo archivo HTML, PWA offline, cero instalación.', 'sa': 4, 's': 12.5},
    {'t': '• Modos: normal (1 jugador), Duelo (2, pasa-la-tablet), Sala (varias máquinas + proyector, requiere internet).', 'sa': 4, 's': 12.5},
    {'t': '• Estadísticas del día: 5 toques en el membrete de la portada. Ranking del día: se limpia solo cada día.', 'sa': 10, 's': 12.5},
    {'t': 'SI ALGO FALLA', 's': 14, 'f': DISP, 'c': ROJO, 'sa': 5},
    {'t': '• No conecta la sala → revisar wifi; si no hay, Plan B: modo normal + comparar en el Ranking del día.', 'sa': 4, 's': 12.5},
    {'t': '• Un equipo se desconecta a mitad de partida → sigue jugando offline; su resultado se canta a mano en el cierre.', 'sa': 4, 's': 12.5},
    {'t': '• La pantalla quedó dormida → tocar y "¡Sigo acá!". En modo sala el timer de inactividad está desactivado.', 'sa': 10, 's': 12.5},
    {'t': 'MATERIALES DEL KIT', 's': 14, 'f': DISP, 'c': VERDE, 'sa': 5},
    {'t': '• Este mazo · Guía del facilitador (PDF) · Tarjetas takeaway · Prompt de la IA asesora · Manual Pin! 2025 (marco oficial).', 'sa': 4, 's': 12.5},
    {'t': '• Repo: github.com/ChelabsWeb/endeudarse-bien-stand — esta presentación se regenera con gen_formadores_pptx.py.', 'sa': 4, 's': 12.5},
])
footer(s)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Formacion_de_Formadores_Endeudarse_Bien_2026.pptx')
prs.save(out)
print('OK →', out, f'({NPAG[0]} slides)')
