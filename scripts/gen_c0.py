#!/usr/bin/env python3
"""Genera Clase 0 (mapa) y Clase 0.1 (siglas) y actualiza index.json + gen_clases.py."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "content"
U2 = ROOT / "u2"


def dump(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}  teoria={len(data['teoria'])} historias={len(data['historias'])}")


c0 = {
    "unitId": "u2",
    "unitLabel": "Unidad 2",
    "unitTitle": "Métodos de pronósticos",
    "id": "c0",
    "title": "Clase 0 · Mapa de la materia",
    "name": "Mapa",
    "lede": "La materia es la anatomía de un ERP: de la empresa como sistema (U1) al software que la gestiona (U7). Esta clase arma el mapa oficial, cómo se conectan las 7 unidades y qué se toma en el final, con las frecuencias reales de los exámenes fechados.",
    "visto": True,
    "source": [
        "clases_previas/SG/MapaMateria_SistemasDeGestion_v2.svg",
        "clases_previas/SG/MapaMateria_SistemasDeGestion.svg",
        "clases_previas/SG/SistemasDeGestion_DocumentoMaestro_v2.txt",
        "programa.md (SG1Progr2008.doc)",
        "patrones_examenes.md",
        "clases_previas/conversacion_previa_notas.md",
        "INDEX.md",
        "aportes_emiliano/examen_2018_transcripcion.md",
    ],
    "laminas": [
        "u2/img/MapaMateria_SistemasDeGestion_v2.svg",
        "u2/img/MapaMateria_SistemasDeGestion.svg",
    ],
    "next": "Clase 0.1 · Siglas",
    "teoria": [
        {
            "type": "callout",
            "kind": "idea",
            "text": "**Idea central (mapa v2):** «la materia es la anatomía de un ERP — de la empresa como sistema (U1) al software que la gestiona (U7)». Las cuatro unidades del medio (pronósticos, producto, proceso y logística) son los insumos; la U6 es el motor donde se juntan; la U7 empaqueta todo en software.",
        },
        {
            "type": "heading",
            "level": 2,
            "text": "1. De dónde sale esta clase",
        },
        {
            "type": "paragraph",
            "text": "No hay un apunte titulado «Clase 0». En la cursada se dictó el mapa general (notas de la conversación previa: serie 0 → 0.1 → 1). Lo que sigue se arma con el mapa v2, el **programa oficial 2008** (`SG1Progr2008.doc`), el Documento Maestro v2 y el mapa de frecuencias de exámenes. Si algo no está en esas fuentes, se marca.",
        },
        {
            "type": "callout",
            "kind": "examen",
            "text": "**Programa vigente en el material:** Sistemas de Gestión 1, UTN FRRo, 2008. No aparece un programa posterior. Estudiar con esa estructura importa: uno de los criterios de evaluación es «el establecimiento de relaciones lógicas y jerárquicas entre los contenidos».",
        },
        {
            "type": "heading",
            "level": 2,
            "text": "2. El mapa oficial (versión 2)",
        },
        {
            "type": "svg",
            "file": "u2/img/MapaMateria_SistemasDeGestion_v2.svg",
            "caption": "Mapa de la materia, versión 2, alineado a las 7 unidades del programa oficial",
        },
        {
            "type": "heading",
            "level": 2,
            "text": "3. Las 7 unidades del programa",
        },
        {
            "type": "paragraph",
            "text": "Títulos (eje conceptual) y objetivos, textuales del programa 2008:",
        },
        {
            "type": "table",
            "headers": ["Unidad", "Eje conceptual", "Objetivo (síntesis del programa)"],
            "rows": [
                ["U1", "La Empresa como productora de Bienes (y Servicios)", "Conocimiento general de las empresas bajo un enfoque sistémico y desde la administración de la producción."],
                ["U2", "Los Métodos de Pronósticos", "Métodos y técnicas de pronósticos más utilizados y su aplicación en la gestión industrial."],
                ["U3", "El Producto", "El concepto de producto y las estructuras de información con que se definen y producen."],
                ["U4", "El Proceso de Producción", "El concepto de Sistema de Producción y el sistema de información que lo mantiene activo."],
                ["U5", "Logística", "Logística integral e interna, y el modelo de gestión de inventarios adecuado a cada proceso."],
                ["U6", "El Sistema de Planificación y Control de la Producción", "Determinar las operaciones básicas de un sistema de gestión, planificación y control de los procesos de conversión."],
                ["U7", "Softwares ERP", "Conocer la oferta de paquetes pre-programados parametrizables para la gestión integral de los recursos en empresas industriales (ERP)."],
            ],
        },
        {
            "type": "heading",
            "level": 2,
            "text": "4. Cómo se conectan",
        },
        {
            "type": "paragraph",
            "text": "El mapa v2 lo plantea así. La **U1** es el marco: la empresa como sistema, el proceso de conversión (insumos → transformación → productos) y el modelo ERP como integrador. Antes de planificar hace falta saber cuatro cosas:",
        },
        {
            "type": "list",
            "ordered": False,
            "items": [
                "**U2 · Pronósticos:** ¿cuánto van a comprar? Demanda y método justificado.",
                "**U3 · El producto:** ¿qué fabricamos y cómo se representa en el sistema? Ciclo de vida, codificación, BOM.",
                "**U4 · El proceso:** ¿cómo se produce físicamente? Centros de trabajo, hombre-máquina, JIT, TOC.",
                "**U5 · Logística:** ¿cuánto material tener y cómo abastecerse? EOQ, stock de seguridad, ABC.",
            ],
        },
        {
            "type": "paragraph",
            "text": "Esos cuatro insumos entran a la **U6**, «el motor donde se juntan». La cadena operativa del mapa es: **plan agregado → MPS → capacidad → MRP → control de piso**. El mapa lo resume en una frase: «La U6 consume: la demanda de U2, el BOM de U3, la capacidad y métodos de U4, y los modelos de stock de U5.»",
        },
        {
            "type": "paragraph",
            "text": "La **U7** es el zoom out final: historia MRP → MRP II → ERP. «Todo lo anterior, empaquetado en software: por eso esta materia es “la anatomía de un ERP”.»",
        },
        {
            "type": "heading",
            "level": 2,
            "text": "5. Qué se calcula y qué se explica",
        },
        {
            "type": "paragraph",
            "text": "El mapa distingue dos marcas, que coinciden con la operatoria del final (notas de cursada y foto 2018):",
        },
        {
            "type": "list",
            "ordered": False,
            "items": [
                "**[P] se calcula** → práctica (eliminatoria, primero).",
                "**[T] se explica** → teoría + coloquio globalizador.",
            ],
        },
        {
            "type": "paragraph",
            "text": "El examen fotografiado de 2018 tenía 1 ejercicio de práctica (40 min, un MPS a partir de ventas confirmadas frente a un pronóstico SES) y 5 preguntas de teoría (30 min).",
        },
        {
            "type": "paragraph",
            "text": "Criterios de evaluación, textuales del programa (van impresos en el encabezado de cada examen):",
        },
        {
            "type": "list",
            "ordered": False,
            "items": [
                "La claridad conceptual al responder las consignas.",
                "El establecimiento de relaciones lógicas y jerárquicas entre los contenidos estudiados.",
                "La utilización de un vocabulario específico.",
                "La interpretación de los resultados obtenidos en la ejercitación.",
                "La fundamentación de las respuestas dadas.",
            ],
        },
        {
            "type": "callout",
            "kind": "examen",
            "text": "**Traducción práctica (Documento Maestro):** nunca entregar solo el número. Cada ejercicio se cierra con interpretación y justificación del método, usando el vocabulario de la cátedra.",
        },
        {
            "type": "heading",
            "level": 2,
            "text": "6. Qué se toma en la práctica (conteo real)",
        },
        {
            "type": "paragraph",
            "text": "Las frecuencias de abajo salen de `patrones_examenes.md`, no de una estimación. Criterio: **una mesa cuenta 1 vez por tema** si ese tema apareció en la práctica con atribución segura. Denominador: **19 finales/exámenes con fecha, 2002–2018**. No se incluyen los sin fecha. También se informan los **7 finales fechados 2011–2018**, más cercanos al formato actual (en general 1 ejercicio de práctica + 3 a 5 preguntas de teoría).",
        },
        {
            "type": "table",
            "headers": ["Tema de práctica", "2002–2018 (n=19)", "%", "2011–2018 (n=7)", "%"],
            "rows": [
                ["MRP", "8", "42%", "2", "29%"],
                ["Pronósticos (series de tiempo)", "6", "32%", "2", "29%"],
                ["Inventarios (EOQ, descuentos, SS, ABC)", "5", "26%", "0", "0%"],
                ["Balanceo", "4", "21%", "1", "14%"],
                ["Plan agregado", "2", "11%", "0", "0%"],
                ["Hombre-máquina", "2", "11%", "1", "14%"],
                ["Otros (estructura / scrap, sin MRP completo)", "2", "11%", "0", "0%"],
                ["MPS", "1", "5%", "1", "14%"],
                ["Capacidad / CRP", "1", "5%", "0", "0%"],
                ["Regresión", "0", "0%", "0", "0%"],
                ["Dígito verificador", "0", "0%", "0", "0%"],
            ],
        },
        {
            "type": "paragraph",
            "text": "Límites de la muestra, también del mismo documento: no hay finales 2016–2017 ni 2019–2026; la muestra reciente es chica (7 mesas); la compilación 2002–2006 a veces mezcla hojas, y se fue conservador. Los porcentajes de 2011–2018 hay que tomarlos con ese límite. **Regresión no aparece en la práctica de ningún final fechado**, pese a tener guía y apunte. El dígito verificador no se tomó como ejercicio de práctica; sí en teoría (2011, 2013, 2018).",
        },
        {
            "type": "callout",
            "kind": "examen",
            "text": "**Tema huérfano:** las notas de cursada dicen que el MRP no se dio en la práctica de la cursada, pero **sí se tomó** en finales (2013, 2015 y, con fuerza, 2002–2006). En el conteo 2002–2018 es el tema de práctica más frecuente (42%).",
        },
        {
            "type": "paragraph",
            "text": "Ojo con el mapa v2: ahí U2 y U6 aparecen como «½ de la práctica» cada una. Eso es un esquema del mapa, no el conteo de mesas. Para estudiar el peso de cada tema, usá la tabla de arriba.",
        },
        {
            "type": "heading",
            "level": 2,
            "text": "7. Qué se toma en la teoría (2011–2018)",
        },
        {
            "type": "paragraph",
            "text": "Conteo de aparición en teoría sobre los **7 finales fechados 2011–2018** (una mesa, un punto, aunque haya más de una pregunta del tema):",
        },
        {
            "type": "table",
            "headers": ["Tema de teoría", "Mesas / 7", "Preguntas típicas (según patrones)"],
            "rows": [
                ["Codificación (saturación, DV, ventajas, potencialidad)", "6", "Incluye dígito verificador IBM-11 (2018: 987-95617-03-01) e IBM13 en el recuerdo de 2011"],
                ["Capacidad (estación, sistema, listas/perfiles)", "5", "En 2018: hipótesis de listas de capacidad y perfiles de recursos"],
                ["Pronósticos (función, para qué, hipótesis, SES)", "5", "Incluye explicar nivelación o suavización exponencial"],
                ["Ciclo de vida del producto", "3", "Función, variables, o graficar (lámpara incandescente, 2013)"],
                ["Estructura de producto / BOM / hoja de ruta", "3", "Incluye BOM en un ERP (2014)"],
                ["MRP / MCP / ERP / JIT", "3", "2012: qué es MRP, MCP, ERP; 2018: cuándo JIT necesita MRP y relación ERP–BI"],
                ["BI / decisiones racionales", "1", "Solo 2018. Están fuera del programa 2008, pero cayeron"],
            ],
        },
        {
            "type": "paragraph",
            "text": "El mapa v2 anota esos complementos con la misma salvedad: «fuera del programa 2008, pero preguntados en el examen 2018» (BI / Data Warehouse y métodos de decisión racional, a nivel conceptual).",
        },
        {
            "type": "heading",
            "level": 2,
            "text": "8. Una versión anterior del mapa",
        },
        {
            "type": "paragraph",
            "text": "Antes de alinear el mapa a las 7 unidades oficiales, había una versión de 18 temas en 4 capas (PREDECIR / PLANIFICAR / EJECUTAR / SISTEMAS). Los temas 1–11 eran práctica y los 12–18 teoría. Se conserva como referencia; el mapa que usamos para estudiar es el v2.",
        },
        {
            "type": "svg",
            "file": "u2/img/MapaMateria_SistemasDeGestion.svg",
            "caption": "Mapa de la materia, versión anterior (18 temas / 4 capas)",
        },
        {
            "type": "heading",
            "level": 2,
            "text": "9. Bibliografía que cita el material",
        },
        {
            "type": "list",
            "ordered": False,
            "items": [
                "Programa oficial: Chase (10.ª ed.), Monks, APICS y apuntes de Sessa.",
                "Práctica de pronósticos (Documento Maestro / notas): Hanke, capítulos 2 a 6, más el apunte de regresión.",
                "APICS aparece citado como American Production & Inventory Control Society, referencia de vocabulario (Documento Maestro).",
            ],
        },
        {
            "type": "heading",
            "level": 2,
            "text": "10. Qué sigue",
        },
        {
            "type": "paragraph",
            "text": "La Clase 0.1 junta las **siglas** con el significado tal como está en los apuntes (y marca las que aparecen sin expansión). Después entra la Clase 1: la base estadística, que ya está cargada.",
        },
        {
            "type": "callout",
            "kind": "idea",
            "text": "**Para llevarte:** 7 unidades, 4 insumos, una cadena en la U6, práctica primero (eliminatoria) y teoría después. El peso de cada tema se lee en el conteo de finales, no en un 50 y 50.",
        },
    ],
    "historias": [
        {
            "type": "concepto",
            "k": "La idea",
            "title": "La materia es la anatomía de un ERP.",
            "text": "Así lo dice el mapa v2: de la empresa como sistema (U1) al software que la gestiona (U7). En el medio están los insumos y el motor que los junta.",
        },
        {
            "type": "concepto",
            "k": "El programa",
            "title": "Son 7 unidades, las del programa 2008.",
            "text": "U1 la empresa, U2 pronósticos, U3 el producto, U4 el proceso, U5 logística, U6 planificación y control, U7 softwares ERP. En el material no hay un programa más nuevo.",
        },
        {
            "type": "concepto",
            "k": "La conexión",
            "title": "Cuatro insumos entran al motor.",
            "text": "U2 te dice la demanda, U3 el BOM, U4 la capacidad y los métodos, U5 los modelos de stock. La U6 los consume y arma: plan agregado → MPS → capacidad → MRP → control de piso.",
        },
        {
            "type": "pregunta",
            "k": "A ver…",
            "title": "Según el mapa v2, ¿qué le entra a la U6?",
            "options": [
                "Solo el pronóstico de la U2",
                "La demanda de U2, el BOM de U3, la capacidad de U4 y el stock de U5",
                "Solo el software de la U7",
            ],
            "correct": 1,
            "feedback": "El mapa lo dice así: «La U6 consume: la demanda de U2, el BOM de U3, la capacidad y métodos de U4, y los modelos de stock de U5.»",
        },
        {
            "type": "concepto",
            "k": "El final",
            "title": "Primero se calcula. Después se explica.",
            "text": "[P] es práctica, eliminatoria y va primero. [T] es teoría. En el examen de 2018: 40 minutos de práctica (un MPS) y 30 minutos de teoría (5 preguntas).",
        },
        {
            "type": "concepto",
            "k": "Cómo te evalúan",
            "title": "No alcanza con el número.",
            "text": "El programa pide claridad conceptual, relaciones entre contenidos, vocabulario específico, interpretación y fundamentación. Esas cinco líneas van impresas en el encabezado del examen.",
        },
        {
            "type": "pregunta",
            "k": "A ver…",
            "title": "Si no aprobás la práctica del final…",
            "options": [
                "Pasás igual a la teoría",
                "Quedás libre",
                "No pasás a la teoría: es eliminatoria",
            ],
            "correct": 2,
            "feedback": "Según las notas de cursada y el Documento Maestro, se rinde primero la práctica y es eliminatoria. Recién después va la teoría.",
        },
        {
            "type": "concepto",
            "k": "La práctica",
            "title": "El peso se cuenta, no se estima.",
            "text": "En 19 finales fechados (2002–2018), una mesa cuenta una vez por tema: MRP 42%, pronósticos 32%, inventarios 26%, balanceo 21%. Plan agregado y hombre-máquina, 11%. MPS y capacidad, 5%.",
        },
        {
            "type": "concepto",
            "k": "Con cuidado",
            "title": "No uses un «50 y 50».",
            "text": "El mapa v2 dibuja U2 y U6 como media práctica cada una; el conteo de mesas no dice eso. Faltan finales 2016–17 y 2019–26, y la muestra 2011–2018 es de solo 7 mesas.",
        },
        {
            "type": "pregunta",
            "k": "A ver…",
            "title": "En esos 19 finales, el tema de práctica más frecuente fue…",
            "options": [
                "Pronósticos",
                "MRP",
                "Inventarios (EOQ)",
            ],
            "correct": 1,
            "feedback": "MRP aparece en 8 de 19 mesas (42%). Importante: en la cursada práctica no se llegó a dar, pero sí cae en el final.",
        },
        {
            "type": "concepto",
            "k": "La teoría",
            "title": "En 7 finales (2011–2018), lo que más sale.",
            "text": "Codificación en 6 de 7, capacidad y pronósticos en 5 de 7. BI y decisiones racionales aparecieron solo en 2018, y están fuera del programa 2008.",
        },
        {
            "type": "concepto",
            "k": "Bibliografía",
            "title": "Lo que cita el material.",
            "text": "Chase, Monks, APICS y los apuntes de Sessa. La práctica de pronósticos se apoya en Hanke (capítulos 2 a 6) y en el apunte de regresión.",
        },
        {
            "type": "cierre",
            "title": "Llevate el mapa.",
            "text": "Siete unidades. Cuatro insumos que alimentan la U6. Práctica primero (eliminatoria), teoría después. El peso de cada tema sale del conteo de finales. Sigue la Clase 0.1: las siglas, con el significado tal como está en los apuntes.",
        },
    ],
}

# --- Clase 0.1 ---
c01 = {
    "unitId": "u2",
    "unitLabel": "Unidad 2",
    "unitTitle": "Métodos de pronósticos",
    "id": "c01",
    "title": "Clase 0.1 · Siglas",
    "name": "Siglas",
    "lede": "El criterio de evaluación pide vocabulario específico. Esta clase junta las siglas del programa, el mapa, los apuntes y los exámenes, con el significado tal como aparece en el material. Si una sigla se usa pero no se desarrolla, va al final: no se inventa.",
    "visto": True,
    "source": [
        "texto/resumenes/Resumen_Sistema_de_Gestion_7p.txt",
        "texto/resumenes/ResumenSG-Final-V6_345p.txt",
        "texto/resumenes/Resumen_Hanke_25p.txt",
        "texto/Preguntas_Frecuentes.txt",
        "clases_previas/SG/SistemasDeGestion_DocumentoMaestro_v2.txt",
        "clases_previas/SG/Clase04_MedidasDeError.md",
        "clases_previas/SG/Clase03b_Autocorrelacion.md",
        "clases_previas/SG/Clase02_Correlacion.md",
        "programa.md (SG1Progr2008.doc)",
        "patrones_examenes.md",
        "clases_previas/SG/MapaMateria_SistemasDeGestion_v2.svg",
        "clases_previas/conversacion_previa_notas.md",
        "aportes_emiliano/examen_2018_transcripcion.md",
    ],
    "laminas": [
        "u2/img/MapaMateria_SistemasDeGestion_v2.svg",
    ],
    "next": "Clase 1 · Base estadística",
    "teoria": [
        {
            "type": "callout",
            "kind": "idea",
            "text": "**Idea central:** no memorices una lista suelta. Las siglas son el vocabulario de la cadena de planificación (plan agregado → MPS → capacidad → MRP → control de piso → ERP) y de los insumos que la alimentan. El programa pide «la utilización de un vocabulario específico».",
        },
        {
            "type": "heading",
            "level": 2,
            "text": "1. De dónde sale esta clase",
        },
        {
            "type": "paragraph",
            "text": "No hay un apunte titulado «Clase 0.1 · Siglas». En la cursada se dictó (notas de la conversación previa). El glosario se reconstruyó con el Resumen de 7 páginas, el Resumen SG Final V6 (Chase), el resumen de Hanke, Preguntas frecuentes, el Documento Maestro v2, el programa 2008, el mapa v2, los apuntes de las Clases 2 a 4 y la transcripción del final 2018. Cada significado lleva la fuente. **No se completa una sigla “de memoria general”.**",
        },
        {
            "type": "heading",
            "level": 2,
            "text": "2. La cadena corta",
        },
        {
            "type": "paragraph",
            "text": "El Resumen de 7 páginas dice que el sistema de **Planificación de los Requerimientos de Materiales (MRP: Material Requirements Planning)** obtiene las necesidades de cada una de las partes, en cada período, para cumplir con las cantidades de los productos finales fijadas en el **Plan Maestro de Producción (MPS)**. El MRP gestiona existencias de **demanda dependiente**: las necesidades se calculan a partir del MPS.",
        },
        {
            "type": "paragraph",
            "text": "En el Resumen V6, «el programa maestro de producción (MPS) es el plan con los tiempos desglosados que especifica cuántas piezas finales va a fabricar la empresa y cuándo».",
        },
        {
            "type": "paragraph",
            "text": "El mismo V6 presenta **MRP II** como **planeación de recursos de manufactura**: una expansión del MRP para planear y monitorear más áreas de la empresa. El programa oficial habla de «Sistemas MRPII (CRP)». El Documento Maestro anota: «MRP II (CRP — planificación de requerimientos de capacidad)» y la pregunta textual «MRP vs. MRP II/MCP vs. ERP». **MCP aparece en esa pregunta; el material leído no desarrolla la sigla** (queda en la sección 8).",
        },
        {
            "type": "paragraph",
            "text": "**ERP**, en el objetivo de la U7 del programa: «paquetes pre-programados parametrizables existentes en el mercado para la gestión integral de los recursos en empresas industriales (ERP)». El V6 habla de «sistemas de planeación de recursos empresariales». El mapa resume la historia: **MRP → MRP II → ERP**. SAP aparece como «caso típico» de sistema comercial, no como una sigla a expandir.",
        },
        {
            "type": "svg",
            "file": "u2/img/MapaMateria_SistemasDeGestion_v2.svg",
            "caption": "Mapa v2: la cadena vive en la U6 y se empaqueta en la U7",
        },
        {
            "type": "heading",
            "level": 2,
            "text": "3. Glosario: planificación y producto",
        },
        {
            "type": "glosario",
            "title": "Planificación, materiales y producto",
            "intro": "Significado según el material. Entre paréntesis, la fuente.",
            "entries": [
                {"simbolo": "MRP", "nombre": "Material Requirements Planning", "significado": "Planificación de los Requerimientos de Materiales. Calcula las necesidades de conjuntos, piezas y materias primas por período para cumplir el MPS. Es gestión de existencias de demanda dependiente. (Resumen 7 p.)"},
                {"simbolo": "MPS", "nombre": "Plan Maestro de Producción / programa maestro", "significado": "Programa o plan maestro de producción: el plan con los tiempos desglosados que especifica cuántas piezas finales va a fabricar la empresa y cuándo. (V6; Resumen 7 p.; examen 2018)"},
                {"simbolo": "MRP II", "nombre": "planeación de recursos de manufactura", "significado": "Planeación de recursos de manufactura: expansión del MRP para planear y monitorear más recursos de la empresa. (V6). El programa lo menciona junto a CRP."},
                {"simbolo": "CRP", "nombre": "planificación de requerimientos de capacidad", "significado": "Así lo anota el Documento Maestro al lado de MRP II. El programa habla de «Sistemas MRPII (CRP)». En la práctica de finales fechados aparece poco (1 de 19); en 2011–2018 sale más en teoría."},
                {"simbolo": "ERP", "nombre": "planeación / gestión integral de recursos empresariales", "significado": "En el programa U7: gestión integral de los recursos en empresas industriales, mediante paquetes pre-programados parametrizables. En el V6: planeación de recursos empresariales. Historia del mapa: MRP → MRP II → ERP."},
                {"simbolo": "BOM", "nombre": "lista de materiales / estructura de producto", "significado": "El programa (U3) dice «Estructura de producto. BOM. Explosión sumarizada y por niveles». Preguntas frecuentes pregunta: «¿En ERP qué información tiene la BOM (lista de materiales)?». El V6 describe el archivo con la lista de materiales que especifica qué se usa para hacer cada pieza."},
                {"simbolo": "PAC", "nombre": "(sigla no expandida en el material leído)", "significado": "Sí hay función: «el objetivo del PAC es realizar el lanzamiento, la programación y el control del progreso de las órdenes de producción» (Preguntas frecuentes). Hay un apunte PAC.pdf, no extraído en este pase. No se inventa una forma inglesa."},
            ],
        },
        {
            "type": "heading",
            "level": 2,
            "text": "4. Glosario: inventarios y loteo",
        },
        {
            "type": "glosario",
            "title": "Inventarios y loteo",
            "intro": None,
            "entries": [
                {"simbolo": "EOQ", "nombre": "Economic Order Quantity", "significado": "Lote económico clásico / cantidad de pedido económico. Se usa cuando la demanda período a período es poco variable. (Resumen 7 p.; V6)"},
                {"simbolo": "LEC", "nombre": "(aparece junto a EOQ)", "significado": "En el Documento Maestro y el mapa: «EOQ/LEC» y «loteo LEC/EOQ». Se usa como par del lote económico. El material leído no desarrolla LEC letra por letra."},
                {"simbolo": "TBO", "nombre": "Time Between Orders", "significado": "Tiempo entre órdenes, expresado en períodos de planificación. (Resumen 7 p.)"},
                {"simbolo": "POQ", "nombre": "Periodic Order Quantity", "significado": "Cantidad periódica de producción: modelo de período fijo y cantidad variable, que usa la fórmula del EOQ para hallar el TBO y luego las cantidades a ordenar. (Resumen 7 p.)"},
                {"simbolo": "PPB", "nombre": "Part Period Balancing", "significado": "Balance cantidad-período: agrupa los requerimientos del MRP para minimizar el costo unitario total de producción y mantenimiento en stock. (Resumen 7 p.)"},
                {"simbolo": "ABC", "nombre": "análisis / clasificación ABC", "significado": "Método para analizar el inventario con base en el valor; el V6 lo presenta como aplicación del análisis de Pareto al inventario. El programa y el mapa lo ubican en logística."},
                {"simbolo": "SS", "nombre": "stock de seguridad", "significado": "Así lo usa el mapa de frecuencias («EOQ + SS»). En el programa y el mapa de la materia el tema se nombra «stock de seguridad»."},
                {"simbolo": "OP / OC", "nombre": "orden de producción / orden de compra", "significado": "En el Resumen 7 p., un ingreso programado significa que existe una OP o una OC, y que las materias primas y piezas ya están comprometidas con esa orden."},
            ],
        },
        {
            "type": "heading",
            "level": 2,
            "text": "5. Glosario: pronósticos",
        },
        {
            "type": "glosario",
            "title": "Pronósticos y error",
            "intro": "Nombres según Hanke y la Clase 4 (Medidas de error).",
            "entries": [
                {"simbolo": "SES", "nombre": "nivelación / suavización exponencial simple", "significado": "Así aparece en finales (p. ej. 2018: el MPS parte de un pronóstico por «Nivelación Exponencial Simple») y en las clases de pronósticos."},
                {"simbolo": "MAD", "nombre": "desviación absoluta media (o de la media)", "significado": "Mide el error de pronóstico en unidades, con valor absoluto. Hanke: Desviación Absoluta de la Media. Clase 4: desviación / error absoluto medio."},
                {"simbolo": "MSE", "nombre": "error cuadrático medio", "significado": "Promedio de los errores al cuadrado; castiga más los errores grandes. Se usa para elegir parámetros. (Hanke; Clase 4). El V6 también nombra RMSE como √MSE."},
                {"simbolo": "MAPE", "nombre": "porcentaje de error medio absoluto", "significado": "El error en porcentaje; permite comparar series de distinta escala. (Hanke; Clase 4)"},
                {"simbolo": "PME", "nombre": "porcentaje medio de error", "significado": "Conserva el signo, por eso muestra el sesgo. Un PME alto y consistente delata un patrón no capturado. (Clase 4)"},
                {"simbolo": "FAC / ACF", "nombre": "función de autocorrelación", "significado": "El correlograma de la Clase 3.b; sirve para probar el patrón de la serie (tendencia, estacionalidad, etc.)."},
                {"simbolo": "r / R²", "nombre": "correlación / coeficiente de determinación", "significado": "Clase 2: r mide si dos variables se mueven juntas (signo = dirección, valor absoluto = fuerza). r² es el porcentaje de variación explicada."},
            ],
        },
        {
            "type": "heading",
            "level": 2,
            "text": "6. Glosario: proceso de producción",
        },
        {
            "type": "glosario",
            "title": "Proceso (U4 del programa)",
            "intro": "El programa nombra SMED, TQM, Kanban, JIT, producción sincronizada y Teoría de las restricciones. Las expansiones de abajo están en el V6 o en el Documento Maestro.",
            "entries": [
                {"simbolo": "JIT", "nombre": "justo a tiempo", "significado": "En Preguntas frecuentes y en el mapa: JIT (justo a tiempo). El V6: «Justo a tiempo significa producir lo que se necesita cuando se necesita». El final 2018 preguntó cuándo una empresa JIT necesita MRP."},
                {"simbolo": "Kanban", "nombre": "«signo» o «tarjeta de instrucción»", "significado": "El V6: «Kanban significa “signo” o “tarjeta de instrucción” en japonés». Sistema de señalización para regular los flujos justo a tiempo."},
                {"simbolo": "SMED", "nombre": "single-minute exchange of die", "significado": "Cambio de troqueles en un minuto: procedimientos para bajar los tiempos de preparación de las máquinas. (V6)"},
                {"simbolo": "TQM", "nombre": "administración de (por) la calidad total", "significado": "El V6 usa «administración de la calidad total» y «administración por calidad total». El programa lo lista entre los conceptos básicos de la U4."},
                {"simbolo": "TOC", "nombre": "Teoría de las Restricciones", "significado": "Documento Maestro: «Teoría de las Restricciones (TOC): cuellos de botella, la meta, mejora continua según Goldratt». El programa nombra «Teoría de las restricciones» sin la sigla inglesa."},
            ],
        },
        {
            "type": "heading",
            "level": 2,
            "text": "7. Glosario: información, BI y otras",
        },
        {
            "type": "glosario",
            "title": "Información, calidad de código y referencias",
            "intro": "BI no está en el programa 2008, pero cayó en la teoría de 2018 (relación ERP–BI).",
            "entries": [
                {"simbolo": "BI", "nombre": "Business Intelligence / Inteligencia de Negocios", "significado": "El V6: «La Inteligencia de Negocios (Business Intelligence, BI) es una disciplina que combina consultas, servicios, aplicaciones y tecnologías» para transformar datos en información útil. El Documento Maestro la relaciona con Data Warehouse y con el examen 2018."},
                {"simbolo": "ETL", "nombre": "Extracción, Transformación y Carga", "significado": "Así lo titula el V6. Sirve para poblar el Data Warehouse, moviendo bloques de datos desde los sistemas operacionales."},
                {"simbolo": "DW", "nombre": "Data Warehouse", "significado": "El V6: «un conjunto de datos integrados orientados a una materia, que varían con el tiempo y que no son transitorios, los cuales soportan el proceso de toma de decisiones de una organización»."},
                {"simbolo": "IBM-11", "nombre": "dígito verificador módulo 11", "significado": "Preguntas frecuentes: el dígito verificador es un elemento de control; el módulo 11 aplica pesos 2 a 7. Cayó en teoría (2013, 2018; código 2018: 987-95617-03-01). No es ejercicio de práctica en los finales fechados."},
                {"simbolo": "APICS", "nombre": "American Production & Inventory Control Society", "significado": "Así la cita el Documento Maestro, como referencia de vocabulario de la bibliografía de cátedra."},
            ],
        },
        {
            "type": "heading",
            "level": 2,
            "text": "8. Siglas que aparecen, pero no se expanden en el material leído",
        },
        {
            "type": "paragraph",
            "text": "Estas se vieron o se preguntaron, y **no se les inventa** una forma larga. Cuando aparezca el apunte correspondiente, se completa.",
        },
        {
            "type": "table",
            "headers": ["Sigla", "Dónde aparece", "Qué sí se sabe (sin inventar la expansión)"],
            "rows": [
                ["MCP", "Pregunta textual de final (2012): «Qué es MRP, MCP, ERP». Documento Maestro: «MRP vs. MRP II/MCP vs. ERP».", "Se la agrupa con MRP II frente a MRP y ERP. No hay desarrollo letra por letra en los textos leídos."],
                ["PAC", "Preguntas frecuentes: «Explique las funciones del PAC». Apunte PAC.pdf (aún no extraído).", "Sí está el objetivo (lanzamiento, programación y control del progreso de las órdenes). Falta la expansión de la sigla."],
                ["DRP", "Mapa v1: «DRP (distribución)». Apunte DRP.pdf, no extraído en este pase.", "Solo esa anotación breve («distribución»). No se completa una forma inglesa."],
                ["DSS", "Documento Maestro, junto a BI / Data Warehouse.", "Aparece en el listado de temas de BI, sin definición ni expansión."],
                ["LEC", "Mapa y Documento Maestro: «EOQ/LEC», «loteo LEC/EOQ».", "Se usa como par del lote económico (EOQ). No hay expansión letra por letra."],
                ["IBM-13", "Recuerdo de un alumno en el final 17/03/2011 («calcular dígito verificador IBM13»; anotó «no me acuerdo»).", "No hay procedimiento de IBM-13 en el material leído. El que sí está desarrollado es IBM-11 / módulo 11."],
                ["WIP", "Aparece en un bloque de examen de 2006 («WIP en depósito»), según patrones.", "No hay definición en los textos leídos."],
            ],
        },
        {
            "type": "callout",
            "kind": "examen",
            "text": "**Para el final:** en 2012 preguntaron MRP, MCP y ERP (y MCP es de las que no están desarrolladas acá). En 2018: dígito verificador IBM-11, relación ERP–BI, y cuándo una empresa JIT necesita MRP. Vocabulario específico es criterio de evaluación.",
        },
        {
            "type": "heading",
            "level": 2,
            "text": "9. Qué sigue",
        },
        {
            "type": "paragraph",
            "text": "Con el mapa y las siglas en su lugar, entra la **Clase 1 · Base estadística** (ya cargada): media, dispersión, n − 1, la campana, Z y t, hasta el stock de seguridad.",
        },
    ],
    "historias": [
        {
            "type": "concepto",
            "k": "Para qué",
            "title": "El examen pide vocabulario específico.",
            "text": "Esta clase no inventa significados. Si una sigla aparece en un final o en un apunte y no se desarrolla, se deja marcada. El resto sale de los textos que ya tenemos.",
        },
        {
            "type": "concepto",
            "k": "La cadena",
            "title": "MPS dice el qué y el cuándo. MRP explota las partes.",
            "text": "MPS: plan maestro, cuántas piezas finales y cuándo (V6). MRP: planificación de los requerimientos de materiales. Parte del MPS y calcula, período a período, conjuntos, piezas y materias primas (Resumen 7 p.). Es demanda dependiente.",
        },
        {
            "type": "concepto",
            "k": "La historia",
            "title": "MRP se agranda y termina en ERP.",
            "text": "MRP II, en el V6, es planeación de recursos de manufactura. El programa habla de sistemas MRPII (CRP); el Documento Maestro anota CRP como planificación de requerimientos de capacidad. ERP, en el programa, es la gestión integral de los recursos en empresas industriales.",
        },
        {
            "type": "pregunta",
            "k": "A ver…",
            "title": "El MRP calcula las necesidades de partes a partir de…",
            "options": [
                "Un pronóstico suelto de cada tornillo",
                "Las cantidades de productos finales fijadas en el MPS",
                "El stock de seguridad de la U5",
            ],
            "correct": 1,
            "feedback": "El Resumen de 7 páginas lo dice: el MRP obtiene las necesidades de cada parte para cumplir el Plan Maestro de Producción. Por eso es demanda dependiente.",
        },
        {
            "type": "concepto",
            "k": "El producto y el lote",
            "title": "BOM es la lista. EOQ es el lote económico.",
            "text": "BOM: lista de materiales / estructura de producto (programa y Preguntas frecuentes). EOQ: Economic Order Quantity, lote económico clásico (7 p. y V6). Junto a él aparecen TBO (tiempo entre órdenes), POQ (cantidad periódica) y PPB (balance cantidad-período).",
        },
        {
            "type": "concepto",
            "k": "El proceso",
            "title": "JIT, Kanban, SMED, TQM, TOC.",
            "text": "JIT es justo a tiempo: producir lo que se necesita cuando se necesita (V6). Kanban es «signo» o «tarjeta de instrucción» en japonés. SMED: cambio de troqueles en un minuto. TQM: administración de la calidad total. TOC: Teoría de las Restricciones (Documento Maestro).",
        },
        {
            "type": "pregunta",
            "k": "A ver…",
            "title": "JIT significa…",
            "options": [
                "Justo a tiempo: producir lo que se necesita cuando se necesita",
                "Un tipo de MRP",
                "Un software ERP",
            ],
            "correct": 0,
            "feedback": "Así lo traen el Resumen V6 y las Preguntas frecuentes. El final 2018, además, preguntó cuándo una empresa JIT necesita MRP.",
        },
        {
            "type": "concepto",
            "k": "Los errores",
            "title": "Cuatro siglas para medir el pronóstico.",
            "text": "MAD: desviación absoluta media (en unidades). MSE: error cuadrático medio (castiga los grandes). MAPE: porcentaje de error medio absoluto (para comparar series). PME: porcentaje medio de error, el que muestra el sesgo. (Hanke y Clase 4)",
        },
        {
            "type": "concepto",
            "k": "Inventarios",
            "title": "ABC por valor. SS, el stock de seguridad.",
            "text": "ABC es el análisis del inventario con base en el valor (V6). SS, en el mapa de exámenes, es stock de seguridad. LEC aparece junto a EOQ como loteo, pero el material leído no la desarrolla letra por letra.",
        },
        {
            "type": "pregunta",
            "k": "A ver…",
            "title": "¿Cuál de estas medidas sirve para ver si el método tiene sesgo?",
            "options": [
                "MAD",
                "MSE",
                "PME",
            ],
            "correct": 2,
            "feedback": "El PME conserva el signo y por eso muestra el sesgo. MAD y MSE miran magnitud, no dirección.",
        },
        {
            "type": "concepto",
            "k": "Información",
            "title": "BI, ETL y el dígito verificador.",
            "text": "BI: Inteligencia de Negocios / Business Intelligence (V6). ETL: Extracción, Transformación y Carga, para poblar el Data Warehouse. IBM-11: dígito verificador módulo 11 (cayó en 2018). APICS: American Production & Inventory Control Society.",
        },
        {
            "type": "concepto",
            "k": "Con honestidad",
            "title": "Hay siglas que aparecen y no se expanden acá.",
            "text": "MCP (cae en «qué es MRP, MCP, ERP»), PAC (sí tiene objetivo: lanzar, programar y controlar las órdenes, pero no la forma larga), DRP (el mapa solo dice «distribución»), DSS (aparece junto a BI). No las inventamos.",
        },
        {
            "type": "cierre",
            "title": "Llevate el vocabulario.",
            "text": "MPS y MRP son el corazón de la cadena; ERP es el software que la integra. JIT, EOQ, BOM, MAD/MSE/MAPE/PME y BI están en los apuntes con nombre y apellido. Si una sigla no está desarrollada, se deja marcada. Sigue la Clase 1: la base estadística.",
        },
    ],
}


def patch_index() -> None:
    path = ROOT / "index.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for unit in data["units"]:
        if unit.get("id") != "u2":
            continue
        unit["lede"] = (
            "Unidad 2 del programa: los métodos de pronósticos. Empieza con el mapa de toda la materia y las siglas (Clases 0 y 0.1), y sigue con las clases que ya vimos: base estadística, correlación, series, autocorrelación, medidas de error y el integrador."
        )
        for cls in unit["classes"]:
            if cls["id"] == "c0":
                cls.update({
                    "title": "Clase 0 · Mapa",
                    "file": "u2/clase00.json",
                    "soon": False,
                    "visto": True,
                    "name": "Mapa",
                })
                cls.pop("nota", None)
            elif cls["id"] == "c01":
                cls.update({
                    "title": "Clase 0.1 · Siglas",
                    "file": "u2/clase01_siglas.json",
                    "soon": False,
                    "visto": True,
                    "name": "Siglas",
                })
                cls.pop("nota", None)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"patched {path.relative_to(ROOT)}")


def patch_gen_clases() -> None:
    path = Path(__file__).resolve().parent / "gen_clases.py"
    text = path.read_text(encoding="utf-8")
    old0 = '{"id": "c0", "title": "Clase 0 · Mapa", "soon": True, "nota": "Dictada, pero no hay un apunte fuente aparte: el mapa está en esta unidad."}'
    new0 = '{"id": "c0", "title": "Clase 0 · Mapa", "file": "u2/clase00.json", "soon": False, "visto": True, "name": "Mapa"}'
    old1 = '{"id": "c01", "title": "Clase 0.1 · Siglas", "soon": True, "nota": "Dictada, pero no hay un archivo fuente de siglas en el material."}'
    new1 = '{"id": "c01", "title": "Clase 0.1 · Siglas", "file": "u2/clase01_siglas.json", "soon": False, "visto": True, "name": "Siglas"}'
    if old0 not in text or old1 not in text:
        raise SystemExit("gen_clases.py: expected c0/c01 literals not found; abort")
    text = text.replace(old0, new0).replace(old1, new1)
    # lede of U2 in the generator, if present
    old_lede = "Unidad 2 del programa: los métodos de pronósticos. Acá están las clases que ya vimos (base estadística, correlación, series, autocorrelación, medidas de error y el integrador). El mapa y el árbol sirven de referencia de toda la unidad."
    new_lede = "Unidad 2 del programa: los métodos de pronósticos. Empieza con el mapa de toda la materia y las siglas (Clases 0 y 0.1), y sigue con las clases que ya vimos: base estadística, correlación, series, autocorrelación, medidas de error y el integrador."
    if old_lede in text:
        text = text.replace(old_lede, new_lede)
    path.write_text(text, encoding="utf-8")
    print("patched gen_clases.py")


def validate(data: dict, nq_min: int = 3) -> None:
    hs = data["historias"]
    assert 10 <= len(hs) <= 14, (data["id"], len(hs))
    types = [h["type"] for h in hs]
    assert types[0] != "pregunta"
    assert types[-1] == "cierre"
    qs = [i for i, t in enumerate(types) if t == "pregunta"]
    assert len(qs) >= nq_min, (data["id"], qs)
    # questions every 3-4 cards: gap from previous content, not necessarily exact, but no two Q adjacent and first Q not too late
    for a, b in zip(qs, qs[1:]):
        gap = b - a
        assert 3 <= gap <= 5, (data["id"], "gap", a, b)
    # first question around card 4 (index 3)
    assert qs[0] in (3, 4), (data["id"], "first Q", qs[0])
    for q in (h for h in hs if h["type"] == "pregunta"):
        assert 0 <= q["correct"] < len(q["options"])
        assert "feedback" in q


if __name__ == "__main__":
    validate(c0)
    validate(c01)
    dump(U2 / "clase00.json", c0)
    dump(U2 / "clase01_siglas.json", c01)
    patch_index()
    patch_gen_clases()
    print("ok")
