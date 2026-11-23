"""Helpers para escribir las clases de la U6 (gen_u6.py). Reusa los bloques de u5lib."""
import json
from u5lib import ROOT, H, P, F, T, L, C, IDEA, AVISO, EXAM, EJ, EX, G, _fix, LOG_PESOS  # noqa: F401

U6 = ROOT / "content" / "u6"

def S(file, caption): return {"type": "svg", "file": "u6/img/" + file, "caption": caption}

BLOCKS = {"intro": "Introducción",
          "A": "Bloque A · Plan agregado y programa maestro",
          "B": "Bloque B · Capacidad",
          "C": "Bloque C · MRP y MRP II",
          "D": "Bloque D · Balanceo y control de la producción",
          "E": "Cierre · Integrador"}


def clase(id_, title, name, block, lede, source, teoria, next_=None, laminas=None):
    return {"unitId": "u6", "unitLabel": "Unidad 6", "unitTitle": "Planificación y control", "id": id_, "title": title,
            "name": name, "lede": lede, "visto": False, "source": source, "laminas": laminas or [],
            "next": next_, "teoria": teoria, "historias": [], "block": block, "blockTitle": BLOCKS[block]}


def write(fname, data):
    data = _fix(data)
    U6.mkdir(parents=True, exist_ok=True)
    (U6 / fname).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return fname

# Fuentes (rutas relativas a /workspace/sdg)
PROG = "programa.md — Unidad 6 · Planificación y control (programa 2008)"
DM = "clases_previas/SG/SistemasDeGestion_DocumentoMaestro_v2.txt — Unidad 6 y Semanas 6, 8, 9 y 10"
PAT = "patrones_examenes.md (conteos de finales)"
EVA = "texto/examenes/SG!EVA.txt y bloques_eva/ (compilado de finales 2002–2006)"
EPOS = "texto/examenes/Ejercicios posibles.txt (Ejercicios posibles.docx del Drive)"
REPASO = "texto/examenes/Preguntas de repaso.txt y preguntasdeteoria.txt (banco «La gestión de producción», respuestas de alumnos)"
MRPN = "drive_u6/12-Planificación de los Requerimientos de Materiales (MRP).pdf — Nota técnica de R. Morán (© 2000), apunte de la cátedra (mismo texto que «MRP- Planiificación de Requerimientos de Materiales.pdf»)"
CAPN = "drive_u6/Planificacion de la Capacidad.pdf — Nota técnica «Planificación de la capacidad de producción», R. Morán (© 2001)"
PACN = "drive_u6/PAC.pdf — Nota técnica «Control de las actividades de producción», R. Morán (© 2001)"
PAN = "drive_u6/Planificacion Agregada.pdf — «Planificación agregada de la producción», R. Morán (UNR, 2012)"
BIG = "drive_u6/Planeacion agregada de vtas y operaciones.pptx — láminas «Planeación agregada», Ing. Cristian G. Bigatti (UTN FRRo, 2015), y su ejercicio JC Company (.docx)"
ODOO = "drive_u6/2015 - TP N 7 - MRP ODOO.pdf y Tutoriales MRP Odoo 01–02 (UTN FRRo, 2015)"
def CH(cap, p, what): return f"Chase, Jacobs y Aquilano 12a ed., cap. {cap}, p. {p} — {what} (drive_u6/txt/cap{cap}_chase12.txt)"
def EFR(p, what): return f"texto/ocr/efr_ppm/p-{p:02d}.png — EjerciciosFinalesResueltos, resolución manuscrita ({what})"
