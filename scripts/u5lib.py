"""Helpers para escribir las clases de la U5 como dicts (gen_u5.py)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
U5 = ROOT / "content" / "u5"


def H(text, level=2): return {"type": "heading", "level": level, "text": text}
def P(text): return {"type": "paragraph", "text": text}
def F(tex, caption=None):
    d = {"type": "formula", "tex": tex}
    if caption: d["caption"] = caption
    return d
def T(headers, rows, caption=None):
    d = {"type": "table", "headers": headers, "rows": rows}
    if caption: d["caption"] = caption
    return d
def L(items, ordered=False): return {"type": "list", "ordered": ordered, "items": items}
def C(kind, text): return {"type": "callout", "kind": kind, "text": text}
def IDEA(t): return C("idea", t)
def AVISO(t): return C("aviso", t)
def EXAM(t): return C("examen", t)
def S(file, caption): return {"type": "svg", "file": "u5/img/" + file, "caption": caption}
def EJ(title, blocks): return {"type": "ejemplo", "title": title, "blocks": blocks}
def EX(title, blocks, solucion=None, estado="resuelto", nota=None):
    d = {"type": "ejercicio", "title": title, "estado": estado, "blocks": blocks}
    if solucion: d["solucion"] = solucion
    if nota: d["nota"] = nota
    return d
def G(title, intro, entries):
    return {"type": "glosario", "title": title, "intro": intro,
            "entries": [{"simbolo": a, "nombre": b, "significado": c} for a, b, c in entries]}

BLOCKS = {"intro": "Introducción",
          "A": "Bloque A · Inventario y modelos determinísticos",
          "B": "Bloque B · Modelos estocásticos y control",
          "C": "Bloque C · Compras, almacenes y logística",
          "D": "Cierre · Integrador"}


def clase(id_, title, name, block, lede, source, teoria, next_=None, laminas=None):
    return {"unitId": "u5", "unitLabel": "Unidad 5", "unitTitle": "Logística", "id": id_, "title": title,
            "name": name, "lede": lede, "visto": False, "source": source, "laminas": laminas or [],
            "next": next_, "teoria": teoria, "historias": [], "block": block, "blockTitle": BLOCKS[block]}


def write(fname, data):
    data = _fix(data)
    U5.mkdir(parents=True, exist_ok=True)
    (U5 / fname).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return fname

# Fuentes frecuentes (rutas relativas a /workspace/sdg)
V6 = "texto/resumenes/ResumenSG-Final-V6_345p.txt — Cap. 17 «Control de inventarios» (Chase), págs. 258–285 del PDF del resumen"
PROG = "programa.md — Unidad 5 · Logística (programa 2008)"
DM = "clases_previas/SG/SistemasDeGestion_DocumentoMaestro_v2.txt — Unidad 5 y Semana 7"
EVA = "texto/examenes/SG!EVA.txt (compilado de finales 2002–2006)"
PAT = "patrones_examenes.md (conteos de finales)"
PA = "texto/examenes/preguntasabastecimiento.txt (Examen 2005, respuestas de alumno)"
MC = "texto/examenes/Examen SG1 mult choice.txt y texto/Preguntas_Frecuentes.txt (multiple choice con marcas de alumno)"
DRP = "texto/apuntes_nuevos/DRP.txt — Nota técnica «Planificación de la distribución», R. Morán (2000)"
def EFR(p, what): return f"texto/ocr/efr_ppm/p-{p:02d}.png — EjerciciosFinalesResueltos, resolución manuscrita ({what})"
def LU(p, what): return f"texto/ocr/sg1_ppm/p-{p:02d}.png — SG1.doc, resolución manuscrita ({what})"


# --- signo pesos: los montos ($15, $7,50) se escapan como \$ para que inline_math no los tome como fórmula
LOG_PESOS = []

def _pesos(s):
    out, i = [], 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s):
            out.append(s[i:i + 2]); i += 2; continue
        if ch != "$":
            out.append(ch); i += 1; continue
        j = i + 1
        while j < len(s) and not (s[j] == "$" and s[j - 1] != "\\"):
            j += 1
        seg = s[i + 1:j]
        nxt = s[i + 1] if i + 1 < len(s) else " "
        prev = s[i - 1] if i else " "
        currency = (nxt in " /)*.,;:" or prev.isalnum()) or (nxt.isdigit() and (
            j >= len(s) or "**" in seg or not any(c in seg for c in "\\^_{=")))
        if currency:
            LOG_PESOS.append(s[max(0, i - 15):i + 12]); out.append("\\$"); i += 1; continue
        out.append(s[i:j + 1]); i = j + 1
    return "".join(out)

def _fix(o, key=None):
    if isinstance(o, dict):
        return {k: (v if k in ("tex", "file") else _fix(v, k)) for k, v in o.items()}
    if isinstance(o, list):
        return [_fix(x, key) for x in o]
    if isinstance(o, str) and "$" in o:
        return _pesos(o)
    return o
