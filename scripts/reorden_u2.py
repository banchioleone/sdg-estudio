#!/usr/bin/env python3
"""Reorden y renombre de la Unidad 2 por bloques (A·B·C·D) + auditoría de textos.

Idempotente: se puede correr más de una vez. Edita content/ en el lugar y
escribe un log de cada cambio en stdout. Los renombres de archivo
(clase03a→clase03, clase02b_teoria→clase04b, Clase03a_SeriesDeTiempo.svg→
Clase03_SeriesDeTiempo.svg) se hicieron con `git mv` antes de correrlo.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
C = ROOT / "content"
LOG = []

def log(f, where, old, new):
    o = old if len(old) < 90 else old[:87] + "…"
    n = new if len(new) < 90 else new[:87] + "…"
    LOG.append(f"{f} · {where}: «{o}» → «{n}»")

BLOCKS = [
    {"id": "intro", "title": "Introducción"},
    {"id": "A", "title": "Bloque A · Base estadística"},
    {"id": "B", "title": "Bloque B · Demanda, datos y patrones"},
    {"id": "C", "title": "Bloque C · Métodos de series de tiempo"},
    {"id": "D", "title": "Bloque D · Regresión"},
]
BT = {b["id"]: b["title"] for b in BLOCKS}

# id, file, title, name (feed), short (avatar), emoji, block
U2 = [
    ("c0",   "u2/clase00.json",      "Clase 0 · Mapa de la materia",                   "Mapa de la materia",            "Mapa",        "🗺️", "intro"),
    ("c01",  "u2/clase01_siglas.json","Clase 0.1 · Siglas",                            "Siglas",                        "Siglas",      "🔤", "intro"),
    ("c1",   "u2/clase01.json",      "Clase 1 · Base estadística",                     "Base estadística",              "Estadística", "1",  "A"),
    ("c1b",  "u2/clase01b.json",     "Clase 1.b · Tabla Z",                            "Tabla Z",                       "Tabla Z",     "1.b","A"),
    ("c2",   "u2/clase02.json",      "Clase 2 · Correlación",                          "Correlación",                   "Correlación", "2",  "B"),
    ("c3",   "u2/clase03.json",      "Clase 3 · Series de tiempo",                     "Series de tiempo",              "Series",      "3",  "B"),
    ("c3b",  "u2/clase03b.json",     "Clase 3.b · Autocorrelación y correlograma",     "Autocorrelación y correlograma","Autocorr.",   "3.b","B"),
    ("c4",   "u2/clase04.json",      "Clase 4 · Medidas de error",                     "Medidas de error",              "Error",       "4",  "B"),
    ("c4b",  "u2/clase04b.json",     "Clase 4.b · Demanda y sistemas de pronóstico",   "Demanda y sistemas de pronóstico","Demanda",   "4.b","B"),
    ("cint", "u2/integrador.json",   "Integrador · El proceso completo de pronóstico", "El proceso completo de pronóstico","Integrador","∑", "B"),
    ("c5",   "u2/clase05.json",      "Clase 5 · Métodos ingenuos y promedios",         "Métodos ingenuos y promedios",  "Promedios",   "5",  "C"),
    ("c6",   "u2/clase06.json",      "Clase 6 · Suavización exponencial simple",       "Suavización exponencial simple","SES",         "6",  "C"),
    ("c7",   "u2/clase07.json",      "Clase 7 · Brown y Holt",                         "Brown y Holt",                  "Holt",        "7",  "C"),
    ("c8",   "u2/clase08.json",      "Clase 8 · Winter",                               "Winter",                        "Winter",      "8",  "C"),
    ("c9",   "u2/clase09.json",      "Clase 9 · Descomposición multiplicativa",        "Descomposición multiplicativa", "Descomp.",    "9",  "C"),
    ("c10",  "u2/clase10.json",      "Clase 10 · Elegir y controlar el método",        "Elegir y controlar el método",  "Control",     "10", "C"),
    ("c11",  "u2/clase11.json",      "Clase 11 · Regresión lineal simple",             "Regresión lineal simple",       "Reg. simple", "11", "D"),
    ("c12",  "u2/clase12.json",      "Clase 12 · Inferencia en regresión",             "Inferencia en regresión",       "Inferencia",  "12", "D"),
    ("c13",  "u2/clase13.json",      "Clase 13 · Regresión múltiple",                  "Regresión múltiple",            "Reg. múltiple","13","D"),
    ("c14",  "u2/clase14.json",      "Clase 14 · Validación y comparación de modelos", "Validación y comparación de modelos","Validación","14","D"),
]
OLD_IDS = {"c3a": "c3", "c2bteoria": "c4b"}

U2_LEDE = ("Unidad 2 del programa: los métodos de pronósticos. Arranca con una introducción "
           "(Clase 0 · Mapa de la materia y Clase 0.1 · Siglas) y sigue en cuatro bloques. "
           "Bloque A · Base estadística: promedio, desvío, distribución normal y tabla Z. "
           "Bloque B · Demanda, datos y patrones: correlación, series de tiempo, autocorrelación, "
           "medidas de error, demanda y sistemas de pronóstico, y el Integrador del proceso completo. "
           "Bloque C · Métodos de series de tiempo: ingenuos y promedios, suavización exponencial simple, "
           "Brown y Holt, Winter, descomposición multiplicativa y cómo elegir y controlar el método. "
           "Bloque D · Regresión: simple, inferencia, múltiple y validación de modelos. "
           "Todas las clases tienen teoría completa e historias.")

# Reemplazos literales, en orden, sobre todos los strings (no SVG ni rutas de fuente).
LIT = [
    ("En la 3.a diagnosticabas", "En la Clase 3 diagnosticabas"),
    ("en la 3.a diagnosticabas", "en la Clase 3 diagnosticabas"),
    ("(clase 3.a)", "(Clase 3)"),
    ("clases 3.a, 3.b y 4", "clases 3, 3.b y 4"),
    ("Clases 3.a, 3.b y 4", "Clases 3, 3.b y 4"),
    ("Integrador 3.a + 3.b + 4", "Integrador 3 + 3.b + 4"),
    ("*3.a me da la SOSPECHA · 3.b me da la PRUEBA", "*la Clase 3 me da la SOSPECHA · la 3.b me da la PRUEBA"),
    ("3.a me da la sospecha", "la Clase 3 me da la sospecha"),
    ("3.a te da la sospecha, 3.b te da", "La Clase 3 te da la sospecha, la 3.b te da"),
    ("3.a es mirar al paciente", "La Clase 3 es mirar al paciente"),
    ("**3.a**", "**Clase 3**"),
    ("Clase 3.a", "Clase 3"),
    ("clase 3.a", "Clase 3"),
    ("Clase 2.b-teoría", "Clase 4.b"),
    ("Llevate esto de la Clase 2.b.", "Llevate esto de la Clase 4.b."),
    ("Clase 8 · Winter multiplicativo", "Clase 8 · Winter"),
    ("Clase 9 · Descomposición y desestacionalización", "Clase 9 · Descomposición multiplicativa"),
    ("Clase 10 · Integrador de métodos y control", "Clase 10 · Elegir y controlar el método"),
    ("Clase 5: Métodos no formales y promedios", "Clase 5 · Métodos ingenuos y promedios"),
    (" No se agregan historias.", ""),
]

# Reemplazos puntuales por archivo (texto completo del bloque o fragmento).
PER = {
    "u2/clase02.json": [
        ("**Próxima clase → Clase 3: Fuentes y tipos de datos + componentes de una serie de tiempo** (tendencia, ciclo, estacionalidad, irregularidad)",
         "**Próxima clase → Clase 3 · Series de tiempo**: fuentes y tipos de datos, y componentes de una serie (tendencia, ciclo, estacionalidad, irregularidad)"),
    ],
    "u2/clase03b.json": [
        ("Cierra la Unidad 2.b y abre los métodos.",
         "Después vienen la Clase 4.b (demanda y sistemas de pronóstico) y el Integrador, que cierran el Bloque B."),
    ],
    "u2/clase04.json": [
        ("**Con esta clase se cierra la Unidad 2.b (demanda, datos y patrones).**",
         "**Con esta clase termina la parte de datos y patrones del Bloque B.** Faltan la Clase 4.b y el Integrador."),
        ("**Sigue → Clase 5: Métodos no formales y promedios** (promedio simple, promedio móvil, promedio móvil doble): el primer bloque de métodos de pronóstico. Arranca la Unidad 2.c. Ya está cargada.",
         "**Sigue → Clase 4.b · Demanda y sistemas de pronóstico**: qué se pronostica y para qué, demanda dependiente e independiente, métodos cualitativos y el sistema de pronósticos. Después, el Integrador cierra el Bloque B y la Clase 5 abre el Bloque C (métodos de series de tiempo)."),
        ("**Sigue → Clase 5 · Métodos ingenuos y promedios** (promedio simple, promedio móvil, promedio móvil doble): el primer bloque de métodos de pronóstico. Arranca la Unidad 2.c. Ya está cargada.",
         "**Sigue → Clase 4.b · Demanda y sistemas de pronóstico**: qué se pronostica y para qué, demanda dependiente e independiente, métodos cualitativos y el sistema de pronósticos. Después, el Integrador cierra el Bloque B y la Clase 5 abre el Bloque C (métodos de series de tiempo)."),
    ],
    "u2/clase04b.json": [
        ("Completamos el marco del programa después de los métodos de series y antes de los modelos causales de regresión.",
         "Cierra el Bloque B con el marco del programa, antes de los métodos de series (Bloque C) y de los modelos causales de regresión (Bloque D)."),
        ("en la Clase 10, inmediatamente anterior a ésta, calculamos RSFE/MAD",
         "en la Clase 10 se calculan RSFE/MAD"),
        ("**Próxima clase → Clase 11 · Regresión lineal simple**",
         "**Próxima clase → Integrador · El proceso completo de pronóstico**"),
        ("Próxima: regresión simple.", "Próxima: el Integrador."),
    ],
    "u2/clase09.json": [
        ("Próxima: integrador y control.", "Próxima: elegir y controlar el método."),
    ],
    "u2/clase10.json": [
        ("**Próxima clase → Clase 4.b · Demanda, cualitativos y sistemas de pronóstico**",
         "**Próxima clase → Clase 11 · Regresión lineal simple** (abre el Bloque D)"),
        ("Próxima: demanda, cualitativos y sistemas.", "Próxima: regresión lineal simple."),
    ],
    "u2/clase14.json": [
        ("**Próxima clase → Fin de la Unidad 2 · Próximo paso: historias para Clases 2.b-teoría, 6–14**",
         "**Fin de la Unidad 2 · Métodos de pronósticos.**"),
        ("**Próxima clase → Fin de la Unidad 2 · Próximo paso: historias para Clases 4.b, 6–14**",
         "**Fin de la Unidad 2 · Métodos de pronósticos.**"),
    ],
    "u2/integrador.json": [],
    "u1/enfoque.json": [
        ("ni una clase 0.x de la Unidad 1 en la serie que ya vimos.",
         "ni una clase 0.x de la Unidad 1 entre las clases previas."),
        ("Esta clase no está marcada como Vista: no se dictó en la serie 0 → 1, se arma ahora",
         "No se dictó en las clases previas: se arma"),
    ],
}

def walk(obj, fn, path=""):
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if k in ("svg", "file", "source", "sources", "fuentes") and not isinstance(v, (dict, list)) and k != "source":
                continue
            if k in ("svg", "file"):
                continue
            if isinstance(v, str):
                nv = fn(v, f"{path}.{k}")
                if nv != v: obj[k] = nv
            else:
                walk(v, fn, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, str):
                nv = fn(v, f"{path}[{i}]")
                if nv != v: obj[i] = nv
            else:
                walk(v, fn, f"{path}[{i}]")

def edit_file(rel, meta=None):
    p = C / rel
    d = json.loads(p.read_text(encoding="utf-8"))
    src_keys = {"sources", "fuentes"}
    def fn(s, where):
        if where.startswith(".sources") or where.startswith(".fuentes"):
            return s
        o = s
        for a, b in PER.get(rel, []):
            if a in s: s = s.replace(a, b)
        for a, b in LIT:
            if a in s: s = s.replace(a, b)
        s = s.replace("u2/img/Clase03a_SeriesDeTiempo.svg", "u2/img/Clase03_SeriesDeTiempo.svg")
        if s != o: log(rel, where, o, s)
        return s
    walk(d, fn)
    # rutas de lámina
    def fix_files(o):
        if isinstance(o, dict):
            if o.get("file") == "u2/img/Clase03a_SeriesDeTiempo.svg":
                o["file"] = "u2/img/Clase03_SeriesDeTiempo.svg"; log(rel, "file", "Clase03a_SeriesDeTiempo.svg", "Clase03_SeriesDeTiempo.svg")
            for v in o.values(): fix_files(v)
        elif isinstance(o, list):
            for v in o: fix_files(v)
    fix_files(d)
    if isinstance(d.get("source"), list):
        d["source"] = [x.replace("u2/img/Clase03a_SeriesDeTiempo.svg", "u2/img/Clase03_SeriesDeTiempo.svg") for x in d["source"]]
    if meta:
        cid, _, title, name, short, emoji, block = meta
        for k, v in (("id", cid), ("title", title), ("name", name)):
            if d.get(k) != v:
                log(rel, k, str(d.get(k)), v); d[k] = v
        d["block"] = block; d["blockTitle"] = BT[block]
        # encabezado estándar de la teoría
        t0 = d.get("teoria", [{}])[0]
        txt = t0.get("text", "")
        blk = "Introducción" if block == "intro" else f"Bloque {block}"
        hdr = f"**Sistemas de Gestión (UTN FRRo) · Unidad 2 · {blk} · {title}**"
        if txt.startswith("**Sistemas de Gestión (UTN FRRo)") and txt != hdr:
            log(rel, "teoria[0]", txt, hdr); t0["text"] = hdr
        elif cid == "cint" and txt.startswith("**Cómo se conectan") and not txt.endswith("· Unidad 2 · Bloque B"):
            new = re.sub(r" · Unidad 2 · Bloque B.*$", "", txt.rstrip()) + " · Unidad 2 · Bloque B"
            log(rel, "teoria[0]", txt, new); t0["text"] = new
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return d

def main():
    idx_p = C / "index.json"
    idx = json.loads(idx_p.read_text(encoding="utf-8"))
    u2 = next(u for u in idx["units"] if u["id"] == "u2")
    old = {c["id"]: c for c in u2["classes"]}
    for o, n in OLD_IDS.items():
        if o in old: old[n] = old.pop(o)
    new_classes = []
    for i, m in enumerate(U2):
        cid, f, title, name, short, emoji, block = m
        c = dict(old.get(cid, {}))
        c.update({"id": cid, "title": title, "file": f, "soon": False, "name": name,
                  "short": short, "emoji": emoji, "block": block})
        c.setdefault("visto", True)
        new_classes.append(c)
    titles_before = [c["title"] for c in u2["classes"]]
    u2["classes"] = new_classes
    u2["blocks"] = BLOCKS
    if u2.get("lede") != U2_LEDE:
        log("index.json", "u2.lede", u2.get("lede", ""), U2_LEDE); u2["lede"] = U2_LEDE
    u2["oldIds"] = OLD_IDS
    for u in idx["units"]:
        for c in u.get("classes", []):
            if u["id"] == "u1" and c["id"] == "u1-intro":
                c.setdefault("short", "Enfoque"); c.setdefault("emoji", "🏭")
    idx_p.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    LOG.append("index.json · u2.classes: orden " + " → ".join(c["title"].split(" · ")[0] for c in new_classes))

    datas = {}
    for m in U2:
        datas[m[0]] = edit_file(m[1], m)
    edit_file("u1/enfoque.json")
    # cadena next
    for i, m in enumerate(U2):
        rel = m[1]; p = C / rel
        d = json.loads(p.read_text(encoding="utf-8"))
        nxt = U2[i + 1][2] if i + 1 < len(U2) else "Fin de la Unidad 2"
        if d.get("next") != nxt:
            log(rel, "next", str(d.get("next")), nxt); d["next"] = nxt
            p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n".join(LOG))
    print(f"\n{len(LOG)} cambios", file=sys.stderr)

if __name__ == "__main__":
    main()
