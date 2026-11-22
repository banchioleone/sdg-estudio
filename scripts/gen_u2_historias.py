#!/usr/bin/env python3
"""Historias (modo stories) para U2 · Clases 4.b y 6–14.

Escribe sólo el campo `historias` de cada content/u2/claseNN.json; la teoría
queda intacta. Los números salen de la teoría de cada clase (y del material
citado allí); los gráficos son redibujos propios con esos datos o esquemas
rotulados como tales.
"""
import json, math
from pathlib import Path
from html import escape as E

ROOT = Path(__file__).resolve().parents[1]
U2 = ROOT / 'content' / 'u2'
BL, OR, GR, GD, GN, YL = '#8cb4d6', '#e25b16', '#b7c0c8', '#5a6570', '#7cc49a', '#e2c46b'

def n(x, d=1):
    s = f'{x:.{d}f}'.replace('.', ',')
    return s.replace('-', '−')

# ---------------------------------------------------------------- SVG helpers
def svg_open(h, label):
    return [f'<svg viewBox="0 0 280 {h}" width="100%" height="{h}" role="img" aria-label="{E(label)}">']

def txt(x, y, s, size=8, fill=GR, anchor='start', bold=False):
    b = ' font-weight="700"' if bold else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{b}>{E(str(s))}</text>'

def line_chart(series, labels=None, title='', note='', h=150, yr=None, marks=(), band=None, hlines=(), every=1):
    """series: (name, ys, color, dashed). marks: (i, v, text, color). band: (lo, hi, color)."""
    vals = [v for _, ys, _, _ in series for v in ys if v is not None]
    vals += [m[1] for m in marks] + [hl[0] for hl in hlines]
    if band: vals += [band[0], band[1]]
    lo, hi = yr or (min(vals), max(vals))
    pad = (hi - lo) * .1 or 1
    lo, hi = lo - pad, hi + pad
    N = max(len(ys) for _, ys, _, _ in series)
    x0, x1, y0, y1 = 36, 266, 26, h - 34
    X = lambda i: x0 + i * (x1 - x0) / max(1, N - 1)
    Y = lambda v: y1 - (v - lo) * (y1 - y0) / (hi - lo)
    s = svg_open(h, title)
    if title: s.append(txt(8, 13, title, 9, BL, bold=True))
    if band:
        s.append(f'<rect x="{x0}" y="{Y(band[1]):.1f}" width="{x1-x0}" height="{Y(band[0])-Y(band[1]):.1f}" fill="{band[2]}" opacity=".14"/>')
    raw = (hi - lo) / 4; mag = 10 ** math.floor(math.log10(raw))
    step = min((m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw))
    dec = max(0, -int(math.floor(math.log10(step) + 1e-9))) if step < 1 else 0
    if step < 1 and round(step / 10 ** -dec, 6) % 1: dec += 1
    v = math.ceil(lo / step) * step
    while v <= hi + 1e-9:
        s.append(f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x1}" y2="{Y(v):.1f}" stroke="{GD}" stroke-width=".5"/>')
        s.append(txt(x0 - 4, Y(v) + 3, n(v, dec), 7, GR, 'end'))
        v += step
    for v, col, lab in hlines:
        s.append(f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x1}" y2="{Y(v):.1f}" stroke="{col}" stroke-width="1.2" stroke-dasharray="5 3"/>')
        if lab: s.append(txt(x1, Y(v) - 3, lab, 7, col, 'end'))
    for name, ys, col, dashed in series:
        pts = ' '.join(f'{X(i):.1f},{Y(v):.1f}' for i, v in enumerate(ys) if v is not None)
        da = ' stroke-dasharray="4 3"' if dashed else ''
        s.append(f'<polyline fill="none" stroke="{col}" stroke-width="1.8"{da} points="{pts}"/>')
        for i, v in enumerate(ys):
            if v is not None and (not dashed or N <= 13):
                s.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="2.3" fill="{col}"/>')
    for mk in marks:
        i, v, t, col = mk[:4]; dy = mk[4] if len(mk) > 4 else -6
        s.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="4.2" fill="none" stroke="{col}" stroke-width="1.8"/>')
        anchor = 'end' if X(i) > 210 else 'start'
        dx = -7 if anchor == 'end' else 7
        s.append(txt(X(i) + dx, Y(v) + dy, t, 8.5, col, anchor, True))
    if labels:
        for i, lab in enumerate(labels):
            if i % every == 0 or i == len(labels) - 1:
                s.append(txt(X(i), y1 + 12, lab, 7, GR, 'middle'))
    lx = 8
    for name, _, col, dashed in series:
        if not name: continue
        s.append(f'<line x1="{lx}" y1="{h-9}" x2="{lx+12}" y2="{h-9}" stroke="{col}" stroke-width="2"' + (' stroke-dasharray="3 2"' if dashed else '') + '/>')
        s.append(txt(lx + 15, h - 6, name, 7.5, col))
        lx += 22 + 4.6 * len(name)
    if note: s.append(txt(272, h - 6, note, 6.5, GR, 'end'))
    s.append('</svg>')
    return ''.join(s)

def bars(items, title='', h=140, ref=None, fmt=lambda v: n(v, 1), yr=None, note=''):
    """items: (label, value, color). ref: (value, label)."""
    vals = [v for _, v, _ in items] + ([ref[0]] if ref else [])
    lo = 0 if yr is None else yr[0]
    hi = (max(vals) * 1.15) if yr is None else yr[1]
    x0, x1, y0, y1 = 12, 268, 30, h - 30
    Y = lambda v: y1 - (v - lo) * (y1 - y0) / (hi - lo)
    w = (x1 - x0) / len(items)
    s = svg_open(h, title)
    if title: s.append(txt(8, 13, title, 9, BL, bold=True))
    s.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{GD}"/>')
    for k, (lab, v, col) in enumerate(items):
        cx = x0 + w * k + w / 2; bw = min(34, w * .62)
        s.append(f'<rect x="{cx-bw/2:.1f}" y="{Y(v):.1f}" width="{bw:.1f}" height="{y1-Y(v):.1f}" rx="3" fill="{col}" opacity=".9"/>')
        s.append(txt(cx, Y(v) - 4, fmt(v), 8, col, 'middle', True))
        for li, part in enumerate(str(lab).split('|')):
            s.append(txt(cx, y1 + 11 + li * 9, part, 7, GR, 'middle'))
    if ref:
        s.append(f'<line x1="{x0}" y1="{Y(ref[0]):.1f}" x2="{x1}" y2="{Y(ref[0]):.1f}" stroke="{YL}" stroke-width="1.2" stroke-dasharray="5 3"/>')
        s.append(f'<line x1="{x1-4.4*len(ref[1])-20:.1f}" y1="21" x2="{x1-4.4*len(ref[1])-8:.1f}" y2="21" stroke="{YL}" stroke-width="1.2" stroke-dasharray="3 2"/>')
        s.append(txt(x1, 24, ref[1], 7, YL, 'end'))
    if note: s.append(txt(272, 24, note, 6.5, GR, 'end'))
    s.append('</svg>')
    return ''.join(s)

def boxes(steps, title='', h=None, color=BL, last=OR, vertical=False):
    """Fila de cajas con flechas. steps: (big, small)."""
    k = len(steps)
    if h is None: h = 96
    s = svg_open(h, title)
    if title: s.append(txt(8, 13, title, 9, BL, bold=True))
    gap = 6; w = (264 - gap * (k - 1)) / k
    for i, (a, b) in enumerate(steps):
        x = 8 + i * (w + gap); col = last if i == k - 1 and last else color
        s.append(f'<rect x="{x:.1f}" y="28" width="{w:.1f}" height="44" rx="7" fill="{col}22" stroke="{col}" stroke-width="1.3"/>')
        s.append(txt(x + w / 2, 47, a, 10 if len(a) < 9 else 8.5, col, 'middle', True))
        s.append(txt(x + w / 2, 62, b, 6.8, GR, 'middle'))
        if i < k - 1:
            ax = x + w + 1
            s.append(f'<path d="M{ax:.1f} 50 l{gap-2} 0 m-3 -3 l3 3 l-3 3" fill="none" stroke="{GR}" stroke-width="1"/>')
    s.append('</svg>')
    return ''.join(s)

def flow_v(steps, title='', color=BL, hi_last=True):
    h = 22 + len(steps) * 30
    s = svg_open(h, title)
    if title: s.append(txt(8, 13, title, 9, BL, bold=True))
    for i, (a, b) in enumerate(steps):
        y = 20 + i * 30; col = OR if (hi_last and i == len(steps) - 1) else color
        s.append(f'<rect x="8" y="{y}" width="264" height="24" rx="6" fill="{col}1f" stroke="{col}" stroke-width="1.1"/>')
        s.append(txt(16, y + 15.5, f'{i+1}. {a}', 8.6, col, bold=True))
        s.append(txt(266, y + 15.5, b, 7.2, GR, 'end'))
    s.append('</svg>')
    return ''.join(s)

def scatter(X, Y, a, b, title='', h=160, xl='', resid=False, xr=None, yr=None, extra='', xticks=None):
    x0, x1 = xr or (min(X) - 2, max(X) + 2)
    lo, hi = yr or (min(Y) - .3, max(Y) + .3)
    px = lambda v: 34 + (v - x0) * 230 / (x1 - x0)
    py = lambda v: (h - 30) - (v - lo) * (h - 58) / (hi - lo)
    s = svg_open(h, title)
    if title: s.append(txt(8, 13, title, 9, BL, bold=True))
    for k in range(4):
        v = lo + (hi - lo) * (k + .5) / 4
        s.append(f'<line x1="34" x2="264" y1="{py(v):.1f}" y2="{py(v):.1f}" stroke="{GD}" stroke-width=".5"/>')
        s.append(txt(30, py(v) + 3, n(v, 0 if hi - lo > 20 else 1), 7, GR, 'end'))
    if resid:
        for u, v in zip(X, Y):
            s.append(f'<line x1="{px(u):.1f}" y1="{py(v):.1f}" x2="{px(u):.1f}" y2="{py(a+b*u):.1f}" stroke="{YL}" stroke-width="1"/>')
    s.append(f'<line x1="{px(x0):.1f}" y1="{py(a+b*x0):.1f}" x2="{px(x1):.1f}" y2="{py(a+b*x1):.1f}" stroke="{OR}" stroke-width="2"/>')
    jit = {}
    for u, v in zip(X, Y):
        s.append(f'<circle cx="{px(u):.1f}" cy="{py(v):.1f}" r="3" fill="{BL}"/>')
    for u in (xticks if xticks is not None else sorted(set(X))):
        s.append(txt(px(u), h - 18, n(u, 0), 7, GR, 'middle'))
    if xl: s.append(txt(150, h - 6, xl, 7.5, GR, 'middle'))
    s.append(extra)
    s.append('</svg>')
    return ''.join(s)

def interval_rows(rows, title='', lo=0, hi=1, h=None, ticks=(), zero=None, dec=2):
    """rows: (label, a, b, color, center)."""
    h = h or (34 + len(rows) * 26 + 14)
    X = lambda v: 92 + (v - lo) * 172 / (hi - lo)
    s = svg_open(h, title)
    if title: s.append(txt(8, 13, title, 9, BL, bold=True))
    for t in ticks:
        s.append(f'<line x1="{X(t):.1f}" y1="24" x2="{X(t):.1f}" y2="{h-16}" stroke="{GD}" stroke-width=".5"/>')
        s.append(txt(X(t), h - 6, n(t, 0 if float(t).is_integer() else dec), 7, GR, 'middle'))
    if zero is not None:
        s.append(f'<line x1="{X(zero):.1f}" y1="24" x2="{X(zero):.1f}" y2="{h-16}" stroke="{YL}" stroke-width="1.2" stroke-dasharray="4 3"/>')
    for i, (lab, a, b, col, c) in enumerate(rows):
        y = 36 + i * 26
        s.append(txt(8, y + 3, lab, 7.6, col, bold=True))
        s.append(f'<line x1="{X(a):.1f}" y1="{y}" x2="{X(b):.1f}" y2="{y}" stroke="{col}" stroke-width="5" stroke-linecap="round" opacity=".85"/>')
        if c is not None: s.append(f'<circle cx="{X(c):.1f}" cy="{y}" r="3.2" fill="#111" stroke="#fff" stroke-width="1"/>')
        s.append(txt(X(a), y + 12, n(a, dec), 6.8, GR, 'middle'))
        s.append(txt(X(b), y + 12, n(b, dec), 6.8, GR, 'middle'))
    s.append('</svg>')
    return ''.join(s)

# ---------------------------------------------------------------- cálculos
def ses(ys, a, f0):
    f = [f0]
    for v in ys[:-1]: f.append(a * v + (1 - a) * f[-1])
    return f, a * ys[-1] + (1 - a) * f[-1]

def holt(ys, a, b, L, T):
    F = [None]
    for v in ys[1:]:
        F.append(L + T); Ln = a * v + (1 - a) * (L + T); T = b * (Ln - L) + (1 - b) * T; L = Ln
    return F, L + T

acme = [500,350,250,400,450,350,200,300,350,200,150,400,550,350,250,550,550,400,350,600,750,500,400,650,850,600,450,700]
f01, F25a = ses(acme[:24], .1, 500); f06, F25b = ses(acme[:24], .6, 500)
perros = [620,840,770,250,1000,870]; fper, ago = ses(perros, .28, 620)
serie = [3550,4280,4830,5120,2100,4676,5240,3980,4720]; fser, f33 = ses(serie, .2, 3550)
t150 = [700,685,648,717,713,728,754,762]
fses_t, _ = ses(t150, 2/9, 650)
fh, F12h = holt(t150, .3, .1, 700, 0)
eh = [y - f for y, f in zip(t150[1:], fh[1:])]
ts_h = [sum(eh[:i+1]) / (sum(abs(e) for e in eh[:i+1]) / (i+1)) for i in range(7)]
es_ = [y - f for y, f in zip(t150[1:], fses_t[1:])]
ts_s = [sum(es_[:i+1]) / (sum(abs(e) for e in es_[:i+1]) / (i+1)) for i in range(7)]
hel = [200,300,200,400,500,600]; fhel, fjul = ses(hel, .28, 200)
pm3 = [None]*3 + [sum(hel[i-3:i]) / 3 for i in range(3, 6)]
xx = [5]*3+[10]*3+[15]*3+[20]*3; yy = [1.6,2.2,1.4,1.9,2.4,2.6,2.3,2.7,2.8,2.6,2.9,3.1]
res = [y - (1.45 + .074 * x) for x, y in zip(xx, yy)]
gY = [9.95,24.45,31.75,35,25.02,16.86,14.38,9.6,24.35,27.5,17.08,37,41.95,11.66,21.65,17.89,69,10.3,34.93,46.59,44.88,54.12,56.23,22.13,21.15]
gC = [2,8,11,10,8,4,2,2,9,8,4,11,12,2,4,4,20,1,10,15,15,16,17,6,5]
gD = [50,110,120,550,295,200,375,52,100,300,412,400,500,360,205,400,600,585,540,250,290,510,590,100,400]
gF = [2.30920043 + 2.74036942 * c + 0.01243958 * d for c, d in zip(gC, gD)]

def check():
    assert abs(F25a - 469.1) < .1 and abs(F25b - 576.0) < .1
    assert abs(ago - 745.13) < .01
    assert abs(f33 - 4266.25) < .02, f33
    assert abs(F12h - 738.47) < .01 and abs(ts_h[-1] - 3.38) < .01 and abs(ts_s[-1] - 6.13) < .01
    assert abs(fjul - 409.04) < .01
    assert abs(fses_t[1] - 661.11) < .01
check()

# ---------------------------------------------------------------- tarjetas
def C(k, title, text, **kw):
    d = dict(type='concepto', k=k, title=title, text=text); d.update(kw); return d
def Q(title, options, correct, feedback, k='A ver…'):
    return dict(type='pregunta', k=k, title=title, options=options, correct=correct, feedback=feedback)
def Z(title, text):
    return dict(type='cierre', k='Para llevar', title=title, text=text)

H = {}

# ======================= Clase 6 · SES
meses = ['Feb','Mar','Abr','May','Jun','Jul','Ago']
H['clase06'] = [
 C('La idea', 'Un pronóstico que aprende de su último error.',
   'La suavización exponencial simple guarda un nivel y lo corrige con una fracción alfa del error que acabás de ver. Error positivo: subís. Error negativo: bajás. Nada más… y nada menos.',
   formula=r'F_{t+1}=F_t+\alpha e_t',
   svg=boxes([('Fₜ','lo que esperabas'),('α·eₜ','parte del error'),('Fₜ₊₁','nuevo nivel')], 'SES = corrección del último pronóstico'),
   chartLabel='Esquema de la recurrencia de Hanke / Chase',
   ejemplo='eₜ = Yₜ − Fₜ: real menos pronosticado. Al cerrar el período t conocés Yₜ y recién ahí construís Fₜ₊₁.'),
 C('Chase en un toque', 'Pronosticaste 1050, vendiste 1000.',
   'Con alfa 0,05 no corregís los 50 enteros: absorbés sólo el 5% del error. El nuevo pronóstico baja apenas a 1047,5.',
   formula=r'1050+0{,}05\cdot(1000-1050)=1047{,}5',
   svg=bars([('F anterior',1050,BL),('Real',1000,GR),('F nuevo',1047.5,OR)], 'Corrección mínima (α = 0,05)', yr=(960,1070), fmt=lambda v: n(v,1)),
   chartLabel='Datos del texto de Chase; la cuenta final es mía'),
 Q('Acme: F₂ = 500, vendiste Y₂ = 350 y α = 0,1. ¿Cuánto da F₃?',
   ['350: copia el dato', '485: corrige el 10% del error', '515: suma el error'], 1,
   'e₂ = 350 − 500 = −150. F₃ = 500 + 0,1 · (−150) = 485. Con α entre 0 y 1, el nuevo pronóstico queda entre el dato y el pronóstico anterior. Con α 0,6 daría 410.'),
 C('¿Por qué «exponencial»?', 'El pasado no se borra: se va apagando.',
   'Si desarmás la fórmula, cada dato viejo pesa alfa por (1 − alfa) elevado a su antigüedad. Con alfa 0,6 el dato actual se lleva el 60% y a los cuatro períodos queda 1,5%. Con alfa 0,1, el pasado sigue pesando.',
   svg=line_chart([('α = 0,1',[.1,.09,.081,.0729,.06561],BL,False),('α = 0,6',[.6,.24,.096,.0384,.01536],OR,False)],
                  ['actual','1 atrás','2 atrás','3 atrás','4 atrás'], 'Peso de cada dato según su antigüedad', yr=(0,.6)),
   chartLabel='Pesos α(1−α)ᵏ de la tabla de la clase'),
 C('Acme / ferretería', 'Alfa chico suaviza, alfa grande persigue.',
   'Mismos 24 trimestres, dos alfas. Con 0,1 la curva casi no se mueve; con 0,6 corre atrás de cada pico. Ninguna dibuja la estación que se repite.',
   svg=line_chart([('Real',acme[:24],GR,False),('α = 0,1',f01,BL,False),('α = 0,6',f06,OR,True)], [str(i) for i in range(1,25)], 'Ferretería: real y SES con F₁ = 500', every=4),
   chartLabel='Cuadro 3 de la práctica = Acme de Hanke; curvas calculadas por mí',
   ejemplo='F₂₅ con α 0,1 = 469,1 (MSE 24262). Con α 0,6 = 576,0 (MSE 22248). Hanke ej. 4.5 y 4.6.'),
 Q('Si el nivel de la demanda cambia de golpe y querés reaccionar rápido, elegís un alfa…',
   ['Chico, cerca de 0,1', 'Grande: pesa más lo reciente', 'Da igual, SES no tiene memoria'], 1,
   'Alfa grande reacciona más (y también transmite más ruido). Alfa chico estabiliza y conserva memoria. Igual, el alfa se elige comparando errores con la misma ventana, no a ojo.'),
 C('El arranque importa', 'Cambiás F₁ y cambia el ganador.',
   'Hanke repite Acme arrancando con la media de seis datos, 383,3, en vez de 500. El MSE de alfa 0,1 pasa de 24262 a 21091, y ahora le gana a alfa 0,6. Moraleja: declarás el arranque y no mezclás protocolos.',
   svg=bars([('α 0,1|F₁=500',24262,BL),('α 0,6|F₁=500',22248,OR),('α 0,1|F₁=383,3',21091,BL),('α 0,6|F₁=383,3',22152,OR)], 'MSE de ajuste según el arranque', yr=(19000,25200), fmt=lambda v: f'{v:,.0f}'.replace(',', '.'), h=150),
   chartLabel='Valores de Hanke, ejemplos 4.5 y 4.6'),
 C('Ejercicio 2.2', 'Perros: ¿cuánto alimento en agosto?',
   'Con la convención de una resolución estudiantil, alfa 0,28 y F de febrero igual a 620, agosto da 745,13 toneladas. Julio vino 173 arriba de lo previsto y el nivel sube 48,56.',
   formula=r'F_{ago}=0{,}28(870)+0{,}72(696{,}57)',
   svg=line_chart([('Real',perros+[None],BL,False),('F emitido',fper+[ago],OR,True)], meses, 'Alimento para perros (t)', marks=[(6,ago,'745,13',OR)]),
   chartLabel='SG1 Final (1), p-03 · resolución estudiantil, recalculada por mí'),
 Q('Otro alumno usa α = 2/7 exacto en vez de 0,28. ¿Le da 745,13?',
   ['Sí: 0,28 y 2/7 son lo mismo', 'No: le da 747,02, y está bien para su α declarado', 'No se puede: el enunciado no da α'], 1,
   'Con 2/7 = 0,2857… da 747,02 t. Ninguno está «mal»: el enunciado no fija alfa, así que cada resultado vale para su convención. Lo que no podés es ocultar cuál usaste.'),
 C('Trampa de final', 'Pesos 2 – 2,5 – 3 – 3,5 no son un alfa.',
   'En la serie trimestral 24 a 32, SES con alfa 0,2 da F₃₃ = 4266,25. Si usás esos cuatro pesos sobre los últimos datos, hacés un promedio móvil ponderado y te da 4628,36. Son dos métodos distintos: no llames SES a la segunda cuenta.',
   svg=line_chart([('Real',serie+[None],BL,False),('SES α 0,2',fser+[f33],OR,True)], [str(t) for t in range(24,34)], 'Serie trimestral 24…32', marks=[(9,f33,'SES 4266,25',OR,14),(9,50912/11,'PMP 4628,36',YL,-7)]),
   chartLabel='Datos del final (SG1 p-11); cálculos míos'),
 C('Otra variante', 'α = 0,4 «equivale» a un móvil de 4.',
   'Una resolución estudiantil usa n = 2 sobre alfa, menos 1: con 0,4 da 4. Ojo: esa regla no está en la bibliografía de SES consultada; es un complemento. Y la segunda parte del ejercicio («40% más de peso histórico») es ambigua: explicitá tu interpretación.',
   formula=r'n=\frac{2}{\alpha}-1=4',
   svg=boxes([('α = 0,4','peso reciente'),('2/0,4 − 1','regla aproximada'),('n = 4','ventana equivalente')], 'Complemento usado por la resolución estudiantil'),
   chartLabel='No es una regla óptima ni universal de cátedra'),
 C('Varios pasos', 'Sin datos nuevos, SES dibuja una línea plana.',
   'Desde julio, el pronóstico de agosto, septiembre y octubre es el mismo: 745,13. No es que no haya incertidumbre: es que el modelo no tiene tendencia ni estación.',
   formula=r'F_{t+p}=F_{t+1}\quad(p\geq1)',
   svg=line_chart([('Real',perros+[None]*3,BL,False),('Pronóstico desde julio',[None]*5+[870,ago,ago,ago],OR,True)], meses+['Sep','Oct'], 'Perros: horizonte de 1 a 3 meses'),
   chartLabel='Mismo origen (julio), α = 0,28'),
 Q('Aplicás SES a una serie que sube sin parar. ¿Qué esperás ver?',
   ['Que el pronóstico queda siempre atrás, con errores positivos', 'Que acierta en promedio porque suaviza', 'Que sobreestima todo el tiempo'], 0,
   'SES no tiene un estado para la pendiente: va detrás de la serie, subestima y acumula errores positivos. La solución no es retocar alfa sino pasar a Brown o Holt (Clase 7).'),
 Z('Llevate esto de la Clase 6.',
   'Fₜ₊₁ = Fₜ + α·eₜ. Alfa grande reacciona, alfa chico estabiliza. Declarás alfa y arranque. Perros: 745,13 t con α 0,28. Pesos de un móvil no son un alfa. Próxima: Brown y Holt.'),
]

# ======================= Clase 7 · Brown y Holt
_, f12s = ses(t150, 2/9, 650)
m412 = [str(m) for m in range(4, 13)]
def nivel_pendiente():
    s = svg_open(130, 'Nivel y pendiente')
    s.append(txt(8, 13, 'Holt: un nivel y una pendiente', 9, BL, bold=True))
    pts = [(30,96),(62,90),(94,84),(126,80),(158,70)]
    s.append('<polyline fill="none" stroke="%s" stroke-width="1.8" points="%s"/>' % (BL, ' '.join(f'{x},{y}' for x, y in pts)))
    for x, y in pts: s.append(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{BL}"/>')
    s.append(f'<circle cx="158" cy="70" r="5" fill="none" stroke="{YL}" stroke-width="1.8"/>')
    s.append(txt(150, 86, 'Lₜ', 9, YL, 'end', True))
    for p in (1, 2, 3):
        x, y = 158 + 32 * p, 70 - 9 * p
        s.append(f'<circle cx="{x}" cy="{y}" r="3.6" fill="none" stroke="{OR}" stroke-width="1.6"/>')
        s.append(txt(x, y - 8, f'L + {p}T' if p > 1 else 'L + T', 8, OR, 'middle', True))
    s.append(f'<line x1="158" y1="70" x2="254" y2="43" stroke="{OR}" stroke-width="1.6" stroke-dasharray="4 3"/>')
    s.append(f'<path d="M190 61 v9 h-32" fill="none" stroke="{GR}" stroke-width=".8"/>')
    s.append(txt(193, 74, 'T por período', 7, GR))
    s.append(txt(140, 122, 'Esquema: desde cada origen la proyección es una recta Lₜ + p·Tₜ', 7.5, GR, 'middle'))
    s.append('</svg>'); return ''.join(s)

H['clase07'] = [
 C('El problema', 'SES llega tarde cuando la serie sube.',
   'T-150, meses 4 a 11: la demanda pasa de 700 a 762. SES con alfa 2/9 va siempre detrás. Su señal de rastreo termina en 6,13: puro error positivo acumulado.',
   svg=line_chart([('Real',t150+[None],BL,False),('SES α 2/9',fses_t+[f12s],OR,True)], m412, 'T-150: SES queda atrás'),
   chartLabel='Final 26/09/2002 (F₄ = 650); curva calculada por mí'),
 C('La idea', 'Para una tendencia hacen falta dos cosas.',
   'Un nivel: dónde está la serie hoy. Una pendiente: cuánto cambia por período. Con los dos proyectás una recta desde el último dato. Brown y Holt hacen eso, cada uno a su manera.',
   formula=r'F_{t+p}=L_t+p\,T_t', svg=nivel_pendiente(), chartLabel='Esquema propio, no es una serie del material'),
 C('Brown', 'Dos suavizados, un solo alfa.',
   'Suavizás la serie (A) y después suavizás ese suavizado (A prima). La distancia entre los dos te da la pendiente; con ella corregís el nivel.',
   formula=r'a_t=2A_t-A′_t\qquad b_t=\frac{\alpha}{1-\alpha}(A_t-A′_t)',
   svg=boxes([('Yₜ','dato'),('Aₜ','suaviza Y'),('A′ₜ','suaviza A'),('aₜ, bₜ','nivel · pend.'),('Fₜ₊ₚ','aₜ + p·bₜ')], 'Brown en cadena'),
   chartLabel='Ojo: el resumen trae una errata (Aₜ = αAₜ…); la primera suavización usa Yₜ'),
 C('Brown en T-150', 'Mes 5: el pronóstico de junio es 691.',
   'Con alfa 0,3 y A₄ = A′₄ = 700: A₅ = 695,5 y A′₅ = 698,65. Nivel a₅ = 692,35 y pendiente b₅ = −1,35. F₆ = 691,00. Al cerrar el mes 11, F₁₂ ≈ 761,7.',
   ejemplo='Cálculo propio para ilustrar el algoritmo, no solución del final ni alfa óptimo.'),
 Q('En Brown, ¿cuántos parámetros de suavización elegís?',
   ['Uno: el mismo alfa mueve las dos suavizaciones', 'Dos: alfa y beta', 'Tres: alfa, beta y gamma'], 0,
   'Brown usa un único alfa. Holt separa alfa (nivel) y beta (pendiente). Winter agrega gamma para la estación.'),
 C('Holt', 'Tres ecuaciones y un orden que no se negocia.',
   'Primero emitís el pronóstico. Llega el dato y actualizás el nivel. Con el nivel nuevo, la pendiente. Recién ahí proyectás. Si medís el error con el nivel posterior al dato, hacés trampa sin querer.',
   svg=flow_v([('Emití Fₜ = Lₜ₋₁ + Tₜ₋₁','antes del dato'),('Actualizá Lₜ con α','usa Yₜ'),('Actualizá Tₜ con β','usa Lₜ − Lₜ₋₁'),('Proyectá Lₜ + p·Tₜ','desde ese origen')], 'Holt paso a paso'),
   chartLabel='Hanke, ecuaciones de Holt (cap. 4)'),
 C('Hanke 4.9', 'Acme, a mano: F₃ = 450,5.',
   'L₁ = 500, T₁ = 0, alfa 0,3 y beta 0,1. Con Y₂ = 350: L₂ = 455 y T₂ = −4,5. Entonces F₃ = 450,5, y como Y₃ = 250 el error es −200,5.',
   formula=r'L_2=0{,}3\cdot350+0{,}7(500+0)=455',
   svg=boxes([('Y₂ = 350','dato nuevo'),('L₂ = 455','nivel'),('T₂ = −4,5','pendiente'),('F₃ = 450,5','L₂ + T₂')], 'Holt: un paso del ejemplo 4.9'),
   chartLabel='Hanke, ejemplo 4.9',
   ejemplo='F₂₅ del libro: 577,7 (mi cálculo: 577,6). MSE: libro 20515,5; reproducción propia 21448,3. Diferencia sin resolver.'),
 Q('Con L₂ = 455 y T₂ = −4,5, ¿cuánto vale F₃?',
   ['455', '450,5', '459,5'], 1,
   'F₃ = L₂ + 1·T₂ = 455 − 4,5 = 450,5. La pendiente negativa baja la proyección; sumar p·T respeta unidades.'),
 C('T-150 con Holt', 'Ahora el pronóstico acompaña la subida.',
   'Holt con alfa 0,3 y beta 0,1 arranca en L₄ = 700 y T₄ = 0. Al cierre del mes 11 tiene nivel 735 y pendiente 3,48: F₁₂ ≈ 738,5.',
   svg=line_chart([('Real',t150+[None],BL,False),('SES',fses_t+[f12s],GR,True),('Holt .3/.1',fh+[F12h],OR,True)], m412, 'T-150: real, SES y Holt'),
   chartLabel='Extensión didáctica propia, no solución oficial del final'),
 C('El tablero', 'Menos error y menos sesgo, en la misma ventana.',
   'Meses 5 a 11. SES: MAD 42,41 y TS 6,13. Holt 0,3/0,1: MAD 34,31 y TS 3,38. Holt 0,5/0,3: MAD 29,16 y TS 3,07. Comparás con igual ventana y denominador, o no comparás.',
   svg=bars([('SES',42.41,GR),('Holt .3/.1',34.31,BL),('Holt .5/.3',29.16,OR)], 'MAD en T-150, meses 5…11', fmt=lambda v: n(v,2), h=150),
   chartLabel='Cálculos propios de la Clase 7'),
 Q('Holt da TS = 3,38, dentro de límites ±4. ¿Ya podés decir que el pronóstico es bueno?',
   ['Sí: la TS lo garantiza', 'No del todo: sólo dice que ese control de sesgo no se activó', 'No: una TS buena tiene que ser exactamente 0'], 1,
   'La TS dentro de límites no garantiza MAD bajo ni buen desempeño futuro. Además, ±4 acá es un límite didáctico, no un dato del final. Respondé en varios planos: patrón, errores, sesgo y uso.'),
 C('Cuidado', 'Brown no es Holt con alfa igual a beta.',
   'Hanke menciona una equivalencia, pero no es literal con estas fórmulas. Complemento algebraico, no está en el material: Brown con alfa 0,3 equivale a un Holt con alfa 0,51 y beta ≈ 0,176. Probá los dos algoritmos, no copies parámetros.'),
 Z('Llevate esto de la Clase 7.',
   'Tendencia = nivel + pendiente. Brown: dos suavizados y un alfa. Holt: emitir, nivel, pendiente, proyectar. En T-150 Holt baja el MAD de 42 a 34 y la TS de 6,1 a 3,4. Próxima: Winter, cuando además hay estación.'),
]

# ======================= Clase 8 · Winter
def amp_svg():
    s = svg_open(120, 'Aditivo vs multiplicativo')
    s.append(txt(8, 13, 'Misma estación, dos formas', 9, BL, bold=True))
    import math as m
    def panel(x0, mult, lab, col):
        pts = []
        for i in range(16):
            base = 78 - i * 2.2
            amp = (6 + i * 1.3) if mult else 10
            pts.append((x0 + i * 7.6, base - amp * m.sin(i * m.pi / 2)))
        s.append(f'<polyline fill="none" stroke="{col}" stroke-width="1.6" points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}"/>')
        s.append(f'<line x1="{x0}" y1="78" x2="{x0+114}" y2="45" stroke="{GR}" stroke-width=".8" stroke-dasharray="3 3"/>')
        s.append(txt(x0 + 57, 108, lab, 7.6, col, 'middle', True))
    panel(14, False, 'Aditivo: amplitud constante', BL)
    panel(150, True, 'Multiplicativo: crece con el nivel', OR)
    s.append('</svg>'); return ''.join(s)

wf = [778.179, 521.917, 393.430, 716.726]; wreal = [850, 600, 450, 700]
H['clase08'] = [
 C('El problema', 'Los picos vuelven en el calendario.',
   'En la ferretería, el tercer trimestre es todos los años el más bajo, el primero y el cuarto se turnan arriba, y el conjunto sube en los últimos años. Holt ve la tendencia pero no la estación. Winter suma un tercer estado: el índice estacional.',
   svg=line_chart([('Ventas',acme[:24],BL,False)], [('I','II','III','IV')[i % 4] for i in range(24)], 'Ferretería / Acme: 24 trimestres', every=4),
   chartLabel='Cuadro 3 de la práctica = Acme de Hanke'),
 C('Tres estados', 'Nivel, pendiente y estación, cada uno con su constante.',
   'L es el nivel sin estación (alfa). T es el cambio del nivel por período (beta). S es el índice de esta estación (gamma). Y hace falta s, cuántos períodos tiene una vuelta.',
   svg=boxes([('Lₜ · α','nivel sin estación'),('Tₜ · β','pendiente'),('Sₜ · γ','índice estacional'),('Fₜ₊ₚ','(L + pT)·S')], 'Winter multiplicativo'),
   chartLabel='Hanke, ecuaciones 4.18 a 4.21'),
 Q('Datos trimestrales con un patrón que se repite cada año. ¿Cuánto vale s?',
   ['12, porque el año tiene doce meses', '4: cuatro trimestres por vuelta', '1: un año'], 1,
   's es la cantidad de períodos observados por vuelta del patrón. Trimestral con ciclo anual: s = 4. Se justifica con calendario, gráfico y autocorrelación.'),
 C('Multiplicativo', '«20% más», no «20 unidades más».',
   'Winter multiplicativo supone que la estación es una proporción del nivel: si el nivel crece, las oscilaciones se agrandan. Si la amplitud se mantiene constante, el esquema aditivo merece consideración.',
   svg=amp_svg(), chartLabel='Esquema propio'),
 C('La clave', 'Sacás la estación para medir el nivel. La devolvés al pronosticar.',
   'En el nivel dividís el dato por el índice de la misma estación de la vuelta anterior. En la estación dividís el dato por el nivel nuevo. En el pronóstico multiplicás por el último índice conocido de la estación que querés anticipar.',
   formula=r'L_t=\alpha\frac{Y_t}{S_{t-s}}+(1-\alpha)(L_{t-1}+T_{t-1})'),
 Q('En la ecuación del nivel, ¿qué índice dividís?',
   ['S del período inmediatamente anterior', 'S de la misma estación, una vuelta atrás', 'El S que vas a calcular ahora'], 1,
   'Sₜ₋ₛ: misma estación, vuelta anterior. Para el trimestre 24 (IV), usás S₂₀. El S₂₄ se calcula después y sirve para el IV del año siguiente.'),
 C('Hanke 4.10', 'Un paso real: el trimestre 24.',
   'Alfa 0,4, beta 0,1, gamma 0,3. Venía L₂₃ = 501,286 y T₂₃ = 9,1484; S₂₀ = 1,39628 y llega Y₂₄ = 650. Resultado: L₂₄ ≈ 492,469, T₂₄ ≈ 7,352 y S₂₄ ≈ 1,37336.',
   formula=r'L_{24}=0{,}4\frac{650}{1{,}39628}+0{,}6(501{,}286+9{,}1484)',
   ejemplo='Antes de ver 650 se había pronosticado 712,712: error −62,712. S₂₄ no se usa para «arreglar» ese pronóstico.'),
 C('El próximo año', 'Cuatro pronósticos desde el mismo origen.',
   'Desde t = 24: F₂₅ = 778,2 (índice del I), F₂₆ = 521,9, F₂₇ = 393,4 y F₂₈ = 716,7. Contra lo real de 2006, el error de prueba da MAD ≈ 55,80 y MSE ≈ 3683,81.',
   svg=line_chart([('Real 2006',wreal,BL,False),('Winter desde t=24',wf,OR,True)], ['I · 25','II · 26','III · 27','IV · 28'], 'Prueba 2006 (horizontes 1 a 4)'),
   chartLabel='Pronósticos de Hanke; MAD y MSE de prueba calculados por mí'),
 Q('El índice del primer trimestre es 1,55691. Significa que…',
   ['Se venden 155,691 unidades más', 'El trimestre I queda ≈ 55,7% sobre el nivel proyectado', 'El nivel sube 1,56 por trimestre'], 1,
   'En el modelo multiplicativo el índice es un factor sin unidades: 1 es neutro. 1,55691 = 55,691% por encima del nivel proyectado de ese trimestre.'),
 C('¿Valió la pena?', 'Para el trimestre I, la estación era lo que faltaba.',
   'Para el primer trimestre de 2006 (real 850), SES pronosticaba 469,1 o 576,0. Winter dice 778,2. La diferencia es el índice del I, que SES no tiene.',
   svg=bars([('SES|α 0,1',469.1,GR),('SES|α 0,6',576.0,GR),('Winter',778.179,OR),('Real',850,BL)], 'F₂₅ (2006-I) según el método', fmt=lambda v: n(v,1)),
   chartLabel='Hanke, ejemplos 4.5, 4.6 y 4.10'),
 C('Errata', 'Es más p·T, no menos.',
   'El resumen de 25 páginas escribe la proyección con «A menos pT». Hanke, ecuación 4.21, usa L más p·T. Una pendiente positiva tiene que subir la base, no bajarla.',
   formula=r'F_{t+p}=(L_t+pT_t)\,S_{t-s+p}',
   svg=boxes([('Lₜ','nivel sin estación'),('+ p·Tₜ','proyectar pendiente'),('× S','estación objetivo')], 'Primero la base, después el calendario'),
   chartLabel='Hanke 4.21: signo + delante de p·T'),
 C('No mezcles', 'Error de ajuste no es error de prueba.',
   'Hanke informa MSE de ajuste 7636,86 para t = 1 a 24. El 3683,81 sale de cuatro pronósticos de 2006, de horizontes 1 a 4 desde un origen fijo. Son protocolos distintos: no los pongas en la misma columna.'),
 Z('Llevate esto de la Clase 8.',
   'Winter = nivel + pendiente + índice, con alfa, beta y gamma. Dividís por S de la misma estación para el nivel y multiplicás al pronosticar. s = 4 en trimestral. Es L + pT. Próxima: descomposición.'),
]

# ======================= Clase 9 · Descomposición
def layers_svg():
    import math as m
    s = svg_open(150, 'Capas de una serie')
    s.append(txt(8, 13, 'Y = T × S × I (esquema)', 9, BL, bold=True))
    rows = [('T', 'tendencia', BL, lambda i: 1 + i * .02),
            ('S', 'estación', OR, lambda i: 1 + .25 * m.sin(i * m.pi / 2)),
            ('I', 'irregular', GR, lambda i: 1 + .08 * m.sin(i * 2.7) * m.cos(i * 1.3)),
            ('Y', 'lo que ves', YL, None)]
    for r, (k, lab, col, fn) in enumerate(rows):
        y0 = 30 + r * 29
        vals = [rows[0][3](i) * rows[1][3](i) * rows[2][3](i) for i in range(20)] if fn is None else [fn(i) for i in range(20)]
        lo, hi = min(vals), max(vals); hi = hi if hi > lo else lo + 1
        pts = ' '.join(f'{70 + i * 10:.1f},{y0 + 20 - (v - lo) * 18 / (hi - lo + .3):.1f}' for i, v in enumerate(vals))
        s.append(txt(10, y0 + 15, k, 11, col, bold=True)); s.append(txt(24, y0 + 15, lab, 7, GR))
        s.append(f'<polyline fill="none" stroke="{col}" stroke-width="1.6" points="{pts}"/>')
    s.append('</svg>'); return ''.join(s)

cav = [518,404,300,210,196,186,247,343,464,680,711,610]
coast_T = [261.24 + .759 * t for t in (29, 30, 31, 32)]
coast_F = [220.842, 288.455, 317.990, 310.654]
H['clase09'] = [
 C('La idea', 'Desarmar la serie para entenderla.',
   'Descomponer es separar tendencia, estación e irregularidad. Pronosticar es volver a armarla con hipótesis explícitas. Sacar la estación no borra ni la tendencia ni la incertidumbre.',
   svg=layers_svg(), chartLabel='Esquema propio'),
 C('Dos modelos', '¿Sumás o multiplicás la estación?',
   'Aditivo: Y = T + S + I, la estación en unidades, neutra en 0, y desestacionalizás restando. Multiplicativo: Y = T · S · I, la estación es un factor, neutra en 1, y desestacionalizás dividiendo. Si las oscilaciones se agrandan con el nivel (forma de embudo), multiplicativo.',
   svg=amp_svg(), chartLabel='Esquema propio'),
 Q('En un modelo multiplicativo, ¿cómo desestacionalizás un dato?',
   ['Y − S', 'Y / S', 'Y · S'], 1,
   'Dividís por el índice. Un índice 0,8 se quita dividiendo por 0,8, no multiplicando. En el aditivo restarías S.'),
 C('Tendencia', 'Ajustar bien no es poder extrapolar.',
   'Lineal: suma lo mismo cada período. Cuadrática: la pendiente cambia. Exponencial: crece a tasa fija. Logística o Gompertz: admiten saturación. Antes de proyectar lejos, preguntate si el fenómeno tiene techo.',
   svg=line_chart([('Lineal',[10+2*i for i in range(10)],BL,False),('Cuadrática',[10+.4*i*i for i in range(10)],OR,False),('Exponencial',[10*1.17**i for i in range(10)],YL,True),('Logística',[10+28/(1+math.exp(-(i-4.5))) for i in range(10)],GN,False)], None, 'Formas de tendencia (esquema)'),
   chartLabel='Curvas de Hanke cap. 5; dibujo esquemático propio'),
 C('Cavanaugh', 'El índice sale de comparar cada mes con su promedio móvil centrado.',
   'Julio de 2004 vendió 247. Los totales de 12 meses que lo rodean son 4869 y 4964: el promedio móvil centrado da 409,7. La razón 247 sobre 409,7 ≈ 0,603: julio quedó bastante debajo de la base.',
   formula=r'PMC_{jul}=\frac{4869+4964}{24}=409{,}71',
   svg=bars([(m,v,OR if m=='Jul' else BL) for m,v in zip(['E','F','M','A','M','J','Jul','A','S','O','N','D'],cav)], 'Cavanaugh 2004 y PMC de julio', ref=(409.71,'PMC jul ≈ 409,7'), fmt=lambda v: f'{v:.0f}', h=150),
   chartLabel='Hanke, tablas 5-2 y 5-3; división verificada por mí'),
 C('Normalizar', 'Los doce índices tienen que sumar 12.',
   'Se toma la mediana de las razones de cada mes (julio ≈ 0,651). Las doce medianas suman 11,948, así que se multiplica todo por 12 sobre 11,948 ≈ 1,0044. Índice de julio publicado: ≈ 0,654, unos 35% debajo de la base.',
   formula=r'S_j=\frac{12\,m_j}{\sum m_j}',
   svg=boxes([('0,651','mediana de julio'),('× 1,0044','12 / 11,948'),('≈ 0,654','índice normalizado')], 'Cavanaugh: normalizar julio'),
   chartLabel='Hanke, tabla 5-3; valores redondeados'),
 Q('Índices trimestrales multiplicativos bien normalizados: ¿cuánto suman?',
   ['1', '4', '0'], 1,
   'Promedian 1, entonces suman 4 en trimestral y 12 en mensual. En el aditivo, en cambio, sumarían 0.'),
 C('Coastal Marine', 'Estación de un vistazo: el índice neutro es 1.',
   'Trimestre I: 0,780, un 22% debajo. II: 1,016. III: 1,117, el pico. IV: 1,088. Leé cada barra contra la línea del 1, no contra el cero.',
   svg=bars([('I',.77967,BL),('II',1.01566,BL),('III',1.11667,OR),('IV',1.088,BL)], 'Coastal Marine: índices estacionales', ref=(1,'neutro = 1'), fmt=lambda v: n(v,3), yr=(0,1.3)),
   chartLabel='Hanke, ejemplo 5.3'),
 C('Qué queda en cada cociente', 'Tres divisiones, tres lecturas distintas.',
   '2000-I: Y = 232,7, T = 262 y S = 0,77967. Y sobre T ≈ 0,888: queda S·C·I. Y sobre S ≈ 298,5: queda T·C·I, en unidades. Y sobre T·S ≈ 1,139: queda C·I, un factor.',
   svg=boxes([('Y/T','0,888 → S·C·I'),('Y/S','298,458 → T·C·I'),('Y/(T·S)','1,139 → C·I')], 'Coastal 2000-I', last=None),
   chartLabel='Valores de Hanke, ejemplo 5.3'),
 Q('Si desestacionalizás con Y / S, ¿eliminaste el ciclo?',
   ['Sí: ya no queda nada para modelar', 'No: Y / S conserva tendencia, ciclo e irregularidad', 'Sí, pero sólo en el modelo aditivo'], 1,
   'Y / S = T · C · I. Sacaste el calendario, no el ciclo. La serie desestacionalizada no es constante.'),
 C('Recomponer', 'La base sube derecho; el pronóstico sube y baja.',
   'Hanke proyecta la tendencia 261,24 + 0,759t y multiplica por el índice de cada trimestre, adoptando C = I = 1. Para 2007: 220,8, 288,5, 318,0 y 310,7. Que baje en el I no contradice la tendencia positiva: es la estación.',
   formula=r'F=(261{,}24+0{,}759\cdot29)\cdot0{,}77967\approx220{,}84',
   svg=line_chart([('Tendencia',coast_T,GR,True),('Pronóstico T·S',coast_F,OR,False)], ['29 · I','30 · II','31 · III','32 · IV'], 'Coastal Marine 2007'),
   chartLabel='Hanke, ejemplo 5.4'),
 C('Chase', 'Otro camino: factor = promedio del trimestre sobre promedio global.',
   'Dividís por el factor, ajustás una recta a la serie desestacionalizada, proyectás y volvés a multiplicar. Con factores 0,82, 1,10, 0,97 y 1,12, Chase llega a 4102,87, 5880,27, 5517,26 y 6753,71. No es lo mismo que razón al promedio móvil.',
   ejemplo='La tabla de datos originales de Chase es una imagen: no se reconstruye la regresión.'),
 Z('Llevate esto de la Clase 9.',
   'Elegí aditivo o multiplicativo mirando la amplitud. Índices: razón al PMC, mediana y normalizar a 4 o 12. Desestacionalizar es dividir por S. Pronóstico = tendencia proyectada × índice, con C = I = 1 como hipótesis. Próxima: elegir y controlar el método.'),
]

# ======================= Clase 10 · Integrador y control
def tree_svg():
    s = svg_open(196, 'Árbol de elección')
    s.append(txt(8, 13, '¿Qué familia miro primero?', 9, BL, bold=True))
    qs = [('¿Hay historia comparable?', 'No → juicio, analogía, escenarios'),
          ('¿Hay una X explicativa disponible?', 'Sí → regresión simple o múltiple'),
          ('¿Estación que se repite?', 'Sí → Winter o descomposición'),
          ('¿Pendiente que evoluciona?', 'Sí → Brown / Holt'),
          ('Nivel estable', '→ informal, promedio, móvil, SES')]
    for i, (q, a) in enumerate(qs):
        y = 22 + i * 34; last = i == len(qs) - 1
        col = GN if last else BL
        s.append(f'<rect x="8" y="{y}" width="124" height="26" rx="6" fill="{col}22" stroke="{col}"/>')
        s.append(txt(70, y + 16, q, 7.2, col, 'middle', True))
        if not last:
            s.append(f'<path d="M132 {y+13} h12" stroke="{GR}" stroke-width="1"/>')
            s.append(f'<rect x="146" y="{y}" width="126" height="26" rx="6" fill="{OR}1f" stroke="{OR}"/>')
            s.append(txt(209, y + 16, a, 6.8, OR, 'middle', True))
            s.append(f'<path d="M70 {y+27} v6" stroke="{GR}" stroke-width="1"/>')
            s.append(txt(76, y + 33, 'no' if i else 'sí', 6.5, GR))
        else:
            s.append(txt(209, y + 16, a, 7, GN, 'middle', True))
    s.append('</svg>'); return ''.join(s)

binom = [math.comb(10, u) / 1024 for u in range(11)]
def rmse_band():
    s = svg_open(120, '±2 RMSE')
    s.append(txt(8, 13, 'Límites de error: 0 ± 2·√MSE (esquema)', 9, BL, bold=True))
    s.append(f'<rect x="36" y="34" width="230" height="52" fill="{GN}" opacity=".14"/>')
    for y, lab in ((34, '+279'), (60, '0'), (86, '−279')):
        s.append(f'<line x1="36" y1="{y}" x2="266" y2="{y}" stroke="{GD if lab=="0" else GN}" stroke-width="1" stroke-dasharray="{"" if lab=="0" else "5 3"}"/>')
        s.append(txt(32, y + 3, lab, 7.5, GR, 'end'))
    s.append(txt(150, 64, 'un error individual cae acá: sin alarma', 7.5, GN, 'middle'))
    s.append(txt(150, 28, 'fuera de la banda: investigá ese período', 7.5, OR, 'middle'))
    s.append(txt(150, 108, 'Hanke 4.8: MSE 19447 → RMSE ≈ 139,5 → ±279 unidades de Y', 7.2, GR, 'middle'))
    s.append('</svg>'); return ''.join(s)

H['clase10'] = [
 C('La idea', 'Elegir es diagnosticar, calcular y defender.',
   'Ningún método gana porque «es el último que vimos». Primero evitás el error de familia mirando el patrón y la información disponible. Después ajustás parámetros. Al final controlás.',
   svg=tree_svg(), chartLabel='Síntesis propia de la matriz de la Clase 10, no un algoritmo oficial'),
 Q('Serie con tendencia y una estación que crece con el nivel. ¿Qué candidato miro primero?',
   ['SES con alfa alto', 'Winter multiplicativo', 'Promedio simple'], 1,
   'Tendencia + estación proporcional → Winter multiplicativo (o descomposición multiplicativa). SES no modela ni pendiente ni estación.'),
 C('El protocolo', 'Del problema a la revisión, en cinco pasos.',
   'Definís decisión, unidad y horizonte. Revisás datos. Graficás y proponés candidatos. Separás ajuste y prueba, con la misma ventana para todos. Emitís, medís y controlás.',
   svg=flow_v([('Definí la decisión','unidad · horizonte · fecha'),('Revisá registros','faltantes · atípicos · unidades'),('Graficá y proponé','patrón y candidatos'),('Ajustá y probá','misma ventana y criterio'),('Emití y controlá','errores · rastreo · revisión')], 'Protocolo de trabajo'),
   chartLabel='Síntesis propia a partir de Hanke (5 pasos y cap. 11)'),
 C('Señal de rastreo', 'TS = errores acumulados sobre MAD.',
   'Con e = real menos pronóstico, una TS positiva acumula subestimaciones y una negativa, sobreestimaciones. Numerador y denominador con la misma ventana. Si el MAD da 0, la razón no está definida.',
   formula=r'TS_t=\frac{RSFE_t}{MAD_t}',
   svg=boxes([('RSFE','errores con signo'),('÷ MAD','magnitud típica'),('TS','vigilar sesgo')], 'Dos partes, una misma ventana'),
   chartLabel='Chase: TS = RSFE / MAD'),
 C('T-150 bajo control', 'Holt adentro, SES afuera.',
   'Con límites didácticos de ±4, la TS de Holt termina en 3,38: no alarma. La de SES llega a 6,13: alarma. Holt arranca en −1 porque el primer error es negativo, y después cambia de signo con los errores positivos.',
   svg=line_chart([('Holt .3/.1',ts_h,OR,False),('SES α 2/9',ts_s,GR,True)], [str(m) for m in range(5,12)], 'TS acumulada, meses 5…11', band=(-4,4,GN), hlines=((4,GN,'+4'),(-4,GN,'−4')), yr=(-4.5,6.5)),
   chartLabel='Cálculo propio; ±4 es una hipótesis didáctica, no un dato del final'),
 Q('Con e = Y − F, una TS de +6 indica…',
   ['Que el método sobreestima', 'Que viene subestimando: errores positivos acumulados', 'Que el MAD es 6'], 1,
   'Errores positivos = vendiste más de lo previsto = subestimaste. Al acumularse, la TS sube. Ojo: la TS es una razón, no un MAD.'),
 C('Conteo U (Hanke)', 'Contá cuántas veces te quedaste corto.',
   'En los últimos k = 10 pronósticos, U es la cantidad de errores positivos. Si el método está sano, U ronda 5. Hanke no alarma entre 2 y 8; con 0, 1, 9 o 10 sí: eso pasa sólo con probabilidad ≈ 0,022 si los signos son al azar.',
   svg=bars([(str(u), p, OR if u in (0,1,9,10) else BL) for u, p in enumerate(binom)], 'Probabilidad de U con k = 10 (signos al azar)', fmt=lambda v: '' if v < .02 else n(v,2), h=140),
   chartLabel='Regla de Hanke; barras binomiales calculadas por mí. Naranja = zona de alarma'),
 C('±2 RMSE', 'Un error suelto demasiado grande.',
   'El tercer control mira cada error contra límites en unidades de Y. En Hanke 4.8, MSE 19447 da RMSE ≈ 139,5 y límites de ±279. No son límites de TS: TS es una razón, esto son unidades.',
   svg=rmse_band(), chartLabel='Esquema con los números de Hanke, ejemplo 4.8'),
 Q('Los ±279 de Hanke 4.8 son límites para…',
   ['La señal de rastreo', 'Un error individual, en unidades de la serie', 'El conteo U'], 1,
   'Son 0 ± 2·RMSE en unidades de Y. Tres controles, tres preguntas: TS (sesgo acumulado), U (cuántas subestimaciones), ±2 RMSE (un error enorme).'),
 C('Heladeras', 'El veredicto del estudiante no se sostiene.',
   'La resolución dice: SES tiene MAD 160 y PM3 200, gana SES. Pero el 160,51 es de febrero a junio y el 200 de abril a junio. En la ventana común, abril a junio, SES da MAD ≈ 224,85: PM3 queda mejor.',
   svg=line_chart([('Real',hel+[None],BL,False),('SES α .28',fhel+[fjul],GR,True),('PM3',pm3+[500],OR,True)], ['Ene','Feb','Mar','Abr','May','Jun','Jul'], 'Heladeras: real, SES y PM3'),
   chartLabel='SG1 p-09 (resolución estudiantil); cálculos míos'),
 Q('¿Cuál es el error de fondo en esa comparación de heladeras?',
   ['Usar MAD en vez de MSE', 'Comparar MAD calculados sobre ventanas distintas', 'Usar alfa 0,28'], 1,
   'Comparás métodos sobre fechas y horizontes comunes, o no comparás. Y con tres errores tampoco hay validación sólida para ninguno.'),
 C('Capacidad al 95%', 'Pronóstico no es cobertura.',
   'Complemento, no está en el enunciado disponible: si la demanda fuera normal con media F y desvío sigma conocido, cubrir el 95% por un lado pide F + 1,645 sigma. El 1,96 es para un intervalo de dos colas: es otra pregunta.',
   formula=r'C=F+1{,}645\,\sigma_e'),
 Z('Llevate esto de la Clase 10.',
   'Familia por patrón e información, parámetros por error de prueba, misma ventana para comparar. Tres controles distintos: TS, conteo U y ±2 RMSE. Una TS dentro de límites no prueba un buen pronóstico. Próxima: regresión lineal simple.'),
]

# ======================= Clase 4.b
def salida_svg():
    s = svg_open(120, 'Tipos de pronóstico')
    s.append(txt(8, 13, 'Tres formas de decir «la demanda será…»', 9, BL, bold=True))
    s.append(f'<circle cx="46" cy="66" r="6" fill="{OR}"/>'); s.append(txt(46, 100, 'Puntual', 8.5, OR, 'middle', True)); s.append(txt(46, 111, 'un valor', 7, GR, 'middle'))
    s.append(f'<line x1="104" y1="66" x2="176" y2="66" stroke="{BL}" stroke-width="6" stroke-linecap="round"/><circle cx="140" cy="66" r="3.5" fill="#111" stroke="#fff"/>')
    s.append(txt(140, 100, 'Intervalo', 8.5, BL, 'middle', True)); s.append(txt(140, 111, 'rango + cobertura', 7, GR, 'middle'))
    pts = ' '.join(f'{200 + i*1.5:.1f},{84 - 44*math.exp(-((i-24)/9)**2):.1f}' for i in range(49))
    s.append(f'<polyline fill="{GN}33" stroke="{GN}" stroke-width="1.6" points="200,84 {pts} 272,84"/>')
    s.append(txt(236, 100, 'Densidad', 8.5, GN, 'middle', True)); s.append(txt(236, 111, 'toda la distribución', 7, GR, 'middle'))
    s.append('</svg>'); return ''.join(s)

def triciclo_svg():
    s = svg_open(130, 'Triciclos')
    s.append(txt(8, 13, 'Demanda independiente → dependiente', 9, BL, bold=True))
    s.append(f'<rect x="90" y="24" width="100" height="32" rx="7" fill="{OR}22" stroke="{OR}"/>')
    s.append(txt(140, 39, '1000 triciclos', 9, OR, 'middle', True)); s.append(txt(140, 50, 'se pronostica', 7, GR, 'middle'))
    for x, a, b in ((20, '1000 ruedas', 'delanteras'), (160, '2000 ruedas', 'traseras')):
        s.append(f'<rect x="{x}" y="84" width="100" height="32" rx="7" fill="{BL}22" stroke="{BL}"/>')
        s.append(txt(x + 50, 99, a, 9, BL, 'middle', True)); s.append(txt(x + 50, 110, b + ' · se calcula', 7, GR, 'middle'))
        s.append(f'<path d="M140 57 L{x+50} 83" stroke="{GR}" stroke-width="1"/>')
    s.append(txt(140, 74, '× 1 y × 2', 7.5, GR, 'middle'))
    s.append('</svg>'); return ''.join(s)

def horizonte_svg():
    s = svg_open(96, 'Horizonte')
    s.append(txt(8, 13, 'Horizonte según Chase', 9, BL, bold=True))
    segs = [(10, 70, 'Corto', '< 3 meses', BL), (80, 110, 'Mediano', '3 meses a 2 años', YL), (190, 82, 'Largo', '> 2 años', OR)]
    for x, w, a, b, col in segs:
        s.append(f'<rect x="{x}" y="34" width="{w}" height="18" rx="4" fill="{col}" opacity=".8"/>')
        s.append(txt(x + w / 2, 47, a, 8.5, '#111', 'middle', True)); s.append(txt(x + w / 2, 66, b, 7.5, col, 'middle'))
    s.append(txt(140, 86, 'Cambian datos, detalle y técnica. Son rangos de esa fuente.', 7.2, GR, 'middle'))
    s.append('</svg>'); return ''.join(s)

def delphi_svg():
    s = svg_open(150, 'Delphi')
    s.append(txt(8, 13, 'Delphi: cuatro rasgos (Hanke)', 9, BL, bold=True))
    cx, cy, r = 140, 82, 46
    labs = ['Anonimato', 'Iteración', 'Retroalimentación|controlada', 'Agregación']
    for i, lab in enumerate(labs):
        a = -math.pi / 2 + i * math.pi / 2
        x, y = cx + r * 1.55 * math.cos(a), cy + r * .95 * math.sin(a)
        s.append(f'<rect x="{x-46:.1f}" y="{y-11:.1f}" width="92" height="22" rx="11" fill="{BL}22" stroke="{BL}"/>')
        parts = lab.split('|')
        for j, p in enumerate(parts):
            s.append(txt(x, y + 3 + (j - (len(parts) - 1) / 2) * 8, p, 7.6, BL, 'middle', True))
    s.append(f'<circle cx="{cx}" cy="{cy}" r="20" fill="{OR}22" stroke="{OR}"/>')
    s.append(txt(cx, cy - 1, 'rondas', 7.5, OR, 'middle', True)); s.append(txt(cx, cy + 8, 'de expertos', 6.5, GR, 'middle'))
    s.append('</svg>'); return ''.join(s)

H['clase04b'] = [
 C('La idea', 'Un pronóstico no es una meta.',
   'Pronosticar reduce incertidumbre: no crea certeza ni reemplaza la decisión. Antes de la fórmula, preguntá para qué decisión es: inventario semanal por artículo o capacidad a varios años piden horizontes, datos y precisión distintos.'),
 C('Salida', 'Decir «500» no termina el problema.',
   'Puntual: un valor central. Por intervalo: un rango con cobertura. De densidad: la distribución completa. Y siempre con unidad y período.',
   svg=salida_svg(), chartLabel='Esquema propio; clasificación de Hanke y Preguntas Frecuentes'),
 C('Demanda vs. venta', 'Pidieron 120, había 90.',
   'Complemento, no está en el material: la venta observada es lo que se transó; la demanda, lo que se quiso comprar. Si ajustás la serie con 90 como si fuera demanda, perpetuás el faltante.',
   svg=bars([('Pedido',120,BL),('Vendido',90,OR),('No atendido',30,GR)], 'Ejemplo propio (no es dato del material)', fmt=lambda v: f'{v:.0f}', h=120),
   chartLabel='Ejemplo propio para ilustrar la distinción'),
 Q('Sólo tenés la facturación: 90 unidades. ¿Podés saber que la demanda fue 120?',
   ['Sí: se deduce de la facturación', 'No, salvo que hayas registrado los pedidos no atendidos', 'Sí: demanda y venta son lo mismo'], 1,
   'El 120 sólo existe si registraste también lo que no pudiste atender. Mirando la factura sola, ves 90.'),
 C('Administrar la demanda', 'Atenderla o intentar moverla.',
   'Chase: coordinar y controlar todas las fuentes de demanda para usar bien el sistema productivo y entregar a tiempo. Papel activo: buscás influir en el momento o el volumen. Pasivo: atendés lo que llega. No es sólo una cuenta estadística.'),
 C('Dependiente o independiente', 'Las ruedas no se pronostican: se calculan.',
   'Chase: para 1000 triciclos hacen falta 1000 ruedas delanteras y 2000 traseras. Pronosticás los triciclos (demanda independiente, externa) y calculás las ruedas (demanda dependiente).',
   svg=triciclo_svg(), chartLabel='Ejemplo de Chase'),
 Q('Las 2000 ruedas traseras de los triciclos son demanda…',
   ['Independiente: hay que pronosticarlas aparte', 'Dependiente: salen de la cantidad de triciclos', 'Cualitativa'], 1,
   'Se derivan del artículo final y de su estructura. Pronosticar tres series por separado podría darte cantidades incompatibles.'),
 C('Clasificar', 'Horizonte, alcance, información, familia y salida.',
   'Chase también pide mirar datos disponibles, precisión requerida, presupuesto y personal capacitado. La técnica más sofisticada puede ser peor elección si no tenés las variables a tiempo o nadie la puede mantener.',
   svg=horizonte_svg(), chartLabel='Rangos de Chase'),
 C('Cualitativos', 'No es adivinar: es juicio con procedimiento.',
   'Chase lista cinco: acumulativo desde la fuerza de ventas, investigación de mercados, consenso o juicio ejecutivo, analogía histórica y Delphi. Sirven ante productos nuevos, cambios tecnológicos o falta de historia comparable.',
   svg=boxes([('Bottom-up','vendedores'),('Mercado','clientes'),('Consenso','ejecutivos'),('Analogía','caso similar'),('Delphi','expertos')], 'Métodos cualitativos de Chase', last=None),
   chartLabel='Chase cap. 15'),
 C('Delphi', 'Expertos por separado, en rondas, sin nombres.',
   'Consultás individualmente para evitar la presión del grupo, resumís sin decir quién opinó qué, devolvés el resumen y pedís revisión. Iterás. Consenso no es verdad: explicá los desacuerdos que quedan.',
   svg=delphi_svg(), chartLabel='Hanke cap. 10; procedimiento de Chase'),
 Q('¿Por qué Delphi consulta a cada experto por separado?',
   ['Para ahorrar tiempo de reunión', 'Para evitar la presión de un grupo reunido o de una jerarquía', 'Porque los expertos no se conocen'], 1,
   'El anonimato y la consulta individual protegen la información que una voz dominante podría silenciar.'),
 C('Combinar', 'Dos pronósticos pueden valer más que uno.',
   'Hanke trata la combinación. Ejemplo propio: si un método dice 480 y otro 520, el promedio simple da 500; con pesos 0,7 y 0,3, da 492. Los pesos se justifican con error sobre datos no usados para elegirlos.',
   formula=r'0{,}7\cdot480+0{,}3\cdot520=492',
   ejemplo='Ajustar «a ojo» sólo agrega valor si incorpora información que el modelo no tiene. Acercar el número a una meta comercial no lo hace más exacto.'),
 C('Sistema de pronósticos', 'Un sistema, no una fórmula.',
   'Hanke, cap. 11: nivel estratégico (qué, para qué, quién, qué precisión y costo) y nivel operativo (recopilar, depurar, modelar, emitir y evaluar). La evaluación vuelve al diagnóstico. Chase suma el pronóstico enfocado y CPFR para colaborar entre empresas.',
   svg=flow_v([('Definí la decisión','producto · horizonte'),('Registrá y depurá','SIG / ERP'),('Diagnosticá y elegí','patrón · costo'),('Ajustá y validá','error fuera del ajuste'),('Decidí y controlá','retroalimentación')], 'Sistema de pronósticos'),
   chartLabel='Esquema propio a partir de Hanke cap. 11'),
 Z('Llevate esto de la Clase 4.b.',
   'Pronóstico ≠ meta. Puntual, intervalo o densidad. Demanda independiente se pronostica, dependiente se calcula. Cualitativos con procedimiento; Delphi: anonimato, rondas, retroalimentación y agregación. Sistema con control y retroalimentación. Próxima: el Integrador.'),
]

# ======================= Clase 11 · RLS
def stack_svg():
    s = svg_open(100, 'SCT = SCR + SCE')
    s.append(txt(8, 13, 'Mascotas: SCT = SCR + SCE', 9, BL, bold=True))
    W = 256; a = W * 2.0535 / 3.0025
    s.append(f'<rect x="12" y="34" width="{a:.1f}" height="26" rx="4" fill="{OR}"/>')
    s.append(f'<rect x="{12+a:.1f}" y="34" width="{W-a:.1f}" height="26" rx="4" fill="{GR}" opacity=".6"/>')
    s.append(txt(12 + a / 2, 51, 'SCR 2,0535 · explicada', 8.5, '#111', 'middle', True))
    s.append(txt(12 + a + (W - a) / 2, 51, 'SCE 0,949', 8.5, '#111', 'middle', True))
    s.append(txt(12, 76, 'SCT = 3,0025', 8, GR)); s.append(txt(268, 76, 'R² = 2,0535 / 3,0025 = 0,684', 8.5, OR, 'end', True))
    s.append(txt(140, 93, 'R² es fracción de variabilidad muestral, no «precisión» del pronóstico', 7, GR, 'middle'))
    s.append('</svg>'); return ''.join(s)

pred_extra = (f'<rect x="{34+(5-0)*230/42:.1f}" y="26" width="{15*230/42:.1f}" height="104" fill="{GN}" opacity=".12"/>'
              + txt(34 + 12.5 * 230 / 42, 36, 'rango observado', 7, GN, 'middle')
              + f'<circle cx="{34+40*230/42:.1f}" cy="{130-(1.45+.074*40-1)*104/3.8:.1f}" r="4" fill="none" stroke="{YL}" stroke-width="1.6"/>'
              + txt(34 + 40 * 230 / 42 - 6, 130 - (1.45 + .074 * 40 - 1) * 104 / 3.8 + 14, 'x = 40: extrapolación', 7.5, YL, 'end', True))

H['clase11'] = [
 C('La idea', 'De «cuándo» a «según qué».',
   'Hasta acá la serie se explicaba con su propia historia. La regresión explica la media de Y según otra variable X. Sirve para pronosticar si vas a conocer X a tiempo. Y ojo: ajustar una recta no prueba causalidad.'),
 C('El modelo', 'Beta es de la población; b, de tu muestra.',
   'Beta cero y beta uno son parámetros que no conocés. b cero y b uno son sus estimaciones. Épsilon junta lo no medido y el azar; el residuo e es lo que calculás después del ajuste. No son lo mismo.',
   formula=r'Y_i=\beta_0+\beta_1x_i+ε_i',
   svg=boxes([('β₀, β₁','parámetros'),('b₀, b₁','estimaciones'),('ε ≠ e','error ≠ residuo')], 'Población vs. muestra'),
   chartLabel='Apunte 2013 / Bigatti'),
 C('Mínimos cuadrados', 'La recta que hace más chicos los cuadrados de los residuos.',
   'Cada segmento amarillo es un residuo: real menos ajustado. Mínimos cuadrados elige b cero y b uno para minimizar la suma de sus cuadrados. Con intercepto, los residuos suman cero… y eso no prueba que el modelo sea bueno.',
   svg=scatter(xx, yy, 1.45, .074, 'Mascotas: datos, recta y residuos', xl='espacio en góndola (dm)', resid=True),
   chartLabel='Apunte 2013 (Bigatti–Leale–Moine); redibujo propio'),
 C('Mascotas', 'Pendiente 0,074; intercepto 1,45.',
   'Con 12 datos: Sxy = 27,75 y Sxx = 375. La pendiente es 27,75 sobre 375 = 0,074. El intercepto, 2,375 − 0,074 · 12,5 = 1,45.',
   formula=r'b_1=\frac{S_{xy}}{S_{xx}}=\frac{27{,}75}{375}=0{,}074',
   svg=boxes([('Sxy = 27,75','covariación'),('Sxx = 375','variación en x'),('b₁ = 0,074','Sxy / Sxx')], 'Mascotas: calcular la pendiente'),
   chartLabel='Apunte 2013',
   ejemplo='Ŷ = 1,45 + 0,074x, con ventas en cientos de pesos y espacio en decímetros.'),
 Q('¿Cómo se lee b₁ = 0,074 en mascotas?',
   ['Cada dm extra garantiza 0,074 pesos más', 'Por cada dm adicional, la venta media estimada sube 0,074 cientos de pesos, o sea 7,40 pesos', 'El 7,4% de las ventas depende del espacio'], 1,
   'La pendiente tiene unidades de Y por unidad de X. Es una media estimada, dentro del rango observado, y no prueba causalidad sin diseño adecuado.'),
 C('¿Cuánto explica?', 'R² = 0,684.',
   'La variabilidad total (3,0025) se parte en lo asociado a x (2,0535) y lo no explicado (0,949). R² = 0,684: la recta explica el 68,4% de la variabilidad de esta muestra. r = 0,827.',
   svg=stack_svg(), chartLabel='Valores del apunte 2013'),
 Q('R² = 0,684. ¿Qué podés afirmar?',
   ['Que el pronóstico acierta el 68,4% de las veces', 'Que la recta explica el 68,4% de la variabilidad muestral de las ventas', 'Que el 68,4% de los puntos está sobre la recta'], 1,
   'R² compara SCE con SCT en la muestra. No es tasa de acierto, y un R² alto tampoco asegura buen pronóstico fuera del rango.'),
 C('Error típico', 'sₑ ≈ 0,3081: unos 30,81 pesos.',
   'El R² dice qué proporción explicás; sₑ dice cuánto se dispersan los puntos alrededor de la recta, en unidades de Y. Con n = 12 usa n − 2 = 10 grados de libertad porque estimaste dos coeficientes.',
   formula=r's_e=\sqrt{\frac{SCE}{n-2}}=\sqrt{\frac{0{,}949}{10}}',
   svg=boxes([('0,949 / 10','varianza residual'),('√0,0949','raíz'),('0,3081','sₑ, cientos de pesos')], 'Mascotas: de SCE a error típico'),
   chartLabel='Apunte 2013'),
 C('Residuos', 'Mirá los restos, no sólo la recta.',
   'Los residuos de mascotas oscilan entre −0,42 y +0,41 sin un patrón evidente por grupo de x. Así se empiezan a revisar los supuestos: media cero, varianza constante, independencia y normalidad para t y F.',
   svg=scatter(xx, res, 0, 0, 'Mascotas: residuos e = y − ŷ por x', xl='espacio (dm)', yr=(-.6,.6)),
   chartLabel='Residuos de la tabla de la Clase 11'),
 C('Pronosticar', 'x = 8 da 2,042; x = 13 da 2,412.',
   'Los dos x están dentro de 5 a 20 dm. Para x = 40 la cuenta sale, pero los datos no dicen nada de esa zona: es extrapolación. Y el número estima una media; una venta individual puede quedar lejos.',
   formula=r'\hat{Y}_0=1{,}45+0{,}074\cdot8=2{,}042',
   svg=scatter(xx, yy, 1.45, .074, 'Rango observado vs. extrapolación', xl='espacio (dm)', xr=(0,42), yr=(1,4.8), extra=pred_extra),
   chartLabel='Redibujo propio con la recta del apunte'),
 Q('Te piden la venta para x = 40 dm. ¿Qué respondés?',
   ['4,41, y listo', 'La cuenta da 4,41, pero es extrapolación: no hay datos que la respalden', 'No se puede calcular nada'], 1,
   '1,45 + 0,074 · 40 = 4,41. El número existe; su validez depende de suponer la misma relación lineal donde no observaste.'),
 C('Hanke', 'Precio y volumen: pendiente negativa.',
   'Con n = 10: Ŷ = 32,14 − 14,54X, r = −0,86 y r² = 0,746. Si el precio sube 1 peso, el volumen medio estimado baja 14,54 unidades. El signo de r y de b₁ coinciden siempre.',
   formula=r'R^2=1-\frac{59{,}42}{233{,}60}\approx0{,}746',
   svg=boxes([('r = −0,86','asociación negativa'),('b₁ = −14,54','pendiente negativa'),('R² = 0,746','sin signo')], 'Precio y volumen: signo y explicación'),
   chartLabel='Hanke en Resumen V6'),
 Z('Llevate esto de la Clase 11.',
   'b₁ = Sxy / Sxx, b₀ = ȳ − b₁x̄. Mascotas: Ŷ = 1,45 + 0,074x. R² = 0,684 explica variabilidad; sₑ = 0,308 mide dispersión. Pronóstico puntual = media condicional, dentro del rango. Próxima: inferencia.'),
]

# ======================= Clase 12 · Inferencia
def tdist_svg(tval=4.652, crit=2.2281):
    s = svg_open(130, 'Distribución t')
    s.append(txt(8, 13, 't con 10 gl: zona de rechazo al 5%', 9, BL, bold=True))
    X = lambda t: 140 + t * 24; Y = lambda d: 104 - d * 190
    dens = lambda t: math.gamma(5.5) / (math.sqrt(10 * math.pi) * math.gamma(5)) * (1 + t * t / 10) ** -5.5
    pts = [(X(t / 10), Y(dens(t / 10))) for t in range(-52, 53)]
    s.append(f'<polyline fill="none" stroke="{BL}" stroke-width="1.8" points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}"/>')
    for sg in (-1, 1):
        reg = [(X(t / 100), Y(dens(t / 100))) for t in range(int(crit * 100), 521)]
        if sg < 0: reg = [(280 - x, y) for x, y in reg]
        poly = ' '.join(f'{x:.1f},{y:.1f}' for x, y in reg)
        s.append(f'<polygon fill="{OR}" opacity=".45" points="{reg[0][0]:.1f},104 {poly} {reg[-1][0]:.1f},104"/>')
    s.append(f'<line x1="14" y1="104" x2="266" y2="104" stroke="{GD}"/>')
    for t in (-crit, crit):
        s.append(txt(X(t), 116, n(t, 3).replace('−', '−'), 7, OR, 'middle'))
    s.append(f'<line x1="{X(tval):.1f}" y1="40" x2="{X(tval):.1f}" y2="104" stroke="{YL}" stroke-width="2"/>')
    s.append(txt(X(tval), 34, f't = {n(tval,3)}', 8.5, YL, 'middle', True))
    s.append(txt(140, 127, 'Dibujo propio de la t de Student; valores de la clase', 6.8, GR, 'middle'))
    s.append('</svg>'); return ''.join(s)

def dw_svg():
    s = svg_open(118, 'Durbin-Watson')
    s.append(txt(8, 13, 'Durbin–Watson: autocorrelación positiva', 9, BL, bold=True))
    X = lambda d: 12 + d * 64
    for a, b, col, lab in ((0, 1.08, OR, 'rechazo'), (1.08, 1.36, YL, ''), (1.36, 4, GN, 'no rechazo')):
        s.append(f'<rect x="{X(a):.1f}" y="32" width="{X(b)-X(a):.1f}" height="20" fill="{col}" opacity=".35"/>')
        if lab: s.append(txt((X(a) + X(b)) / 2, 45, lab, 7.5, col, 'middle', True))
    s.append(txt(X(1.22), 62, 'inconcluso', 7, YL, 'middle', True))
    s.append(txt(X(1.08) - 1, 27, 'dL 1,08', 6.8, GR, 'end')); s.append(txt(X(1.36) + 1, 27, 'dU 1,36', 6.8, GR))
    for d in (0, 1, 2, 3, 4): s.append(txt(X(d), 74, str(d), 7, GR, 'middle'))
    s.append(f'<path d="M{X(.883):.1f} 78 l-4 8 h8 z" fill="{OR}"/>')
    s.append(txt(X(.883) - 6, 96, 'Clientes: D = 0,883', 8.5, OR, 'start', True))
    s.append(txt(268, 112, 'D ≈ 2: compatible con independencia de 1.er orden', 7, GR, 'end'))
    s.append('</svg>'); return ''.join(s)

xs = list(range(5, 21)); tt, se_, Sxx = 2.2281, .3081, 375
fit = [1.45 + .074 * x for x in xs]
icw = [tt * se_ * math.sqrt(1/12 + (x - 12.5) ** 2 / Sxx) for x in xs]
ipw = [tt * se_ * math.sqrt(1 + 1/12 + (x - 12.5) ** 2 / Sxx) for x in xs]
assert abs(fit[3] - icw[3] - 1.7876) < .001 and abs(fit[3] + ipw[3] - 2.7740) < .001

H['clase12'] = [
 C('La idea', 'Una pendiente distinta de cero en tu muestra no alcanza.',
   'b₁ = 0,074 podría salir por azar aunque en la población no hubiera relación. La inferencia pregunta: con este ruido y estos datos, ¿hay evidencia de que beta uno no es cero?',
   formula=r'H_0:\beta_1=0\qquad H_1:\beta_1\neq0'),
 C('El test t', 'Mascotas: t ≈ 4,652, bien lejos de 2,228.',
   'El error estándar de la pendiente es sₑ sobre raíz de Sxx: 0,3081 / raíz de 375 ≈ 0,01591. t = 0,074 / 0,01591 ≈ 4,652. Con 10 grados de libertad el crítico es 2,2281: rechazás H₀ (p ≈ 0,0009).',
   formula=r't=\frac{b_1}{s_{b_1}}=\frac{0{,}074}{0{,}01591}\approx4{,}652',
   svg=tdist_svg(), chartLabel='Apunte 2013; curva dibujada por mí'),
 Q('No rechazás H₀: β₁ = 0. ¿Eso prueba que no hay relación?',
   ['Sí: quedó demostrado que β₁ = 0', 'No: puede faltar potencia o haber mucha variabilidad', 'Sí, si n es mayor que 10'], 1,
   'No rechazar no es probar. Y al revés: rechazar no garantiza que el modelo sirva para decidir ni que haya causalidad.'),
 C('IC de la pendiente', 'Entre 3,90 y 10,90 pesos por decímetro.',
   'b₁ ± t · s_b = 0,074 ± 2,2281 · 0,01591 = (0,03855; 0,10945) cientos de pesos. No contiene el cero: coherente con el test al 5%.',
   formula=r'0{,}074\pm2{,}2281\cdot0{,}01591',
   svg=interval_rows([('β₁ (IC 95%)', .03855, .10945, OR, .074)], 'Intervalo para la pendiente', lo=-.01, hi=.13, ticks=(0, .04, .08, .12), zero=0, h=86, dec=2),
   chartLabel='Apunte 2013'),
 C('ANOVA', 'F = 21,64, que es t al cuadrado.',
   'Cuadrado medio de regresión 2,0535 sobre cuadrado medio del error 0,0949: F ≈ 21,64. En regresión simple con intercepto, F = t²: 4,652² ≈ 21,64. En múltiple ya no: ahí F prueba todas las pendientes juntas.',
   formula=r'F=\frac{2{,}0535/1}{0{,}949/10}\approx21{,}64',
   svg=boxes([('SCR / 1','2,0535'),('SCE / 10','0,0949'),('F ≈ 21,64','= 4,652²')], 'ANOVA en mascotas'),
   chartLabel='Apunte 2013'),
 Q('En regresión simple con intercepto, F y t de la pendiente…',
   ['Son pruebas distintas que pueden contradecirse', 'Son la misma prueba: F = t²', 'F siempre es t multiplicado por 2'], 1,
   '4,652² ≈ 21,64. Esa equivalencia es exclusiva del caso de una sola X; en RLM la F global y las t individuales responden preguntas distintas.'),
 C('IC vs. IP', 'La media es más fácil de acertar que una venta.',
   'Para x = 8: IC de la media (1,79; 2,30), IP de una observación nueva (1,31; 2,77). El IP es más ancho porque suma el error de una venta individual. Ambos se ensanchan al alejarte de x̄ = 12,5.',
   svg=line_chart([('Ajuste',fit,OR,False),('IC 95%',[f-w for f,w in zip(fit,icw)],BL,True),('',[f+w for f,w in zip(fit,icw)],BL,True),('IP 95%',[f-w for f,w in zip(fit,ipw)],GR,True),('',[f+w for f,w in zip(fit,ipw)],GR,True)], [str(x) for x in xs], 'Mascotas: bandas de confianza y predicción', every=5, h=160),
   chartLabel='Bandas calculadas por mí con los valores del apunte'),
 Q('Querés acotar la venta de UN comercio con x = 13. ¿Qué intervalo usás?',
   ['El IC de la media: (2,21; 2,61)', 'El IP: (1,70; 3,13)', 'Cualquiera, son iguales'], 1,
   'Una observación individual pide intervalo de predicción, que incluye la variabilidad propia de ese caso. El IC habla del promedio de comercios con x = 13.'),
 C('Residuos', 'Lo que el R² no te muestra.',
   'Residuos contra ajustados: buscás una nube pareja alrededor de cero. Curvatura o embudo piden revisar el modelo o transformar (log y, raíz de y, 1 sobre y). Gráfica normal: puntos aproximadamente rectos. Contra el tiempo: patrón temporal.',
   svg=boxes([('OK','nube pareja'),('Embudo','varianza crece'),('Curva','falta forma'),('Ola','autocorrelación')], 'Qué buscás en un gráfico de residuos', last=None),
   chartLabel='Tabla de diagnóstico de la Clase 12'),
 C('Durbin–Watson', 'Clientes y ventas: D = 0,883.',
   'Con 15 semanas, D = 10,058 / 11,39 ≈ 0,883. Como queda debajo de dL = 1,08, hay evidencia de autocorrelación positiva: los errores no son independientes.',
   svg=dw_svg(), chartLabel='Diapositivas de Bigatti; verificado por mí'),
 Q('En mascotas, el docx informa D = 2,50864. ¿Cómo lo leés?',
   ['Independencia confirmada', 'Con cautela: esos datos son grupos de espacio, no una secuencia temporal', 'Autocorrelación negativa segura'], 1,
   'Durbin–Watson necesita un orden con sentido (tiempo). Calculado sobre un orden arbitrario, da un número sin interpretación.'),
 C('Palanca y Cook', 'Lejos en x no es lo mismo que lejos en y.',
   'Un atípico está lejos verticalmente; un punto de alta palanca, lejos en x. En mascotas, h = 0,2333 en los extremos (5 y 20 dm) y 0,1 en el centro. La máxima distancia de Cook es ≈ 0,369, debajo de 1.',
   svg=bars([('x = 5',.2333,OR),('x = 10',.1,BL),('x = 15',.1,BL),('x = 20',.2333,OR)], 'Palanca hᵢ = 1/n + (x − x̄)² / Sxx', fmt=lambda v: n(v,3), yr=(0,.3)),
   chartLabel='Complemento verificado por mí con la definición estándar'),
 Z('Llevate esto de la Clase 12.',
   't = b₁ / s_b: 4,652 > 2,228, rechazás H₀. IC de β₁: (0,039; 0,109). En simple F = t². IP más ancho que IC. Residuos y Durbin–Watson (sólo con orden temporal). Palanca ≠ atípico. Próxima: regresión múltiple.'),
]

# ======================= Clase 13 · RLM
def dummy_svg():
    s = svg_open(140, 'Variable indicadora')
    s.append(txt(8, 13, 'Una dummy corre el intercepto', 9, BL, bold=True))
    X = lambda v: 30 + v * 2.3; Y = lambda v: 118 - (v + 4.5) * 6
    for j, (b0, col, lab) in enumerate(((-1.96, BL, 'X₂ = 0: Ŷ = −1,96 + 0,12X₁'), (-4.14, OR, 'X₂ = 1: Ŷ = −4,14 + 0,12X₁'))):
        s.append(f'<line x1="{X(0):.1f}" y1="{Y(b0):.1f}" x2="{X(100):.1f}" y2="{Y(b0+12):.1f}" stroke="{col}" stroke-width="2"/>')
        s.append(txt(12, 32 + j * 11, lab, 7.8, col, 'start', True))
    s.append(f'<path d="M{X(60):.1f} {Y(-1.96+7.2):.1f} V{Y(-4.14+7.2):.1f}" stroke="{YL}" stroke-width="1.4"/>')
    s.append(txt(X(60) + 5, (Y(-1.96 + 7.2) + Y(-4.14 + 7.2)) / 2 + 3, '−2,18', 8, YL, bold=True))
    s.append(f'<line x1="30" y1="122" x2="262" y2="122" stroke="{GD}"/>')
    s.append(txt(146, 134, 'X₁ (puntaje). Rectas paralelas: misma pendiente', 7, GR, 'middle'))
    s.append('</svg>'); return ''.join(s)

vif_r = [i / 20 for i in range(0, 19)]
H['clase13'] = [
 C('La idea', 'Varias X, cada una «con las demás quietas».',
   'En regresión múltiple cada coeficiente mide un efecto parcial: el cambio promedio de Y por unidad de esa X, manteniendo constantes las otras. Si dos X se mueven siempre juntas, esa condición puede quedar lejos de tus datos.',
   formula=r'Y_i=\beta_0+\beta_1x_{i1}+\ldots+\beta_kx_{ik}+ε_i'),
 C('Grados de libertad', 'Se pierden k + 1: las pendientes y el intercepto.',
   'k cuenta las variables explicativas, sin el intercepto. El error residual usa n − k − 1. En la versión matricial, X lleva una columna de unos para el intercepto.',
   formula=r's_e^2=\frac{SCE}{n-k-1}',
   svg=boxes([('n = 25','observaciones'),('k + 1 = 3','coeficientes'),('gl = 22','25 − 3')], 'Gaseosas: 2 X y un intercepto'),
   chartLabel='Ejemplo de Bigatti'),
 Q('Tenés 25 entregas y 2 variables explicativas. ¿Grados de libertad del error?',
   ['23', '22', '25'], 1,
   'n − k − 1 = 25 − 2 − 1 = 22. Es el caso de gaseosas.'),
 C('Gaseosas', 'Tiempo de entrega según cajas y distancia.',
   'Con 25 entregas de las diapositivas de Bigatti: Ŷ = 2,309 + 2,740 cajas + 0,0124 metros. R² = 0,9811 y sₑ = 2,287. Cada punto compara el tiempo observado con el ajustado: cerca de la diagonal, buen ajuste.',
   formula=r'\hat{Y}=2{,}309+2{,}740X_1+0{,}0124X_2',
   svg=scatter(gF, gY, 0, 1, 'Gaseosas: observado vs. ajustado', xl='tiempo ajustado', xr=(5,72), yr=(5,72), xticks=(10,30,50,70)),
   chartLabel='Datos de Bigatti (2012); ajuste verificado por mí. Línea = diagonal'),
 Q('Mismas cajas, 100 metros más de recorrido. ¿Cuánto cambia el tiempo esperado?',
   ['+0,0124', '+1,24', '+2,74'], 1,
   '100 · 0,0124 = 1,24 unidades de tiempo, con las cajas constantes. El 2,74 corresponde a una caja más con la misma distancia.'),
 C('F primero, t después', 'F global ≈ 570,7. Después mirás cada t.',
   'F prueba si al menos una pendiente es distinta de cero. Si es significativa, revisás las t individuales: cajas 29,32 y distancia 4,45, ambas bien por encima del crítico ≈ 2,074.',
   svg=bars([('Intercepto',2.18,GR),('Cajas',29.32,OR),('Distancia',4.45,BL)], 't de cada término (22 gl)', ref=(2.074,'crítico ≈ 2,074'), fmt=lambda v: n(v,2)),
   chartLabel='Bigatti (2012), salida de R'),
 C('R² ajustado', 'Agregar variables siempre sube el R². El ajustado cobra por eso.',
   'Hanke: con R² = 0,932, n = 10 y k = 2, el R² ajustado baja a 0,912. Penaliza la complejidad. En gaseosas: 0,9811 contra 0,9794.',
   formula=r'R^2_{aj}=1-(1-0{,}932)\frac{9}{7}=0{,}912',
   svg=bars([('Hanke|R²',.932,BL),('Hanke|R²aj',.912,OR),('Gaseosas|R²',.9811,BL),('Gaseosas|R²aj',.9794,OR)], 'Ajuste y penalización (misma escala)', fmt=lambda v: n(v,3), yr=(0,1.1)),
   chartLabel='Hanke / V6 y Bigatti'),
 C('Multicolinealidad', 'Cuando dos X dicen lo mismo.',
   'VIF = 1 / (1 − Rⱼ²), donde Rⱼ² es cuánto explican las otras X a la X j. Con Rⱼ² = 0,90, VIF = 10. En gaseosas cajas y distancia correlacionan ≈ 0,378 y el VIF es ≈ 1,167: sin problema.',
   svg=line_chart([('VIF',[1/(1-r) for r in vif_r],OR,False)], [n(r,2) if i % 6 == 0 else '' for i, r in enumerate(vif_r)], 'VIF según Rⱼ²', marks=[(18,10,'Rⱼ² 0,90 → 10',YL),((1-1/1.167)*20,1.167,'gaseosas ≈ 1,17',GN)], every=1),
   chartLabel='Curva de la fórmula del V6; punto de gaseosas verificado por mí'),
 Q('VIF = 10 significa que…',
   ['La Y tiene R² = 90%', 'El 90% de la variación de esa X se explica con las otras X', 'El pronóstico se equivoca por 10 unidades'], 1,
   'VIFⱼ = 1 / (1 − Rⱼ²). Si VIF = 10, Rⱼ² = 0,90. Es una regresión de una X contra las otras X, no de Y.'),
 C('Intervalos', '8 cajas y 275 metros.',
   'Tiempo medio estimado 27,65. IC 95% para la media de entregas así: 26,65 a 28,65. IP 95% para UNA entrega: 22,81 a 32,50. Y la combinación de X tiene que parecerse a las observadas.',
   svg=interval_rows([('IC media', 26.65, 28.65, BL, 27.653), ('IP entrega', 22.81, 32.50, OR, 27.653)], 'Gaseosas, x₀ = (8 cajas; 275 m)', lo=20, hi=35, ticks=(20, 25, 30, 35), dec=2),
   chartLabel='Diapositiva de Bigatti; verificado por mí'),
 C('Dummies', 'Una variable 0 / 1 cambia el intercepto.',
   'Hanke: Ŷ = −1,96 + 0,12X₁ − 2,18X₂, con X₂ = 0 o 1 según el grupo. Quedan dos rectas paralelas separadas por 2,18. Con c categorías e intercepto usás c − 1 dummies.',
   svg=dummy_svg(), chartLabel='Ejemplo de Hanke en el V6; dibujo propio'),
 Q('Una variable tiene 3 categorías y el modelo tiene intercepto. ¿Cuántas dummies?',
   ['3', '2', '1'], 1,
   'c − 1 = 2. La categoría que queda afuera es la de referencia. Con las 3 tendrías colinealidad perfecta.'),
 C('Viviendas', 'F significativa y ninguna t significativa.',
   'Salida estudiantil: precio con dormitorios, superficie cubierta y de lote. F = 40,72 significativa, pero p de 0,742, 0,167 y 0,805, con VIF 83,23 y 78,99 en las superficies. Juntas explican; por separado no se distinguen: redundancia.',
   ejemplo='Resolución estudiantil, no oficial. Se sigue en la Clase 14 con la grilla de siete modelos.'),
 Z('Llevate esto de la Clase 13.',
   'bⱼ = efecto parcial con las demás constantes. Error con n − k − 1. F global primero, t individuales después. R² ajustado penaliza. VIF = 1 / (1 − Rⱼ²). Dummies: c − 1 y una referencia. Próxima: validación y comparación.'),
]

# ======================= Clase 14 · Validación
combos = ['D·SC·SL', 'D·SC', 'D·SL', 'SC·SL', 'D', 'SC', 'SL']
def combos_svg():
    s = svg_open(124, 'Siete modelos')
    s.append(txt(8, 13, '3 variables → 2³ − 1 = 7 modelos (grilla RLM_Ej8)', 9, BL, bold=True))
    for i, c in enumerate(combos):
        x = 8 + (i % 4) * 67; y = 24 + (i // 4) * 40
        col = OR if i == 0 else (BL if i < 4 else GN)
        s.append(f'<rect x="{x}" y="{y}" width="61" height="32" rx="7" fill="{col}22" stroke="{col}"/>')
        s.append(txt(x + 30.5, y + 20, c, 9, col, 'middle', True))
    s.append(txt(140, 118, 'D = dormitorios · SC = sup. cubierta · SL = sup. del lote', 7, GR, 'middle'))
    s.append('</svg>'); return ''.join(s)

def overfit_svg():
    s = svg_open(130, 'Sobreajuste')
    s.append(txt(8, 13, 'Sobreajuste (esquema)', 9, BL, bold=True))
    xs_ = list(range(10))
    fit_e = [100 - 9 * i + .2 * i * i for i in xs_]
    test_e = [100 - 11 * i + 1.35 * i * i for i in xs_]
    X = lambda i: 36 + i * 24; Y = lambda v: 112 - v * .8
    for vals, col, lab in ((fit_e, BL, 'error de ajuste'), (test_e, OR, 'error en datos nuevos')):
        s.append(f'<polyline fill="none" stroke="{col}" stroke-width="2" points="{" ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(vals))}"/>')
        s.append(txt(X(9) - 2, Y(vals[9]) - 5, lab, 7.5, col, 'end', True))
    s.append(f'<line x1="36" y1="112" x2="262" y2="112" stroke="{GD}"/>')
    s.append(txt(150, 124, 'más variables / más complejidad →', 7.5, GR, 'middle'))
    s.append('</svg>'); return ''.join(s)

gcook = [0.033,0.012,0.059,0.019,0.024,0.007,0.036,0.019,0.16,0.001,0.012,0.001,0.002,0.003,0.186,0.001,0.589,0.153,0.017,0.0,0.05,0.03,0.0,0.04,0.0]
H['clase14'] = [
 C('La idea', 'El mejor modelo no es el de más variables.',
   'Hanke plantea dos fuerzas: sumar variables que aporten exactitud y conservar pocas, porque medirlas y monitorearlas cuesta. Gana el modelo coherente, con supuestos razonables y que pronostica bien fuera de su ajuste.'),
 C('Tres pasos', 'Juntar, depurar, reducir y validar.',
   'Reunís X justificadas. Descartás las no fundamentales, duplicadas, con grandes errores de medición o difíciles de medir. Reducís a la mejor combinación y la validás.',
   svg=boxes([('Reunir','X justificadas'),('Depurar','duplicadas, caras'),('Reducir','mejor combinación'),('Validar','fuera del ajuste')], 'Selección de variables (Hanke)')),
 C('Todas las posibles', 'Con 3 variables hay 7 modelos.',
   'Todas las regresiones posibles examina cada combinación no vacía: 2 a la p, menos 1. La grilla RLM_Ej8 tiene justamente esas siete columnas. Por pasos agrega o saca de a una variable: más rápido, pero puede no hallar la mejor combinación global.',
   formula=r'2^p-1=2^3-1=7', svg=combos_svg(), chartLabel='Grilla RLM_Ej8 (material); conteo verificado por mí'),
 Q('Con 4 predictores candidatos, ¿cuántos modelos examina «todas las posibles»?',
   ['8', '15', '16'], 1,
   '2⁴ − 1 = 15 combinaciones no vacías. Crece rápido y, con tantas pruebas, también el riesgo de elegir por azar.'),
 C('Gaseosas: ¿suma la distancia?', 'Tres modelos, tres errores típicos.',
   'Sólo cajas: sₑ 3,082 y R²aj 0,9625. Sólo distancia: sₑ 14,157 y R²aj 0,2094. Las dos: sₑ 2,287 y R²aj 0,9794. La distancia sola explica poco, pero junto a las cajas mejora.',
   svg=bars([('Cajas',3.082,BL),('Distancia',14.157,GR),('Cajas +|distancia',2.287,OR)], 'Error típico sₑ (más bajo = mejor)', fmt=lambda v: n(v,3)),
   chartLabel='Cálculo propio con las 25 observaciones de Bigatti'),
 C('F parcial', 'Agregar distancia: F parcial ≈ 19,78 = t².',
   'SCE del modelo reducido ≈ 218,49 y del completo ≈ 115,05, con un término agregado: F parcial ≈ 19,78, que es 4,45² (la t de distancia). Con un solo término, F parcial y t² son la misma prueba.',
   formula=r'F_{parcial}=\frac{(218{,}49-115{,}05)/1}{115{,}05/22}\approx19{,}78',
   svg=bars([('Sólo cajas',218.49,BL),('Cajas + distancia',115.05,OR)], 'SCE en los mismos 25 datos', fmt=lambda v: n(v,2), h=110),
   chartLabel='Cálculo propio con los datos de Bigatti'),
 Q('La distancia da significativa. ¿Ya sabés si conviene registrarla?',
   ['Sí: significativa = conveniente', 'No: falta comparar la mejora con el costo de medirla', 'No: hay que sacarla porque su t es menor que la de cajas'], 1,
   'La significación dice que aporta información estadística. Si vale el costo de medirla y tenerla a tiempo es otra pregunta: es la segunda fuerza de Hanke.'),
 C('Validar con datos nuevos', 'Ajustás con 20 y probás con 5.',
   'Complemento calculado por mí, no protocolo de la cátedra: ajustando con las primeras 20 entregas y probando en las 5 restantes, sólo cajas da RMSE ≈ 2,341 y cajas más distancia ≈ 1,567. La mejora se sostiene fuera del ajuste.',
   svg=bars([('Cajas',2.341,BL),('Cajas + distancia',1.567,OR)], 'RMSE en las 5 entregas retenidas', fmt=lambda v: n(v,3), h=120),
   chartLabel='Partición ilustrativa en orden, no aleatoria'),
 C('Diagnóstico', 'El mejor ajuste puede tener puntos que miran feo.',
   'Gaseosas: residuos estandarizados de 2,65 (obs. 15) y 2,25 (obs. 17). Mayor palanca: obs. 18, h ≈ 0,293. Mayor Cook: obs. 17, ≈ 0,589, debajo de 1. DW = 2,1312. No se borran: se investigan.',
   svg=bars([(str(i+1) if (i+1) in (9,15,17,18) else '', v, OR if v == max(gcook) else BL) for i, v in enumerate(gcook)], 'Distancia de Cook por observación', ref=(1,'orientación Dᵢ = 1'), fmt=lambda v: n(v,2) if v > .15 else '', yr=(0,1.1)),
   chartLabel='Cook calculado por mí con la definición estándar; DW de la diapositiva'),
 C('Sobreajuste', 'Brilla en la muestra, falla afuera.',
   'Agregar variables que siguen excentricidades de la muestra baja el error de ajuste y sube el de pronóstico. El V6 sugiere al menos 10 observaciones por variable y evaluar con datos no usados. En series de tiempo, ajustás con el pasado y probás con lo posterior.',
   svg=overfit_svg(), chartLabel='Esquema propio, no son datos'),
 Q('El modelo con mayor R² dentro de la muestra, ¿ya está validado?',
   ['Sí, es el mejor por definición', 'No: el R² dentro de muestra no es validación', 'Sí, si además tiene F significativa'], 1,
   'Validar es medir el error en datos que no usaste para ajustar, con el horizonte y las variables que vas a tener al pronosticar.'),
 C('Viviendas', 'Una conclusión prudente.',
   'Respuesta guía propia, no clave oficial: estimá los siete modelos de la grilla y compará supuestos, influencia, F, t, R² ajustado y error de validación. Con lo que hay: «el modelo completo explica conjuntamente, pero no separa efectos; hay que comparar modelos reducidos».'),
 Z('Llevate esto de la Clase 14 y de la Unidad 2.',
   'Elegís con validez, significación, ajuste penalizado, simplicidad y error fuera de muestra. 3 variables = 7 modelos. F parcial = t² con un término. Diagnóstico antes de borrar. Y en series y en regresión: medí donde el modelo no miró. ¡Unidad 2 cerrada!'),
]

def main():
    for name, cards in H.items():
        p = U2 / f'{name}.json'
        d = json.loads(p.read_text(encoding='utf-8'))
        assert 9 <= len(cards) <= 16, (name, len(cards))
        assert cards[-1]['type'] == 'cierre'
        for c in cards:
            if c['type'] == 'pregunta':
                assert 0 <= c['correct'] < len(c['options'])
        d['historias'] = cards
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'{name}: {len(cards)} tarjetas, {sum(1 for c in cards if c.get("svg"))} con gráfico, {sum(1 for c in cards if c["type"]=="pregunta")} preguntas')

if __name__ == '__main__':
    main()
