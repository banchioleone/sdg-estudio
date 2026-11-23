"""Gráficos (SVG inline) para las historias de la U6. Redibujos propios con datos
del material (Chase 12a ed., Morán, finales) o esquemas rotulados como tales."""
import math
from gen_u2_historias import n, txt, svg_open, line_chart, bars, boxes, flow_v, interval_rows, BL, OR, GR, GD, GN, YL  # noqa: F401

ST = ['#5B9BD5', '#70AD47', '#E0A800', '#ED7D31', '#8E7CC3']


def prec(nodes, edges, title, h=150, est=None, legend=None):
    """nodes: {k: (x, y, tiempo)} en coordenadas 0..280 x 0..h. est: {k: estación (1..5)}."""
    s = svg_open(h, title)
    s.append(txt(8, 13, title, 9, BL, bold=True))
    for a, b in edges:
        (x1, y1, _), (x2, y2, _) = nodes[a], nodes[b]
        d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d
        xa, ya, xb, yb = x1 + ux * 11, y1 + uy * 11, x2 - ux * 12, y2 - uy * 12
        s.append(f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="{GR}" stroke-width="1"/>')
        ang = math.atan2(uy, ux)
        p1 = (xb - 4 * math.cos(ang - .5), yb - 4 * math.sin(ang - .5)); p2 = (xb - 4 * math.cos(ang + .5), yb - 4 * math.sin(ang + .5))
        s.append(f'<path d="M{xb:.1f} {yb:.1f} L{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f} Z" fill="{GR}"/>')
    for k, (x, y, tm) in nodes.items():
        col = ST[(est[k] - 1) % 5] if est else BL
        s.append(f'<circle cx="{x}" cy="{y}" r="10.5" fill="{col}33" stroke="{col}" stroke-width="1.3"/>')
        s.append(txt(x, y + 3, k, 8.5, col, 'middle', True))
        s.append(txt(x, y + 19, tm, 6.5, GR, 'middle'))
    if legend:
        for i, lab in enumerate(legend):
            x = 8 + (i % 3) * 90; y = h - 22 + (i // 3) * 10
            s.append(f'<rect x="{x}" y="{y-6}" width="7" height="7" fill="{ST[i]}"/>')
            s.append(txt(x + 10, y, lab, 6.6, GR))
    s.append('</svg>')
    return ''.join(s)


def grid(header, rows, title, hi_row=None, h=None, neg_red=True):
    """Tabla chica: header (lista), rows: (label, [valores])."""
    nc = len(header)
    h = h or 30 + (len(rows) + 1) * 17 + 6
    s = svg_open(h, title)
    s.append(txt(8, 13, title, 9, BL, bold=True))
    lw = 74; cw = (272 - 8 - lw) / (nc)
    y = 22
    s.append(f'<rect x="8" y="{y}" width="264" height="16" fill="{BL}"/>')
    for j, c in enumerate(header):
        s.append(txt(8 + lw + j * cw + cw / 2, y + 11.5, c, 7.2, '#fff', 'middle', True))
    for i, (lab, vals) in enumerate(rows):
        y = 22 + (i + 1) * 17
        fill = '#FFF3E8' if hi_row is not None and i == hi_row else ('#F4F6F8' if i % 2 else '#fff')
        s.append(f'<rect x="8" y="{y}" width="264" height="17" fill="{fill}"/>')
        s.append(txt(12, y + 12, lab, 7, '#222', bold=(i == hi_row)))
        for j, v in enumerate(vals):
            col = '#B03A2E' if (neg_red and str(v).startswith('−')) else ('#9a5b00' if i == hi_row else '#222')
            s.append(txt(8 + lw + j * cw + cw / 2, y + 12, v, 7.2, col, 'middle', i == hi_row))
    s.append('</svg>')
    return ''.join(s)


def zones(segs, title, total, unit='semanas', h=96):
    """segs: (desde, hasta, nombre, color)."""
    s = svg_open(h, title)
    s.append(txt(8, 13, title, 9, BL, bold=True))
    X = lambda v: 10 + v * 258 / total
    for a, b, nm, col in segs:
        s.append(f'<rect x="{X(a):.1f}" y="26" width="{X(b)-X(a):.1f}" height="34" fill="{col}2a" stroke="{col}" stroke-width="1.2"/>')
        s.append(txt((X(a) + X(b)) / 2, 46, nm, 7.4, col, 'middle', True))
    ticks = sorted({a for a, _, _, _ in segs} | {b for _, b, _, _ in segs})
    s.append(f'<line x1="10" y1="68" x2="268" y2="68" stroke="{GR}"/>')
    for v in ticks:
        s.append(f'<line x1="{X(v):.1f}" y1="65" x2="{X(v):.1f}" y2="71" stroke="{GR}"/>')
        s.append(txt(X(v), 81, n(v, 0), 7, GR, 'middle'))
    s.append(txt(268, 91, unit, 6.8, GR, 'end'))
    s.append('</svg>')
    return ''.join(s)
