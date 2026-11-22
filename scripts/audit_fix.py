#!/usr/bin/env python3
"""Audit fixes: inline charts, story visuals, a few content gaps. Run from anywhere."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "content"


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def save(rel: str, data: dict) -> None:
    path = ROOT / rel
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("saved", rel)


# ---------- SVG helpers ----------
def svg_open(w=280, h=130, dark=True):
    bg = "none"
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="{h}" aria-hidden="true">'


def svg_close():
    return "</svg>"


INK = {"dark": "#d5dbe2", "light": "#1a2330"}
MUTED = {"dark": "#9aa3ad", "light": "#5c6670"}
ACC = {"dark": "#8cb4d6", "light": "#1f4e79"}
GOLD = {"dark": "#e8c56a", "light": "#a67c00"}
RUST = {"dark": "#e25b16", "light": "#c45c26"}
OK = {"dark": "#7dcea0", "light": "#1e7a46"}
GRID = {"dark": "rgba(255,255,255,.22)", "light": "#d0d5db"}


def axis(w, h, pad=28, dark=True, y0=None):
    y0 = h - 22 if y0 is None else y0
    c = GRID["dark" if dark else "light"]
    return f'<line x1="{pad}" y1="{y0}" x2="{w-8}" y2="{y0}" stroke="{c}" stroke-width="1.2"/>'


def factories_chart(dark=True):
    # A: 490,510,495,505  B: 200,800,350,650
    A, B = [490, 510, 495, 505], [200, 800, 350, 650]
    w, h, pad, y0 = 280, 132, 28, 108
    ymin, ymax = 0, 850
    def yy(v):
        return y0 - (v - ymin) / (ymax - ymin) * 86
    xs = [48, 100, 152, 204]
    d = "dark" if dark else "light"
    acc, rust, muted, gold = ACC[d], RUST[d], MUTED[d], GOLD[d]
    parts = [svg_open(w, h), axis(w, h, pad, dark, y0)]
    # mean line 500
    parts.append(f'<line x1="{pad}" y1="{yy(500)}" x2="250" y2="{yy(500)}" stroke="{gold}" stroke-width="1" stroke-dasharray="3 3"/>')
    parts.append(f'<text x="254" y="{yy(500)+3}" font-size="9" fill="{gold}">500</text>')
    def poly(vals, color):
        pts = " ".join(f"{x},{yy(v)}" for x, v in zip(xs, vals))
        dots = "".join(f'<circle cx="{x}" cy="{yy(v)}" r="3.2" fill="{color}"/>' for x, v in zip(xs, vals))
        return f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{pts}"/>{dots}'
    parts.append(poly(A, acc))
    parts.append(poly(B, rust))
    for i, lab in enumerate(["1", "2", "3", "4"]):
        parts.append(f'<text x="{xs[i]}" y="124" font-size="9" fill="{muted}" text-anchor="middle">Mes {lab}</text>')
    parts.append(f'<text x="40" y="14" font-size="10" fill="{acc}" font-weight="700">A (s≈9)</text>')
    parts.append(f'<text x="110" y="14" font-size="10" fill="{rust}" font-weight="700">B (s≈274)</text>')
    parts.append(svg_close())
    return "".join(parts)


def campana(case="c1", dark=True):
    """Schematic normal curve. case: c1 P(X<620), c2 P(X>620), c3 P(X<420), c4 between, c5 inverse."""
    d = "dark" if dark else "light"
    acc, gold, rust, muted, ink = ACC[d], GOLD[d], RUST[d], MUTED[d], INK[d]
    w, h = 280, 120
    # curve
    curve = '<path d="M 16 100 C 40 100, 58 18, 140 18 C 222 18, 240 100, 264 100" fill="none" stroke="%s" stroke-width="2.2"/>' % acc
    base = f'<line x1="20" y1="100" x2="260" y2="100" stroke="{GRID[d]}" stroke-width="1.2"/>'
    mu = f'<line x1="140" y1="18" x2="140" y2="100" stroke="{gold}" stroke-width="1" stroke-dasharray="3 3"/>'
    mu_t = f'<text x="140" y="114" font-size="10" fill="{gold}" text-anchor="middle">μ=500</text>'
    parts = [svg_open(w, h), curve, base, mu, mu_t]
    if case == "c1":
        # fill left of 200 (620)
        parts.append(f'<path d="M 16 100 C 40 100, 58 18, 140 18 C 175 18, 190 40, 200 58 L 200 100 L 16 100 Z" fill="{acc}" fill-opacity=".35"/>')
        parts.append(f'<line x1="200" y1="100" x2="200" y2="58" stroke="{rust}" stroke-width="2"/>')
        parts.append(f'<text x="200" y="114" font-size="9" fill="{rust}" text-anchor="middle" font-weight="700">620</text>')
        parts.append(f'<text x="90" y="72" font-size="12" fill="{ink}" font-weight="700">93,3%</text>')
    elif case == "c2":
        parts.append(f'<path d="M 200 58 C 222 80, 240 100, 264 100 L 200 100 Z" fill="{rust}" fill-opacity=".4"/>')
        parts.append(f'<line x1="200" y1="100" x2="200" y2="58" stroke="{rust}" stroke-width="2"/>')
        parts.append(f'<text x="200" y="114" font-size="9" fill="{rust}" text-anchor="middle" font-weight="700">620</text>')
        parts.append(f'<text x="222" y="86" font-size="11" fill="{ink}" font-weight="700">6,7%</text>')
    elif case == "c3":
        parts.append(f'<path d="M 16 100 C 40 100, 58 18, 80 58 L 80 100 Z" fill="{rust}" fill-opacity=".4"/>')
        parts.append(f'<line x1="80" y1="100" x2="80" y2="58" stroke="{rust}" stroke-width="2"/>')
        parts.append(f'<text x="80" y="114" font-size="9" fill="{rust}" text-anchor="middle" font-weight="700">420</text>')
        parts.append(f'<text x="44" y="86" font-size="11" fill="{ink}" font-weight="700">15,9%</text>')
    elif case == "c4":
        parts.append(f'<path d="M 80 58 C 100 30, 120 18, 140 18 C 175 18, 190 40, 200 58 L 200 100 L 80 100 Z" fill="{acc}" fill-opacity=".35"/>')
        parts.append(f'<line x1="80" y1="100" x2="80" y2="58" stroke="{rust}" stroke-width="2"/>')
        parts.append(f'<line x1="200" y1="100" x2="200" y2="58" stroke="{rust}" stroke-width="2"/>')
        parts.append(f'<text x="80" y="114" font-size="9" fill="{rust}" text-anchor="middle">420</text>')
        parts.append(f'<text x="200" y="114" font-size="9" fill="{rust}" text-anchor="middle">620</text>')
        parts.append(f'<text x="140" y="70" font-size="12" fill="{ink}" font-weight="700" text-anchor="middle">77,5%</text>')
    elif case == "c5":
        parts.append(f'<path d="M 16 100 C 40 100, 58 18, 140 18 C 185 18, 205 48, 214 64 L 214 100 L 16 100 Z" fill="{acc}" fill-opacity=".35"/>')
        parts.append(f'<line x1="214" y1="100" x2="214" y2="64" stroke="{rust}" stroke-width="2"/>')
        parts.append(f'<text x="214" y="114" font-size="9" fill="{rust}" text-anchor="middle" font-weight="700">631</text>')
        parts.append(f'<text x="100" y="72" font-size="12" fill="{ink}" font-weight="700">95%</text>')
    parts.append(svg_close())
    return "".join(parts)


def scatter(dark=True):
    pts = [(10, 120), (15, 135), (8, 105), (18, 140), (6, 100)]
    w, h, pad, y0 = 280, 140, 32, 118
    d = "dark" if dark else "light"
    acc, muted, gold = ACC[d], MUTED[d], GOLD[d]
    xmin, xmax, ymin, ymax = 4, 20, 90, 150
    def xx(x):
        return pad + (x - xmin) / (xmax - xmin) * 220
    def yy(y):
        return y0 - (y - ymin) / (ymax - ymin) * 92
    parts = [svg_open(w, h), axis(w, h, pad, dark, y0)]
    parts.append(f'<line x1="{pad}" y1="20" x2="{pad}" y2="{y0}" stroke="{GRID[d]}" stroke-width="1.2"/>')
    # rough fit line
    parts.append(f'<line x1="{xx(6)}" y1="{yy(100)}" x2="{xx(18)}" y2="{yy(140)}" stroke="{gold}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    for x, y in pts:
        parts.append(f'<circle cx="{xx(x)}" cy="{yy(y)}" r="4" fill="{acc}"/>')
    parts.append(f'<text x="150" y="134" font-size="9" fill="{muted}" text-anchor="middle">Publicidad X (miles $)</text>')
    parts.append(f'<text x="12" y="70" font-size="9" fill="{muted}" transform="rotate(-90 12 70)">Ventas Y</text>')
    parts.append(svg_close())
    return "".join(parts)


def waves(dark=True):
    """Additive (constant amplitude) vs multiplicative (growing) schematic."""
    d = "dark" if dark else "light"
    acc, rust, muted = ACC[d], RUST[d], MUTED[d]
    w, h = 280, 128

    def series(ybase, grow, color, label, ylab):
        pts = []
        for i in range(25):
            x = 20 + i * 5
            trend = ybase - i * 0.9
            amp = 8 * (1 + grow * i / 12)
            y = trend + amp * __import__("math").sin(i * 0.85)
            pts.append(f"{x:.1f},{y:.1f}")
        return (
            f'<polyline fill="none" stroke="{color}" stroke-width="1.8" points="{" ".join(pts)}"/>'
            f'<text x="20" y="{ylab}" font-size="9" fill="{color}" font-weight="700">{label}</text>'
        )

    parts = [svg_open(w, h)]
    parts.append(series(44, 0, acc, "Aditivo: ondas del mismo tamaño", 14))
    parts.append(series(100, 1.1, rust, "Multiplicativo: ondas que se agrandan", 70))
    parts.append(svg_close())
    return "".join(parts)


def correlogram(values, highlight=None, band=0.29, dark=True, labels=None, w=280, h=140):
    """values: list of (k, r) ; highlight: set of k."""
    highlight = set(highlight or [])
    d = "dark" if dark else "light"
    acc, rust, gold, muted, grid = ACC[d], RUST[d], GOLD[d], MUTED[d], GRID[d]
    ks = [k for k, _ in values]
    pad, y0, top = 28, 78, 16
    def yy(r):
        # r from -0.2 to 1.0
        return y0 - (r - (-0.15)) / (1.0 - (-0.15)) * (y0 - top)
    n = len(values)
    gap = (w - pad - 10) / max(n, 1)
    parts = [svg_open(w, h)]
    parts.append(f'<line x1="{pad}" y1="{yy(0)}" x2="{w-8}" y2="{yy(0)}" stroke="{grid}" stroke-width="1.2"/>')
    if band:
        parts.append(f'<line x1="{pad}" y1="{yy(band)}" x2="{w-8}" y2="{yy(band)}" stroke="{gold}" stroke-width="1" stroke-dasharray="3 3"/>')
        parts.append(f'<line x1="{pad}" y1="{yy(-band)}" x2="{w-8}" y2="{yy(-band)}" stroke="{gold}" stroke-width="1" stroke-dasharray="3 3"/>')
        parts.append(f'<text x="{w/2}" y="12" font-size="8" fill="{gold}" text-anchor="middle">banda ±2/√n</text>')
    bw = max(6, gap * 0.55)
    for i, (k, r) in enumerate(values):
        x = pad + i * gap + gap * 0.2
        color = rust if k in highlight else acc
        y = yy(r)
        yb = yy(0)
        top_y, ht = (y, yb - y) if r >= 0 else (yb, y - yb)
        parts.append(f'<rect x="{x}" y="{top_y}" width="{bw}" height="{max(ht,0.8)}" fill="{color}"/>')
        parts.append(f'<text x="{x+bw/2}" y="{h-8}" font-size="8" fill="{muted}" text-anchor="middle">{k}</text>')
    parts.append(svg_close())
    return "".join(parts)


def error_bars(dark=True):
    # MAD, MSE, MAPE, PME for A and B. PME can be negative.
    # Scale each group independently? Better 4 panels. Or two groups: precision vs bias.
    # I'll do grouped bars for MAD, MSE/10, MAPE, PME (same chart with note).
    d = "dark" if dark else "light"
    acc, rust, muted, gold = ACC[d], RUST[d], MUTED[d], GOLD[d]
    # values already comparable if we plot 4 mini charts
    items = [
        ("MAD", 4.83, 6.50, False),
        ("MSE", 26.2, 65.2, False),
        ("MAPE %", 4.3, 5.9, False),
        ("PME %", 2.5, -0.6, True),
    ]
    w, h = 280, 132
    parts = [svg_open(w, h)]
    parts.append(f'<text x="28" y="12" font-size="9" fill="{acc}" font-weight="700">A</text>')
    parts.append(f'<text x="52" y="12" font-size="9" fill="{rust}" font-weight="700">B</text>')
    for i, (name, a, b, signed) in enumerate(items):
        x0 = 16 + i * 66
        # scale
        mx = max(abs(a), abs(b), 0.1)
        axis_y = 100 if signed else 110
        def ht(v):
            return abs(v) / mx * (50 if signed else 70)
        def bar(val, color, dx):
            hh = ht(val)
            if signed:
                y = axis_y - hh if val >= 0 else axis_y
            else:
                y = axis_y - hh
            return f'<rect x="{x0+dx}" y="{y}" width="14" height="{max(hh,0.8)}" fill="{color}"/>'
        parts.append(bar(a, acc, 12))
        parts.append(bar(b, rust, 30))
        parts.append(f'<line x1="{x0+6}" y1="{axis_y}" x2="{x0+52}" y2="{axis_y}" stroke="{GRID[d]}" stroke-width="1"/>')
        parts.append(f'<text x="{x0+30}" y="126" font-size="9" fill="{muted}" text-anchor="middle">{name}</text>')
        # labels
        def fmt(v):
            s = f"{v:.2f}".replace(".", ",")
            return s
        parts.append(f'<text x="{x0+19}" y="24" font-size="8" fill="{acc}" text-anchor="middle">{fmt(a)}</text>')
        parts.append(f'<text x="{x0+37}" y="24" font-size="8" fill="{rust}" text-anchor="middle">{fmt(b)}</text>')
    parts.append(svg_close())
    return "".join(parts)


def unit_chain(dark=True):
    d = "dark" if dark else "light"
    acc, gold, muted, rust = ACC[d], GOLD[d], MUTED[d], RUST[d]
    boxes = [
        (8, 40, 52, 36, "U1", "marco", acc),
        (72, 14, 48, 28, "U2", "demanda", gold),
        (72, 46, 48, 28, "U3", "BOM", gold),
        (128, 14, 48, 28, "U4", "proceso", gold),
        (128, 46, 48, 28, "U5", "stock", gold),
        (188, 40, 52, 36, "U6", "motor", rust),
        (248, 40, 28, 36, "U7", "ERP", acc),
    ]
    parts = [svg_open(284, 100)]
    # arrows
    parts.append(f'<path d="M 60 58 L 70 58" stroke="{muted}" stroke-width="1.4" marker-end=""/>')
    parts.append(f'<path d="M 176 44 L 186 56" stroke="{muted}" stroke-width="1.4"/>')
    parts.append(f'<path d="M 240 58 L 248 58" stroke="{muted}" stroke-width="1.4"/>')
    for x, y, w, h, t, sub, col in boxes:
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="none" stroke="{col}" stroke-width="1.6"/>')
        parts.append(f'<text x="{x+w/2}" y="{y+16}" font-size="11" fill="{col}" font-weight="700" text-anchor="middle">{t}</text>')
        parts.append(f'<text x="{x+w/2}" y="{y+28}" font-size="8" fill="{MUTED[d]}" text-anchor="middle">{sub}</text>')
    parts.append(svg_close())
    return "".join(parts)


def freq_bars(dark=True):
    # practice frequencies n=19
    items = [("MRP", 8), ("Pron", 6), ("Inv", 5), ("Bal", 4), ("PA", 2), ("HM", 2), ("MPS", 1), ("Cap", 1)]
    d = "dark" if dark else "light"
    acc, muted, gold = ACC[d], MUTED[d], GOLD[d]
    w, h, pad, y0 = 280, 132, 28, 112
    mx = 8
    gap = (w - pad - 8) / len(items)
    parts = [svg_open(w, h), axis(w, h, pad, dark, y0)]
    for i, (name, v) in enumerate(items):
        x = pad + i * gap + 4
        hh = v / mx * 82
        col = gold if name == "MRP" else acc
        parts.append(f'<rect x="{x}" y="{y0-hh}" width="{gap*0.6}" height="{hh}" fill="{col}"/>')
        parts.append(f'<text x="{x+gap*0.3}" y="126" font-size="8" fill="{muted}" text-anchor="middle">{name}</text>')
        parts.append(f'<text x="{x+gap*0.3}" y="{y0-hh-3}" font-size="8" fill="{col}" text-anchor="middle">{v}</text>')
    parts.append(svg_close())
    return "".join(parts)


def plan_chain(dark=True):
    d = "dark" if dark else "light"
    acc, gold, muted = ACC[d], GOLD[d], MUTED[d]
    labels = ["MPS", "CRP", "MRP", "PAC", "ERP"]
    parts = [svg_open(280, 72)]
    for i, lab in enumerate(labels):
        x = 8 + i * 55
        col = gold if lab in ("MPS", "MRP") else acc
        parts.append(f'<rect x="{x}" y="18" width="46" height="32" rx="6" fill="none" stroke="{col}" stroke-width="1.6"/>')
        parts.append(f'<text x="{x+23}" y="39" font-size="12" fill="{col}" font-weight="700" text-anchor="middle">{lab}</text>')
        if i < len(labels) - 1:
            parts.append(f'<text x="{x+50}" y="40" font-size="12" fill="{muted}">→</text>')
    parts.append(svg_close())
    return "".join(parts)


def conversion(dark=True):
    d = "dark" if dark else "light"
    acc, gold, rust = ACC[d], GOLD[d], RUST[d]
    labs = [("Insumos", acc), ("Transformación", gold), ("Productos", rust)]
    parts = [svg_open(280, 72)]
    for i, (lab, col) in enumerate(labs):
        x = 8 + i * 92
        parts.append(f'<rect x="{x}" y="16" width="80" height="36" rx="8" fill="none" stroke="{col}" stroke-width="1.6"/>')
        parts.append(f'<text x="{x+40}" y="39" font-size="10" fill="{col}" font-weight="700" text-anchor="middle">{lab}</text>')
        if i < 2:
            parts.append(f'<text x="{x+82}" y="40" font-size="14" fill="{MUTED[d]}">→</text>')
    parts.append(svg_close())
    return "".join(parts)


def circuit(dark=True):
    d = "dark" if dark else "light"
    acc, gold, rust, muted = ACC[d], GOLD[d], RUST[d], MUTED[d]
    labs = ["1 Graficar", "2 Diagnosticar", "3 Elegir", "4 Aplicar", "5 Medir"]
    parts = [svg_open(280, 100)]
    for i, lab in enumerate(labs):
        x = 8 + i * 54
        col = rust if i == 4 else (gold if i in (1, 2) else acc)
        parts.append(f'<rect x="{x}" y="16" width="50" height="36" rx="6" fill="none" stroke="{col}" stroke-width="1.5"/>')
        parts.append(f'<text x="{x+25}" y="38" font-size="8" fill="{col}" font-weight="700" text-anchor="middle">{lab}</text>')
        if i < 4:
            parts.append(f'<text x="{x+50}" y="39" font-size="11" fill="{muted}">→</text>')
    # back arrow
    parts.append(f'<path d="M 258 54 Q 140 92, 22 54" fill="none" stroke="{rust}" stroke-width="1.4" stroke-dasharray="3 2"/>')
    parts.append(f'<text x="140" y="94" font-size="9" fill="{rust}" text-anchor="middle">si el error anda mal, volvés a elegir</text>')
    parts.append(svg_close())
    return "".join(parts)


def upsert_svg(teoria, caption_sub, svg):
    for b in teoria:
        if b.get("type") == "svg" and caption_sub in (b.get("caption") or ""):
            b["svg"] = svg
            return True
    return False

def already(teoria, block):
    cap = block.get("caption") or block.get("tex") or block.get("text") or ""
    if not cap:
        return False
    blob = json.dumps(teoria, ensure_ascii=False)
    return cap in blob

def insert_after(teoria, pred, blocks):
    blocks = [b for b in blocks if not already(teoria, b)]
    if not blocks:
        return False
    for i, b in enumerate(teoria):
        if pred(b):
            for j, nb in enumerate(blocks):
                teoria.insert(i + 1 + j, nb)
            return True
    return False


def find_story(historias, title_sub):
    for c in historias:
        if title_sub in (c.get("title") or ""):
            return c
    return None


# ---------- per-class patches ----------
def fix_c0(d):
    # story visuals
    h = d["historias"]
    find_story(h, "Son 7 unidades")["svg"] = unit_chain(True)
    find_story(h, "Son 7 unidades")["chartLabel"] = "U1 marco · U2–U5 insumos · U6 motor · U7 software"
    find_story(h, "Cuatro insumos")["svg"] = unit_chain(True)
    find_story(h, "Cuatro insumos")["chartLabel"] = "La U6 consume demanda, BOM, capacidad y stock"
    c = find_story(h, "El peso se cuenta")
    c["svg"] = freq_bars(True)
    c["chartLabel"] = "Mesas con el tema en la práctica (n=19 finales con fecha)"
    # also add light chart in teoria after frequency table heading? after the practice table
    insert_after(
        d["teoria"],
        lambda b: b.get("type") == "table" and (b.get("headers") or [""])[0] == "Tema de práctica",
        [{"type": "svg", "svg": freq_bars(False), "caption": "Conteo de mesas (n=19) por tema de práctica. MRP es el más frecuente; la regresión no aparece en este set."}],
    )
    return d


def fix_c01(d):
    h = d["historias"]
    c = find_story(h, "MPS dice el qué")
    c["svg"] = plan_chain(True)
    c["chartLabel"] = "Cadena corta: el MPS alimenta al MRP; el ERP las empaqueta"
    # shorten ABC card
    c8 = find_story(h, "ABC por valor")
    if c8 and len(c8.get("text") or "") > 260:
        c8["text"] = "ABC clasifica ítems por valor de consumo (A pocos y valiosos, C muchos y baratos). SS es el stock de seguridad: cubre la incertidumbre de la demanda o del lead time. OP/OC es el punto de pedido."
    # LEC glossary
    for b in d["teoria"]:
        if b.get("type") == "glosario":
            for e in b.get("entries") or []:
                if e.get("simbolo") == "LEC":
                    extra = " En el OCR de EjerciciosFinalesResueltos.pdf (p.30), un EOQ de *compra* (hospital, 500 kg de algodón) pregunta «Cual es su L.E.C.». Eso refuerza esta lectura, pero la frase «lote económico de compra» sigue sin aparecer completa en el material."
                    if "Cual es su L.E.C." not in (e.get("significado") or ""):
                        e["significado"] = (e.get("significado") or "") + extra
    return d


def fix_c1(d):
    insert_after(
        d["teoria"],
        lambda b: b.get("type") == "table" and "Promedio" in (b.get("headers") or []),
        [{"type": "svg", "svg": factories_chart(False), "caption": "Mismo promedio (500). La A casi no se mueve; la B pega saltos de 200 a 800."}],
    )
    # stories already have some charts; ensure factory chart on first data card if missing is ok
    return d


def fix_c1b(d):
    # add Z formulas after 4-step method list
    insert_after(
        d["teoria"],
        lambda b: b.get("type") == "heading" and "Método de los 4 pasos" in (b.get("text") or ""),
        [
            {"type": "formula", "tex": r"Z = \frac{X - \mu}{\sigma}"},
            {"type": "paragraph", "text": "*¿A cuántos desvíos del promedio está X?* Después, en el caso inverso:"},
            {"type": "formula", "tex": r"X = \mu + Z\cdot\sigma"},
            {"type": "paragraph", "text": "Es la des-estandarización: la del stock de seguridad. Para cola izquierda, X = μ − Z·σ."},
        ],
    )
    h = d["historias"]
    mapping = {
        "«Menos que» un X mayor": ("c1", "μ = 500, σ = 80 · P(X < 620) = 93,3%"),
        "«Más que» es el complemento": ("c2", "P(X > 620) = 6,7%, complemento del caso 1"),
        "Z negativo: usá la simetría": ("c3", "P(X < 420): Z = −1 → por simetría, 15,9%"),
        "Entre dos valores: sumo o resto": ("c4", "P(420 < X < 620) = 0,3413 + 0,4332 = 77,5%"),
        "El inverso: el del stock de seguridad": ("c5", "Cobertura 95% → Z ≈ 1,64 → X = 500 + 1,64×80 = 631"),
    }
    for sub, (case, lab) in mapping.items():
        c = find_story(h, sub)
        if c:
            c["svg"] = campana(case, True)
            c["chartLabel"] = lab
    return d


def fix_c2(d):
    insert_after(
        d["teoria"],
        lambda b: b.get("type") == "paragraph" and "Al graficar se ve que suben juntos" in (b.get("text") or ""),
        [{"type": "svg", "svg": scatter(False), "caption": "Diagrama de dispersión del ejemplo: publicidad (X) vs. ventas (Y). Nube lineal positiva, puntos apretados — el r ≈ 0,98 se ve antes de calcularlo."}],
    )
    h = d["historias"]
    c = find_story(h, "Siempre se grafica primero")
    if c:
        c["svg"] = scatter(True)
        c["chartLabel"] = "Publicidad vs. ventas (5 meses del apunte)"
    c = find_story(h, "Publicidad y ventas")
    if c:
        c["svg"] = scatter(True)
        c["chartLabel"] = "r ≈ 0,98: casi una recta"
    # shorten close a bit
    cl = find_story(h, "Llevate esto de la Clase 2")
    if cl and len(cl.get("text") or "") > 250:
        cl["text"] = "Siempre graficá primero. r dice si hay relación lineal, no si hay causa, y un r bajo no descarta una curva. r² es el % de variación que explica el modelo. El ejercicio de temperatura y bebidas queda para resolver juntos."
    return d


def fix_c3a(d):
    insert_after(
        d["teoria"],
        lambda b: b.get("type") == "heading" and "Cómo se combinan" in (b.get("text") or ""),
        [{"type": "svg", "svg": waves(False), "caption": "Arriba, modelo aditivo (ondas de amplitud constante). Abajo, multiplicativo (las ondas se agrandan con la tendencia). Esquema del criterio del apunte, no una serie real."}],
    )
    h = d["historias"]
    c = find_story(h, "Aditivo o multiplicativo")
    if c:
        c["svg"] = waves(True)
        c["chartLabel"] = "Aditivo: mismas ondas. Multiplicativo: se agrandan con la tendencia"
        # the card also has a formula and long text — trim text slightly
        if len(c.get("text") or "") > 240:
            c["text"] = "Aditivo: los componentes se suman (en diciembre, +200 unidades). Multiplicativo: se multiplican (en diciembre, +40%). En la industria, el multiplicativo es el más común, y es el que nombra el programa."
    c = find_story(h, "T, C, S e I")
    if c and len(c.get("text") or "") > 260:
        c["text"] = "Tendencia (largo plazo), ciclo (ondas de varios años, período variable), estacionalidad (se repite con período fijo: L=4 trimestral, L=12 mensual) e irregularidad (el ruido impredecible)."
    cl = find_story(h, "Llevate esto de la Clase 3.a")
    if cl and len(cl.get("text") or "") > 250:
        cl["text"] = "El orden de la serie es información. Diagnosticá T, C, S e I a ojo, decidí aditivo o multiplicativo, y usá el árbol para justificar el método. El ejercicio de las 4 series queda para resolver juntos."
    return d


def fix_c3b(d):
    # n=48 values: r1=0.85 ... r4=0.50, r11=0.15, r12=0.68, r13=0.55. Don't invent r5-r10.
    vals = [(1, 0.85), (2, 0.72), (3, 0.61), (4, 0.50), (11, 0.15), (12, 0.68), (13, 0.55)]
    chart = correlogram(vals, highlight={12}, band=2 / (48 ** 0.5), dark=False)
    insert_after(
        d["teoria"],
        lambda b: b.get("type") == "list" and any("r₁₂=0,68" in (i or "") or "r12=0,68" in (i or "") or "repunte marcado" in (i or "") for i in (b.get("items") or []))
        or (b.get("type") == "paragraph" and "r₁=0,85" in (b.get("text") or "")),
        [{"type": "svg", "svg": correlogram(vals, highlight={12}, band=2 / (48 ** 0.5), dark=False), "caption": "Correlograma del ejemplo (n=48): decaimiento de r₁ a r₄, y un pico en r₁₂ que rompe la caída. Solo se grafican los lags que da el apunte (no se inventan r₅–r₁₀). La banda punteada es ±2/√48 ≈ ±0,29."}],
    )
    h = d["historias"]
    c = find_story(h, "Ventas mensuales, n = 48") or find_story(h, "n = 48")
    if not c:
        c = find_story(h, "Cada patrón deja")
    if c:
        c["svg"] = correlogram(vals, highlight={12}, band=2 / (48 ** 0.5), dark=True)
        c["chartLabel"] = "n=48 · pico en r₁₂ (estacionalidad anual) · banda ±2/√n"
    cl = find_story(h, "Llevate esto de la Clase 3.b")
    if cl and len(cl.get("text") or "") > 250:
        cl["text"] = "El correlograma es el diagnóstico con números: decaimiento = tendencia, pico en r_L = estacionalidad. Fuera de ±2/√n, el patrón es real. También se aplica a los errores del modelo. El ejercicio queda para resolver juntos."
    return d


def fix_c4(d):
    insert_after(
        d["teoria"],
        lambda b: b.get("type") == "paragraph" and "cada medida dice algo" in (b.get("text") or "").lower()
        or (b.get("type") == "callout" and "Se recomienda el método A" in (b.get("text") or "")),
        [{"type": "svg", "svg": error_bars(False), "caption": "Comparación del ejemplo (6 meses): A gana en MAD, MSE y MAPE (más preciso); B está un poco mejor centrado (PME más cerca de 0). El MSE de B se dispara por el error de −15 del mes 5."}],
    )
    # fallback: after PME of method B numbers
    if not any(b.get("type") == "svg" and "Comparación del ejemplo" in (b.get("caption") or "") for b in d["teoria"]):
        insert_after(
            d["teoria"],
            lambda b: b.get("type") == "heading" and "Interpretación" in (b.get("text") or ""),
            [{"type": "svg", "svg": error_bars(False), "caption": "Comparación del ejemplo (6 meses): A más preciso; B un poco mejor centrado. El MSE de B se dispara por el −15 del mes 5."}],
        )
    h = d["historias"]
    c = find_story(h, "Cada medida dice algo distinto") or find_story(h, "Unidades reales vs")
    if c:
        c["svg"] = error_bars(True)
        c["chartLabel"] = "Método A vs. B: MAD, MSE, MAPE y PME del ejemplo"
    cl = find_story(h, "Llevate esto de la Clase 4")
    if cl and len(cl.get("text") or "") > 250:
        cl["text"] = "Usá las cuatro medidas: MAD (unidades), MSE (castiga lo grande), MAPE (%) y PME (sesgo). Validá en datos de prueba, no en los de ajuste. El ejercicio X vs. Y queda para resolver juntos."
    return d


def fix_cint(d):
    insert_after(
        d["teoria"],
        lambda b: b.get("type") == "heading" and ("proceso completo" in (b.get("text") or "").lower() or "5 pasos" in (b.get("text") or "")),
        [{"type": "svg", "svg": circuit(False), "caption": "El pronóstico es un circuito: si el error delata un patrón no capturado (PME alto y del mismo signo), se vuelve a elegir el método."}],
    )
    # ice-cream / winter correlogram schematic from the example description: pico r4 and r8
    vals = [(1, 0.72), (2, 0.55), (3, 0.38), (4, 0.82), (5, 0.30), (6, 0.22), (7, 0.18), (8, 0.61)]
    # WAIT - don't invent ice cream correlogram numbers. The integrador table is qualitative ("pico grande en r4 y otro en r8; las primeras barras decaen").
    # I should NOT invent exact r values. Use a clearly schematic chart labeled as such, or skip numbers.
    # Skip invented numbers. Only use circuit visual.
    h = d["historias"]
    c = find_story(h, "Tres clases, un solo procedimiento") or find_story(h, "Elegir, aplicar, medir")
    if c:
        c["svg"] = circuit(True)
        c["chartLabel"] = "Graficar → correlograma → árbol → aplicar → medir, y volver si falla"
    c = find_story(h, "De punta a punta")
    if c and len(c.get("text") or "") > 260:
        c["text"] = "Heladería, ventas trimestrales: el gráfico sospecha T+S; el correlograma lo prueba (pico en r₄ y decaimiento); el árbol pide Winter; el MAPE 5% y el PME ≈ 0 confirman."
    c = find_story(h, "Elegir, aplicar, medir")
    if c and len(c.get("text") or "") > 250:
        c["text"] = "El árbol propone el método (paso 3). Lo aplicás (paso 4, clases 5 en adelante). Medís MAD, MSE, MAPE y PME (paso 5). Si el error anda mal, no afines a ciegas: volvé a elegir."
    return d


def fix_u1(d):
    insert_after(
        d["teoria"],
        lambda b: b.get("type") == "heading" and "conversión" in (b.get("text") or "").lower()
        or (b.get("type") == "paragraph" and "insumos" in (b.get("text") or "").lower() and "transform" in (b.get("text") or "").lower()),
        [{"type": "svg", "svg": conversion(False), "caption": "Proceso de conversión del mapa y del Documento Maestro: insumos → transformación → productos."}],
    )
    h = d["historias"]
    c = find_story(h, "Insumos → transformación")
    if c:
        c["svg"] = conversion(True)
        c["chartLabel"] = "El proceso de conversión"
    return d


def main():
    jobs = [
        ("u2/clase00.json", fix_c0),
        ("u2/clase01_siglas.json", fix_c01),
        ("u2/clase01.json", fix_c1),
        ("u2/clase01b.json", fix_c1b),
        ("u2/clase02.json", fix_c2),
        ("u2/clase03a.json", fix_c3a),
        ("u2/clase03b.json", fix_c3b),
        ("u2/clase04.json", fix_c4),
        ("u2/integrador.json", fix_cint),
        ("u1/enfoque.json", fix_u1),
    ]
    for rel, fn in jobs:
        d = load(rel)
        fn(d)
        save(rel, d)


if __name__ == "__main__":
    main()
