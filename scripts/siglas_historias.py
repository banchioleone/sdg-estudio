#!/usr/bin/env python3
"""Clase 0.1 · Siglas: una tarjeta por sigla + tabla rápida en la teoría.

Fuente de cada definición: el glosario de la misma clase (content/u2/clase01_siglas.json),
que cita los apuntes. Las expansiones en inglés marcadas con * no están en el material:
son complemento (uso estándar). Idempotente.
"""
import json
from pathlib import Path

P = Path(__file__).resolve().parent.parent / "content/u2/clase01_siglas.json"
STAR = "* complemento: la expansión en inglés no está en el material."

# (grupo, unidad, sigla, inglés, castellano, definición de una línea, inglés_es_complemento)
S = [
 ("Pronósticos", "U2", "SES", "Simple Exponential Smoothing", "Suavización (nivelación) exponencial simple", "Nuevo pronóstico = anterior + α × último error.", True),
 ("Pronósticos", "U2", "MAD", "Mean Absolute Deviation", "Desviación absoluta media", "Error promedio en valor absoluto, en unidades.", True),
 ("Pronósticos", "U2", "MSE", "Mean Squared Error", "Error cuadrático medio", "Promedio de errores al cuadrado: castiga los grandes.", True),
 ("Pronósticos", "U2", "MAPE", "Mean Absolute Percentage Error", "Porcentaje de error medio absoluto", "Error en %: compara series de distinta escala.", True),
 ("Pronósticos", "U2", "PME", "sigla en castellano", "Porcentaje medio de error", "Conserva el signo: muestra el sesgo.", False),
 ("Pronósticos", "U2", "FAC / ACF", "Autocorrelation Function", "Función de autocorrelación", "El correlograma: prueba tendencia o estación con números.", True),
 ("Pronósticos", "U2", "r / R²", "sin expansión", "Correlación / coeficiente de determinación", "r: si dos variables se mueven juntas; R²: % de variación explicada.", False),
 ("Planificación", "U6", "MPS", "Master Production Schedule", "Plan (programa) maestro de producción", "Cuántos productos finales se fabrican y cuándo.", False),
 ("Planificación", "U6", "MRP", "Material Requirements Planning", "Planificación de los requerimientos de materiales", "Partes y materias primas por período para cumplir el MPS.", False),
 ("Planificación", "U6", "MRP II", "Manufacturing Resource Planning", "Planeación de recursos de manufactura", "El MRP ampliado a más recursos y áreas de la empresa.", True),
 ("Planificación", "U6", "CRP", "Capacity Requirements Planning", "Planificación de los requerimientos de capacidad", "Capacidad detallada, período a período, que exige el MRP.", False),
 ("Planificación", "U6", "RCCP", "Rough-Cut Capacity Planning", "Planificación aproximada de la capacidad (trad. propia)", "Chequeo grueso de capacidad; el apunte lo pone como complementario del CRP.", False),
 ("Planificación", "U6", "PAC", "Production Activity Control", "Control de las actividades de producción", "Lanza, programa y controla las órdenes en curso.", False),
 ("Planificación", "U6", "SFC", "Shop Floor Control", "Control del taller", "Otro nombre del PAC.", False),
 ("Planificación", "U6", "WIP", "Work in Process", "Trabajo en proceso (en curso)", "Lo que ya entró a producción y no terminó; lo administra el PAC.", True),
 ("Planificación", "U6", "OP / OC", "siglas en castellano", "Orden de producción / orden de compra", "Si hay un ingreso programado, existe una OP o una OC.", False),
 ("Planificación", "U6", "TBO", "Time Between Orders", "Tiempo entre órdenes", "Cada cuántos períodos se lanza una orden.", False),
 ("Planificación", "U6", "POQ", "Periodic Order Quantity", "Cantidad periódica de producción", "Período fijo, cantidad variable: usa el EOQ para hallar el TBO.", False),
 ("Planificación", "U6", "PPB", "Part Period Balancing", "Balance cantidad-período", "Agrupa requerimientos para minimizar producción + stock.", False),
 ("Inventarios y logística", "U5", "EOQ", "Economic Order Quantity", "Lote económico (cantidad económica de pedido)", "El lote clásico, para demanda poco variable.", False),
 ("Inventarios y logística", "U5", "LEC", "sigla en castellano", "Lote económico de compra", "El lote económico de lo que se compra; pareja del LEF.", False),
 ("Inventarios y logística", "U5", "LEF", "sigla en castellano", "Lote económico de fabricación", "El lote económico de lo que se fabrica.", False),
 ("Inventarios y logística", "U5", "SS", "Safety Stock", "Stock de seguridad", "Colchón contra la incertidumbre de la demanda o del lead time.", True),
 ("Inventarios y logística", "U5", "ABC", "no se expande", "Análisis / clasificación ABC", "Pareto aplicado al inventario: clasifica por valor.", False),
 ("Inventarios y logística", "U5", "DRP", "Distribution Requirements Planning", "Planificación de los requerimientos de distribución", "Un MRP de productos finales para centros de distribución.", False),
 ("Producto", "U3", "BOM", "Bill of Materials", "Lista de materiales / estructura de producto", "Qué componentes, y cuántos, lleva cada producto.", True),
 ("Producto", "U3", "IBM-11", "sin expansión", "Dígito verificador módulo 11", "Control de un código con pesos 2 a 7.", False),
 ("Proceso", "U4", "JIT", "Just In Time", "Justo a tiempo", "Producir lo que se necesita cuando se necesita.", True),
 ("Proceso", "U4", "Kanban", "palabra japonesa", "«Signo» o «tarjeta de instrucción»", "La señal que regula el flujo justo a tiempo.", False),
 ("Proceso", "U4", "SMED", "Single-Minute Exchange of Die", "Cambio de troqueles en un minuto", "Bajar los tiempos de preparación de las máquinas.", False),
 ("Proceso", "U4", "TQM", "Total Quality Management", "Administración de la calidad total", "Concepto básico de la U4 en el programa.", True),
 ("Proceso", "U4", "TOC", "Theory of Constraints", "Teoría de las restricciones", "Cuellos de botella, la meta y mejora continua (Goldratt).", True),
 ("ERP e información", "U7", "ERP", "Enterprise Resource Planning", "Planificación de recursos empresariales", "Paquete parametrizable para la gestión integral de la empresa.", True),
 ("ERP e información", "U7", "BI", "Business Intelligence", "Inteligencia de negocios", "Convierte datos en información útil para decidir.", False),
 ("ERP e información", "U7", "DW", "Data Warehouse", "Almacén de datos (trad. propia)", "Datos integrados, por materia, históricos y no volátiles.", False),
 ("ERP e información", "U7", "ETL", "Extract, Transform, Load", "Extracción, transformación y carga", "Lleva los datos de los sistemas operacionales al DW.", True),
 ("ERP e información", "U7", "DSS / SSD", "Decision Support System", "Sistema de soporte de decisiones", "Sistema de computación para apoyar decisiones.", False),
 ("ERP e información", "ref.", "APICS", "American Production & Inventory Control Society", "Sociedad estadounidense de control de producción e inventarios (trad. propia)", "Referencia de vocabulario de la bibliografía.", False),
 ("En duda", "U7", "MCP", "sin expansión en la cátedra", "—", "Cae en «Qué es MRP, MCP, ERP» (2012); ningún apunte la define.", False),
 ("En duda", "U3", "IBM-13", "sin expansión", "—", "Sólo un recuerdo de un final de 2011; sin procedimiento en los apuntes.", False),
]

QUIZ = {
 "Pronósticos": {"type": "pregunta", "k": "A ver…", "qid": "sq-pme", "title": "¿Qué sigla muestra si el método tiene sesgo?",
   "options": ["MAD", "MSE", "PME"], "correct": 2,
   "feedback": "El PME conserva el signo. MAD y MSE miran magnitud, no dirección."},
 "Planificación": {"type": "pregunta", "k": "A ver…", "qid": "sq-mps", "title": "¿Qué es el MPS?",
   "options": ["El cálculo de partes y materias primas", "Cuántos productos finales se fabrican y cuándo", "El control del taller"], "correct": 1,
   "feedback": "MPS = Master Production Schedule, plan maestro de producción. El cálculo de partes es el MRP; el control del taller, el PAC (SFC)."},
 "Inventarios y logística": {"type": "pregunta", "k": "A ver…", "qid": "sq-drp", "title": "¿Qué es el DRP?",
   "options": ["Un MRP de productos finales para centros de distribución", "El stock de seguridad", "El lote económico de compra"], "correct": 0,
   "feedback": "DRP = Distribution Requirements Planning: muy similar al MRP, pero referido sólo a productos finales."},
 "Proceso": {"type": "pregunta", "k": "A ver…", "qid": "sq-jit", "title": "JIT significa…",
   "options": ["Un tipo de MRP", "Justo a tiempo: producir lo que se necesita cuando se necesita", "Un software ERP"], "correct": 1,
   "feedback": "Así lo traen el Resumen V6 y las Preguntas frecuentes. El final 2018 preguntó cuándo una empresa JIT necesita MRP."},
}

def main():
    d = json.loads(P.read_text(encoding="utf-8"))
    H = [{"type": "concepto", "k": "Siglas", "title": "Una sigla por tarjeta.",
          "text": "Sigla, qué significa en inglés, cómo se traduce y una línea. Agrupadas por unidad. Las expansiones con * no están en el material."}]
    prev = None
    for g, u, s, en, es, df, star in S:
        if prev and g != prev and prev in QUIZ: H.append(QUIZ[prev])
        prev = g
        H.append({"type": "sigla", "k": f"{u} · {g}", "sigla": s, "en": en + (" *" if star else ""),
                  "es": es, "text": df})
    if prev in QUIZ: H.append(QUIZ[prev])
    H.append({"type": "cierre", "title": "Llevate el vocabulario.",
              "text": "MPS dice qué y cuándo; MRP calcula las partes; CRP mide la capacidad; PAC controla el taller; DRP lleva el MRP a la distribución; ERP integra todo. MAD, MSE, MAPE y PME miden el error. MCP e IBM-13 siguen en duda. Sigue la Clase 1: la base estadística."})
    d["historias"] = H

    rows = [[s, en + (" *" if star else ""), es, df, u] for g, u, s, en, es, df, star in S]
    table = {"type": "table", "id": "tabla-rapida",
             "headers": ["Sigla", "Significado", "Traducción", "Definición corta", "Unidad"], "rows": rows,
             "caption": "Tabla rápida. Definiciones resumidas del glosario de abajo, que cita la fuente de cada una. "
                        + STAR + " La columna Unidad ubica la sigla según el programa y el mapa v2; cuando el material no la ubica, es una lectura propia."}
    head = {"type": "heading", "id": "tabla-rapida-h", "level": 2, "text": "Tabla rápida: una línea por sigla"}
    T = [b for b in d["teoria"] if b.get("id") not in ("tabla-rapida", "tabla-rapida-h")]
    T[1:1] = [head, table]   # después de la idea central
    d["teoria"] = T
    P.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    nq = sum(1 for h in H if h["type"] == "pregunta")
    print(f"{len(S)} siglas · {nq} preguntas · {len(H)} tarjetas")

if __name__ == "__main__":
    main()
