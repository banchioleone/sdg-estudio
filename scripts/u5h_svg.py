"""Gráficos (SVG inline) para las historias de la U5. Redibujos propios con datos
del material (Chase 12a ed. y finales) o esquemas rotulados como tales."""
import math
from gen_u2_historias import n, txt, svg_open, line_chart, bars, boxes, flow_v, interval_rows, BL, OR, GR, GD, GN, YL, E

def _axes(s, x0, y0, x1, y1):
    s.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{GD}"/>')
    s.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="{GD}"/>')

def sierra(Q=250, R=150, d=30, L=5, days=25, title='BIT-Kaffee: Q = 250, PP = 150'):
    h = 160; x0, x1, y0, y1 = 34, 268, 26, h - 30
    X = lambda t: x0 + t * (x1 - x0) / days; Y = lambda v: y1 - v * (y1 - y0) / (Q * 1.1)
    s = svg_open(h, title); s.append(txt(8, 13, title, 9, BL, bold=True)); _axes(s, x0, y0, x1, y1)
    cyc = Q / d; pts = []; t = 0
    while t < days:
        pts += [(t, Q), (min(t + cyc, days), Q - d * (min(t + cyc, days) - t))]; t += cyc
    p = ' '.join(f'{X(a):.1f},{Y(b):.1f}' for a, b in pts)
    s.append(f'<polyline fill="none" stroke="{BL}" stroke-width="2" points="{p}"/>')
    s.append(f'<line x1="{x0}" x2="{x1}" y1="{Y(R):.1f}" y2="{Y(R):.1f}" stroke="{YL}" stroke-dasharray="5 3"/>')
    s.append(txt(x1, Y(R) - 4, f'PP = {R}', 7.5, YL, 'end', True))
    t = (Q - R) / d; k = 0
    while t + L <= days + 1e-9:
        s.append(f'<circle cx="{X(t):.1f}" cy="{Y(R):.1f}" r="3.5" fill="{OR}"/>')
        s.append(f'<path d="M{X(t):.1f} {y1+6} L{X(t+L):.1f} {y1+6}" stroke="{OR}" stroke-width="1.4"/>')
        if k == 0: s.append(txt((X(t) + X(t + L)) / 2, y1 + 16, f'L = {L} días', 7, OR, 'middle', True))
        t += cyc; k += 1
    s.append(txt(x0 - 4, Y(Q) + 3, Q, 7, GR, 'end')); s.append(txt(x0 - 4, y1 + 3, 0, 7, GR, 'end'))
    s.append(txt(x1, y1 + 16, 'días', 7, GR, 'end'))
    s.append(txt(X(cyc) + 4, Y(Q) - 3, 'llega Q', 7.5, BL, 'start', True))
    s.append('</svg>'); return ''.join(s)

def desc_libreria():
    """CT por caja de la librería: una curva por precio; tramo factible en trazo lleno."""
    h = 170; x0, x1, y0, y1 = 36, 266, 26, h - 34; qa, qb = 20, 160; lo, hi = 7.2, 8.4
    X = lambda q: x0 + (q - qa) * (x1 - x0) / (qb - qa); Y = lambda v: y1 - (v - lo) * (y1 - y0) / (hi - lo)
    ct = lambda c, q: c + 16 / q + c * 0.36 * q / 1200
    s = svg_open(h, 'Librería: costo por caja'); s.append(txt(8, 13, 'Librería: costo total por caja', 9, BL, bold=True)); _axes(s, x0, y0, x1, y1)
    for v in (7.4, 7.6, 7.8, 8.0, 8.2):
        s.append(f'<line x1="{x0}" x2="{x1}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{GD}" stroke-width=".4"/>'); s.append(txt(x0 - 4, Y(v) + 3, n(v, 1), 7, GR, 'end'))
    for (c, a, b, col) in ((7.50, 1, 49, GR), (7.35, 50, 99, BL), (7.00, 100, 1e9, OR)):
        full = ' '.join(f'{X(q):.1f},{Y(ct(c,q)):.1f}' for q in range(qa, qb + 1, 2))
        s.append(f'<polyline fill="none" stroke="{col}" stroke-width="1" stroke-dasharray="3 3" opacity=".6" points="{full}"/>')
        seg = ' '.join(f'{X(q):.1f},{Y(ct(c,q)):.1f}' for q in range(max(qa, a), int(min(qb, b)) + 1))
        s.append(f'<polyline fill="none" stroke="{col}" stroke-width="2.4" points="{seg}"/>')
    for q, v, lab, col in ((85, ct(7.35, 85), '85 → 7,73', BL), (100, ct(7.0, 100), '100 → 7,37', OR)):
        s.append(f'<circle cx="{X(q):.1f}" cy="{Y(v):.1f}" r="4" fill="none" stroke="{col}" stroke-width="1.8"/>')
        s.append(txt(X(q) + 6, Y(v) + (12 if col == OR else -6), lab, 8, col, 'start', True))
    for q in (50, 100, 150): s.append(txt(X(q), y1 + 11, q, 7, GR, 'middle'))
    s.append(txt(x1, y1 + 22, 'cajas por pedido', 7, GR, 'end'))
    lx = 8
    for lab, col in (('7,50', GR), ('7,35', BL), ('7,00', OR)):
        s.append(f'<line x1="{lx}" y1="{h-9}" x2="{lx+12}" y2="{h-9}" stroke="{col}" stroke-width="2"/>'); s.append(txt(lx + 15, h - 6, lab, 7.5, col)); lx += 46
    s.append('</svg>'); return ''.join(s)

def qvsp():
    h = 188; s = svg_open(h, 'Perpetuo vs periódico (esquema)')
    s.append(txt(8, 13, 'Perpetuo: misma Q, fechas que cambian', 8.6, BL, bold=True))
    s.append(txt(8, 104, 'Periódico: fechas fijas, cantidades que cambian', 8.6, OR, bold=True))
    # perpetuo: pendientes distintas, salto fijo de 60 (de 15 a 75), R = 30
    x0, y1, sc = 20, 92, .9
    Yp = lambda v: y1 - v * sc
    x = x0; pts = [(x, Yp(75))]
    for sl in (1.0, 0.55, 1.5, 0.8):
        xr = x + 45 / sl; x2 = x + 60 / sl
        if x2 > 262: break
        s.append(f'<circle cx="{xr:.1f}" cy="{Yp(30):.1f}" r="2.6" fill="{YL}"/>')
        pts += [(x2, Yp(15)), (x2, Yp(75))]
        s.append(f'<line x1="{x2:.1f}" x2="{x2:.1f}" y1="{Yp(15):.1f}" y2="{Yp(75):.1f}" stroke="{BL}" stroke-width="3" opacity=".35"/>')
        s.append(txt(x2, y1 + 6, 'Q', 7, GR, 'middle')); x = x2
    s.append(f'<polyline fill="none" stroke="{BL}" stroke-width="1.8" points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in pts)}"/>')
    s.append(f'<line x1="{x0}" x2="268" y1="{Yp(30):.1f}" y2="{Yp(30):.1f}" stroke="{YL}" stroke-dasharray="4 3"/>')
    s.append(txt(268, Yp(30) - 3, 'R', 7.5, YL, 'end', True))
    # periódico: revisión cada 60 px, sube hasta M=75
    y1b = 180; x = x0; lvl = 75; pts = [(x, y1b - lvl * sc)]
    for sl in (0.55, 0.9, 0.4, 0.75):
        x2 = x + 60; lvl2 = lvl - sl * 60; pts += [(x2, y1b - lvl2 * sc), (x2, y1b - 75 * sc)]
        s.append(f'<line x1="{x2:.1f}" x2="{x2:.1f}" y1="{y1b-lvl2*sc:.1f}" y2="{y1b-75*sc:.1f}" stroke="{OR}" stroke-width="3" opacity=".35"/>')
        s.append(txt(x2, y1b + 6, 'T', 7, GR, 'middle')); x = x2; lvl = 75
    s.append(f'<polyline fill="none" stroke="{OR}" stroke-width="1.8" points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in pts)}"/>')
    s.append(f'<line x1="{x0}" x2="268" y1="{y1b-75*sc:.1f}" y2="{y1b-75*sc:.1f}" stroke="{GR}" stroke-dasharray="4 3"/>')
    s.append(txt(268, y1b - 75 * sc - 3, 'máximo', 7, GR, 'end'))
    s.append('</svg>'); return ''.join(s)

def normal(mu, sd, R, z, title, ns, lo=None, hi=None):
    h = 160; x0, x1, y0, y1 = 14, 266, 28, h - 34
    lo = lo if lo is not None else mu - 3.2 * sd; hi = hi if hi is not None else mu + 3.2 * sd
    X = lambda v: x0 + (v - lo) * (x1 - x0) / (hi - lo); f = lambda v: math.exp(-((v - mu) / sd) ** 2 / 2)
    Y = lambda p: y1 - p * (y1 - y0)
    s = svg_open(h, title); s.append(txt(8, 13, title, 9, BL, bold=True))
    vs = [lo + (hi - lo) * k / 120 for k in range(121)]
    area = [v for v in vs if v <= R] + [R]
    s.append(f'<path d="M{X(lo):.1f},{y1} ' + ' '.join(f'L{X(v):.1f},{Y(f(v)):.1f}' for v in area) + f' L{X(R):.1f},{y1} Z" fill="{BL}" opacity=".28"/>')
    s.append(f'<polyline fill="none" stroke="{BL}" stroke-width="2" points="' + ' '.join(f'{X(v):.1f},{Y(f(v)):.1f}' for v in vs) + '"/>')
    s.append(f'<line x1="{x0}" x2="{x1}" y1="{y1}" y2="{y1}" stroke="{GD}"/>')
    for v, col, lab in ((mu, GR, n(mu, 0)), (R, OR, n(R, 0))):
        s.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{y0-2}" y2="{y1}" stroke="{col}" stroke-width="1.3" stroke-dasharray="4 3"/>')
        s.append(txt(X(v), y1 + 11, lab, 7.5, col, 'middle', True))
    s.append(f'<path d="M{X(mu):.1f} {y0+8} L{X(R):.1f} {y0+8}" stroke="{YL}" stroke-width="1.6"/>')
    s.append(txt((X(mu) + X(R)) / 2, y0 + 4, 'SS', 8, YL, 'middle', True))
    s.append(txt(X(mu) - 8, y1 - 22, ns, 9, BL, 'end', True))
    s.append(txt(X(R) + 4, y1 - 8, 'falta', 7, OR))
    s.append(txt(x1, h - 8, f'z = {z} · demanda en el lead time', 7, GR, 'end'))
    s.append('</svg>'); return ''.join(s)

def centroide():
    pts = [('Long Beach', 325, 75, 1500), ('Anaheim', 400, 150, 250), ('La Habra', 450, 350, 450), ('Glendale', 350, 400, 350), ('Thousand Oaks', 25, 450, 450)]
    h = 200; x0, x1, y0, y1 = 30, 266, 24, h - 22
    X = lambda v: x0 + v * (x1 - x0) / 500; Y = lambda v: y1 - v * (y1 - y0) / 500
    s = svg_open(h, 'HiOctane: centroide'); s.append(txt(8, 13, 'HiOctane: el centroide pesa por volumen', 9, BL, bold=True)); _axes(s, x0, y0, x1, y1)
    cx, cy = 923750 / 3000, 650000 / 3000
    for nm, x, y, v in pts:
        s.append(f'<line x1="{X(x):.1f}" y1="{Y(y):.1f}" x2="{X(cx):.1f}" y2="{Y(cy):.1f}" stroke="{GD}" stroke-width=".8"/>')
    for nm, x, y, v in pts:
        r = 3 + math.sqrt(v) / 4
        s.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="{r:.1f}" fill="{BL}" opacity=".55" stroke="{BL}"/>')
        dx, dy, anc = {'Long Beach': (r + 4, 4, 'start'), 'Anaheim': (r + 4, 4, 'start'), 'La Habra': (0, r + 10, 'middle'),
                       'Glendale': (0, -r - 4, 'middle'), 'Thousand Oaks': (r + 4, 4, 'start')}[nm]
        s.append(txt(X(x) + dx, Y(y) + dy, f'{nm} ({v})', 7, GR, anc))
    s.append(f'<path d="M{X(cx):.1f} {Y(cy)-7:.1f} l2 5 5 .5 -4 3.5 1.5 5 -4.5 -3 -4.5 3 1.5 -5 -4 -3.5 5 -.5z" fill="{OR}"/>')
    s.append(txt(X(cx) - 9, Y(cy) + 3, 'centroide (308; 217)', 8.5, OR, 'end', True))
    for v in (0, 250, 500): s.append(txt(X(v), y1 + 10, v, 7, GR, 'middle'))
    s.append('</svg>'); return ''.join(s)

def latigo():
    xs = list(range(13))
    ser = [('Consumidor', [100 + 6 * math.sin(i / 1.7) for i in xs], GR, False),
           ('Detallista', [100 + 14 * math.sin(i / 1.7 - .5) for i in xs], BL, False),
           ('Mayorista', [100 + 26 * math.sin(i / 1.7 - 1) for i in xs], OR, False)]
    sv = line_chart(ser, title='Efecto látigo: la variación crece aguas arriba', h=150, yr=(70, 130))
    return sv

def waterfall(items, title, h=150, unit=''):
    """items: (label, delta, color, is_total)."""
    x0, x1, y0, y1 = 12, 268, 30, h - 30; acc = 0; tops = []
    for lab, dv, col, tot in items:
        a, b = (0, dv) if tot else (acc, acc + dv); tops.append((a, b)); acc = b if not tot else dv
    hi = max(max(a, b) for a, b in tops) * 1.12
    Y = lambda v: y1 - v * (y1 - y0) / hi; w = (x1 - x0) / len(items)
    s = svg_open(h, title); s.append(txt(8, 13, title, 9, BL, bold=True)); s.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{GD}"/>')
    for k, ((lab, dv, col, tot), (a, b)) in enumerate(zip(items, tops)):
        cx = x0 + w * k + w / 2; bw = min(40, w * .6); top, bot = max(a, b), min(a, b)
        s.append(f'<rect x="{cx-bw/2:.1f}" y="{Y(top):.1f}" width="{bw:.1f}" height="{Y(bot)-Y(top):.1f}" rx="3" fill="{col}" opacity=".9"/>')
        s.append(txt(cx, Y(top) - 4, (('+' if dv > 0 and not tot and k else '') if True else '') + n(dv, 1 if abs(dv) % 1 else 0), 8, col, 'middle', True))
        for li, part in enumerate(lab.split('|')): s.append(txt(cx, y1 + 11 + li * 9, part, 7, GR, 'middle'))
    s.append('</svg>'); return ''.join(s)
