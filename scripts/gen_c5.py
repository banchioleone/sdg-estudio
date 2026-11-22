#!/usr/bin/env python3
"""Genera clase05.json a partir del material (Hanke 25p/7p, Resumen V6, Chase, árbol 3.a, examen SG!EVA)."""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "content" / "u2" / "clase05.json"

NAVY = "#1f4e79"
ORANGE = "#c45c26"
MUTED = "#5c6670"
LINE = "#d0d5db"
INK = "#1a1f24"
ST_BLUE = "#8cb4d6"
ST_ORANGE = "#e25b16"
ST_MUTED = "#b7c0c8"
ST_LINE = "#5a6570"


def svg_chase(dark: bool = False) -> str:
    """Ventas Chase (Resumen V6): 100, 90, 105, 95 y Ŷ5 = 97,5."""
    ink = "#e8eef4" if dark else INK
    navy = ST_BLUE if dark else NAVY
    orange = ST_ORANGE if dark else ORANGE
    muted = ST_MUTED if dark else MUTED
    grid = ST_LINE if dark else LINE
    # plot box
    L, R, T, B = 32, 268, 22, 108
    # y range 80–115
    ymin, ymax = 80, 116

    def X(m):
        return L + (m - 1) * (R - L) / 5

    def Y(v):
        return B - (v - ymin) / (ymax - ymin) * (B - T)

    pts = [(1, 100), (2, 90), (3, 105), (4, 95)]
    path = " ".join(f"{X(m):.1f},{Y(v):.1f}" for m, v in pts)
    ticks = "".join(
        f'<text x="{X(m):.1f}" y="{B+14:.0f}" font-size="9" fill="{muted}" text-anchor="middle">{lab}</text>'
        for m, lab in [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
    )
    ylabs = "".join(
        f'<text x="{L-6}" y="{Y(v)+3:.1f}" font-size="8" fill="{muted}" text-anchor="end">{v}</text>'
        for v in (90, 100, 110)
    )
    grids = "".join(
        f'<line x1="{L}" y1="{Y(v):.1f}" x2="{R}" y2="{Y(v):.1f}" stroke="{grid}" stroke-width="0.6"/>'
        for v in (90, 100, 110)
    )
    dots = "".join(
        f'<circle cx="{X(m):.1f}" cy="{Y(v):.1f}" r="3.2" fill="{navy}"/>'
        for m, v in pts
    )
    return (
        f'<svg viewBox="0 0 280 140" width="100%" height="140" aria-hidden="true">'
        f'<text x="8" y="12" font-size="9" fill="{navy}" font-weight="700">Ventas reales</text>'
        f'<text x="118" y="12" font-size="9" fill="{orange}" font-weight="700">Ŷ mes 5 = 97,5</text>'
        f"{grids}"
        f'<line x1="{L}" y1="{T}" x2="{L}" y2="{B}" stroke="{grid}" stroke-width="1"/>'
        f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="{grid}" stroke-width="1"/>'
        f'{ylabs}{ticks}'
        f'<polyline fill="none" stroke="{navy}" stroke-width="1.8" points="{path}"/>'
        f"{dots}"
        f'<line x1="{X(4):.1f}" y1="{Y(95):.1f}" x2="{X(5):.1f}" y2="{Y(97.5):.1f}" stroke="{orange}" stroke-width="1.8" stroke-dasharray="4 3"/>'
        f'<circle cx="{X(5):.1f}" cy="{Y(97.5):.1f}" r="4" fill="none" stroke="{orange}" stroke-width="1.8"/>'
        f'<text x="{X(5)+6:.1f}" y="{Y(97.5)+3:.1f}" font-size="9" fill="{orange}" font-weight="700">97,5</text>'
        f'<text x="140" y="134" font-size="8" fill="{muted}" text-anchor="middle">Datos de Chase, Resumen V6</text>'
        f"</svg>"
    )


def svg_weights(dark: bool = False) -> str:
    navy = ST_BLUE if dark else NAVY
    orange = ST_ORANGE if dark else ORANGE
    muted = ST_MUTED if dark else MUTED
    line = ST_LINE if dark else LINE
    # weights 10, 20, 30, 40 for months 1..4 (oldest to newest)
    ws = [10, 20, 30, 40]
    cols = [navy, navy, navy, orange]
    L, R, T, B = 28, 260, 22, 108
    maxw = 40
    bar_w = 28
    gap = (R - L) / 4
    bars = []
    for i, (w, c) in enumerate(zip(ws, cols)):
        cx = L + gap * (i + 0.5)
        h = (w / maxw) * (B - T)
        x = cx - bar_w / 2
        y = B - h
        bars.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w}" height="{h:.1f}" fill="{c}" rx="3"/>'
            f'<text x="{cx:.1f}" y="{y-4:.1f}" font-size="10" fill="{c}" font-weight="700" text-anchor="middle">{w}%</text>'
            f'<text x="{cx:.1f}" y="{B+14:.0f}" font-size="9" fill="{muted}" text-anchor="middle">Mes {i+1}</text>'
        )
    return (
        f'<svg viewBox="0 0 280 136" width="100%" height="136" aria-hidden="true">'
        f'<text x="8" y="12" font-size="9" fill="{muted}">Ponderaciones de Chase (suman 100%)</text>'
        f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="{line}" stroke-width="1"/>'
        + "".join(bars)
        + f'<text x="140" y="132" font-size="8" fill="{muted}" text-anchor="middle">El mes más reciente (4) lleva el 40%.</text>'
        f"</svg>"
    )


def svg_window(dark: bool = False) -> str:
    """Esquema de ventana deslizante MA(k). No es una serie del apunte."""
    navy = ST_BLUE if dark else NAVY
    orange = ST_ORANGE if dark else ORANGE
    muted = ST_MUTED if dark else MUTED
    line = ST_LINE if dark else LINE
    fill_win = "#e25b1633" if dark else "#c45c2622"
    boxes = []
    labels = ["Yₜ₋₄", "Yₜ₋₃", "Yₜ₋₂", "Yₜ₋₁", "Yₜ", "Ŷₜ₊₁"]
    # 5 observations + forecast
    xs = [18, 58, 98, 138, 178, 230]
    for i, (x, lab) in enumerate(zip(xs, labels)):
        if i < 5:
            color = navy if i >= 2 else muted
            stroke = navy if i >= 2 else line
            boxes.append(
                f'<rect x="{x}" y="48" width="34" height="28" rx="5" fill="none" stroke="{stroke}" stroke-width="1.4"/>'
                f'<text x="{x+17}" y="66" font-size="9" fill="{color}" text-anchor="middle" font-weight="700">{lab}</text>'
            )
        else:
            boxes.append(
                f'<rect x="{x}" y="48" width="40" height="28" rx="5" fill="none" stroke="{orange}" stroke-width="1.6" stroke-dasharray="4 3"/>'
                f'<text x="{x+20}" y="66" font-size="9" fill="{orange}" text-anchor="middle" font-weight="700">{lab}</text>'
            )
    return (
        f'<svg viewBox="0 0 280 128" width="100%" height="128" aria-hidden="true">'
        f'<text x="8" y="14" font-size="9" fill="{muted}">Esquema — no es una serie del apunte</text>'
        f'<rect x="94" y="42" width="122" height="40" rx="8" fill="{fill_win}" stroke="{navy}" stroke-width="1.2"/>'
        f'<text x="155" y="36" font-size="9" fill="{navy}" font-weight="700" text-anchor="middle">ventana de k = 3</text>'
        + "".join(boxes)
        + f'<path d="M214 62 H228" stroke="{orange}" stroke-width="1.6" marker-end="none"/>'
        f'<text x="140" y="96" font-size="9" fill="{muted}" text-anchor="middle">Entra Yₜ, sale Yₜ₋₃. El promedio de la ventana es Ŷₜ₊₁.</text>'
        f'<text x="140" y="114" font-size="8" fill="{muted}" text-anchor="middle">Pesos iguales dentro de la ventana (Hanke / V6).</text>'
        f"</svg>"
    )


def svg_doble(dark: bool = False) -> str:
    navy = ST_BLUE if dark else NAVY
    orange = ST_ORANGE if dark else ORANGE
    muted = ST_MUTED if dark else MUTED
    line = ST_LINE if dark else LINE
    boxes = [
        (8, "Yₜ", "serie"),
        (60, "Mₜ", "MA(k)"),
        (112, "M′ₜ", "MA de M"),
        (164, "aₜ, bₜ", "nivel y pendiente"),
        (222, "Ŷₜ₊ₚ", "aₜ + bₜ p"),
    ]
    parts = []
    for i, (x, title, sub) in enumerate(boxes):
        color = orange if i == 4 else navy
        parts.append(
            f'<rect x="{x}" y="36" width="50" height="44" rx="8" fill="none" stroke="{color}" stroke-width="1.4"/>'
            f'<text x="{x+25}" y="54" font-size="11" fill="{color}" font-weight="700" text-anchor="middle">{title}</text>'
            f'<text x="{x+25}" y="70" font-size="7.5" fill="{muted}" text-anchor="middle">{sub}</text>'
        )
        if i < len(boxes) - 1:
            x2 = boxes[i + 1][0]
            parts.append(f'<path d="M{x+52} 58 H{x2-2}" stroke="{line}" stroke-width="1.2"/>')
    return (
        f'<svg viewBox="0 0 280 112" width="100%" height="112" aria-hidden="true">'
        f'<text x="8" y="16" font-size="9" fill="{muted}">Promedio móvil doble (Hanke / V6) · tendencia lineal</text>'
        + "".join(parts)
        + f'<text x="140" y="100" font-size="8" fill="{muted}" text-anchor="middle">aₜ = 2Mₜ − M′ₜ  bₜ = [2/(k−1)](Mₜ − M′ₜ)</text>'
        f"</svg>"
    )


def svg_k(dark: bool = False) -> str:
    """Esquema k chico vs k grande. No es una serie del apunte."""
    navy = ST_BLUE if dark else NAVY
    orange = ST_ORANGE if dark else ORANGE
    muted = ST_MUTED if dark else MUTED
    # a step change at mid, small k follows, large k lags
    def series_points():
        ys = [40, 38, 42, 39, 41, 80, 78, 82, 79, 81]
        n = len(ys)
        return [(16 + i * 24, 100 - y) for i, y in enumerate(ys)]

    def ma(k):
        ys = [40, 38, 42, 39, 41, 80, 78, 82, 79, 81]
        out = []
        for t in range(k - 1, len(ys)):
            m = sum(ys[t - k + 1 : t + 1]) / k
            out.append((16 + t * 24, 100 - m))
        return out

    def poly(pts, color, dash=""):
        s = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<polyline fill="none" stroke="{color}" stroke-width="1.7"{d} points="{s}"/>'

    raw = series_points()
    return (
        f'<svg viewBox="0 0 280 128" width="100%" height="128" aria-hidden="true">'
        f'<text x="8" y="12" font-size="9" fill="{muted}">Esquema — no es una serie del apunte</text>'
        f'<text x="8" y="26" font-size="9" fill="{navy}" font-weight="700">serie</text>'
        f'<text x="60" y="26" font-size="9" fill="{orange}" font-weight="700">k chico</text>'
        f'<text x="130" y="26" font-size="9" fill="{muted}" font-weight="700">k grande</text>'
        + poly(raw, navy)
        + poly(ma(3), orange)
        + poly(ma(6), muted, "4 3")
        + f'<text x="140" y="118" font-size="8" fill="{muted}" text-anchor="middle">k chico reacciona más rápido al cambio de nivel; k grande suaviza más y retrasa.</text>'
        f"</svg>"
    )


def svg_informal(dark: bool = False) -> str:
    """Esquema del informal «sin cambio»: el pronóstico copia el último valor."""
    navy = ST_BLUE if dark else NAVY
    orange = ST_ORANGE if dark else ORANGE
    muted = ST_MUTED if dark else MUTED
    ys = [62, 48, 70, 40, 58]
    pts = [(24 + i * 42, 20 + y) for i, y in enumerate(ys)]
    last = pts[-1]
    fut = (24 + 5 * 42, last[1])
    dots = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="{navy}"/>' for x, y in pts
    )
    path = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return (
        f'<svg viewBox="0 0 280 120" width="100%" height="120" aria-hidden="true">'
        f'<text x="8" y="14" font-size="9" fill="{muted}">Esquema — no es una serie del apunte</text>'
        f'<polyline fill="none" stroke="{navy}" stroke-width="1.8" points="{path}"/>'
        f"{dots}"
        f'<line x1="{last[0]:.1f}" y1="{last[1]:.1f}" x2="{fut[0]:.1f}" y2="{fut[1]:.1f}" stroke="{orange}" stroke-width="1.8" stroke-dasharray="4 3"/>'
        f'<circle cx="{fut[0]:.1f}" cy="{fut[1]:.1f}" r="4" fill="none" stroke="{orange}" stroke-width="1.8"/>'
        f'<text x="{fut[0]:.1f}" y="{fut[1]-10:.1f}" font-size="9" fill="{orange}" font-weight="700" text-anchor="middle">Ŷₜ₊₁ = Yₜ</text>'
        f'<text x="140" y="112" font-size="8" fill="{muted}" text-anchor="middle">El 100% del peso va al valor actual. Copia también las fluctuaciones.</text>'
        f"</svg>"
    )


def doc() -> dict:
    return {
        "unitId": "u2",
        "unitLabel": "Unidad 2",
        "unitTitle": "Métodos de pronósticos",
        "id": "c5",
        "title": "Clase 5 · Métodos no formales y promedios",
        "name": "No formales y promedios",
        "lede": "Los períodos recientes son, en estos métodos, los mejores pronosticadores del futuro. Arrancamos por los modelos informales y seguimos por promedio simple, móvil, móvil doble y —con Chase— el móvil ponderado. La suavización exponencial queda para la Clase 6.",
        "visto": False,
        "source": [
            "texto/resumenes/Resumen_Hanke_25p.txt (sección Promedios móviles y métodos de atenuación)",
            "texto/resumenes/Resumen_Sistema_de_Gestion_7p.txt",
            "texto/resumenes/ResumenSG-Final-V6_345p.txt (Cap. 4 Hanke y promedio ponderado de Chase, págs. 16–19 y 222–224 del resumen)",
            "texto/examenes/Formulas SdG.txt (título del capítulo)",
            "clases_previas/SG/ArbolDecisorio_MetodosPronostico.svg",
            "clases_previas/SG/Clase03a_SeriesDeTiempo.md (tabla estacionaria / tendencia)",
            "texto/examenes/SG!EVA.txt (ejercicio alimento para perros)",
            "texto/ocr/sg1_ppm/p-02.png (resolución manuscrita de SG1.doc, Final (1), ítem 2.1)",
        ],
        "laminas": ["u2/img/ArbolDecisorio_MetodosPronostico.svg"],
        "next": "Clase 6 · Suavizado exponencial simple (próximamente)",
        "teoria": teoria(),
        "historias": historias(),
    }


def teoria() -> list:
    return [
        {
            "type": "paragraph",
            "text": "**Sistemas de Gestión (UTN FRRo) · Unidad 2.c · Serie: 0 → 0.1 → 1 → 1.b → 2 → 3.a → 3.b → 4 → Integrador → **5**",
        },
        {
            "type": "callout",
            "kind": "aviso",
            "text": "**De dónde sale esta clase.** No hay un apunte de la cátedra titulado «Clase 5». Se arma con el resumen de Hanke (25 páginas y 7 páginas), el Capítulo 4 del Resumen V6, el árbol de la Clase 3.a y un ejemplo de promedio móvil ponderado de Chase que está en el mismo Resumen V6. En el plan de clases y en el Documento Maestro se habló de «métodos ingenuos»; Hanke y el V6 dicen **métodos no formales** o **informales**. No presento «ingenuo» como término de Hanke. La suavización exponencial, que el Documento Maestro agrupa en la misma semana, queda para la **Clase 6**.",
        },
        {
            "type": "callout",
            "kind": "idea",
            "text": "**Idea central:** hay tres enfoques sencillos en este capítulo: el **informal**, el de **promedios** y el de **suavización**. Esta clase cubre los dos primeros. Todos parten de la misma idea: las fluctuaciones de corto plazo se tratan como apartamientos aleatorios de una estructura, y esa estructura se proyecta hacia adelante.",
        },
        {
            "type": "heading",
            "level": 2,
            "text": "1. Dónde encajan en el árbol",
        },
        {
            "type": "paragraph",
            "text": "En la Clase 3.a quedó armada la primera bifurcación: *¿la serie es estacionaria?* (el promedio no cambia a lo largo del tiempo). El árbol de la cátedra asigna así las familias de esta clase:",
        },
        {
            "type": "table",
            "headers": ["Diagnóstico (Clase 3.a)", "Métodos de esta clase"],
            "rows": [
                [
                    "**Estacionaria**",
                    "promedio simple, promedio móvil (además, más adelante: suavizado exponencial simple y Box-Jenkins)",
                ],
                [
                    "**Tiene tendencia**",
                    "promedio móvil doble (además: Brown, Holt, regresión, modelos exponenciales)",
                ],
            ],
            "caption": "Recorte del árbol y de la tabla de la Clase 3.a. No se inventan asignaciones nuevas.",
        },
        {
            "type": "svg",
            "file": "u2/img/ArbolDecisorio_MetodosPronostico.svg",
            "caption": "Árbol decisorio de métodos de pronóstico (lámina oficial de la cátedra)",
        },
        {
            "type": "callout",
            "kind": "examen",
            "text": "**En el examen**, «justifique la metodología aplicada» se responde con este árbol: si la serie es estacionaria, un promedio simple o un promedio móvil son candidatos; si tiene tendencia lineal, el candidato de esta clase es el promedio móvil doble.",
        },
        {
            "type": "heading",
            "level": 2,
            "text": "2. Tres enfoques, y cómo se evalúan",
        },
        {
            "type": "paragraph",
            "text": "El capítulo (en el Resumen V6 aparece como **Capítulo 4: Métodos de promedios móviles y de suavización**; en los resúmenes de Hanke de 25 y de 7 páginas, como **Capítulo 5** — cambia el numerado según la edición) describe tres enfoques:",
        },
        {
            "type": "list",
            "ordered": True,
            "items": [
                "**Informal / no formal:** modelos simples que suponen que los datos más recientes ofrecen las mejores predicciones del futuro.",
                "**Promedios:** el pronóstico es un promedio de observaciones pasadas.",
                "**Suavización:** promedio de valores pasados con ponderaciones que decrecen en forma exponencial. **Eso es la Clase 6.**",
            ],
        },
        {
            "type": "paragraph",
            "text": "Hanke repite acá la misma **estrategia de evaluación** que ya vimos en la Clase 4:",
        },
        {
            "type": "list",
            "ordered": True,
            "items": [
                "Se elige un método según el análisis y la intuición del pronosticador sobre la naturaleza de los datos.",
                "Se divide el conjunto en una sección de **inicio o ajuste** y una sección de **prueba o pronóstico**.",
                "Se ajusta la técnica con la primera parte.",
                "Se pronostica la segunda, se compara con lo real y se evalúa el **error de pronóstico** ($e_t$).",
                "Se decide: dejar la técnica como está, modificarla, o probar otra y comparar.",
            ],
        },
        {
            "type": "paragraph",
            "text": "No midas el error sobre los mismos datos con los que ajustaste: eso ya quedó en la Clase 4. Acá lo traigo porque el capítulo de promedios **abre** con esos cinco pasos.",
        },
        {
            "type": "heading",
            "level": 2,
            "text": "3. Modelos no formales (informales)",
        },
        {
            "type": "paragraph",
            "text": "Hanke los llama **no formales**; el Resumen V6, **informales**. Sirven cuando hay **muy pocos datos** —el V6 pone el caso de un negocio nuevo— porque muchas técnicas piden series largas. También se usan **como base de comparación** para evaluar métodos más complejos. El V6 lo dice claro: el número y la complejidad de estos modelos están limitados solo por el **ingenio del analista**, pero hay que usarlos con buen juicio.",
        },
        {
            "type": "heading",
            "level": 3,
            "text": "3.1 El más sencillo: «sin cambio»",
        },
        {
            "type": "paragraph",
            "text": "La hipótesis: los períodos recientes son los mejores para predecir el futuro. El modelo más simple es el pronóstico de cada período igual a la observación inmediata anterior. El V6 lo llama pronóstico **«sin cambio»**. Se da el **100% del peso** al valor actual de la serie. $\\hat{Y}_{t+1}$ es el pronóstico hecho en el momento $t$ (origen del pronóstico) para el tiempo $t+1$.",
        },
        {"type": "formula", "tex": r"\hat{Y}_{t+1} = Y_t"},
        {
            "type": "svg",
            "svg": svg_informal(False),
            "caption": "Esquema del informal «sin cambio»: el próximo pronóstico copia el último valor observado. No es una serie del apunte.",
        },
        {
            "type": "paragraph",
            "text": "Como descarta cualquier otra observación, **detecta los cambios muy rápido**. El problema, dice el V6, es que las **fluctuaciones aleatorias** se reproducen con la misma fidelidad que los cambios de fondo.",
        },
        {
            "type": "heading",
            "level": 3,
            "text": "3.2 Si hay tendencia",
        },
        {
            "type": "paragraph",
            "text": "Cuando los valores aumentan con el tiempo, el V6 dice que son de **nivel no estacionario** o que tienen una **tendencia**. Se puede ajustar el informal **sumando la diferencia** entre este período y el anterior (Hanke 25p trae la misma ecuación):",
        },
        {"type": "formula", "tex": r"\hat{Y}_{t+1} = Y_t + (Y_t - Y_{t-1})"},
        {
            "type": "paragraph",
            "text": "En algunos casos, dice el V6, conviene más la **tasa de cambio** que el cambio absoluto:",
        },
        {"type": "formula", "tex": r"\hat{Y}_{t+1} = Y_t \cdot \frac{Y_t}{Y_{t-1}}"},
        {
            "type": "heading",
            "level": 3,
            "text": "3.3 Si hay estacionalidad trimestral",
        },
        {
            "type": "paragraph",
            "text": "Si el patrón estacional es fuerte, el V6 propone, para datos **trimestrales**, copiar el mismo trimestre del año anterior:",
        },
        {"type": "formula", "tex": r"\hat{Y}_{t+1} = Y_{t-3}"},
        {
            "type": "paragraph",
            "text": "Eso quiere decir: el próximo trimestre tendrá el mismo valor que el trimestre correspondiente del año anterior. La debilidad, según el V6, es que **ignora todo lo ocurrido desde el año anterior y también cualquier tendencia**. Una forma de meter esa información reciente:",
        },
        {
            "type": "formula",
            "tex": r"\hat{Y}_{t+1} = Y_{t-3} + \frac{Y_t - Y_{t-4}}{4}",
        },
        {
            "type": "paragraph",
            "text": "El término $Y_{t-3}$ arrastra el patrón estacional; el otro promedia la magnitud del cambio de los cuatro trimestres anteriores y estima la tendencia. (En el V6 también aparece escrito como el promedio de las cuatro diferencias $(Y_t-Y_{t-1})+…+(Y_{t-3}-Y_{t-4})$, que es lo mismo que $(Y_t-Y_{t-4})/4$.)",
        },
        {
            "type": "heading",
            "level": 2,
            "text": "4. Métodos basados en promedios",
        },
        {
            "type": "paragraph",
            "text": "Estas técnicas usan alguna forma de **promedio ponderado** de observaciones pasadas para suavizar las fluctuaciones de corto plazo. La suposición (Hanke / V6): esas fluctuaciones son apartamientos aleatorios de una estructura (una «curva atenuada», en el 25p). Una vez identificada, se la proyecta hacia el futuro.",
        },
        {
            "type": "heading",
            "level": 3,
            "text": "4.1 Promedio simple",
        },
        {
            "type": "paragraph",
            "text": "Se usa la **media de todos los valores pertinentes** (Hanke 25p y 7p) como pronóstico del período siguiente. En la práctica, se toma una parte de los datos como **inicialización**, se la promedia, y ese promedio pronostica el período que sigue. El Resumen V6 lo escribe así ($n$ es la cantidad de observaciones de esa parte de inicialización; el índice superior de la suma aparece como $t$):",
        },
        {"type": "formula", "tex": r"\hat{Y}_{t+1} = \frac{1}{n}\sum_{i=1}^{t} Y_i"},
        {
            "type": "paragraph",
            "text": "Cuando entra una observación nueva, no hace falta guardar toda la historia: alcanza el último pronóstico y el último dato. El V6 da esta forma de actualización:",
        },
        {
            "type": "formula",
            "tex": r"\hat{Y}_{t+2} = \frac{t \hat{Y}_{t+1} + Y_{t+1}}{t+1}",
        },
        {
            "type": "paragraph",
            "text": "**Cuándo usarlo.** Hanke 25p y 7p: cuando los datos son **estacionarios** (sin tendencia, estacionalidad u otros patrones). El V6 lo dice en otros términos: cuando los factores que producen la serie **se estabilizaron** y el ambiente **permanece sin cambios**.",
        },
        {
            "type": "heading",
            "level": 3,
            "text": "4.2 Promedio móvil, $MA(k)$",
        },
        {
            "type": "paragraph",
            "text": "El promedio simple usa **todos** los datos. Si el analista está más interesado en las observaciones recientes, se fija un número constante de puntos y se calcula la media solo con los **más recientes**. Cuando entra un dato nuevo, se suma ese valor y se **elimina el más antiguo**. El tamaño de la ventana no cambia con el tiempo.",
        },
        {
            "type": "paragraph",
            "text": "El V6 llama $k$ al número de términos (un promedio móvil de orden $k$, $MA(k)$). El resumen de Hanke de 25 páginas usa $n$ para lo mismo. Acá dejo la $k$ del V6:",
        },
        {
            "type": "formula",
            "tex": r"\hat{Y}_{t+1} = \frac{Y_t + Y_{t-1} + \ldots + Y_{t-k+1}}{k}",
        },
        {
            "type": "svg",
            "svg": svg_window(False),
            "caption": "Esquema de la ventana del promedio móvil: entra el dato nuevo, sale el más viejo. No es una serie del apunte.",
        },
        {
            "type": "paragraph",
            "text": "En un promedio móvil (el de Hanke / V6, no el ponderado de Chase) se asignan **pesos iguales** a cada observación de la ventana. El porcentaje de respuesta a los cambios del patrón depende de $k$.",
        },
        {
            "type": "list",
            "ordered": False,
            "items": [
                "**$k$ chico:** más peso en los períodos recientes. Conveniente cuando hay **cambios repentinos** de nivel: el pronóstico alcanza más rápido el nivel real.",
                "**$k$ grande:** más suavizado, menos atención a las fluctuaciones. Conveniente cuando hay **fluctuaciones amplias** (Hanke 25p) o **amplias y poco frecuentes** (V6).",
            ],
        },
        {
            "type": "svg",
            "svg": svg_k(False),
            "caption": "Esquema (no es una serie del apunte): ante un salto de nivel, un $k$ chico sigue el cambio más de cerca; un $k$ grande suaviza más y se atrasa. La misma idea aparece en Chase (Resumen V6) al comparar promedios de 3 y de 9 semanas.",
        },
        {
            "type": "paragraph",
            "text": "**Límite importante (Hanke / V6):** el promedio móvil **no maneja muy bien la tendencia ni la estacionalidad**, aunque lo hace **mejor que el promedio simple**. Sigue siendo, en el árbol, un método de serie **estacionaria**.",
        },
        {
            "type": "heading",
            "level": 3,
            "text": "4.3 Promedio móvil doble",
        },
        {
            "type": "paragraph",
            "text": "Para series con **tendencia lineal**, Hanke y el V6 proponen el promedio móvil doble: se calcula un conjunto de promedios móviles y después un **segundo conjunto** como promedio móvil del primero. (En la tabla de la Clase 3.a aparece también como *promedio móvil lineal*.)",
        },
        {
            "type": "paragraph",
            "text": "Primero, el promedio móvil de orden $k$ (el V6 lo llama $M_t$; coincide con $\\hat{Y}_{t+1}$ de ese primer promedio):",
        },
        {
            "type": "formula",
            "tex": r"M_t = \hat{Y}_{t+1} = \frac{Y_t + Y_{t-1} + \ldots + Y_{t-k+1}}{k}",
        },
        {"type": "paragraph", "text": "Después, el segundo promedio móvil:"},
        {
            "type": "formula",
            "tex": r"M'_t = \frac{M_t + M_{t-1} + \ldots + M_{t-k+1}}{k}",
        },
        {
            "type": "paragraph",
            "text": "Se arma un pronóstico sumando al promedio simple la diferencia entre el simple y el segundo. Eso define el **nivel** $a_t$. El V6 agrega un factor de ajuste $b_t$, «similar a la medida de cambio a lo largo de la serie»:",
        },
        {"type": "formula", "tex": r"a_t = 2M_t - M'_t"},
        {"type": "formula", "tex": r"b_t = \frac{2}{k-1}(M_t - M'_t)"},
        {
            "type": "paragraph",
            "text": "El pronóstico a $p$ períodos hacia adelante:",
        },
        {"type": "formula", "tex": r"\hat{Y}_{t+p} = a_t + b_t p"},
        {
            "type": "svg",
            "svg": svg_doble(False),
            "caption": "Circuito del promedio móvil doble, con las fórmulas de $a_t$ y $b_t$ del Resumen V6 / Hanke 25p. En el 25p el orden se llama $n$ en vez de $k$.",
        },
        {
            "type": "paragraph",
            "text": "En los resúmenes de Hanke y en el V6 **no hay una tabla numérica resuelta** de móvil doble. No invento una serie para rellenar ese hueco. Las fórmulas y el orden de los pasos están completos; el número se practica con un ejercicio cuando haya datos en el material.",
        },
        {
            "type": "heading",
            "level": 3,
            "text": "4.4 Promedio móvil ponderado (Chase, Resumen V6)",
        },
        {
            "type": "callout",
            "kind": "aviso",
            "text": "**Esta sección no está desarrollada en el capítulo de Hanke** de los resúmenes 25p / 7p / V6 (ahí el promedio móvil lleva pesos **iguales**). Sí está en el mismo Resumen V6, más adelante, en el capítulo de pronósticos de Chase (págs. 222–224 del resumen; ilustración y fórmulas 15.1 / 15.2, estas últimas no se pudieron leer porque son imagen). Chase es bibliografía oficial de la materia. Lo marco así porque en los finales aparece seguido el promedio móvil **ponderado**.",
        },
        {
            "type": "paragraph",
            "text": "Chase: el promedio móvil simple da **igual importancia** a cada dato de la ventana; el **ponderado** permite asignar otra importancia a cada elemento, **siempre que la suma de las ponderaciones sea igual a uno**. Las ponderaciones pueden estar en cualquier orden e incluso algunos períodos pueden tener peso cero; la regla que no se negocia es que sumen 1.",
        },
        {
            "type": "paragraph",
            "text": "**Elección de pesos (Chase):** la experiencia y las pruebas. Por regla general, el pasado más reciente es el indicador más importante y debería tener mayor ponderación. Si los datos son estacionales, los pesos se acomodan a esa estación (el ejemplo del V6: trajes de baño en julio del año anterior vs. diciembre, en el hemisferio norte).",
        },
        {
            "type": "ejemplo",
            "title": "Ejemplo de Chase (Resumen V6, págs. 223–224)",
            "blocks": [
                {
                    "type": "paragraph",
                    "text": "Una tienda departamental encuentra que, en un período de cuatro meses, el mejor pronóstico sale de usar **40%** de las ventas del mes más reciente, **30%** de hace dos meses, **20%** de hace tres y **10%** de hace cuatro. Las ventas reales fueron:",
                },
                {
                    "type": "table",
                    "headers": ["Mes 1", "Mes 2", "Mes 3", "Mes 4", "Mes 5"],
                    "rows": [
                        ["100", "90", "105", "95", "?"],
                    ],
                },
                {
                    "type": "paragraph",
                    "text": "El pronóstico para el mes 5, aplicando esos porcentajes a las ventas (el cálculo es imagen en el PDF; acá está hecha la cuenta con los números que sí están en el texto):",
                },
                {
                    "type": "formula",
                    "tex": r"0{,}40\cdot 95 + 0{,}30\cdot 105 + 0{,}20\cdot 90 + 0{,}10\cdot 100 = 97{,}5",
                },
                {
                    "type": "paragraph",
                    "text": "El V6 sigue: supongamos que las ventas del mes 5 resultaron ser **110**. Entonces el pronóstico para el mes 6 (misma cuenta, con los cuatro meses más recientes):",
                },
                {
                    "type": "formula",
                    "tex": r"0{,}40\cdot 110 + 0{,}30\cdot 95 + 0{,}20\cdot 105 + 0{,}10\cdot 90 = 102{,}5",
                },
                {
                    "type": "svg",
                    "svg": svg_weights(False),
                    "caption": "Pesos de Chase para el ejemplo: 10%, 20%, 30% y 40% (el más reciente).",
                },
                {
                    "type": "svg",
                    "svg": svg_chase(False),
                    "caption": "Serie del ejemplo de Chase y el pronóstico 97,5 para el mes 5. Datos del Resumen V6.",
                },
            ],
        },
        {
            "type": "heading",
            "level": 2,
            "text": "5. Cómo elegir, en una frase",
        },
        {
            "type": "table",
            "headers": ["Método", "Idea", "Cuándo, según el material"],
            "rows": [
                [
                    "Informal «sin cambio»",
                    r"$\hat{Y}_{t+1}=Y_t$",
                    "Pocos datos; detecta cambios rápido, pero copia el ruido. Base de comparación.",
                ],
                [
                    "Informal con tendencia",
                    "Se suma (o se aplica) el último cambio",
                    "Nivel no estacionario / tendencia. El V6 también da la versión por tasa y la estacional trimestral.",
                ],
                [
                    "Promedio simple",
                    "Media de toda la inicialización",
                    "Serie estacionaria, ambiente estable.",
                ],
                [
                    "Promedio móvil $MA(k)$",
                    "Media de los últimos $k$, pesos iguales",
                    "Estacionaria; mejor que el simple si hay algo de patrón, pero no resuelve bien tendencia ni estacionalidad. $k$ chico si el nivel cambia de golpe; $k$ grande si las fluctuaciones son amplias.",
                ],
                [
                    "Promedio móvil doble",
                    r"$a_t$, $b_t$ y $\hat{Y}_{t+p}=a_t+b_t p$",
                    "Tendencia lineal.",
                ],
                [
                    "Promedio móvil ponderado (Chase)",
                    "Pesos que suman 1",
                    "Misma familia que el móvil, con más peso (en general) en lo reciente o en la estación que corresponda.",
                ],
            ],
        },
        {
            "type": "heading",
            "level": 2,
            "text": "6. Lo que no entra en esta clase",
        },
        {
            "type": "paragraph",
            "text": "Inmediatamente después del móvil doble, Hanke y el V6 entran en **suavización exponencial simple**, elección de $\\alpha$ y sistemas de control del error (el V6 habla de señal de control; la **señal de rastreo** ya la viste en la Clase 4). Eso se arma en la **Clase 6**. No adelanto fórmulas de $\\alpha$ acá.",
        },
        {
            "type": "heading",
            "level": 2,
            "text": "7. Mini-resumen para tu doc",
        },
        {
            "type": "callout",
            "kind": "examen",
            "text": "**Clase 5.** Informales (Hanke: no formales): el más simple es Ŷₜ₊₁ = Yₜ («sin cambio», 100% al actual). Si hay tendencia, se suma la última diferencia o se aplica la tasa; si es trimestral estacional, Ŷₜ₊₁ = Yₜ₋₃, y se le puede sumar (Yₜ − Yₜ₋₄)/4. Promedio simple: media de toda la inicialización, solo si la serie es estacionaria. Promedio móvil MA(k): media de los últimos k, pesos iguales; k chico reacciona, k grande suaviza; no resuelve bien tendencia ni estacionalidad. Móvil doble: M, M′, aₜ = 2M − M′, bₜ = [2/(k−1)](M − M′), Ŷₜ₊ₚ = aₜ + bₜ p, para tendencia lineal. Promedio ponderado (Chase): pesos que suman 1. Evaluar siempre sobre una parte de prueba, no sobre la de ajuste.",
        },
        {
            "type": "ejercicio",
            "title": "8. EJERCICIO — Clase 5 (de un final, SG!EVA)",
            "estado": "parcial",
            "blocks": [
                {
                    "type": "paragraph",
                    "text": "Enunciado tal cual figura en `SG!EVA.txt` (compilado de evaluaciones hasta 2006, ítem 2; también en EFR como ítem 3, con una variante en 3.3). **Demanda mensual en toneladas** de un fabricante de alimentos para perros:",
                },
                {
                    "type": "table",
                    "headers": ["Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago"],
                    "rows": [
                        ["620", "840", "770", "250", "1000", "870", "?"],
                    ],
                },
                {
                    "type": "paragraph",
                    "text": "**2.1** ¿Cuál hubiera sido el resultado para **mayo** y **junio** si se utilizaba un promedio móvil ponderado **fp (1,2,3)** de tres meses? Interpretar y analizar el resultado obtenido.\n\n**2.2** (se resuelve con la Clase 6) Utilizando nivelación exponencial, pronosticar para agosto. Interpretar y analizar el resultado. En esta clase no lo pedimos.",
                },
            ],
            "solucion": [
                {
                    "type": "callout",
                    "kind": "aviso",
                    "text": "**Fuente de esta resolución:** no es una clave oficial de la cátedra. Es la resolución **manuscrita** de SG1.doc, rotulada Final (1), pág. 2 (`texto/ocr/sg1_ppm/p-02.png`). Transcribo el procedimiento y los números que se leen en esa hoja.",
                },
                {
                    "type": "paragraph",
                    "text": "En esa hoja el promedio móvil ponderado se define:",
                },
                {
                    "type": "formula",
                    "tex": r"fp(1,2,3)=\frac{\sum(\text{peso}\cdot\text{demanda})}{\sum\text{peso}}",
                },
                {
                    "type": "paragraph",
                    "text": "Para mayo (usa feb, mar y abr; el peso 1 es el más antiguo y el 3, el más reciente):",
                },
                {
                    "type": "formula",
                    "tex": r"\frac{1\cdot 620 + 2\cdot 840 + 3\cdot 770}{1+2+3}=\frac{4610}{6}=768{,}33",
                },
                {
                    "type": "paragraph",
                    "text": "Para junio (mar, abr y may):",
                },
                {
                    "type": "formula",
                    "tex": r"\frac{1\cdot 840 + 2\cdot 770 + 3\cdot 250}{6}=\frac{3130}{6}=521{,}67",
                },
                {
                    "type": "paragraph",
                    "text": "Interpretación, también de esa hoja (transcripción): el valor pronosticado para mayo con fp es 768,33, con una diferencia de 518,33 respecto del valor original 250. «Esto se debe a que 250 puede ser un valor anómalo; lo mismo para junio.»",
                },
            ],
        },
        {
            "type": "glosario",
            "title": "9. Glosario de símbolos",
            "intro": "Notación de Hanke / V6 para esta clase. Chase usa $A$ para la observación en algunos renglones que no se pudieron leer (son imagen).",
            "entries": [
                {"simbolo": "Yₜ", "nombre": "i griega sub te", "significado": "Observación real en el período t"},
                {"simbolo": "Ŷₜ₊₁", "nombre": "i griega sombrero", "significado": "Pronóstico hecho en t (origen) para el período t+1"},
                {"simbolo": "t", "nombre": "origen del pronóstico", "significado": "El momento en que se calcula Ŷ; el V6 lo llama origen del pronóstico"},
                {"simbolo": "k (V6) / n (Hanke 25p)", "nombre": "orden del promedio", "significado": "Cantidad de términos de la ventana del promedio móvil. En el promedio simple, n es el tamaño de la inicialización"},
                {"simbolo": "MA(k)", "nombre": "promedio móvil de orden k", "significado": "Media de las últimas k observaciones; pesos iguales"},
                {"simbolo": "Mₜ", "nombre": "eme sub te", "significado": "Primer promedio móvil (móvil doble)"},
                {"simbolo": "M′ₜ", "nombre": "eme prima", "significado": "Segundo promedio móvil: media de los M"},
                {"simbolo": "aₜ", "nombre": "a sub te", "significado": "Nivel: aₜ = 2Mₜ − M′ₜ"},
                {"simbolo": "bₜ", "nombre": "be sub te", "significado": "Pendiente: bₜ = [2/(k−1)](Mₜ − M′ₜ)"},
                {"simbolo": "p", "nombre": "pe", "significado": "Períodos hacia adelante en el móvil doble: Ŷₜ₊ₚ = aₜ + bₜ p"},
                {"simbolo": "wᵢ", "nombre": "ponderaciones (Chase)", "significado": "Pesos del promedio móvil ponderado; tienen que sumar 1"},
                {"simbolo": "fp(1,2,3)", "nombre": "factores de ponderación", "significado": "En el final resuelto de SG1, pesos 1, 2 y 3 (el 3 al más reciente), divididos por 6. No aparece definido en Hanke"},
            ],
        },
        {
            "type": "paragraph",
            "text": "**Material asociado:** `ArbolDecisorio_MetodosPronostico.svg` · Resumen Hanke 25p y 7p · Resumen V6 (Cap. 4 y Chase págs. 222–224) · `Formulas SdG` (título del capítulo; las fórmulas son imagen y no se pudieron extraer).\n**No está en el material descargado:** un apunte «Clase 5», las tablas de la ilustración 15.5 de Chase, ni `practica_1.pdf` / `tablas_practica_1.xlsx` que cita el Documento Maestro.",
        },
        {
            "type": "paragraph",
            "text": "**Próxima clase → Clase 6: Suavizado exponencial simple** (elección de α, inicialización). La señal de rastreo ya está en la Clase 4.",
        },
    ]


def historias() -> list:
    return [
        {
            "type": "concepto",
            "k": "El árbol",
            "title": "¿Estacionaria o con tendencia?",
            "text": "Si la serie es estacionaria, en esta clase los candidatos son el promedio simple y el móvil. Si tiene tendencia lineal, el candidato es el móvil doble. Eso ya lo fijó el árbol de la Clase 3.a: no se inventan asignaciones nuevas.",
        },
        {
            "type": "concepto",
            "k": "Tres enfoques",
            "title": "Informal, promedios y suavización.",
            "text": "Hanke abre el capítulo con esos tres. Esta clase cubre los dos primeros. La suavización exponencial es la Clase 6, aunque el Documento Maestro la lista en la misma semana.",
            "ejemplo": "En el plan las llamamos «ingenuos»; Hanke dice no formales, el V6 dice informales.",
        },
        {
            "type": "concepto",
            "k": "Sin cambio",
            "title": "El informal más simple copia el último valor.",
            "text": "Ŷₜ₊₁ = Yₜ. El 100% del peso va al valor actual. Detecta los cambios rápido, pero también copia el ruido. El V6 lo llama pronóstico «sin cambio». Sirve cuando hay pocos datos, y como base para comparar métodos más complejos.",
            "formula": r"\hat{Y}_{t+1} = Y_t",
            "svg": svg_informal(True),
            "chartLabel": "Esquema: el próximo punto copia el último (no es una serie del apunte)",
        },
        {
            "type": "pregunta",
            "k": "A ver…",
            "title": "Si la serie viene subiendo, el informal «sin cambio»…",
            "options": [
                "Suma la última diferencia, o se queda corto si no lo ajustás",
                "Promedia toda la historia y atrapa la tendencia",
                "Usa siempre el mismo trimestre del año anterior",
            ],
            "correct": 0,
            "feedback": "Sin ajuste, Ŷₜ₊₁ = Yₜ no incorpora la tendencia. El V6 / Hanke lo corrigen sumando (Yₜ − Yₜ₋₁), o con la tasa Yₜ/Yₜ₋₁. El trimestral Yₜ₋₃ es otro informal, para estacionalidad.",
        },
        {
            "type": "concepto",
            "k": "Más informales",
            "title": "Tendencia, tasa o estación.",
            "text": "Con tendencia: Ŷₜ₊₁ = Yₜ + (Yₜ − Yₜ₋₁), o Ŷₜ₊₁ = Yₜ · (Yₜ/Yₜ₋₁). Si es trimestral y la estación es fuerte: Ŷₜ₊₁ = Yₜ₋₃, y se le puede sumar (Yₜ − Yₜ₋₄)/4 para estimar la tendencia de esos cuatro trimestres.",
            "formula": r"\hat{Y}_{t+1} = Y_t + (Y_t - Y_{t-1})",
        },
        {
            "type": "concepto",
            "k": "Promedio simple",
            "title": "La media de toda la inicialización.",
            "text": "Se promedian todos los valores pertinentes y esa media es el pronóstico del período que sigue. Hanke: usalo cuando la serie es estacionaria, sin tendencia ni estacionalidad. El V6 agrega una forma de actualizar sin guardar toda la historia.",
            "formula": r"\hat{Y}_{t+1} = \frac{1}{n}\sum_{i=1}^{t} Y_i",
        },
        {
            "type": "concepto",
            "k": "La ventana",
            "title": "El móvil mira solo los últimos k.",
            "text": "Entra el dato nuevo, sale el más viejo. Pesos iguales. k chico reacciona a un cambio de nivel; k grande suaviza más. No maneja muy bien tendencia ni estacionalidad, aunque lo hace mejor que el promedio simple.",
            "formula": r"\hat{Y}_{t+1} = \frac{Y_t + Y_{t-1} + \ldots + Y_{t-k+1}}{k}",
            "svg": svg_window(True),
            "chartLabel": "Ventana MA(3): entra Yₜ, sale Yₜ₋₃ (esquema)",
        },
        {
            "type": "pregunta",
            "k": "A ver…",
            "title": "Si el nivel de la serie cambia de golpe, conviene un k…",
            "options": [
                "Grande: suaviza las fluctuaciones amplias",
                "Chico: pone más peso en lo reciente y alcanza antes el nuevo nivel",
                "Da igual: el móvil no usa k",
            ],
            "correct": 1,
            "feedback": "Hanke y el V6: un número pequeño es deseable cuando hay cambios repentinos, porque carga más la historia reciente. El k grande conviene cuando las fluctuaciones son amplias.",
        },
        {
            "type": "concepto",
            "k": "Móvil doble",
            "title": "Para tendencia lineal: dos promedios, después a y b.",
            "text": "M es el móvil de Y; M′ es el móvil de los M. El nivel aₜ = 2Mₜ − M′ₜ y la pendiente bₜ = [2/(k−1)](Mₜ − M′ₜ). El pronóstico a p períodos es aₜ + bₜ p. En los resúmenes no hay una tabla numérica resuelta.",
            "formula": r"\hat{Y}_{t+p} = a_t + b_t p",
            "svg": svg_doble(True),
            "chartLabel": "Y → M → M′ → a, b → Ŷₜ₊ₚ",
        },
        {
            "type": "concepto",
            "k": "Chase",
            "title": "Ponderado: los pesos suman 1.",
            "text": "Chase, Resumen V6: pesos 40-30-20-10 (el 40% al más reciente) sobre ventas 95, 105, 90 y 100. Ŷ del mes 5 = 97,5. Si ese mes cierra en 110, el del 6 queda 102,5. No está en el capítulo de Hanke.",
            "formula": r"0{,}40\cdot 95 + 0{,}30\cdot 105 + 0{,}20\cdot 90 + 0{,}10\cdot 100 = 97{,}5",
            "svg": svg_chase(True),
            "chartLabel": "Ventas de Chase y Ŷ₅ = 97,5",
        },
        {
            "type": "pregunta",
            "k": "A ver…",
            "title": "En el promedio móvil ponderado de Chase, los pesos…",
            "options": [
                "Tienen que ser todos iguales a 1/k",
                "Pueden ser cualquiera, mientras sumen 1",
                "Tienen que crecer siempre hacia el pasado",
            ],
            "correct": 1,
            "feedback": "Chase: se puede asignar cualquier importancia, incluso en otro orden o con algún peso en cero, pero la suma de las ponderaciones debe ser igual a uno.",
        },
        {
            "type": "concepto",
            "k": "Cómo se evalúa",
            "title": "Ajustá con una parte, medí el error en la otra.",
            "text": "Hanke abre este capítulo con los cinco pasos de la Clase 4: elegir el método según el patrón, partir en inicio y prueba, ajustar, pronosticar la prueba y decidir. El error no se mide sobre los datos con los que ajustaste.",
        },
        {
            "type": "cierre",
            "k": "Para llevar",
            "title": "Llevate esto de la Clase 5.",
            "text": "Informales: Ŷ = Yₜ, o con tendencia, tasa o estación. Promedio simple si es estacionaria. Móvil MA(k): ventana, pesos iguales; k chico reacciona, k grande suaviza. Móvil doble si hay tendencia lineal. Ponderado (Chase): pesos que suman 1. Siguiente: suavizado exponencial simple.",
        },
    ]


def main() -> None:
    data = doc()
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    n_t = len(data["teoria"])
    n_h = len(data["historias"])
    print(f"OK {OUT} teoria={n_t} historias={n_h}")


if __name__ == "__main__":
    main()
