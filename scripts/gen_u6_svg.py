#!/usr/bin/env python3
"""Láminas propias de la U6 (esquemas y gráficos con datos del material). Salen en content/u6/img/.
Cada una dice en el subtítulo si es esquema propio o de qué fuente salen los datos."""
from __future__ import annotations
from pathlib import Path
from gen_u5_svg import svg, arrow_defs, axes, AZ, NAR, VER, ROJ, GR, LG

OUT = Path(__file__).resolve().parent.parent / "content" / "u6" / "img"
BG = "#EEF3F8"; BGN = "#FFF3E8"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def box(x, y, w, h, title, sub="", fill=BG, stroke=AZ, tcol=AZ, fs=13.5):
    b = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>'
    lines = sub.split("\n") if sub else []
    ty = y + (h / 2 + 5 if not lines else 20)
    b += f'<text x="{x+w/2}" y="{ty}" font-size="{fs}" font-weight="700" fill="{tcol}" text-anchor="middle">{esc(title)}</text>'
    for k, ln in enumerate(lines):
        b += f'<text x="{x+w/2}" y="{y+38+k*14}" font-size="11" fill="#333" text-anchor="middle">{esc(ln)}</text>'
    return b


def ar(pid, x1, y1, x2, y2, col=AZ, dash=False):
    d = ' stroke-dasharray="5 4"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="1.8"{d} marker-end="url(#{pid})"/>'


def t(x, y, s, fs=11.5, col=GR, anchor="start", bold=False):
    w = ' font-weight="700"' if bold else ""
    return f'<text x="{x}" y="{y}" font-size="{fs}" fill="{col}" text-anchor="{anchor}"{w}>{esc(s)}</text>'


def hbars(items, x0=200, y0=70, bw=420, bh=26, gap=14, vmax=None, fmt=str, cols=None, best=None):
    vmax = vmax or max(v for _, v in items)
    b = ""
    for k, (lab, v) in enumerate(items):
        y = y0 + k * (bh + gap)
        w = bw * v / vmax
        c = (cols[k] if cols else AZ)
        if best is not None and k == best:
            c = VER
        b += t(x0 - 10, y + bh / 2 + 4, lab, 12.5, "#222", "end")
        b += f'<rect x="{x0}" y="{y}" width="{w:.1f}" height="{bh}" rx="4" fill="{c}"/>'
        b += t(x0 + w + 8, y + bh / 2 + 4, fmt(v), 12.5, "#222", bold=True)
    return b


def mil(v):
    s = f"{v:,.0f}".replace(",", ".")
    return s


def mapa():
    pid = "u6m"
    b = arrow_defs(pid)
    rows = [("Plan agregado (PA)", "familias · meses (mediano plazo)", "RRP · recursos", 70),
            ("Programa maestro (MPS)", "productos finales · semanas", "RCCP · CPOF / CB / RP", 140),
            ("MRP", "piezas y materiales · semanas", "CRP · carga por centro", 210),
            ("Control de la producción (PAC)", "órdenes · días y turnos", "control de entradas / salidas", 280)]
    for name, sub, cap, y in rows:
        b += box(40, y, 330, 52, name, sub)
        b += box(430, y, 230, 52, cap, "", BGN, NAR, "#8A5A16", 12.5)
        b += f'<line x1="370" y1="{y+26}" x2="430" y2="{y+26}" stroke="{NAR}" stroke-width="1.6" stroke-dasharray="5 4"/>'
    for y in (122, 192, 262):
        b += ar(pid, 205, y, 205, y + 16)
    b += t(350, 360, "Cada nivel desagrega al anterior y se valida contra su propio cálculo de capacidad (columna naranja).", 11.5, GR, "middle")
    b += t(350, 376, "Balanceo de línea (Clase 11) es el equivalente en producción repetitiva.", 11.5, GR, "middle")
    return svg(700, 392, b, "Mapa de la Unidad 6 · Planificación y control",
               "Esquema propio con la jerarquía de Morán y Chase (no es lámina de la cátedra)")


def estrategias():
    items = [("Plan 1 · ajuste", 172800), ("Plan 2 · nivel", 162488), ("Plan 3 · subcontrato", 160000), ("Plan 4 · horas extras", 165491)]
    b = hbars(items, 220, 80, 380, 34, 18, 180000, lambda v: "$" + mil(v), best=2)
    b += t(20, 320, "El más barato es el Plan 3, pero Chase advierte que la subcontratación es de «alto riesgo» (calidad, dependencia).", 11.5)
    b += t(20, 336, "Barras empiezan en 0; la diferencia entre planes es de 8% como mucho: el costo de tiempo regular domina.", 11.5)
    return svg(700, 350, b, "JC Company: costo total de cada estrategia (6 meses)", "Datos de Chase, ejemplo 16.1 / ilustración 16.5; gráfico propio")


def time_fences():
    pid = "u6tf"
    b = arrow_defs(pid)
    x0, x1 = 40, 660
    sc = (x1 - x0) / 26
    zones = [(0, 8, "Congelado", "sin cambios (o menores)", ROJ), (8, 15, "Moderadamente firme", "cambios dentro del grupo", NAR), (15, 26, "Flexible", "casi cualquier cambio", VER)]
    for a, c, n, s, col in zones:
        xa, xc = x0 + a * sc, x0 + c * sc
        b += f'<rect x="{xa:.1f}" y="90" width="{xc-xa:.1f}" height="90" fill="{col}" fill-opacity="0.18" stroke="{col}" stroke-width="1.6"/>'
        b += t((xa + xc) / 2, 128, n, 13.5, col, "middle", True)
        b += t((xa + xc) / 2, 148, s, 11.5, "#333", "middle")
    b += ar(pid, x0, 205, x1 + 15, 205)
    for w in (0, 8, 15, 26):
        x = x0 + w * sc
        b += f'<line x1="{x:.1f}" y1="198" x2="{x:.1f}" y2="212" stroke="{AZ}" stroke-width="1.6"/>'
        b += t(x, 230, f"{w}", 12.5, AZ, "middle", True)
    b += t(x1 + 10, 248, "semanas", 11.5, AZ, "end")
    b += t(20, 270, "Más cerca de hoy, más caro cambiar: los materiales ya se compraron y la capacidad ya se asignó.", 11.5)
    b += t(20, 286, "Disponible para prometer (Chase): lo que queda sin comprometer, p. ej. 100 programadas − 65 vendidas = 35.", 11.5)
    return svg(700, 300, b, "Restricciones de tiempo (time fences) del MPS", "Datos de Chase, ilustración 18.2; dibujo propio")


def bom_x():
    pid = "u6b"
    b = arrow_defs(pid)
    nodes = {"X": (350, 70, "X", "nivel 0 · LT 1"), "A": (220, 170, "A (×1)", "nivel 1 · LT 2"), "B": (480, 170, "B (×2)", "nivel 1 · LT 2"),
             "C": (140, 270, "C (×1)", "nivel 2 · LT 2"), "D": (300, 270, "D (×3)", "nivel 2 · LT 2")}
    for k, (x, y, n, s) in nodes.items():
        b += box(x - 70, y, 140, 52, n, s)
    for p, c in (("X", "A"), ("X", "B"), ("A", "C"), ("A", "D")):
        xp, yp = nodes[p][0], nodes[p][1] + 52
        xc, yc = nodes[c][0], nodes[c][1]
        b += ar(pid, xp, yp, xc, yc - 2)
    b += t(20, 352, "Leer hacia abajo: para cada X hacen falta 1 A y 2 B; para cada A, 1 C y 3 D.", 11.5)
    b += t(20, 368, "Stock inicial X 20, A 10; ingresos en la semana 1: X 50, C 30, D 100.", 11.5)
    return svg(700, 382, b, "Árbol de producto del ejemplo X (Morán)", "Datos de la nota técnica MRP de Morán; dibujo propio")


def registro():
    cols = ["", "1", "2", "3", "4", "5", "6"]
    rows = [("Brutos", ["50", "", "", "50", "", "60"]), ("Ingr. programados", ["50", "", "", "", "", ""]),
            ("Disponible (S₀ 20)", ["20", "20", "20", "−30", "−30", "−90"]), ("Netos", ["", "", "", "30", "", "60"]),
            ("Órd. planificadas", ["", "", "30", "", "60", ""])]
    x0, y0, cw, rh, lw = 30, 70, 78, 34, 170
    b = ""
    for j, c in enumerate(cols):
        x = x0 + (lw if j else 0) + max(j - 1, 0) * cw
        w = lw if j == 0 else cw
        b += f'<rect x="{x}" y="{y0}" width="{w}" height="{rh}" fill="{AZ}"/>'
        b += t(x + w / 2, y0 + 22, "semana" if j == 0 else c, 12.5, "#fff", "middle", True)
    for i, (lab, vals) in enumerate(rows):
        y = y0 + (i + 1) * rh
        fill = BGN if lab.startswith("Órd") else ("#F6F8FA" if i % 2 else "#fff")
        b += f'<rect x="{x0}" y="{y}" width="{lw + 6*cw}" height="{rh}" fill="{fill}" stroke="{LG}"/>'
        b += t(x0 + 8, y + 22, lab, 12.5, "#222", bold=lab.startswith("Órd"))
        for j, v in enumerate(vals):
            col = ROJ if v.startswith("−") else ("#8A5A16" if lab.startswith("Órd") else "#222")
            b += t(x0 + lw + j * cw + cw / 2, y + 22, v, 12.5, col, "middle", bool(v) and lab.startswith(("Órd", "Netos")))
    pid = "u6r"
    b += arrow_defs(pid)
    # arrows from net week4 to order week3, net week6 to order week5
    yN = y0 + 4 * rh + 17; yO = y0 + 5 * rh + 17
    for wk in (4, 6):
        xn = x0 + lw + (wk - 1) * cw + cw / 2
        xo = xn - cw
        b += f'<path d="M{xn+14},{yN+4} C{xn+30},{yO} {xo+40},{yO+14} {xo+16},{yO+6}" fill="none" stroke="{NAR}" stroke-width="1.8" marker-end="url(#{pid})"/>'
    b += t(30, 300, "Disponible = anterior + ingresos − brutos. El primer negativo es un neto; la orden se planifica un lead time antes (LT de X = 1).", 11.5)
    b += t(30, 316, "Las órdenes de X son los brutos de A (×1) y de B (×2): así baja la explosión nivel por nivel.", 11.5)
    return svg(700, 330, b, "Cómo se lee el registro MRP (producto X, semanas 1 a 6)", "Datos de Morán, nota técnica MRP; esquema propio")


def loteo_moran():
    items = [("EOQ", 1835), ("TBO / POQ", 1650), ("Silver-Meal", 1572)]
    b = hbars(items, 180, 90, 420, 40, 24, 2000, lambda v: "$" + mil(v), best=2)
    b += t(20, 300, "Pieza Z (demanda propia de 300 por semana + la que generan las órdenes de X). Mismo orden en la pieza Y: 789 / 682 / 654.", 11.5)
    b += t(20, 316, "El lote dinámico (Silver-Meal) genera menos stock; el EOQ propaga excesos a los niveles inferiores (Morán).", 11.5)
    return svg(700, 330, b, "Pieza Z: costo total con cada regla de lote", "Datos de Morán, MRP §2.1; gráfico propio")


def loteo_chase():
    items = [("Lote por lote", 376.00), ("EOQ (351)", 171.05), ("Costo total mínimo", 140.50), ("Costo unitario mínimo", 153.50)]
    b = hbars(items, 220, 80, 380, 34, 18, 400, lambda v: "$" + f"{v:.2f}".replace(".", ","), best=2)
    b += t(20, 318, "Netos 50, 60, 70, 60, 95, 75, 60, 55; preparación $47; mantener 0,5% de $10 por semana (sobre el inventario final).", 11.5)
    return svg(700, 334, b, "Chase: costo de 8 semanas con cada técnica de lote", "Datos de Chase, ilustraciones 18.19 a 18.22; gráfico propio")


def ciclo():
    pid = "u6c"
    b = arrow_defs(pid)
    steps = [(30, 70, "Plan agregado"), (30, 150, "MPS"), (30, 230, "MRP"), (260, 230, "CRP"), (490, 230, "¿Es realista?"), (490, 310, "Ejecución: PAC y compras")]
    for x, y, n in steps:
        b += box(x, y, 180, 46, n, "", BGN if "realista" in n else BG)
    b += ar(pid, 120, 116, 120, 148) + ar(pid, 120, 196, 120, 228) + ar(pid, 210, 253, 258, 253) + ar(pid, 440, 253, 488, 253) + ar(pid, 580, 276, 580, 308)
    b += t(590, 298, "sí", 12, VER, bold=True)
    b += f'<path d="M580,230 C580,120 300,110 212,170" fill="none" stroke="{ROJ}" stroke-width="1.8" stroke-dasharray="5 4" marker-end="url(#{pid})"/>'
    b += t(430, 130, "no: replanificar (hasta el MPS)", 12, ROJ, "middle", True)
    b += t(20, 384, "«Ciclo cerrado»: la ejecución informa y el sistema se corrige. Sumando finanzas y simulación, Wight lo llama MRP II.", 11.5)
    return svg(700, 400, b, "MRP de ciclo cerrado", "Esquema según Chase, ilustración 18.17, y Morán; dibujo propio")


def precedencias_j():
    pid = "u6p"
    b = arrow_defs(pid)
    pos = {"A": (60, 110), "B": (150, 110), "C": (240, 110), "F": (340, 80), "G": (340, 140), "D": (60, 250), "E": (150, 250), "H": (340, 220), "I": (340, 280), "J": (460, 180), "K": (570, 180)}
    tm = {"A": 45, "B": 11, "C": 9, "D": 50, "E": 15, "F": 12, "G": 12, "H": 12, "I": 12, "J": 8, "K": 9}
    est = {"A": 1, "D": 2, "B": 3, "E": 3, "C": 3, "F": 3, "G": 4, "H": 4, "I": 4, "J": 4, "K": 5}
    colors = {1: "#DDEBF7", 2: "#E2F0D9", 3: "#FFF2CC", 4: "#FCE4D6", 5: "#EDE7F6"}
    edges = [("A", "B"), ("B", "C"), ("C", "F"), ("C", "G"), ("D", "E"), ("E", "H"), ("E", "I"), ("F", "J"), ("G", "J"), ("H", "J"), ("I", "J"), ("J", "K")]
    for a, c in edges:
        (x1, y1), (x2, y2) = pos[a], pos[c]
        import math
        d = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / d, (y2 - y1) / d
        b += ar(pid, x1 + ux * 24, y1 + uy * 24, x2 - ux * 26, y2 - uy * 26)
    for k, (x, y) in pos.items():
        b += f'<circle cx="{x}" cy="{y}" r="23" fill="{colors[est[k]]}" stroke="{AZ}" stroke-width="1.6"/>'
        b += t(x, y + 1, k, 14, AZ, "middle", True) + t(x, y + 15, f"{tm[k]} s", 10.5, "#333", "middle")
    ly = 330
    for s in range(1, 6):
        x = 30 + (s - 1) * 132
        b += f'<rect x="{x}" y="{ly}" width="18" height="18" fill="{colors[s]}" stroke="{AZ}"/>'
        lab = {1: "Est. 1: A (5,4 ocioso)", 2: "Est. 2: D (0,4)", 3: "Est. 3: B E C F (3,4)", 4: "Est. 4: G H I J (6,4)", 5: "Est. 5: K (41,4)"}[s]
        b += t(x + 24, ly + 14, lab, 11, "#222")
    b += t(20, 380, "C = 25.200 s / 500 = 50,4 s · T = 195 s · Nt = 4 · con esta regla salen 5 estaciones: eficiencia 195 / (5 × 50,4) = 77%.", 11.5)
    return svg(700, 396, b, "Camioneta J: precedencias y estaciones", "Datos de Chase, ejemplo 7A.1 (ilustraciones 7A.9 a 7A.11); dibujo propio")


def ventanas():
    pid = "u6v"
    b = arrow_defs(pid)
    import math
    pos = {"A": (70, 190), "B": (220, 90), "C": (220, 170), "D": (220, 250), "E": (220, 320), "F": (380, 110), "G": (380, 200), "H": (580, 250)}
    tm = {"A": 70, "B": 80, "C": 40, "D": 20, "E": 40, "F": 30, "G": 50, "H": 50}
    est = {"A": 1, "D": 1, "B": 2, "C": 3, "E": 3, "F": 4, "G": 4, "H": 5}
    colors = {1: "#DDEBF7", 2: "#E2F0D9", 3: "#FFF2CC", 4: "#FCE4D6", 5: "#EDE7F6"}
    edges = [("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"), ("B", "F"), ("C", "F"), ("C", "G"), ("D", "H"), ("E", "H"), ("F", "H"), ("G", "H")]
    for a, c in edges:
        (x1, y1), (x2, y2) = pos[a], pos[c]
        d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d
        b += ar(pid, x1 + ux * 24, y1 + uy * 24, x2 - ux * 26, y2 - uy * 26)
    for k, (x, y) in pos.items():
        b += f'<circle cx="{x}" cy="{y}" r="23" fill="{colors[est[k]]}" stroke="{AZ}" stroke-width="1.6"/>'
        b += t(x, y + 1, k, 14, AZ, "middle", True) + t(x, y + 15, f"{tm[k]} s", 10.5, "#333", "middle")
    for s_ in range(1, 6):
        x = 470
        y = 60 + (s_ - 1) * 22
        b += f'<rect x="{x}" y="{y}" width="16" height="16" fill="{colors[s_]}" stroke="{AZ}"/>'
        b += t(x + 22, y + 13, {1: "Est. 1: A + D (90)", 2: "Est. 2: B (80)", 3: "Est. 3: C + E (80)", 4: "Est. 4: F + G (80)", 5: "Est. 5: H (50)"}[s_], 11, "#222")
    b += t(20, 372, "Balance propio con C = 90 s (dos turnos): {A,D} 90 · {B} 80 · {C,E} 80 · {F,G} 80 · {H} 50 → 380 / (5 × 90) = 84,4%.", 11.5)
    b += t(20, 388, "El ciclo de 90 s y el 84,44% están en la resolución manuscrita (EFR p. 19); la asignación por colores es cálculo propio.", 11.5)
    return svg(700, 402, b, "Ventanas de aluminio: precedencias y un balance de 5 estaciones", "Datos del final 22/05/2003 (Ejercicios posibles); dibujo propio")


def perfil():
    x0, y0, h = 70, 300, 210
    vmax = 70
    ct200 = {1: 39, 2: 34.5, 4: 43.5, 6: 46.5, 9: 42}
    ct300 = {2: 51, 3: 45, 5: 57, 7: 61, 10: 55}
    pid = "u6pf"
    b = arrow_defs(pid) + axes(x0, y0, 670, 70, "", "horas", pid) + t(660, y0 + 34, "período", 12, AZ, "end")
    bw = 22
    for p in range(1, 11):
        xc = x0 + 15 + (p - 1) * 58
        for k, (dd, col) in enumerate(((ct200, AZ), (ct300, NAR))):
            v = dd.get(p, 0)
            if v:
                hh = h * v / vmax
                b += f'<rect x="{xc + k*bw}" y="{y0-hh:.1f}" width="{bw-2}" height="{hh:.1f}" fill="{col}"/>'
                b += t(xc + k * bw + bw / 2 - 1, y0 - hh - 4, f"{v:g}".replace(".", ","), 10, "#222", "middle")
        b += t(xc + bw, y0 + 16, str(p), 11.5, AZ, "middle")
    b += f'<rect x="460" y="62" width="14" height="14" fill="{AZ}"/>' + t(480, 74, "CT200 (OP10)", 11.5, "#222")
    b += f'<rect x="570" y="62" width="14" height="14" fill="{NAR}"/>' + t(590, 74, "CT300 (OP20)", 11.5, "#222")
    b += t(20, 340, "Carga = puesta a punto + tiempo por unidad × lote. La OP20 cae un período después que la OP10.", 11.5)
    b += t(20, 356, "Es solo la pieza Y: se suma a las demás piezas y se compara con 200 h por período en cada centro.", 11.5)
    return svg(700, 370, b, "CRP: carga que la pieza Y pone en cada centro", "Datos de Morán, Planificación de la capacidad (ejemplo de la pieza Y); gráfico propio")


def pac():
    pid = "u6k"
    b = arrow_defs(pid)
    b += box(20, 70, 200, 60, "Entradas", "MPS · MRP · CRP\ningeniería (rutas, tiempos)", fill="#F6F8FA")
    phases = [(250, "1 · Lanzamiento", "hoja de ruta · requisición\nvales de trabajo y movimiento\nlista de piezas"),
              (250, "2 · Programación", "lista de despacho por centro\n(carga + secuencia,\nreglas de prioridad)"),
              (250, "3 · Control del progreso", "datos de planta · órdenes abiertas\ninformes de estado, progreso\ny excepción · control E/S")]
    for k, (x, n, s) in enumerate(phases):
        y = 70 + k * 100
        b += box(x, y, 220, 80, n, s)
        if k:
            b += ar(pid, 360, y - 20, 360, y - 2)
    b += ar(pid, 220, 100, 248, 100)
    b += box(500, 170, 180, 80, "Decisor humano", "adelantar / atrasar órdenes\nhoras extra, rutas alternativas", BGN, NAR, "#8A5A16")
    b += f'<path d="M470,310 C520,310 590,300 590,252" fill="none" stroke="{NAR}" stroke-width="1.8" stroke-dasharray="5 4" marker-end="url(#{pid})"/>'
    b += f'<path d="M500,195 C480,150 490,110 472,110" fill="none" stroke="{NAR}" stroke-width="1.8" stroke-dasharray="5 4" marker-end="url(#{pid})"/>'
    b += t(20, 380, "Morán: «aún los sistemas más evolucionados cierran el bucle de control con un decisor humano».", 11.5)
    return svg(700, 396, b, "Control de las actividades de producción (PAC)", "Esquema propio según Morán, PAC (figura 1 y §2)")


def reglas():
    items = [("FCFS", 10.0), ("SOT", 7.2), ("EDD", 7.8), ("LCFS", 9.2), ("Aleatorio", 10.6), ("STR", 8.6)]
    b = hbars(items, 140, 70, 440, 26, 12, 12, lambda v: f"{v:.1f} días".replace(".", ","), best=1)
    b += t(20, 316, "Cinco trabajos en una sola fotocopiadora (A 3/5, B 4/6, C 2/7, D 6/9, E 1/2 días de proceso/plazo).", 11.5)
    b += t(20, 332, "SOT minimiza el tránsito; SOT y EDD empatan en retardo promedio (2,4 días).", 11.5)
    return svg(700, 346, b, "Tiempo de tránsito promedio según la regla de prioridad", "Datos de Chase, ejemplo 19.1 (Legal Copy-Express); gráfico propio")


def familias():
    items = [("MRP", 8), ("Balanceo", 4), ("Plan agregado", 2), ("Hombre–máquina", 2), ("MPS", 1), ("Capacidad (cálculo)", 1)]
    b = hbars(items, 190, 70, 400, 26, 12, 19, lambda v: f"{v} de 19", cols=[AZ, AZ, AZ, LG, AZ, AZ])
    b += t(20, 316, "Finales con fecha 2002–2018 (patrones_examenes.md). En la teoría 2011–2018 la capacidad de una estación salió en 5 de 7.", 11.5)
    b += t(20, 332, "Hombre–máquina en gris: lo trae el final pero corresponde a estudio del trabajo (Monks), no al material de esta unidad.", 11.5)
    return svg(700, 346, b, "¿Qué ejercicios de la U6 toman en el final?", "Conteos propios sobre los 19 finales con fecha del Drive")


def matriz():
    pid = "u6x"
    b = arrow_defs(pid)
    x0, y0, x1, y1 = 60, 310, 680, 60
    b += axes(x0, y0, x1, y1, "", "", pid)
    b += t(x1, y0 + 20, "volumen y estandarización →", 12, AZ, "end", True)
    b += t(x0 + 8, y1 + 4, "flujo más continuo ↓", 12, AZ, bold=True)
    names = ["Proyecto", "Centro de trabajo (taller)", "Celda de manufactura", "Línea de ensamble", "Proceso continuo"]
    ex = ["casas, caminos", "perforadoras juntas", "familias de piezas", "autos, aparatos", "petróleo, químicos"]
    for k, (n, e) in enumerate(zip(names, ex)):
        cx = x0 + 90 + k * 115; cy = y1 + 40 + k * 48
        b += f'<rect x="{cx-75}" y="{cy-18}" width="150" height="40" rx="8" fill="{BG}" stroke="{AZ}" stroke-width="1.4"/>'
        b += t(cx, cy, n, 11.5, AZ, "middle", True) + t(cx, cy + 14, e, 10.5, "#333", "middle")
    b += t(20, 350, "Fuera de la diagonal (p. ej. un producto masivo hecho en taller) el proceso queda caro o poco flexible.", 11.5)
    b += t(20, 366, "Cómo se planifica: proyecto → técnicas de proyectos; taller → MRP y secuencia; línea → tasa y balanceo.", 11.5)
    return svg(700, 380, b, "Las cinco estructuras de proceso y el volumen", "Esquema propio de la matriz producto–proceso de Chase cap. 7 (no es la ilustración del libro)")


def ajuste_nivel():
    req = [1850, 1425, 1000, 850, 1150, 1725]
    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun"]
    x0, y0, h = 80, 300, 220
    vmax = 2000
    pid = "u6an"
    b = arrow_defs(pid) + axes(x0, y0, 660, 60, "", "unidades", pid)
    pts = []
    for k, v in enumerate(req):
        x = x0 + 50 + k * 95; y = y0 - h * v / vmax
        pts.append((x, y))
        b += t(x, y0 + 18, meses[k], 12, AZ, "middle")
        b += t(x, y - 10, mil(v), 11, AZ, "middle", True)
    b += '<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="none" stroke="{AZ}" stroke-width="2.6"/>'
    for x, y in pts:
        b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{AZ}"/>'
    yl = y0 - h * 8000 / 6 / vmax
    b += f'<line x1="{x0}" y1="{yl:.1f}" x2="640" y2="{yl:.1f}" stroke="{NAR}" stroke-width="2.4" stroke-dasharray="7 5"/>'
    b += t(400, yl - 10, "nivel: 8.000 / 6 ≈ 1.333 por mes", 11.5, "#8A5A16", "middle", True)
    b += t(20, 338, "Azul = ajuste (producir lo que pide cada mes, moviendo la fuerza de trabajo). Naranja = nivel (tasa constante:", 11.5)
    b += t(20, 354, "sobra stock en marzo–mayo y falta en enero, febrero y junio). Los requerimientos ya incluyen el stock de seguridad.", 11.5)
    return svg(700, 368, b, "Ajuste vs. nivel con los requerimientos de JC Company", "Datos de Chase, ilustración 16.3; la línea de nivel es cálculo propio (promedio)")


def maquinas():
    pid = "u6mq"
    b = arrow_defs(pid)
    b += box(20, 110, 110, 70, "Entran", "1064 piezas", "#F6F8FA")
    b += box(170, 100, 140, 90, "M1", "23\" / 0,80 = 28,75 s\nscrap 2,5%\n→ 1037 buenas")
    b += box(350, 100, 130, 90, "Depósito D1-2", "máx. ≈ 272 piezas\n(M2 es más lenta)", BGN, NAR, "#8A5A16", 12.5)
    b += box(520, 100, 160, 90, "M2", "30\" / 0,75 = 40 s\nscrap 3,5%\n→ 1000 buenas")
    b += ar(pid, 130, 145, 168, 145) + ar(pid, 310, 145, 348, 145) + ar(pid, 480, 145, 518, 145)
    b += t(20, 240, "Se calcula hacia atrás: 1000 / 0,965 = 1037 que procesa M2; 1037 / 0,975 = 1064 que procesa M1.", 11.5)
    b += t(20, 256, "Tiempo real = estándar / factor de actividad. El cuello de botella (M2, 40 s) fija el tiempo de entrega:", 11.5)
    b += t(20, 272, "≈ 28,75 + 1037 × 40 ≈ 41.509 s ≈ 11 h 32 min, con transferencia de a una pieza (cálculo propio).", 11.5)
    return svg(700, 290, b, "Dos máquinas en serie con scrap (final, versión de EFR p. 20)", "Datos del enunciado; los dos primeros pasos están en la hoja manuscrita, el resto es cálculo propio")


def arbol_2013():
    pid = "u6t"
    b = arrow_defs(pid)
    nodes = {"A": (190, 70, "A"), "S": (500, 70, "S"), "B": (100, 170, "B (×2)"), "C1": (260, 170, "C (×2)"),
             "T": (600, 170, "T (×1)"), "D": (40, 280, "D (×3)"), "E": (160, 280, "E (×2)"), "F": (280, 280, "F (×1)"),
             "E2": (400, 170, "E (×1)"), "F2": (500, 170, "F (×4)"), "C2": (600, 280, "C (×3)")}
    for k, (x, y, n) in nodes.items():
        b += box(x - 48, y, 96, 40, n, "", BGN if k in ("C1", "C2", "E", "E2", "F", "F2") else BG)
    for p_, c_ in (("A", "B"), ("A", "C1"), ("B", "D"), ("B", "E"), ("B", "F"), ("S", "E2"), ("S", "F2"), ("S", "T"), ("T", "C2")):
        xp, yp = nodes[p_][0], nodes[p_][1] + 40
        xc, yc = nodes[c_][0], nodes[c_][1]
        b += ar(pid, xp, yp, xc, yc - 2)
    b += t(20, 352, "En naranja, los componentes comunes a A y S (C, E y F): cada uno se netea una sola vez, en su nivel más bajo.", 11.5)
    b += t(20, 368, "C está en el nivel 1 de A pero en el 2 de S (debajo de T): se planifica en el nivel 2, sumando los brutos de A y de T.", 11.5)
    return svg(700, 382, b, "Estructura del final 08/08/2013: dos productos con componentes comunes", "Datos del enunciado (Final SG1 8 de agosto de 2013); dibujo propio")


ALL = {"u6_mapa": mapa, "u6_estrategias": estrategias, "u6_time_fences": time_fences, "u6_bom_x": bom_x, "u6_registro_mrp": registro,
       "u6_perfil_carga": perfil, "u6_loteo_moran": loteo_moran, "u6_loteo_chase": loteo_chase, "u6_ciclo_cerrado": ciclo,
       "u6_precedencias_j": precedencias_j, "u6_ventanas": ventanas, "u6_pac": pac, "u6_reglas": reglas, "u6_familias": familias,
       "u6_matriz": matriz, "u6_ajuste_nivel": ajuste_nivel, "u6_maquinas": maquinas, "u6_arbol_2013": arbol_2013}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in ALL.items():
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
    print("svgs:", len(ALL))


if __name__ == "__main__":
    main()
