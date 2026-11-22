#!/usr/bin/env python3
"""Láminas propias de la U5 (esquemas y gráficos calculados). Salen en content/u5/img/.
Todas dicen en el pie que son esquemas propios, no láminas de la cátedra."""
from __future__ import annotations
from math import sqrt, exp, pi
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "content" / "u5" / "img"
AZ = "#1F4E79"; NAR = "#D9954A"; VER = "#2E7D4F"; ROJ = "#B03A2E"; GR = "#5c6670"; LG = "#d0d5db"
FONT = 'font-family="Segoe UI, Calibri, Helvetica, Arial, sans-serif"'


def svg(w, h, body, title, sub):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT}>'
            f'<rect width="{w}" height="{h}" fill="#FFFFFF"/>'
            f'<text x="20" y="26" font-size="17" font-weight="700" fill="{AZ}">{title}</text>'
            f'<text x="20" y="44" font-size="11.5" fill="{GR}">{sub}</text>' + body + "</svg>")


def arrow_defs(pid):
    return (f'<defs><marker id="{pid}" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">'
            f'<path d="M0,0 L9,3.5 L0,7 Z" fill="{AZ}"/></marker></defs>')


def axes(x0, y0, x1, y1, xl, yl, pid):
    return (f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{AZ}" stroke-width="1.6" marker-end="url(#{pid})"/>'
            f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="{AZ}" stroke-width="1.6" marker-end="url(#{pid})"/>'
            f'<text x="{x1}" y="{y0-8}" font-size="12" fill="{AZ}" text-anchor="end">{xl}</text>'
            f'<text x="{x0+6}" y="{y1+4}" font-size="12" fill="{AZ}">{yl}</text>')


def sierra():
    pid = "u5a1"
    x0, y0 = 60, 300
    b = arrow_defs(pid) + axes(x0, y0, 660, 60, "tiempo", "existencias", pid)
    ss, q = 40, 170   # alturas en px
    top = y0 - ss - q
    ys = y0 - ss
    cyc = 170; L = 50
    pts = []
    x = x0
    for k in range(3):
        pts += [(x, top), (x + cyc, ys)]
        x += cyc
    path = "M" + " L".join(f"{a},{b_}" for a, b_ in [(x0, top)] + [p for i, p in enumerate(pts) if i > 0])
    # vertical jumps
    d = f"M{x0},{top}"
    x = x0
    for k in range(3):
        d += f" L{x+cyc},{ys}"
        if k < 2:
            d += f" L{x+cyc},{top}"
        x += cyc
    b += f'<path d="{d}" fill="none" stroke="{AZ}" stroke-width="2.4"/>'
    # SS line
    b += f'<line x1="{x0}" y1="{ys}" x2="650" y2="{ys}" stroke="{VER}" stroke-width="1.4" stroke-dasharray="6 4"/>'
    b += f'<text x="652" y="{ys+4}" font-size="12" fill="{VER}">SS</text>'
    # R line: level at which order placed = demand during L + SS
    r_y = ys - q * L / cyc
    b += f'<line x1="{x0}" y1="{r_y:.1f}" x2="650" y2="{r_y:.1f}" stroke="{NAR}" stroke-width="1.4" stroke-dasharray="6 4"/>'
    b += f'<text x="652" y="{r_y+4:.1f}" font-size="12" fill="{NAR}">R (PP)</text>'
    # mark order points and L
    x = x0
    for k in range(3):
        xo = x + cyc - L
        b += f'<circle cx="{xo}" cy="{r_y:.1f}" r="4.5" fill="{NAR}"/>'
        b += f'<line x1="{xo}" y1="{y0+8}" x2="{x+cyc}" y2="{y0+8}" stroke="{NAR}" stroke-width="2"/>'
        b += f'<text x="{xo+L/2}" y="{y0+24}" font-size="11.5" fill="{NAR}" text-anchor="middle">L</text>'
        x += cyc
    # Q brace
    b += f'<line x1="{x0+cyc+6}" y1="{top}" x2="{x0+cyc+6}" y2="{ys}" stroke="{ROJ}" stroke-width="1.6"/>'
    b += f'<text x="{x0+cyc+12}" y="{(top+ys)/2:.0f}" font-size="13" font-weight="700" fill="{ROJ}">Q</text>'
    b += f'<text x="{x0+12}" y="{top-8}" font-size="11.5" fill="{GR}">llega el pedido: sube Q</text>'
    b += (f'<text x="20" y="352" font-size="11.5" fill="{GR}">Se pide Q cuando la posición del inventario baja a R. El pedido llega L después. '
          'Con demanda incierta, R = d̄·L + SS.</text>')
    return svg(700, 368, b, "Modelo de cantidad fija (perpetuo): el «efecto sierra»",
               "Esquema propio a partir del texto de Chase cap. 17 (las ilustraciones 17.5 y 17.7 son imagen en el resumen V6)")


def costos():
    pid = "u5a2"
    D, S, H = 7500, 15, 3.6   # BIT-Kaffee
    x0, y0, x1, y1 = 70, 320, 660, 60
    qmax, cmax = 700, 2500
    X = lambda q: x0 + (x1 - x0 - 20) * q / qmax
    Y = lambda c: y0 - (y0 - y1 - 20) * c / cmax
    b = arrow_defs(pid) + axes(x0, y0, x1, y1, "Q (cajas por pedido)", "$ / año", pid)
    def curve(f, col, dash=""):
        pts = " ".join(f"{X(q):.1f},{Y(min(f(q), cmax)):.1f}" for q in range(40, qmax + 1, 5))
        return f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.2" {dash}/>'
    b += curve(lambda q: H * q / 2, VER)
    b += curve(lambda q: D * S / q, NAR)
    b += curve(lambda q: H * q / 2 + D * S / q, AZ)
    qo = sqrt(2 * D * S / H); co = H * qo / 2 + D * S / qo
    b += f'<line x1="{X(qo):.1f}" y1="{y0}" x2="{X(qo):.1f}" y2="{Y(co):.1f}" stroke="{ROJ}" stroke-dasharray="5 4"/>'
    b += f'<circle cx="{X(qo):.1f}" cy="{Y(co):.1f}" r="5" fill="{ROJ}"/>'
    b += f'<text x="{X(qo)+8:.1f}" y="{Y(co)-10:.1f}" font-size="12.5" font-weight="700" fill="{ROJ}">Q* = 250 · $900/año</text>'
    for q in (0, 100, 200, 300, 400, 500, 600, 700):
        b += f'<text x="{X(q):.1f}" y="{y0+15}" font-size="10.5" fill="{GR}" text-anchor="middle">{q}</text>'
    for c in (500, 1000, 1500, 2000, 2500):
        b += f'<text x="{x0-6}" y="{Y(c)+4:.1f}" font-size="10.5" fill="{GR}" text-anchor="end">{c}</text>'
    b += f'<text x="{X(560):.1f}" y="{Y(H*560/2)-8:.1f}" font-size="12" fill="{VER}">mantenimiento (Q/2)·H</text>'
    b += f'<text x="{X(75):.1f}" y="{Y(1500)+0:.1f}" font-size="12" fill="{NAR}">pedidos (D/Q)·S</text>'
    b += f'<text x="{X(520):.1f}" y="{Y(H*520/2+D*S/520)-10:.1f}" font-size="12" fill="{AZ}">total</text>'
    b += (f'<text x="20" y="358" font-size="11.5" fill="{GR}">Datos de BIT-Kaffee (D = 7500 cajas/año, S = $15, H = 30% de $12 = $3,60). '
          'En Q* pedir y mantener cuestan lo mismo: $450 cada uno.</text>')
    return svg(700, 372, b, "Costos anuales en función de Q (sin el costo de compra D·C)",
               "Gráfico propio, calculado con un ejercicio de final (EjerciciosFinalesResueltos p.16)")


def descuentos():
    pid = "u5a3"
    D, S, i = 600, 16, 0.36
    tramos = [(7.5, 1, 49), (7.35, 50, 99), (7.0, 100, 400)]
    x0, y0, x1, y1 = 70, 320, 660, 60
    qmin, qmax, cmin, cmax = 20, 300, 4300, 4900
    X = lambda q: x0 + (x1 - x0 - 20) * (q - qmin) / (qmax - qmin)
    Y = lambda c: y0 - (y0 - y1 - 20) * (c - cmin) / (cmax - cmin)
    TC = lambda q, c: D * c + D * S / q + c * i * q / 2
    b = arrow_defs(pid) + axes(x0, y0, x1, y1, "Q (cajas)", "CT anual ($)", pid)
    cols = [NAR, VER, AZ]
    for (c, lo, hi), col in zip(tramos, cols):
        full = " ".join(f"{X(q):.1f},{Y(min(max(TC(q, c), cmin), cmax)):.1f}" for q in range(qmin, qmax + 1, 2))
        b += f'<polyline points="{full}" fill="none" stroke="{col}" stroke-width="1.2" stroke-dasharray="4 4" opacity="0.7"/>'
        a, z = max(lo, qmin), min(hi, qmax)
        seg = " ".join(f"{X(q):.1f},{Y(min(TC(q, c), cmax)):.1f}" for q in range(a, z + 1))
        b += f'<polyline points="{seg}" fill="none" stroke="{col}" stroke-width="3"/>'
        b += f'<text x="{X(z if z < qmax else 250)-4:.1f}" y="{Y(min(TC(z if z<qmax else 250, c), cmax))-8:.1f}" font-size="12" fill="{col}" text-anchor="end">${str(c).replace(".", ",")}</text>'
    for q, c, lab in ((49, 7.5, "Q=49: $4762"), (85, 7.35, "Q*=85: $4635"), (100, 7.0, "Q=100: $4422 ← mínimo")):
        b += f'<circle cx="{X(q):.1f}" cy="{Y(TC(q, c)):.1f}" r="5" fill="{ROJ}"/>'
        b += f'<text x="{X(q)+8:.1f}" y="{Y(TC(q, c))+16:.1f}" font-size="11.5" fill="{ROJ}">{lab}</text>'
    for q in (50, 100, 150, 200, 250, 300):
        b += f'<text x="{X(q):.1f}" y="{y0+15}" font-size="10.5" fill="{GR}" text-anchor="middle">{q}</text>'
    for c in (4400, 4600, 4800):
        b += f'<text x="{x0-6}" y="{Y(c)+4:.1f}" font-size="10.5" fill="{GR}" text-anchor="end">{c}</text>'
    b += (f'<text x="20" y="358" font-size="11.5" fill="{GR}">Caso librería (D = 600 cajas, S = $16, manejo 36%). Trazo grueso = tramo donde ese precio vale; '
          'punteado = la curva fuera de su tramo.</text>')
    return svg(700, 372, b, "EOQ con descuentos: una curva de costo total por precio",
               "Gráfico propio con los datos del final (SG!EVA, EFR p.3, SG1 Lu Final 2)")


def qvsp():
    pid = "u5a4"
    b = arrow_defs(pid)
    # panel Q
    def panel(ox, title, kind):
        s = ""
        x0, y0, x1, y1 = ox + 30, 290, ox + 310, 90
        s += axes(x0, y0, x1, y1, "t", "stock", pid)
        s += f'<text x="{ox+30}" y="74" font-size="13.5" font-weight="700" fill="{AZ}">{title}</text>'
        if kind == "Q":
            # irregular slopes, same Q, R line
            R = 200; top0 = 110
            seq = [(0, top0), (70, R), (95, 260), (95, 260-150), ]
            d = f"M{x0},{top0}"
            x = x0; y = top0
            slopes = [1.9, 1.2, 2.6]
            for sl in slopes:
                xr = x + (R - y) / -sl if False else x + (R - y) / sl * -1
                # reach R
                dx = (R - y) / sl
                xr = x + dx
                d += f" L{xr:.1f},{R}"
                # lead time 30 px more consumption
                xl = xr + 32; yl = R + 32 * sl
                d += f" L{xl:.1f},{yl:.1f} L{xl:.1f},{yl-120:.1f}"
                s += f'<circle cx="{xr:.1f}" cy="{R}" r="4" fill="{NAR}"/>'
                x, y = xl, yl - 120
            s += f'<path d="{d}" fill="none" stroke="{AZ}" stroke-width="2.2"/>'
            s += f'<line x1="{x0}" y1="{R}" x2="{x1-10}" y2="{R}" stroke="{NAR}" stroke-dasharray="5 4"/>'
            s += f'<text x="{x1-8}" y="{R+4}" font-size="11.5" fill="{NAR}">R</text>'
            s += f'<text x="{ox+30}" y="316" font-size="11.5" fill="{GR}">Cantidad fija Q, fechas variables.</text>'
            s += f'<text x="{ox+30}" y="332" font-size="11.5" fill="{GR}">Se dispara por un evento: llegar a R.</text>'
        else:
            T = 80; y = 120; x = x0
            d = f"M{x0},{y}"
            slopes = [1.0, 1.8, 0.7]
            M = 110
            for sl in slopes:
                xr = x + T; yr = y + T * sl
                d += f" L{xr:.1f},{yr:.1f}"
                s += f'<circle cx="{xr:.1f}" cy="{yr:.1f}" r="4" fill="{NAR}"/>'
                s += f'<line x1="{xr:.1f}" y1="{yr:.1f}" x2="{xr:.1f}" y2="{M}" stroke="{ROJ}" stroke-width="1.4" stroke-dasharray="3 3"/>'
                s += f'<text x="{xr+3:.1f}" y="{(yr+M)/2:.1f}" font-size="10.5" fill="{ROJ}">q</text>'
                d += f" L{xr:.1f},{M}"
                x, y = xr, M
            s += f'<path d="{d}" fill="none" stroke="{AZ}" stroke-width="2.2"/>'
            s += f'<line x1="{x0}" y1="{M}" x2="{x1-10}" y2="{M}" stroke="{VER}" stroke-dasharray="5 4"/>'
            s += f'<text x="{x1-8}" y="{M+4}" font-size="11.5" fill="{VER}">M</text>'
            for k in range(1, 4):
                s += f'<text x="{x0+k*T:.1f}" y="{y0+15}" font-size="11" fill="{NAR}" text-anchor="middle">T</text>'
            s += f'<text x="{ox+30}" y="316" font-size="11.5" fill="{GR}">Período fijo T, cantidades q variables.</text>'
            s += f'<text x="{ox+30}" y="332" font-size="11.5" fill="{GR}">Se dispara por el paso del tiempo.</text>'
        return s
    b += panel(0, "Perpetuo (modelo Q)", "Q") + panel(350, "Periódico (modelo P)", "P")
    b += f'<text x="20" y="356" font-size="11.5" fill="{GR}">Simplificado: en el periódico el pedido q lleva la posición hasta M; la llegada real ocurre L después (no dibujado).</text>'
    return svg(700, 370, b, "Perpetuo vs. periódico", "Esquema propio a partir de Chase cap. 17 y de la definición del banco de preguntas (preguntasabastecimiento)")


def normal():
    pid = "u5a5"
    x0, y0, x1 = 60, 290, 660
    mu_x = 300; sc = 70   # px por desvío
    pdf = lambda z: exp(-z * z / 2) / sqrt(2 * pi)
    Y = lambda v: y0 - v * 520
    b = arrow_defs(pid)
    b += f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{AZ}" stroke-width="1.6" marker-end="url(#{pid})"/>'
    z85 = 1.036
    # shaded area up to z85
    pts = [(mu_x - 3.5 * sc, y0)] + [(mu_x + z * sc, Y(pdf(z))) for z in [k / 50 for k in range(-175, int(z85 * 50) + 1)]] + [(mu_x + z85 * sc, y0)]
    b += '<polygon points="' + " ".join(f"{a:.1f},{c:.1f}" for a, c in pts) + f'" fill="{AZ}" opacity="0.16"/>'
    tail = [(mu_x + z85 * sc, y0)] + [(mu_x + z * sc, Y(pdf(z))) for z in [k / 50 for k in range(int(z85 * 50), 176)]] + [(mu_x + 3.5 * sc, y0)]
    b += '<polygon points="' + " ".join(f"{a:.1f},{c:.1f}" for a, c in tail) + f'" fill="{ROJ}" opacity="0.25"/>'
    curve = " ".join(f"{mu_x + z * sc:.1f},{Y(pdf(z)):.1f}" for z in [k / 50 for k in range(-175, 176)])
    b += f'<polyline points="{curve}" fill="none" stroke="{AZ}" stroke-width="2.4"/>'
    b += f'<line x1="{mu_x}" y1="{y0}" x2="{mu_x}" y2="{Y(pdf(0)):.1f}" stroke="{GR}" stroke-dasharray="4 4"/>'
    xr = mu_x + z85 * sc
    b += f'<line x1="{xr:.1f}" y1="{y0}" x2="{xr:.1f}" y2="{Y(pdf(z85))-30:.1f}" stroke="{NAR}" stroke-width="2"/>'
    b += f'<text x="{mu_x}" y="{y0+18}" font-size="12" fill="{AZ}" text-anchor="middle">d̄·L = 150</text>'
    b += f'<text x="{xr:.1f}" y="{y0+18}" font-size="12" fill="{NAR}" text-anchor="middle">R = 168</text>'
    b += f'<text x="{xr+4:.1f}" y="{Y(pdf(z85))-34:.1f}" font-size="12" fill="{NAR}">z = 1,04</text>'
    b += f'<line x1="{mu_x}" y1="{y0+30}" x2="{xr:.1f}" y2="{y0+30}" stroke="{VER}" stroke-width="2.2"/>'
    b += f'<text x="{(mu_x+xr)/2:.1f}" y="{y0+46}" font-size="12" font-weight="700" fill="{VER}" text-anchor="middle">SS = z·σL ≈ 18</text>'
    b += f'<text x="{mu_x-60}" y="{Y(0.18):.1f}" font-size="13" font-weight="700" fill="{AZ}" text-anchor="middle">85%</text>'
    b += f'<text x="{mu_x-60}" y="{Y(0.18)+15:.1f}" font-size="11" fill="{AZ}" text-anchor="middle">no falta</text>'
    b += f'<text x="{xr+70:.1f}" y="{y0-12}" font-size="12" font-weight="700" fill="{ROJ}">15%: falta</text>'
    b += (f'<text x="20" y="362" font-size="11.5" fill="{GR}">Demanda en el lead time del final N(50,10) cajas/día, L = 3 días: media 150, σL = 10·√3 = 17,3. '
          'Nivel de servicio 85%.</text>')
    return svg(700, 376, b, "Stock de seguridad: cuánto me corro a la derecha de la media",
               "Gráfico propio (cálculo con tabla normal; ver Clase 1.b de la U2)")


def pareto():
    pid = "u5a6"
    rows = [("003", 0.897, 702), ("004", 0.782, 1100), ("041", 0.738, 1176), ("036", 0.738, 1281), ("020", 0.706, 510),
            ("051", 0.684, 2432), ("002", 0.667, 1125), ("040", 0.609, 2048), ("021", 0.595, 546), ("038", 0.568, 968),
            ("035", 0.5, 510), ("037", 0.476, 966), ("042", 0.474, 2356), ("060", 0.472, 1116), ("033", 0.444, 1440),
            ("001", 0.423, 780), ("023", 0.411, 4480), ("037", 0.404, 658), ("020", 0.394, 1320), ("055", 0.273, 968)]
    tot = sum(r[2] for r in rows)
    x0, y0, x1, y1 = 60, 300, 670, 60
    n = len(rows); bw = (x1 - x0 - 20) / n
    Y = lambda f: y0 - (y0 - y1 - 20) * f
    b = arrow_defs(pid) + axes(x0, y0, x1, y1, "ítems", "% capital", pid)
    acc = 0; pts = []
    for k, (it, inc, cap) in enumerate(rows):
        acc += cap
        x = x0 + k * bw
        col = ROJ if acc / tot <= 0.5051 else LG
        b += f'<rect x="{x+3:.1f}" y="{Y(cap/tot):.1f}" width="{bw-6:.1f}" height="{y0-Y(cap/tot):.1f}" fill="{col}"/>'
        b += f'<text x="{x+bw/2:.1f}" y="{y0+13}" font-size="9" fill="{GR}" text-anchor="middle">{it}</text>'
        pts.append((x + bw / 2, Y(acc / tot)))
    b += '<polyline points="' + " ".join(f"{a:.1f},{c:.1f}" for a, c in pts) + f'" fill="none" stroke="{AZ}" stroke-width="2.2"/>'
    for a, c in pts:
        b += f'<circle cx="{a:.1f}" cy="{c:.1f}" r="3" fill="{AZ}"/>'
    b += f'<line x1="{x0}" y1="{Y(0.5):.1f}" x2="{x1-10}" y2="{Y(0.5):.1f}" stroke="{NAR}" stroke-dasharray="6 4"/>'
    b += f'<text x="{x0+4}" y="{Y(0.5)-6:.1f}" font-size="12" fill="{NAR}">50% del capital inmovilizado</text>'
    for f in (0.25, 0.5, 0.75, 1.0):
        b += f'<text x="{x0-6}" y="{Y(f)+4:.1f}" font-size="10.5" fill="{GR}" text-anchor="end">{int(f*100)}%</text>'
    b += (f'<text x="20" y="338" font-size="11.5" fill="{GR}">Ítems ordenados de mayor a menor MO/costo primo. Rojo: los 12 que se venden (50,5% del capital = cantidad × costo primo). '
          'Línea: acumulado.</text>')
    return svg(700, 352, b, "ABC aplicado: ¿qué ítems inmovilizados vendo?",
               "Gráfico propio con la tabla del final (EFR p.8–9); criterio de orden: MO / costo primo")


def mapa():
    pid = "u5a7"
    b = arrow_defs(pid)
    boxes = [
        (20, 70, 200, 70, "Demanda", "independiente → pronóstico (U2)\ndependiente → MRP (U6)"),
        (250, 70, 200, 70, "Modelo de stock", "perpetuo (Q) · periódico (P)\nEOQ · SS · descuentos"),
        (480, 70, 200, 70, "Compras", "cotizar · evaluar · asignar\ncolocar la O.C. · seguir"),
        (480, 190, 200, 70, "Proveedores", "precio · entrega · calidad\nJIT: pocos, cerca, frecuentes"),
        (250, 190, 200, 70, "Almacenes", "recepción · registro · conteo\nABC · trazabilidad"),
        (20, 190, 200, 70, "Distribución", "CD · DRP · transporte\nubicación de plantas"),
    ]
    for x, y, w, h, t, s in boxes:
        b += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#EEF3F8" stroke="{AZ}" stroke-width="1.6"/>'
        b += f'<text x="{x+w/2}" y="{y+22}" font-size="14" font-weight="700" fill="{AZ}" text-anchor="middle">{t}</text>'
        for k, line in enumerate(s.split("\n")):
            b += f'<text x="{x+w/2}" y="{y+42+k*15}" font-size="11.5" fill="#333" text-anchor="middle">{line}</text>'
    ar = lambda x1, y1, x2, y2: f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{AZ}" stroke-width="2" marker-end="url(#{pid})"/>'
    b += ar(220, 105, 248, 105) + ar(450, 105, 478, 105) + ar(580, 140, 580, 188) + ar(480, 225, 452, 225) + ar(250, 225, 222, 225)
    b += f'<rect x="20" y="290" width="660" height="44" rx="10" fill="#FFF3E8" stroke="{NAR}" stroke-width="1.4"/>'
    b += f'<text x="350" y="309" font-size="12.5" font-weight="700" fill="#8A5A16" text-anchor="middle">Cliente: nivel de servicio = probabilidad de no quedarse sin stock</text>'
    b += f'<text x="350" y="325" font-size="11.5" fill="#8A5A16" text-anchor="middle">Todo el circuito se mide contra eso y contra el costo de tener inventario (25–35% de su valor por año, Chase)</text>'
    return svg(700, 350, b, "Mapa de la Unidad 5 · Logística", "Esquema propio que ordena los temas del programa 2008; no es una lámina de la cátedra")


def latigo():
    pid = "u5a8"
    b = arrow_defs(pid)
    import math
    names = ["Consumidor", "Detallista", "Mayorista", "Fabricante"]
    amps = [6, 12, 22, 34]
    for k, (nm, a) in enumerate(zip(names, amps)):
        yc = 90 + k * 68
        b += f'<text x="20" y="{yc+4}" font-size="12.5" font-weight="700" fill="{AZ}">{nm}</text>'
        pts = " ".join(f"{130+t*5:.1f},{yc - a*math.sin(t/3.2 + k*0.6):.1f}" for t in range(0, 105))
        b += f'<line x1="130" y1="{yc}" x2="660" y2="{yc}" stroke="{LG}"/>'
        b += f'<polyline points="{pts}" fill="none" stroke="{[VER,AZ,NAR,ROJ][k]}" stroke-width="2.2"/>'
    b += f'<text x="20" y="358" font-size="11.5" fill="{GR}">Cada nivel pide con más variabilidad que la que ve.</text>'
    b += f'<text x="20" y="374" font-size="11.5" fill="{GR}">Remedio que da Chase: compartir información (EDI) y reabastecimiento continuo (Campbell Soup).</text>'
    return svg(700, 386, b, "Efecto látigo en la cadena de suministro", "Esquema propio de la idea de Chase cap. 10 (la ilustración 10.3, pañales de P&amp;G, es imagen en el resumen)")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = {"u5_mapa.svg": mapa(), "u5_sierra.svg": sierra(), "u5_costos.svg": costos(), "u5_descuentos.svg": descuentos(),
             "u5_QvsP.svg": qvsp(), "u5_normal.svg": normal(), "u5_pareto.svg": pareto(), "u5_latigo.svg": latigo()}
    for name, s in files.items():
        (OUT / name).write_text(s, encoding="utf-8")
        print("ok", name, len(s))


if __name__ == "__main__":
    main()
