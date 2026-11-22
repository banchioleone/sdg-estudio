#!/usr/bin/env python3
"""Build class JSON from the previous-class markdown + story cards."""
from __future__ import annotations
import json
import shutil
from pathlib import Path
from copy import deepcopy

from mdparse import parse_md, slice_sections

ROOT = Path(__file__).resolve().parents[1] / "content"
SRC = Path("/workspace/sdg/clases_previas/SG")
IMG = ROOT / "u2" / "img"
OUT = ROOT / "u2"

UNIT = {
    "unitId": "u2",
    "unitLabel": "Unidad 2",
    "unitTitle": "Métodos de pronósticos",
}

_c1=json.loads((OUT / "clase01.json").read_text()); C1_STORIES=_c1.get("historias") or _c1.get("cards")


def load(name: str) -> list[dict]:
    return parse_md((SRC / name).read_text(encoding="utf-8"))


def starts(h: str, *prefixes) -> bool:
    h = " ".join((h or "").split())
    return any(h.startswith(p) or p in h for p in prefixes)


def find_heading_index(blocks, pred, start=0):
    for i, b in enumerate(blocks[start:], start):
        if b.get("type") == "heading" and pred(b.get("text") or ""):
            return i
    return -1


def section_range(blocks, pred, stop_pred=None):
    i = find_heading_index(blocks, pred)
    if i < 0:
        return 0, 0
    level = blocks[i].get("level") or 2
    j = i + 1
    while j < len(blocks):
        b = blocks[j]
        if b.get("type") == "heading" and (b.get("level") or 3) <= level:
            if stop_pred is None or stop_pred(b.get("text") or ""):
                break
            if stop_pred is None:
                break
        j += 1
    return i, j


def take_until_h2(blocks, start_pred):
    i, j = section_range(blocks, start_pred)
    return blocks[i:j], i, j


def transform_ejercicio(blocks: list[dict]) -> list[dict]:
    out = []
    i = 0
    while i < len(blocks):
        b = blocks[i]
        t = b.get("text") or ""
        if b.get("type") == "heading" and "EJERCICIO" in t.upper() and "acumulados" not in t.lower():
            level = b.get("level") or 2
            j = i + 1
            while j < len(blocks):
                nb = blocks[j]
                if nb.get("type") == "heading" and (nb.get("level") or 3) <= level:
                    break
                j += 1
            body = blocks[i + 1 : j]
            out.append({
                "type": "ejercicio",
                "title": t,
                "estado": "para resolver",
                "blocks": body,
                "nota": "Para resolver — en el material no figura la resolución. Cuando lo corriamos, la cargamos acá.",
            })
            i = j
            continue
        out.append(b)
        i += 1
    return out


def transform_glosario(blocks: list[dict]) -> list[dict]:
    out = []
    i = 0
    while i < len(blocks):
        b = blocks[i]
        t = b.get("text") or ""
        if b.get("type") == "heading" and "Glosario" in t:
            level = b.get("level") or 2
            j = i + 1
            while j < len(blocks):
                nb = blocks[j]
                if nb.get("type") == "heading" and (nb.get("level") or 3) <= level:
                    break
                j += 1
            chunk = blocks[i + 1 : j]
            intro_parts = []
            entries = []
            rest = []
            for c in chunk:
                if c.get("type") == "table" and not entries:
                    headers = c.get("headers") or []
                    for row in c.get("rows") or []:
                        # pad
                        row = list(row) + [""] * 3
                        entries.append({
                            "simbolo": row[0],
                            "nombre": row[1],
                            "significado": row[2] if len(row) > 2 else "",
                        })
                elif c.get("type") in ("paragraph", "callout") and not entries:
                    intro_parts.append(c.get("text") or "")
                else:
                    rest.append(c)
            out.append({
                "type": "glosario",
                "title": t,
                "intro": "\n\n".join(intro_parts),
                "entries": entries,
            })
            out.extend(rest)
            i = j
            continue
        out.append(b)
        i += 1
    return out


def wrap_ejemplos(blocks: list[dict]) -> list[dict]:
    out = []
    i = 0
    while i < len(blocks):
        b = blocks[i]
        t = b.get("text") or ""
        if b.get("type") == "heading" and t.lower().startswith("ejemplo"):
            level = b.get("level") or 3
            j = i + 1
            while j < len(blocks):
                nb = blocks[j]
                if nb.get("type") == "heading" and (nb.get("level") or 3) <= level:
                    break
                j += 1
            out.append({"type": "ejemplo", "title": t, "blocks": blocks[i + 1 : j]})
            i = j
            continue
        out.append(b)
        i += 1
    return out


def drop_title_h1(blocks: list[dict]) -> tuple[str, list[dict]]:
    title = ""
    out = []
    for i, b in enumerate(blocks):
        if b.get("type") == "heading" and b.get("level") == 1 and not title:
            title = b.get("text") or ""
            continue
        out.append(b)
    return title, out


def first_callout(blocks):
    for b in blocks:
        if b.get("type") == "callout":
            return b.get("text") or ""
    return ""


def insert_after_first_callout(blocks, new_blocks):
    """Prefer after the first formula so the page opens with theory + fórmula and the lámina follows."""
    out = []
    done = False
    for b in blocks:
        out.append(b)
        if not done and b.get("type") == "formula":
            out.extend(new_blocks)
            done = True
    if done:
        return out
    out = []
    for b in blocks:
        out.append(b)
        if not done and b.get("type") == "callout":
            out.extend(new_blocks)
            done = True
    if not done:
        return new_blocks + out
    return out


def tidy(blocks):
    blocks = transform_glosario(blocks)
    blocks = transform_ejercicio(blocks)
    blocks = wrap_ejemplos(blocks)
    return blocks


def strip_md_stars(s: str) -> str:
    return s.replace("**", "")


# ---------- historias helpers ----------
def concepto(k, title, text, **kw):
    d = {"type": "concepto", "k": k, "title": title, "text": text}
    d.update(kw)
    return d


def pregunta(title, options, correct, feedback, k="A ver…"):
    return {"type": "pregunta", "k": k, "title": title, "options": options, "correct": correct, "feedback": feedback}


def cierre(title, text):
    return {"type": "cierre", "title": title, "text": text}


# ---- C1.b stories ----
H_C1B = [
    concepto("La idea", "Una tabla, para todas las campanas.",
             "Z convierte cualquier campana en una sola. El método es siempre el mismo: calcular Z, dibujar y pintar el área, buscar en la tabla y armar la respuesta con ±0,5."),
    concepto("Paso cero", "Primero, identificá tu tabla.",
             "Buscá Z = 1,00. Si dice 0,3413, es tabla «centro→Z» (máximo 0,5): la usual en UTN y la de este apunte. Si dice 0,8413, es acumulada (ya incluye el 0,5 izquierdo).",
             ejemplo="Anotalo arriba de la tabla. Es EL error clásico de examen."),
    pregunta("Si para Z = 1,00 la tabla da 0,3413, ¿qué tabla tenés?",
             ["Acumulada, desde −∞ hasta Z", "Centro→Z, el área entre el medio y tu Z", "Una tabla t de Student"],
             1, "0,3413 es el área entre el centro y Z = 1. Es la tabla centro→Z, la usual en UTN. La acumulada, para el mismo Z, daría 0,8413."),
    concepto("El método", "Siempre los mismos 4 pasos.",
             "① Z = (X − μ) / σ. ② Dibujá la campana y pintá el área que pide la pregunta. ③ Buscá en la tabla el área de tu Z. ④ Armá la respuesta sumando o restando 0,5 (cada mitad vale 0,5).",
             ejemplo="Cómo se busca: fila = Z hasta el primer decimal; columna = segundo decimal. Z = 1,64 → fila 1,6, columna 0,04 → 0,4495."),
    concepto("Caso 1", "«Menos que» un X mayor al promedio.",
             "Ejemplo base: μ = 500, σ = 80. P(X < 620): Z = (620−500)/80 = +1,5. Pinto todo lo izquierdo de 620.",
             ejemplo="Tabla(1,50) = 0,4332 → P = 0,5 + 0,4332 = 0,9332 → 93,3%. Chequeo: 620 está sobre μ ⇒ debe dar > 50%."),
    concepto("Caso 2", "«Más que» es el complemento.",
             "P(X > 620) usa el mismo Z = +1,5. Pinto la colita derecha: 0,5 − 0,4332 = 0,0668 → 6,7%.",
             ejemplo="Chequeo: 93,3% + 6,7% = 100%."),
    pregunta("Si P(X < 620) = 93,3%, ¿cuánto vale P(X > 620)?",
             ["También 93,3%", "6,7%, porque son complementarias", "50%, porque es la mitad derecha"],
             1, "«Más que» y «menos que» del mismo X suman 100%. 100 − 93,3 = 6,7%."),
    concepto("Caso 3", "Z negativo: usá la simetría.",
             "P(X < 420): Z = (420−500)/80 = −1,0. La tabla no tiene negativos: buscá Z = +1,00 → 0,3413. Pinto la colita izquierda: 0,5 − 0,3413 = 0,1587 → 15,9%.",
             ejemplo="Chequeo: 420 está bajo μ ⇒ debe dar < 50%."),
    concepto("Caso 4", "Entre dos valores: sumo o resto.",
             "P(420 < X < 620): piezas 0,3413 (izq.) y 0,4332 (der.), en lados opuestos del centro → se SUMAN: 77,5%. Si ambos quedan del mismo lado, se RESTAN.",
             ejemplo="Regla: distinto lado de μ → sumo · mismo lado → resto. El dibujo evita confundirse."),
    concepto("Caso 5 ★", "El inverso: el del stock de seguridad.",
             "Tengo la probabilidad y busco el X. Cubrir la demanda el 95% de las veces: área 0,5 + 0,45. Tabla al revés: Z ≈ 1,64. X = μ + Z·σ = 500 + 1,64×80 = 631.",
             ejemplo="Z famosos: 90% → 1,28 · 95% → 1,64 · 97,5% → 1,96 · 99% → 2,33."),
    pregunta("Para cubrir la demanda el 95% de las veces, el Z que se usa es…",
             ["1,28", "1,64", "1,96"],
             1, "Se busca el área 0,45 en la tabla centro→Z: 0,4495 → Z = 1,64. Es el número estrella del stock de seguridad. 1,96 es el 97,5% (o el 95% a dos colas)."),
    concepto("Pocos datos", "Con n chico, entra t de Student.",
             "La t es más baja en el centro y con colas más gordas: para la misma confianza exige un multiplicador mayor que Z. Se lee con dos entradas: confianza + grados de libertad (n−1).",
             ejemplo="n < 30 y desvío estimado de la muestra → t. n ≥ 30 o σ conocido → Z. En regresión, siempre t (con n−2 gl). Con n = 5, gl = 4, t al 95% = 2,776 (contra Z = 1,96)."),
    concepto("Chequeos", "Si no cierra, revisá el dibujo.",
             "X sobre el promedio ⇒ P(«menos que X») > 50%. Un área jamás es negativa ni mayor que 1. «Más que» y «menos que» del mismo X suman 100%.",
             ejemplo="Si el resultado viola algo de esto: revisá el DIBUJO, no la tabla."),
    cierre("Llevate esto de la Clase 1.b.",
           "Paso cero: identificá la tabla (0,3413 = centro→Z). Método: Z → dibujo → tabla → armar con ±0,5. Cinco casos: menos-que, más-que, Z negativo, entre-dos, inverso. Z famosos: 1,28 / 1,64 / 1,96 / 2,33. t: colas gordas, dos entradas, converge a Z cerca de n = 30."),
]

H_C2 = [
    concepto("La idea", "Ahora miramos dos variables juntas.",
             "Hasta ahora mirábamos una variable (ventas y su dispersión). La correlación mide si dos variables se mueven juntas. Si encontrás una que acompaña a tus ventas, entendés por qué varían y podés pronosticarlas. Es la antesala de la regresión."),
    concepto("La pregunta útil", "¿De qué dependen mis ventas?",
             "No alcanza con «¿cuánto vendo en promedio?». Si dos variables se mueven juntas, entendés el fenómeno y, si conocés una (la publicidad del mes que viene), estimás la otra."),
    concepto("Paso uno", "Siempre se grafica primero.",
             "Cada punto es un par: X en el horizontal, Y en el vertical. X es la independiente (la que explica, la que conocés primero). Y es la dependiente (la que querés explicar o predecir).",
             ejemplo="Para estimar ventas a partir de publicidad: publicidad = X, ventas = Y. Con 5 meses (10→120, 15→135, 8→105, 18→140, 6→100) se ve que suben juntos. Eso ya es información, antes de cualquier fórmula."),
    pregunta("Si querés estimar ventas a partir de la publicidad, ¿cuál es X?",
             ["Las ventas, porque es lo que más te importa", "La publicidad: es la independiente, la que conocés primero", "Da igual: r no distingue X de Y"],
             1, "X es la independiente, la causa candidata, la que conocés primero. Y es la que querés explicar o predecir. Publicidad = X, ventas = Y."),
    concepto("Seis patrones", "Hanke, capítulo 2.",
             "Lineal positiva o negativa, perfecta o imperfecta; curva; o sin relación. En la práctica, el caso realista es la nube alargada (imperfecta).",
             ejemplo="Qué buscar, en este orden: ¿lineal o curva? Si es lineal, ¿positiva o negativa? ¿Cuán apretados están los puntos?"),
    concepto("El coeficiente r", "Mide la relación LINEAL.",
             "Se arma una tabla con X, Y, XY, X², Y², se suma cada columna y se reemplaza en la fórmula. r siempre está entre −1 y +1. El signo es la dirección; el valor absoluto, la fuerza.",
             formula="r = \\frac{n\\sum XY - \\sum X \\sum Y}{\\sqrt{\\left[n\\sum X^2 - (\\sum X)^2\\right]\\cdot\\left[n\\sum Y^2 - (\\sum Y)^2\\right]}}",
             ejemplo="Si te da 1,3 o −2, hay error de cálculo."),
    concepto("Paso a paso", "Publicidad y ventas: r ≈ 0,98.",
             "n = 5, ΣX = 57, ΣY = 600, ΣXY = 7.185, ΣX² = 749, ΣY² = 73.250. Numerador 1.725, denominador ≈ 1.760,7.",
             ejemplo="r ≈ 0,98: correlación positiva muy fuerte. Se mueven casi en línea recta. Un modelo de regresión sobre estos datos va a ajustar muy bien."),
    pregunta("Un r = 0,98 entre publicidad y ventas significa…",
             ["Que la publicidad causa el 98% de las ventas", "Correlación positiva muy fuerte: se mueven casi en línea recta", "Que no hay relación, porque r tiene que ser entero"],
             1, "r = 0,98 es positiva y muy fuerte (cerca de +1). No autoriza a hablar de causa: r mide asociación, no causalidad."),
    concepto("Advertencia 1", "Correlación no implica causalidad.",
             "Que dos cosas se muevan juntas no significa que una cause la otra. Puede haber una tercera variable moviendo a ambas, o pura coincidencia (correlaciones espurias).",
             ejemplo="Ejemplo clásico del apunte: la venta de helados y los ahogamientos suben juntos; no es que el helado ahogue, es el calor que causa ambos. Quien decide si hay causalidad es el criterio del analista sobre el negocio, no la fórmula."),
    concepto("Advertencia 2", "Un r bajo no es «sin relación».",
             "r mide solo relación lineal. Una relación en forma de U perfecta puede dar r ≈ 0 y ser, igual, una relación fortísima.",
             ejemplo="Por eso: primero se grafica, después se calcula. Si te guiás solo por el número, te perdés las curvas. Es exactamente por lo que la cátedra insiste con el análisis de gráficos."),
    pregunta("Si el gráfico muestra una U clara pero r ≈ 0, ¿qué pasa?",
             ["No hay ninguna relación entre las variables", "Hay error de cálculo: r no puede dar 0", "Hay relación, pero no es lineal: r no la captura"],
             2, "r solo mide relación lineal. Una curva puede dar r ≈ 0 y ser una relación fortísima. Por eso se grafica primero."),
    concepto("El puente", "r² es el porcentaje que explica el modelo.",
             "r te dice si hay relación lineal y cuán fuerte. La regresión te da la ecuación para pronosticar. R² = r² es el % de la variación de Y que explica el modelo.",
             ejemplo="En el ejemplo, r = 0,98 → R² = 0,96 → «la publicidad explica el 96% de la variación de las ventas». Esa frase es el tipo de interpretación que puntúa la cátedra."),
    cierre("Llevate esto de la Clase 2.",
           "Siempre graficar primero (X independiente, Y dependiente) e identificar el patrón. r ∈ [−1, +1]: signo = dirección, valor absoluto = fuerza. Dos advertencias: correlación ≠ causalidad, y r bajo solo descarta relación lineal. r² = % de variación explicada; enlaza con la regresión."),
]

H_C3A = [
    concepto("La idea", "Mirar el gráfico es elegir el método.",
             "Toda serie de ventas es la superposición de cuatro componentes: tendencia, ciclo, estacionalidad e irregularidad. Aprender a mirar un gráfico y decir qué componentes tiene es lo que permite elegir y justificar el método de pronóstico: exactamente lo que evalúa la cátedra."),
    concepto("Dos tipos de datos", "En una serie, el orden ES la información.",
             "Corte transversal: datos en un solo momento (el sueldo de 50 empleados hoy); el orden no importa. Serie de tiempo: secuencia ordenada (ventas de ene, feb, mar…). Mezclar los períodos destruye la información.",
             ejemplo="Notación: Yₜ = valor en el período t · Yₜ₋₁ = el anterior · Ŷₜ = pronóstico para ese período. Si descubro el patrón del pasado, puedo proyectarlo al futuro."),
    concepto("Cuatro componentes", "T, C, S e I, como instrumentos de una canción.",
             "Tendencia: largo plazo (crecía de 100 a 300 en cinco años). Ciclo: ondas de varios años, sin período fijo (el más difícil de modelar). Estacionalidad: patrón que se repite cada año, período fijo y conocido (L = 4 trimestral, 12 mensual, 7 diario). Irregularidad: el ruido impredecible.",
             ejemplo="Helados en verano, pico en diciembre: estacionalidad. Recesión de varios años: ciclo."),
    pregunta("¿Qué diferencia a la estacionalidad del ciclo?",
             ["El ciclo se repite todos los años en la misma fecha", "La estacionalidad tiene período fijo y se puede marcar en el calendario; el ciclo no", "No hay diferencia: son dos nombres del mismo componente"],
             1, "Regla del apunte: si podés poner en el calendario cuándo va a pasar → estacionalidad. Si depende de la economía y nadie sabe cuándo → ciclo."),
    concepto("La confusión clásica", "Si va en el calendario, es estacionalidad.",
             "Estacionalidad: duración fija, dentro del año, predecible, clima o calendario. Ciclo: duración variable, varios años, difícil de anticipar, economía o mercado."),
    concepto("Cómo se combinan", "Aditivo o multiplicativo.",
             "Aditivo: Y = T + C + S + I. La estacionalidad es una cantidad fija («en diciembre vendo 200 más»). En el gráfico, ondas de amplitud constante. Multiplicativo: Y = T × C × S × I. La estacionalidad es un porcentaje («un 40% más»). Las ondas se agrandan con la tendencia.",
             formula="Y = T \\times C \\times S \\times I",
             ejemplo="En la práctica industrial el multiplicativo es el más común, y es el que menciona el programa de la cátedra («modelos de descomposición multiplicativo»)."),
    pregunta("Si en el gráfico las ondas se agrandan a medida que crece la serie, el modelo es…",
             ["Aditivo: la estacionalidad es una cantidad fija de unidades", "Multiplicativo: la estacionalidad es un porcentaje", "Solo irregularidad, no hay estacionalidad"],
             1, "Ondas que se agrandan con el nivel (embudo abierto) → multiplicativo. Si mantienen el mismo tamaño → aditivo."),
    concepto("Estacionaria", "La primera pregunta del árbol.",
             "Una serie es estacionaria cuando su valor promedio no cambia a través del tiempo. Fluctúa, pero alrededor de un nivel constante. «¿Es estacionaria?» es la primera bifurcación del árbol de decisión.",
             ejemplo="Si no lo es, se puede diferenciar: trabajar con Yₜ − Yₜ₋₁. Si una serie crece de a 10 por mes, sus diferencias son todas 10: queda plana, estacionaria."),
    concepto("El árbol ★", "Esta tabla justifica la metodología.",
             "Estacionaria → promedio simple, móvil, suavizado exponencial simple, Box-Jenkins. Tendencia → móvil doble, Brown, Holt, regresión. Estacionalidad → Winter, descomposición, regresión múltiple de series, Census II. Ciclo → descomposición, indicadores, econométricos.",
             ejemplo="Este cuadro es la respuesta a «justifique la metodología aplicada» del examen."),
    concepto("Ejemplo", "Aires acondicionados, ventas trimestrales.",
             "Cada año vende más: tendencia. Cada verano se dispara y cada invierno se hunde: estacionalidad, L = 4. En 2020 cayó por la recesión: ciclo. Un pedido raro de un hotel: irregularidad. Los picos de verano cada vez más grandes: multiplicativo. No es estacionaria.",
             ejemplo="¿Qué método? Winter o descomposición, porque tiene tendencia Y estacionalidad."),
    pregunta("Ventas trimestrales de aires: tendencia + estacionalidad, no estacionaria. ¿Qué familia usarías?",
             ["Promedio móvil o suavizado exponencial simple", "Winter o descomposición", "Solo un promedio simple, porque es más estable"],
             1, "El árbol: si tiene tendencia y estacionalidad, corresponden Winter o descomposición. El suavizado simple es para series estacionarias."),
    cierre("Llevate esto de la Clase 3.a.",
           "Serie de tiempo = secuencia ordenada (Yₜ); el orden es información. Cuatro componentes: T + C + S + I. Ciclo vs. estacionalidad: si va en el calendario, es estacionalidad. Aditivo (ondas parejas) o multiplicativo (ondas crecientes). «¿Es estacionaria?» abre el árbol de métodos."),
]

H_C3B = [
    concepto("La idea", "El mismo diagnóstico, con números.",
             "En la 3.a diagnosticabas la serie a ojo. La autocorrelación es esa misma lectura, pero objetiva: evidencia de qué patrón tiene la serie y, por lo tanto, de qué método corresponde."),
    concepto("El giro", "La serie, correlacionada consigo misma.",
             "En la Clase 2 correlacionabas dos variables distintas. Acá se correlaciona la serie con su propio pasado, corrida k períodos. Ese corrimiento es el desfasamiento o lag (k).",
             ejemplo="r₁ compara cada mes con el anterior. r₄, en datos trimestrales, cada trimestre con el mismo del año pasado. r₁₂, en mensuales, cada mes con el mismo mes del año anterior."),
    concepto("La fórmula", "rₖ mide la «memoria» de la serie.",
             "El numerador suma, para cada par separado por k períodos, el producto de sus desvíos contra la media. El denominador normaliza entre −1 y +1.",
             formula="r_k = \\frac{\\sum_{t=k+1}^{n}(Y_t - \\bar{Y})(Y_{t-k} - \\bar{Y})}{\\sum_{t=1}^{n}(Y_t - \\bar{Y})^2}",
             ejemplo="Un rₖ alto significa que saber el valor de hace k períodos te dice mucho sobre el de hoy. Hay memoria en la serie."),
    pregunta("En una serie mensual, un pico en r₁₂ te está diciendo…",
             ["Que hay tendencia, porque 12 es un número grande", "Estacionalidad anual: cada mes se parece al mismo mes del año anterior", "Que la serie es aleatoria"],
             1, "El lag donde salta el pico te dice la longitud estacional. Datos mensuales con pico en r₁₂ → estacionalidad anual. En trimestrales, el pico típico es r₄."),
    concepto("El correlograma", "Cada patrón deja una huella dactilar.",
             "Se calculan muchos rₖ (r₁, r₂, … hasta r₁₂ o más) y se grafican como barras: eje horizontal = lag, eje vertical = valor. Eso es el correlograma (FAC/ACF). Un rₖ suelto sirve poco."),
    concepto("Huella 1 y 2", "Aleatoria o con tendencia.",
             "Aleatoria (estacionaria pura): todas las barras cerca de cero. Métodos: promedio móvil, suavizado exponencial simple. Tendencia: primeras barras grandes y positivas que caen gradualmente. La serie NO es estacionaria. Métodos: Holt, Brown, regresión — o diferenciar."),
    concepto("Huella 3 y 4", "Estacionalidad, sola o combinada.",
             "Estacionalidad: pico aislado en el lag del ciclo (r₄ trimestral, r₁₂ mensual), a veces repetido en r₈, r₂₄. Métodos: Winter, descomposición. Combinación (lo más frecuente): decaen lento (tendencia) y además hay picos cada L lags.",
             ejemplo="El criterio más útil: el lag del pico te dice la longitud estacional."),
    pregunta("Barras altas al principio que caen de a poco, y un pico que se destaca en r₁₂. ¿Qué hay?",
             ["Solo una serie aleatoria", "Tendencia y estacionalidad anual (huella combinada)", "Solo ciclo económico"],
             1, "Decaimiento gradual → tendencia. Pico en r₁₂ → estacionalidad anual. Es la huella combinada: Winter o descomposición multiplicativa."),
    concepto("La banda", "¿Cuándo un rₖ es de verdad?",
             "Un rₖ nunca da exactamente cero por azar. La banda de significancia es ±2/√n. Fuera de la banda = patrón real. Dentro = ruido.",
             formula="\\pm \\frac{2}{\\sqrt{n}}",
             ejemplo="Con n = 48, la banda es ±0,29. En los correlogramas de Minitab (el software de la cátedra) las bandas aparecen como líneas punteadas."),
    concepto("Ejemplo de examen", "Ventas mensuales, n = 48.",
             "r₁=0,85, r₂=0,72, r₃=0,61… r₁₁=0,15, r₁₂=0,68, r₁₃=0,55. Las primeras decaen (tendencia) y hay un repunte en r₁₂ (estacionalidad anual). Ambos superan ±0,29.",
             ejemplo="Redacción: «La serie presenta tendencia (autocorrelaciones significativas que decaen gradualmente) y estacionalidad de período 12 (pico significativo en el desfasamiento 12). No es estacionaria. Corresponde aplicar Winter o descomposición multiplicativa.»"),
    concepto("El truco de los errores", "El correlograma también evalúa tu modelo.",
             "Después del pronóstico, calculá el correlograma de los errores. Si todavía tienen autocorrelación, el modelo dejó un patrón sin capturar. Si son ruido puro (todo dentro de la banda), exprimiste la información disponible.",
             ejemplo="Es el mejor test de calidad de un modelo de pronóstico."),
    pregunta("Hiciste un suavizado exponencial simple y el correlograma de los errores tiene un pico significativo en r₁₂. ¿Qué te dice?",
             ["Que el método está perfecto: r₁₂ alto es una buena señal", "Que quedó un patrón estacional anual sin capturar: hay que cambiar o completar el método", "Nada: los errores siempre tienen r₁₂ alto"],
             1, "Si los errores todavía tienen autocorrelación, el modelo dejó un patrón sin capturar. Un pico en r₁₂ es estacionalidad anual: el suavizado simple no la modela; correspondería Winter o descomposición."),
    cierre("Llevate esto de la Clase 3.b.",
           "rₖ = correlación de la serie consigo misma desfasada k períodos. El correlograma deja huellas: aleatoria, tendencia, estacionalidad (pico en L) o combinada. Banda ±2/√n. Es el diagnóstico objetivo que respalda el método, y aplicado a los errores verifica si quedó un patrón suelto."),
]

H_C4 = [
    concepto("La idea", "El árbol propone. Las medidas deciden.",
             "Pronosticaste 500 y vendiste 480. ¿Estuviste bien o mal? Y si otro método dijo 510, ¿cuál es mejor? Un mes suelto no alcanza. Hay que medir el error a lo largo de toda la serie y resumirlo en un número."),
    concepto("El ladrillo", "El residual: lo real menos lo pronosticado.",
             "eₜ = Yₜ − Ŷₜ. El signo importa: e positivo = vendiste MÁS de lo previsto (subestimaste). e negativo = vendiste MENOS (sobreestimaste).",
             formula="e_t = Y_t - \\hat{Y}_t"),
    pregunta("Vendiste 480 y el pronóstico era 500. El residual es…",
             ["+20: subestimaste", "−20: sobreestimaste", "−20: subestimaste"],
             1, "e = 480 − 500 = −20. Vendiste menos de lo previsto → sobreestimaste."),
    concepto("Por qué son cuatro", "Si promediás los errores crudos, se cancelan.",
             "Un mes +50 y otro −50: el promedio da 0 y parecerías perfecto. Hay dos soluciones a la cancelación: valor absoluto (MAD, MAPE) o elevar al cuadrado (MSE). Y una medida que aprovecha la cancelación a propósito para medir sesgo: PME."),
    concepto("MAD y MSE", "Unidades reales vs. castigo a los grandes.",
             "MAD = promedio de |e|: queda en las unidades originales («me equivoco típicamente en 15 unidades»). Es la base de la señal de rastreo. MSE = promedio de e²: castiga fuerte los errores grandes y es el criterio estándar para elegir parámetros (el α que minimiza el error).",
             ejemplo="Errores 10 y 10 → MSE = 100. Errores 0 y 20 (mismo total) → MSE = 200. El MSE está en unidades al cuadrado: sirve para comparar, no para comunicar."),
    concepto("MAPE y PME", "Porcentaje, con y sin valor absoluto.",
             "MAPE deja el error en % y permite comparar series distintas (un MAD de 500 es horrible para una panadería y excelente para una automotriz). Cuidado: explota si algún Yₜ es cero. PME es igual pero SIN valor absoluto: mide el SESGO.",
             ejemplo="PME ≈ 0: método centrado. Positivo y grande: subestima sistemáticamente. Negativo y grande: sobreestima sistemáticamente."),
    pregunta("Un PME positivo y grande te está diciendo…",
             ["Que el método es impreciso, nada más", "Que subestima sistemáticamente: se le está escapando un patrón", "Que sobreestima, porque el signo del PME se lee al revés"],
             1, "PME positivo = subestima (siempre pronostica de menos). Un PME grande no dice «impreciso»: dice que al método se le escapa un patrón. Caso típico: suavizado simple sobre una serie con tendencia creciente → conviene pasar a Holt."),
    concepto("El caso típico", "Si el PME delata tendencia, cambiá de método.",
             "Aplicás suavizado exponencial simple a una serie con tendencia creciente. El método siempre va «atrás», siempre pronostica de menos → PME positivo consistente. La solución no es afinar el α: es cambiar a un método con tendencia (Holt)."),
    concepto("Ejemplo A vs. B", "Cada medida dice algo distinto.",
             "Método A: MAD 4,83 · MSE 26,2 · MAPE 4,3% · PME +2,5%. Método B: MAD 6,50 · MSE 65,2 · MAPE 5,9% · PME −0,6%. A es más preciso (sobre todo en MSE: B tiene un error de −15 en el mes 5). B está mejor centrado.",
             ejemplo="Se recomienda A por su mayor precisión, monitoreando la tendencia a subestimar. Usar las cuatro medidas es lo que convierte una cuenta en una interpretación."),
    concepto("Validación (Hanke)", "No midas el error sobre los datos con los que ajustaste.",
             "Elegí el método según el patrón (árbol). Partí los datos en inicialización (para ajustar) y prueba (que el método no vio). Ajustá con una, pronosticá la otra, medí ahí. Después decidí: usar, modificar o probar otro.",
             ejemplo="Si medís el error sobre los mismos datos con los que ajustaste, hacés trampa sin querer."),
    concepto("Señal de rastreo", "Un método que hoy funciona puede dejar de funcionar.",
             "Se monitorea alguna medida del error y se fijan límites; cuando los rebasa, se alerta para revisar o recalibrar (por ejemplo, cambiar el α).",
             ejemplo="Versión simple de Hanke: contar cuántas de las últimas n predicciones fueron subestimaciones (U). Si está sano, deberían ser ≈ n/2. Muy lejos de n/2 indica sesgo sistemático."),
    pregunta("MAD, MSE y MAPE ¿pueden ser negativos?",
             ["Sí, si sobreestimaste", "No: llevan valor absoluto o cuadrado. El que sí puede ser negativo es el PME", "Solo el MSE puede ser negativo"],
             1, "MAD, MSE y MAPE nunca pueden ser negativos. El PME sí: de hecho su signo es toda la información."),
    cierre("Llevate esto de la Clase 4.",
           "Residual e = Y − Ŷ (positivo = subestimé). MAD (unidades, intuitiva), MSE (castiga grandes, elige parámetros), MAPE (en %, comparable entre series), PME (sesgo). Un PME alto delata un patrón no capturado. Validación: partir en inicialización y prueba. Señal de rastreo: control continuo."),
]

H_INT = [
    concepto("La idea", "Tres clases, un solo procedimiento.",
             "3.a te da la sospecha, 3.b te da la prueba, el árbol te da el método, la clase 4 te dice si acertaste. No son temas sueltos."),
    concepto("La analogía", "Como un médico.",
             "3.a es mirar al paciente (los síntomas a simple vista). 3.b es pedir análisis (confirmar con números). El árbol es recetar. La clase 4 es el control posterior: ¿mejoró? Si no, cambiás el remedio."),
    concepto("Paso 1 y 2", "Graficar y diagnosticar.",
             "Paso 1: dibujás la serie y mirás si sube, si tiene olas, si es plana → la SOSPECHA. Paso 2: autocorrelaciones contra la banda ±2/√n → la PRUEBA. El gráfico daba una impresión; esto es un dato verificable."),
    concepto("Paso 3, 4 y 5", "Elegir, aplicar, medir.",
             "Con el árbol, el diagnóstico se vuelve método (estacionaria → móvil o suavizado simple; tendencia → Holt, Brown, regresión; estacionalidad → Winter o descomposición; ciclo → descomposición o indicadores). Después aplicás y obtenés los Ŷ. Al final, MAD, MSE, MAPE y PME responden «¿acerté?»."),
    pregunta("El pronóstico es un circuito, no una línea recta. Si el error anda mal, ¿qué hacés?",
             ["Ajustás un poco los números a mano y listo", "Volvés al paso 3 y cambiás de método", "Tiras el modelo y usás el promedio, siempre"],
             1, "Si el error dice que algo anda mal, volvés al paso 3 y cambiás de método."),
    concepto("Heladería", "De punta a punta.",
             "Graficar: cada verano se dispara, cada invierno se hunde, y cada año vende un poco más → sospecha de estacionalidad + tendencia. Correlograma: pico en r₄ y r₈, primeras barras que decaen → prueba, L = 4. Árbol: Winter (o descomposición). Medir: MAPE 5%, PME ≈ 0. Preciso y sin sesgo: te quedás con Winter."),
    concepto("¿Y si salía mal?", "El PME delata un diagnóstico equivocado.",
             "Si en el paso 4 hubieras usado suavizado exponencial simple, ignorando el diagnóstico, el paso 5 te habría dado PME = +12%, siempre positivo: estás subestimando todos los meses, el método no captura la tendencia. Volvés al paso 3 y cambiás a Winter.",
             ejemplo="Método impreciso pero centrado (PME ≈ 0): método correcto, datos ruidosos. Método sesgado (PME alto y del mismo signo): método EQUIVOCADO para ese patrón."),
    pregunta("Un método tiene MAPE bajo pero PME alto y siempre del mismo signo. ¿Qué significa?",
             ["Está bien: el MAPE bajo gana siempre", "Es preciso pero sesgado: el método es equivocado para ese patrón y hay que cambiarlo", "Hay que borrar los datos atípicos y nada más"],
             1, "El PME de la clase 4 te delata cuando te equivocaste en el diagnóstico de la clase 3. Sesgo alto y consistente → cambiar de método."),
    concepto("En el examen", "Una justificación completa puntúa.",
             "El molde: 1) diagnóstico (qué componentes tiene), 2) evidencia (gráfico y/o correlograma), 3) método, 4) justificación (por qué ese método para ese patrón), 5) validación (qué dicen las medidas de error).",
             ejemplo="«La serie presenta tendencia y estacionalidad (pico significativo en r₄ y decaimiento gradual), por lo que apliqué Winter; el MAPE de 5% y el PME cercano a cero confirman que el método es adecuado y no presenta sesgo.»"),
    cierre("Llevate el circuito.",
           "Graficar (sospecha) → correlograma (prueba) → árbol (método) → aplicar (números) → medir el error (¿acerté?). Si el PME es alto y consistente, se vuelve al paso 3. La respuesta de examen combina las tres clases: diagnóstico + evidencia + método + justificación + validación."),
]


def make_class(*, id, title, name, lede, source, laminas, teoria, historias, next_cls=None, visto=True):
    return {
        **UNIT,
        "id": id,
        "title": title,
        "name": name,
        "lede": lede,
        "visto": visto,
        "source": source,
        "laminas": laminas,
        "next": next_cls,
        "teoria": teoria,
        "historias": historias,
    }


def lede_from(blocks, fallback):
    t = first_callout(blocks)
    t = " ".join(t.split())
    t = t.replace("**", "")
    t = t.replace("Idea central de toda la clase:", "").replace("Idea central:", "").strip()
    return t or fallback


def main():
    # ---- C1 + C1.b split ----
    all1 = load("Clase01_y_01b_BaseEstadistica.md")
    # indices of h2-ish numbered sections
    def idx(pred):
        return find_heading_index(all1, pred)

    i6 = idx(lambda t: t.startswith("6."))
    i10 = idx(lambda t: t.startswith("10."))
    i11 = idx(lambda t: t.startswith("11."))
    i12 = idx(lambda t: t.startswith("12."))
    i13 = idx(lambda t: t.startswith("13."))

    intro_and_c1 = all1[:i6]  # title, idea, §§1-5
    c1b_body = all1[i6:i10]  # §§6-9
    glos = all1[i10:i11]
    ejercicio = all1[i11:i12]
    minis = all1[i12:i13]
    reaparece = all1[i13:]

    # Split mini-resúmenes: two callouts after the heading
    mini_heading = [b for b in minis if b.get("type") == "heading"][:1]
    mini_quotes = [b for b in minis if b.get("type") == "callout"]
    mini_rest = [b for b in minis if b not in mini_heading and b not in mini_quotes]
    # usually two callouts: Clase 1 and Clase 1.b
    c1_mini = mini_heading + (mini_quotes[:1] if mini_quotes else [])
    c1b_mini = ([{"type": "heading", "level": 2, "text": "Mini-resumen de la Clase 1.b"}] + mini_quotes[1:2] if len(mini_quotes) > 1 else [])

    c1_teoria = tidy(intro_and_c1[1:] + glos + c1_mini + reaparece)  # drop h1, keep rest
    c1_teoria = insert_after_first_callout(c1_teoria, [{
        "type": "svg",
        "file": "u2/img/Clase01_BaseEstadistica.svg",
        "caption": "Lámina de la Clase 1 · Base estadística",
    }])

    c1b_intro = [
        {"type": "callout", "kind": "idea", "text": mini_quotes[1]["text"] if len(mini_quotes) > 1 else "La tabla Z y los cinco casos."},
    ]
    c1b_teoria = tidy(c1b_intro + c1b_body + ejercicio + c1b_mini)
    c1b_teoria = insert_after_first_callout(c1b_teoria, [{
        "type": "svg",
        "file": "u2/img/Clase01b_TablaZ_5Casos.svg",
        "caption": "Lámina de la Clase 1.b · La tabla normal Z — los 5 casos",
    }])

    classes = []

    classes.append(make_class(
        id="c1",
        title="Clase 1 · Base estadística",
        name="Base estadística",
        lede=lede_from(all1, "El promedio dice el centro; el desvío estándar dice la dispersión."),
        source=["clases_previas/SG/Clase01_y_01b_BaseEstadistica.md", "clases_previas/SG/Clase01_BaseEstadistica.svg"],
        laminas=["u2/img/Clase01_BaseEstadistica.svg"],
        teoria=c1_teoria,
        historias=C1_STORIES,
        next_cls="Clase 1.b · La tabla Z y los 5 casos",
    ))

    classes.append(make_class(
        id="c1b",
        title="Clase 1.b · Tabla Z",
        name="Tabla Z",
        lede=lede_from(c1b_intro, "Cómo se lee la tabla Z y los cinco casos."),
        source=["clases_previas/SG/Clase01_y_01b_BaseEstadistica.md", "clases_previas/SG/Clase01b_TablaZ_5Casos.svg"],
        laminas=["u2/img/Clase01b_TablaZ_5Casos.svg"],
        teoria=c1b_teoria,
        historias=H_C1B,
        next_cls="Clase 2 · Correlación",
    ))

    def standard(id, title, name, md, svg, historias, next_cls, extra_svgs=None):
        blocks = load(md)
        title_h1, body = drop_title_h1(blocks)
        # drop the metadata paragraph right after h1 if it is the "Sistemas de Gestión (UTN FRRo)" line — keep it, it's source.
        teoria = tidy(body)
        caps = {
            "Clase02_Correlacion.svg": "Lámina de la Clase 2 · Correlación",
            "Clase03a_SeriesDeTiempo.svg": "Lámina de la Clase 3.a · Serie de tiempo y componentes",
            "Clase03b_Autocorrelacion.svg": "Lámina de la Clase 3.b · Autocorrelación y correlograma",
            "Clase04_MedidasDeError.svg": "Lámina de la Clase 4 · Medidas de error",
            "ProcesoCompleto_Pronostico.svg": "Lámina · El proceso completo de pronóstico",
            "ArbolDecisorio_MetodosPronostico.svg": "Árbol decisorio de métodos de pronóstico",
        }
        inject = [{"type": "svg", "file": f"u2/img/{svg}", "caption": caps.get(svg, svg)}]
        for ev in extra_svgs or []:
            inject.append({"type": "svg", "file": f"u2/img/{ev}", "caption": caps.get(ev, ev)})
        teoria = insert_after_first_callout(teoria, inject)
        src = [f"clases_previas/SG/{md}", f"clases_previas/SG/{svg}"]
        for ev in extra_svgs or []:
            src.append(f"clases_previas/SG/{ev}")
        laminas = [f"u2/img/{svg}"] + [f"u2/img/{ev}" for ev in (extra_svgs or [])]
        classes.append(make_class(
            id=id, title=title, name=name,
            lede=lede_from(body, title),
            source=src, laminas=laminas, teoria=teoria, historias=historias, next_cls=next_cls,
        ))

    standard("c2", "Clase 2 · Correlación", "Correlación",
             "Clase02_Correlacion.md", "Clase02_Correlacion.svg", H_C2,
             "Clase 3.a · Series de tiempo")
    standard("c3a", "Clase 3.a · Series de tiempo", "Series de tiempo",
             "Clase03a_SeriesDeTiempo.md", "Clase03a_SeriesDeTiempo.svg", H_C3A,
             "Clase 3.b · Autocorrelación",
             extra_svgs=["ArbolDecisorio_MetodosPronostico.svg"])
    standard("c3b", "Clase 3.b · Autocorrelación", "Autocorrelación",
             "Clase03b_Autocorrelacion.md", "Clase03b_Autocorrelacion.svg", H_C3B,
             "Clase 4 · Medidas de error",
             extra_svgs=["ArbolDecisorio_MetodosPronostico.svg"])
    standard("c4", "Clase 4 · Medidas de error", "Medidas de error",
             "Clase04_MedidasDeError.md", "Clase04_MedidasDeError.svg", H_C4,
             "Integrador · El proceso completo",
             extra_svgs=["ArbolDecisorio_MetodosPronostico.svg"])
    standard("cint", "Integrador · Proceso completo", "Proceso completo",
             "Integrador_ProcesoCompleto.md", "ProcesoCompleto_Pronostico.svg", H_INT,
             "Clase 5 · Métodos ingenuos y promedios (próximamente)",
             extra_svgs=["ArbolDecisorio_MetodosPronostico.svg"])

    for c in classes:
        path = OUT / {
            "c1": "clase01.json",
            "c1b": "clase01b.json",
            "c2": "clase02.json",
            "c3a": "clase03a.json",
            "c3b": "clase03b.json",
            "c4": "clase04.json",
            "cint": "integrador.json",
        }[c["id"]]
        path.write_text(json.dumps(c, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        n_teo = len(c["teoria"])
        n_hi = len(c["historias"])
        n_q = sum(1 for x in c["historias"] if x["type"] == "pregunta")
        n_ej = sum(1 for x in c["teoria"] if x["type"] == "ejercicio")
        n_svg = sum(1 for x in c["teoria"] if x["type"] == "svg")
        print(f"{c['id']:5} {path.name:18} teoria={n_teo:3} historias={n_hi:2} preg={n_q} ej={n_ej} svg={n_svg}")

    index = {
        "title": "Sistemas de Gestión",
        "subtitle": "UTN FRRo · Ingeniería en Sistemas",
        "units": [
            {"id": "u1", "title": "U1 · La empresa como productora de bienes", "kind": "Teoría",
             "classes": [{"id": "u1-intro", "title": "Enfoque sistémico", "file": "u1/enfoque.json", "soon": False, "visto": False, "name": "Enfoque sistémico"}]},
            {
                "id": "u2",
                "title": "U2 · Métodos de pronósticos",
                "kind": "Práctica",
                "laminas": [
                    {"file": "u2/img/MapaMateria_SistemasDeGestion_v2.svg", "caption": "Mapa de la materia (versión 2)"},
                    {"file": "u2/img/ArbolDecisorio_MetodosPronostico.svg", "caption": "Árbol decisorio de métodos de pronóstico"},
                ],
                "lede": "Unidad 2 del programa: los métodos de pronósticos. Empieza con el mapa de toda la materia y las siglas (Clases 0 y 0.1), y sigue con las clases que ya vimos: base estadística, correlación, series, autocorrelación, medidas de error y el integrador.",
                "classes": [
                    {"id": "c0", "title": "Clase 0 · Mapa", "file": "u2/clase00.json", "soon": False, "visto": True, "name": "Mapa"},
                    {"id": "c01", "title": "Clase 0.1 · Siglas", "file": "u2/clase01_siglas.json", "soon": False, "visto": True, "name": "Siglas"},
                    {"id": "c1", "title": "Clase 1 · Base estadística", "file": "u2/clase01.json", "soon": False, "visto": True, "name": "Base estadística"},
                    {"id": "c1b", "title": "Clase 1.b · Tabla Z", "file": "u2/clase01b.json", "soon": False, "visto": True, "name": "Tabla Z"},
                    {"id": "c2", "title": "Clase 2 · Correlación", "file": "u2/clase02.json", "soon": False, "visto": True, "name": "Correlación"},
                    {"id": "c3a", "title": "Clase 3.a · Series de tiempo", "file": "u2/clase03a.json", "soon": False, "visto": True, "name": "Series de tiempo"},
                    {"id": "c3b", "title": "Clase 3.b · Autocorrelación", "file": "u2/clase03b.json", "soon": False, "visto": True, "name": "Autocorrelación"},
                    {"id": "c4", "title": "Clase 4 · Medidas de error", "file": "u2/clase04.json", "soon": False, "visto": True, "name": "Medidas de error"},
                    {"id": "cint", "title": "Integrador · Proceso completo", "file": "u2/integrador.json", "soon": False, "visto": True, "name": "Proceso completo"},
                    {"id": "c5", "title": "Clase 5 · Promedios", "soon": True},
                    {"id": "c6", "title": "Clase 6 · Suavizado simple", "soon": True},
                ],
            },
            {"id": "u3", "title": "U3 · El producto", "kind": "Teoría + cálculo",
             "classes": [{"id": "u3-intro", "title": "Ciclo de vida, BOM, codificación", "soon": True}]},
            {"id": "u4", "title": "U4 · El proceso de producción", "kind": "Teoría + práctica",
             "classes": [{"id": "u4-intro", "title": "JIT, TOC, hombre-máquina", "soon": True}]},
            {"id": "u5", "title": "U5 · Logística", "kind": "Práctica + teoría",
             "classes": [{"id": "u5-intro", "title": "EOQ, stock, ABC", "soon": True}]},
            {"id": "u6", "title": "U6 · Planificación y control", "kind": "Práctica",
             "classes": [{"id": "u6-intro", "title": "Plan agregado, MPS, MRP", "soon": True}]},
            {"id": "u7", "title": "U7 · Softwares ERP", "kind": "Teoría",
             "classes": [{"id": "u7-intro", "title": "De MRP a ERP", "soon": True}]},
        ],
    }
    (ROOT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("index.json ok")


if __name__ == "__main__":
    main()
