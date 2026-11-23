"""PS-12: integra el Resumen de Monks del Drive (U6) y complementos de internet marcados como fuente externa (U5 y U6).

Prioridad: material del Drive. Lo de internet va siempre como «Fuente externa» con la fuente nombrada y su URL.
Se aplica desde gen_u6.py y gen_u5.py, antes de escribir cada clase.
"""
from u5lib import H, P, T, L, IDEA, AVISO, EXAM, F, EJ  # noqa: F401
import copy
import re
from gen_u2_historias import boxes, flow_v

# ---------------------------------------------------------------- fuentes
RM = "drive_u5/Resumen_Monks.docx — resumen de alumnos de Monks, «Administración de operaciones» (material del Drive; no es el libro)"
def RMC(cap): return f"{RM}, cap. {cap}"
VOLL_URL = "http://koha.undef.edu.ar/cgi-bin/koha/opac-detail.pl?biblionumber=23682"
VOLL = ("Fuente externa: Vollmann, Berry y Whybark, «Sistemas de planificación y control de la fabricación» (Irwin, 1994, ISBN 84-8086-195-9), "
        "índice del catálogo de la Biblioteca UNDEF, " + VOLL_URL)
UNICEN_URL = "https://users.exa.unicen.edu.ar/catedras/modemp/12_MRP.pdf"
UNICEN = ("Fuente externa: UNICEN, Fac. de Ciencias Exactas, cátedra «Sistemas de información para administración de operaciones», "
          "«Planificación y Control de la Producción: Planificación Agregada, MPS, MRP-I, MRP-II» (láminas, 2003), " + UNICEN_URL)
TIC_URL = "https://www.ticportal.es/glosario-tic/planificacion-capacidad-maquinas-mcp"
REY1_URL = "https://www.ucv.cl/uuaa/site/docs/20181123/20181123195708/apuntedocentecontroldeinventariosyr.pdf"
REY2_URL = "https://www.ucv.cl/uuaa/site/docs/20181123/20181123195708/apuntedocenteinventariosdedemandaaleatoriayr.pdf"
REY1 = "Fuente externa: Y. Reyes Fernández, «Control de inventarios», Apunte docente, Esc. de Ingeniería Comercial, PUCV (Chile), " + REY1_URL
REY2 = "Fuente externa: Y. Reyes Fernández, «Inventarios de demanda aleatoria», Apunte docente, Esc. de Ingeniería Comercial, PUCV (Chile), " + REY2_URL
HALL = "/workspace/sdg/web_gaps/HALLAZGOS_WEB.md (relevamiento web PS-11, 23/11/2026)"
AO = {
    "monks82": "https://archive.org/details/operationsmanage0002monk",
    "monks87": "https://archive.org/details/operationsmanage0003monk",
    "voll88": "https://archive.org/details/manufacturingpla00voll",
}

def C(k, title, text, **kw):
    d = dict(type='concepto', k=k, title=title, text=text); d.update(kw); return d
def Q(title, options, correct, feedback, k='A ver…'):
    return dict(type='pregunta', k=k, title=title, options=options, correct=correct, feedback=feedback)

MONKS_NOTA = ("**Qué es este material:** el Drive no tiene el libro de Monks, pero sí un **resumen de alumnos** (`Resumen_Monks.docx`). "
              "Lo que sigue sale de ese resumen, con sus palabras entre comillas. Monks usa siglas en castellano: **PRM** = MRP, **PRC** = CRP, **PMP** = MPS, **LDM** = lista de materiales (BOM).")

# ---------------------------------------------------------------- U6: teoría
TEO = {}
SRC = {}
HX = {}      # cartas nuevas: se insertan antes del cierre
HREPL = {}   # reemplazos de cartas existentes: {id: {title_viejo: carta_nueva}}

TEO['u6c0'] = [
    AVISO("**Actualización (Drive + internet):** el libro de Monks no está en el Drive, pero sí el **resumen de alumnos de Monks** (`drive_u5/Resumen_Monks.docx`, caps. 5, 6, 7, 9, 10 y 13). Ahora se usa en las Clases 2, 4, 5, 6, 7, 10 y 11. "
          "Lo que se buscó en internet (Vollmann, láminas de UNICEN, la sigla «MCP») entra solo como **fuente externa**, con la fuente y la URL, y nunca reemplaza al material del Drive. El detalle está en el Integrador, sección 4."),
]
SRC['u6c0'] = [RM]

TEO['u6c2'] = [
    H("6. Lo que agrega el resumen de Monks (Drive)"),
    AVISO(MONKS_NOTA),
    P("Monks llama **planeación total** a lo que Chase y Morán llaman plan agregado: «el proceso de la planeación de la cantidad y cronología de la producción sobre un rango intermedio de tiempo ajustando la tasa de producción, empleo, inventarios y otras variables controlables». "
      "Su objetivo: «responder a las demandas irregulares de mercado mediante la utilización efectiva de los recursos de la organización»."),
    T(["Estrategias (cursos de acción) según el resumen de Monks", "Equivalente en esta clase"], [
        ["Variación en la fuerza de trabajo", "contratar y despedir (Chase)"],
        ["Tiempo extra y tiempo ocioso", "horas extra / capacidad ociosa"],
        ["Variación en los niveles de inventarios", "acumular stock (plan nivelado)"],
        ["Aceptación de reproceso", "así figura en el resumen; no está explicado. Lo más cercano en esta clase son los pedidos pendientes (Chase): tomalo con cuidado"],
        ["Subcontratación", "subcontratar"],
        ["Utilización de la capacidad", "usar la capacidad disponible"],
    ], "Estrategias de la planeación total según drive_u5/Resumen_Monks.docx, cap. 10"),
    L(["Lineamientos de la planeación total (resumen de Monks): «usar un buen pronóstico como base de planeación», «mantener el control necesario sobre los inventarios» y «responder a la demanda en forma controlada»."]),
    IDEA("Si en el final te preguntan por la **planeación total**, es el plan agregado. Contestá con la definición de Monks y las estrategias de Chase."),
]
SRC['u6c2'] = [RMC(10)]
HX['u6c2'] = [
    C('Monks', 'Planeación total = plan agregado.',
      'Según el resumen de Monks del Drive: planear cantidad y cronología de la producción a mediano plazo, ajustando tasa de producción, empleo e inventarios. Estrategias: fuerza de trabajo, tiempo extra u ocioso, inventarios, subcontratación y uso de la capacidad.',
      ejemplo='Lineamientos: un buen pronóstico, control de inventarios y responder a la demanda en forma controlada.'),
]

TEO['u6c4'] = [
    H("6. El PMP según el resumen de Monks (Drive)"),
    AVISO(MONKS_NOTA),
    P("La programación maestra «sigue a la planeación total y expresa el plan global en términos de artículos finales específicos, a los cuales pueden asignarse prioridades». "
      "El resumen lo dice así: «la planeación total sería los requerimientos de demanda a satisfacer y la programación maestra sería cómo utilizo los recursos para cumplir con esa demanda»."),
    L(["Generar requerimientos de materiales.", "Generar requerimientos de capacidad.", "Generar requerimientos de información.",
       "Evaluar alternativas de programación.", "Usar la capacidad con efectividad."], ordered=True),
    T(["Tipo de manufactura", "Por dónde empieza el PMP (resumen de Monks)"], [
        ["**Ensamble directo** (muchas materias primas y componentes que se combinan)", "por los **artículos finales** y va hacia atrás, hacia materias primas y componentes"],
        ["**Proceso industrial** (poca materia prima que se transforma en muchos productos)", "por la **materia prima** y va hacia los productos finales"],
    ], "Dirección del PMP según el tipo de manufactura (drive_u5/Resumen_Monks.docx, cap. 10)"),
    P("**Insumos:** pronósticos y pedidos de clientes. Los pronósticos «constituyen el impulso principal», y los pedidos «reducen la incertidumbre en empresas que trabajan bajo pedido». Es lo mismo que la regla de la cátedra: demanda = pedidos + pronóstico (sección 2). "
      "**Horizonte:** «depende del tipo de producto, el volumen de producción y los tiempos de entrega de los componentes»."),
]
SRC['u6c4'] = [RMC(10)]
HX['u6c4'] = [
    C('Monks', 'Las cinco funciones del PMP.',
      'Resumen de Monks del Drive: generar requerimientos de materiales, de capacidad y de información; evaluar alternativas de programación; usar la capacidad con efectividad. Sus insumos son pronósticos y pedidos de clientes.',
      svg=boxes([('Pronósticos', ''), ('Pedidos', ''), ('PMP', 'artículos finales'), ('Salidas', 'requerimientos')], 'Insumos y salidas del PMP'),
      chartLabel='Esquema propio con el resumen de Monks (Drive)'),
    Q('Según el resumen de Monks, en una manufactura de proceso industrial, ¿por dónde empieza el PMP?',
      ['Por los artículos finales', 'Por la materia prima, hacia los productos finales', 'Por la capacidad de planta'], 1,
      'En ensamble directo se parte de los artículos finales y se va hacia atrás. En proceso industrial, poca materia prima se transforma en muchos productos, así que se parte de la materia prima.'),
]

TEO['u6c5'] = [
    H("7. Capacidad de diseño, del sistema y eficiencia (resumen de Monks, Drive)"),
    AVISO(MONKS_NOTA),
    T(["Concepto", "Definición del resumen de Monks"], [
        ["Capacidad de diseño", "«la tasa de salida de productos estandarizados en condiciones de operación normal»; se deriva de conocer la demanda y fijar una política para satisfacerla"],
        ["Capacidad del sistema", "«la máxima producción de un producto que se genera». «Es la capacidad de la estación que menos produce»"],
        ["Eficiencia del sistema (ES)", "«una medida de la producción real de bienes y servicios como porcentaje de la capacidad del sistema»"],
        ["Capacidad por estación", "tiempo total de trabajo (por ejemplo, 7 h/día) dividido por el tiempo que insume la tarea"],
    ], "drive_u5/Resumen_Monks.docx, cap. 5"),
    F(r"ES = \frac{\text{producción real}}{\text{capacidad del sistema}} \qquad \text{Capacidad por estación} = \frac{\text{tiempo total de trabajo}}{\text{tiempo que insume la tarea}}",
      "Fórmulas del resumen de Monks (Drive)"),
    EXAM("Esto suma a la pregunta más repetida de los finales 2011–2018, la **capacidad de una estación de trabajo**. La fórmula de la cátedra (sección 4) sigue siendo la principal. La de Monks es la versión simple (tiempo disponible / tiempo por unidad) y sirve para explicar el **cuello de botella**: la capacidad del sistema es la de la estación que menos produce."),
]
SRC['u6c5'] = [RMC(5)]
HX['u6c5'] = [
    C('Monks', 'El sistema rinde lo que su estación más lenta.',
      'Resumen de Monks del Drive: la capacidad del sistema «es la capacidad de la estación que menos produce». La eficiencia del sistema es la producción real sobre esa capacidad.',
      formula=r'ES = \frac{\text{producción real}}{\text{capacidad del sistema}}'),
]

TEO['u6c6'] = [
    H("6. PRC, cargas infinitas y finitas (resumen de Monks, Drive)"),
    AVISO(MONKS_NOTA),
    P("**PRC** (planeación de requerimiento de capacidad, el CRP): «una técnica para determinar qué capacidades de personal y equipo son necesarias para cumplir los objetivos de producción incorporados en la Programación Maestra y el plan de requerimientos de materiales». "
      "El resumen remarca: «PRM se enfoca sobre las prioridades de los materiales, la PRC está interesada en el tiempo»."),
    T(["", "Carga infinita", "Carga finita"], [
        ["Qué hace", "satura los centros con todas las cargas cuando son requeridas, «sin importar la capacidad actual»", "limita la carga de un centro «a la capacidad máxima de éste»"],
        ["Cuándo se usa", "al principio, para medir la carga que propone el PMP y decidir tiempo extra, rutas alternativas, etc.", "en la asignación final de trabajo a los centros, después de los ajustes hechos con carga infinita"],
    ], "Cargas infinitas y finitas según drive_u5/Resumen_Monks.docx, cap. 13"),
    T(["Entradas de PRC", "Salidas de PRC"], [
        ["Planeación y programación de órdenes del sistema PRM", "Reportes de carga de órdenes planeadas y programadas en los centros de trabajo clave"],
        ["Capacidades de carga de los centros de trabajo", "Verificación de reportes del sistema PRM"],
        ["Datos de ruteo", "Datos de modificación de capacidades"],
        ["Cambios que modifiquen capacidades u órdenes planeadas", "Reprogramación de datos a PMP"],
    ], "Entrada–salida de PRC (drive_u5/Resumen_Monks.docx, cap. 13)"),
]
SRC['u6c6'] = [RMC(13)]
HX['u6c6'] = [
    C('Monks', 'Primero infinita, después finita.',
      'Resumen de Monks del Drive: la carga infinita sirve para medir la carga del PMP y decidir tiempo extra o rutas alternativas. La finita se usa en la asignación final, después de esos ajustes.',
      svg=flow_v([('PMP + PRM', 'órdenes'), ('Carga infinita', 'medir'), ('Ajustes', 'extra, rutas'), ('Carga finita', 'asignación final')], 'El orden de Monks'),
      chartLabel='Esquema propio con el resumen de Monks (Drive)'),
    Q('Según el resumen de Monks, ¿en qué se diferencian PRM y PRC?',
      ['PRM mira prioridades de materiales; PRC, el tiempo (horas de capacidad)', 'Son lo mismo con otro nombre', 'PRC calcula el lote económico'], 0,
      'PRC traslada las decisiones de PRM a horas de capacidad requeridas en cada centro.'),
]

TEO['u6c7'] = [
    H("6. PRM: el MRP según el resumen de Monks (Drive)"),
    AVISO(MONKS_NOTA),
    P("**PRM** (planeación de requerimiento de materiales): «una técnica para determinar la cantidad y periodicidad para la adquisición de artículos dependientes de la demanda necesaria para satisfacer los requerimientos de la Programación Maestra». "
      "Al identificar qué, cuánto y cuándo, permite reducir costos de inventarios, mejorar la efectividad de la programación y responder rápido a cambios del mercado."),
    L(["**LDM** (lista de materiales): todos los materiales y componentes para una unidad de producto final. Se describe con el **árbol de estructura del producto** o con la **LDM desglosada**. También existen LDM ficticias o artificiales, que se crean para facilitar la planeación.",
       "**Requerimientos brutos**: las necesidades totales. **Netos**: lo que queda después de usar el inventario disponible.",
       "**Explosión de materiales**: descomponer los artículos en sus partes para planearlas y programarlas por separado.",
       "**Fase de tiempo**: producir o recibir el material para que esté disponible cuando se necesite, «no antes ni después»."]),
    T(["Entradas de PRM", "Salidas de PRM"], [
        ["PMP de artículos finales requeridos", "Datos de programación de órdenes para los perfiles de carga de PRC"],
        ["Registros de estado de inventarios: disponible, tamaño de lotes, tiempos de entrega", "Órdenes de compra y de producción interna"],
        ["Registro de estructura del producto (LDM)", "Reprogramación del PMP"],
        ["", "Reportes administrativos y actualización del inventario"],
    ], "Entrada–salida de PRM (drive_u5/Resumen_Monks.docx, cap. 13)"),
    IDEA("Estas son las tres entradas de Morán y Chase con otros nombres: MPS, registro de inventarios y BOM. Si un enunciado viejo dice **PRM** o **LDM**, es MRP y BOM."),
]
SRC['u6c7'] = [RMC(13)]
HX['u6c7'] = [
    C('Siglas de Monks', 'PRM, PRC, PMP, LDM.',
      'Si ves esas siglas en un final viejo, son MRP, CRP, MPS y BOM. Así figuran en el resumen de Monks del Drive. Las entradas del PRM son el PMP, el estado de inventarios y la LDM.',
      svg=boxes([('PMP', 'MPS'), ('LDM', 'BOM'), ('Inventarios', 'estado'), ('PRM', 'MRP')], 'Entradas del PRM'),
      chartLabel='Esquema propio con el resumen de Monks (Drive)'),
]

MCP_BLOCK = AVISO(
    "**«MCP» en el final 13/12/2012** («Qué es MRP, MCP, ERP»). **No es una definición de la cátedra:** MCP no aparece definido en ningún material del Drive (notas de Morán, Chase, resumen de Monks, OCR de exámenes). "
    "**Hipótesis (fuente externa, confianza media-baja):** lo más probable es que se refiera a **MPC, Planificación y Control de la Fabricación (o de la Manufactura)**. Ese es el marco del libro de **Vollmann, Berry y Whybark**, que está en la bibliografía del programa. "
    "Su índice (catálogo UNDEF, " + VOLL_URL + ") arma todo alrededor del «sistema MPC»: administración de la demanda, planificación de la producción, MPS, MRP, planificación de capacidad, control de la actividad de producción, JIT y DRP, más capítulos de «Sistemas MPC integrados» y «Límites del sistema MPC». "
    "«MCP» sería el orden en castellano de la sigla o una inversión, y encaja en la secuencia **MRP → MRP II / sistema MPC → ERP**. "
    "Otra lectura posible, menos probable para 2012: «Machine Capacity Planning» (planificación de capacidad de máquinas), que solo aparece en glosarios actuales de ERP (" + TIC_URL + "). "
    "**Si te lo toman:** aclarás que no figura definido en el material, decís que lo interpretás como MPC (Vollmann) y respondés MRP, MPC y ERP como una evolución.")

TEO['u6c10'] = [
    H("6. PRM II, regenerativo y cambio neto (resumen de Monks, Drive)"),
    AVISO(MONKS_NOTA),
    P("**PRM II** (MRP II): «una extensión de los conceptos de PRM que incluye información de costos del producto que proporcionará reportes financieros, así como de capacidad y proveedores». El circuito incluye retroalimentación de operaciones internas y de órdenes a proveedores. "
      "El sistema crece con LDM planeadas, órdenes planeadas por la empresa y la capacidad de identificar y reprogramar."),
    T(["Sistema", "Cómo procesa (resumen de Monks)"], [
        ["**Regenerativo**", "procesamiento intermitente: replanea el sistema total (explosión completa de todos los artículos) sobre una base regular, por ejemplo semanal"],
        ["**Cambio neto**", "en línea: reacciona continuamente a cambios en el programa maestro, los inventarios y otras transacciones"],
    ], "drive_u5/Resumen_Monks.docx, cap. 13"),
    H("7. MRP II como lazo cerrado (fuente externa: láminas de UNICEN)"),
    AVISO("**Fuente externa, no es de la cátedra:** láminas de UNICEN (2003), " + UNICEN_URL + ". Se suman porque ordenan en un solo esquema lo que el Drive explica por partes."),
    P("Las láminas definen MRP II como «una extensión natural del concepto del MRP, incorporando a las funciones de planeamiento funciones de control y de planificación de recursos, así como de planeamiento de capacidad (CRP)», y dicen que «administra el proceso de producción como un sistema con lazo cerrado». "
      "El esquema de funciones va en tres niveles: **planeamiento** (de negocios, de ventas, de producto y de producción), **operaciones** (MPS, MRP y CRP) y **control** (compras, piso de producción, inventario y distribución). Si no hay material o no hay capacidad «económicamente», se modifica el MPS."),
    P("También dicen que un software MRP II tiene dos grandes componentes. Uno **describe el proceso de manufactura** (BOM, rutas, capacidades de máquinas, tiempos de respuesta de proveedores). El otro **incorpora funciones de control** del proceso de producción."),
    H("8. La sigla «MCP»"),
    MCP_BLOCK,
]
SRC['u6c10'] = [RMC(13), UNICEN, VOLL, "Fuente externa: TIC Portal, glosario, «Planificación de capacidad de máquinas (MCP)», " + TIC_URL]
HX['u6c10'] = [
    C('Monks', 'Regenerativo o cambio neto.',
      'Resumen de Monks del Drive: el regenerativo replanea todo, con explosión completa, en forma periódica (por ejemplo, semanal). El de cambio neto está en línea y reacciona a cada cambio del MPS o del inventario.'),
    C('Fuente externa · UNICEN', 'MRP II es un lazo cerrado.',
      'Láminas de UNICEN (2003): planeamiento de negocios y ventas, después MPS, MRP y CRP, y control de compras y planta. Si falta material o capacidad, se vuelve a modificar el MPS.',
      svg=flow_v([('Planeamiento', 'negocios, ventas, producción'), ('MPS → MRP → CRP', 'operaciones'), ('¿Material y capacidad?', 'no → modificar MPS'), ('Control', 'compras, planta, inventario')], 'MRP II a lazo cerrado'),
      chartLabel='Fuente externa: UNICEN, 12_MRP.pdf'),
]
HREPL['u6c10'] = {
    '«MCP» no está definido.': C('Hipótesis · fuente externa', '«MCP»: probablemente MPC.',
        'No está definido en el Drive ni en ningún apunte de la cátedra. Lo más probable (confianza media-baja) es que sea MPC, Planificación y Control de la Fabricación, el sistema del libro de Vollmann, que está en la bibliografía. Si te lo toman, aclaralo y respondé MRP → MPC → ERP.',
        ejemplo='Fuente externa: índice del Vollmann en el catálogo de la UNDEF. No es una definición de la cátedra.'),
}

TEO['u6c11'] = [
    H("5. Las fórmulas de balanceo en el resumen de Monks (Drive)"),
    AVISO(MONKS_NOTA),
    P("Balanceo de línea: «una distribución de las actividades secuenciales de trabajo para lograr el máximo aprovechamiento posible de la mano de obra y del equipo y de este modo reducir o eliminar el tiempo ocioso»."),
    T(["Fórmula (resumen de Monks)", "Equivale en Chase (sección 1)"], [
        ["Ciclo de tiempo CT = tiempo disponible por período / producción requerida por período", "C"],
        ["Número mínimo teórico de trabajadores = ∑t / CT", "N_t"],
        ["Eficiencia del balance = ∑t / (CT · n), con n = estaciones reales; o mínimo teórico / número real de trabajadores", "E"],
        ["Ciclo de tiempo meta CTm = ∑t / n; debe ser ≥ que la actividad más larga", "—"],
        ["Producción = tiempo total de trabajo / cadencia (tiempo de la estación más lenta)", "—"],
        ["Número de estaciones = capacidad requerida / capacidad por estación", "—"],
    ], "drive_u5/Resumen_Monks.docx, cap. 5"),
    P("**Regla heurística** del resumen: moverse hacia abajo en el diagrama de red y elegir primero las tareas con **mayor tiempo** que entren en el ciclo de la estación, respetando las precedencias. Es la misma regla del tiempo más largo que usa Chase. "
      "Además: «Si el tiempo requerido en cualquier estación > CT → agregar trabajador»."),
    EXAM("La **cadencia** (la estación más lenta) fija el ritmo de la línea. Por eso la producción por día es el tiempo de trabajo sobre la cadencia. Es la misma idea que la capacidad del sistema de la Clase 5."),
]
SRC['u6c11'] = [RMC(5)]
HX['u6c11'] = [
    C('Monks', 'La cadencia manda.',
      'Resumen de Monks del Drive: producción = tiempo total de trabajo / cadencia, donde la cadencia es el tiempo de la estación más lenta. El ciclo meta, suma de tareas / estaciones, no puede ser menor que la tarea más larga.',
      formula=r'\text{Producción} = \frac{\text{tiempo total de trabajo}}{\text{cadencia}} \qquad CT_m = \frac{\sum t}{n}'),
]

# ---------------------------------------------------------------- bibliografía (integradores)
FALTAN_ROWS = [
    ["Monks, «Administración de operaciones» (McGraw-Hill)", "**No está en el Drive**, solo el resumen de alumnos. En castellano hay fichas de biblioteca (Serie Schaum, México 1991, ISBN 968-422-886-4: https://biblioteca-fceco.uner.edu.ar/bib/14899). En inglés se puede pedir en **préstamo gratuito en archive.org**, con cuenta propia: " + AO["monks82"] + " (1982) y " + AO["monks87"] + " (1987)"],
    ["Vollmann, Berry y Whybark, «Sistemas de planificación y control de la fabricación»", "**No está en el Drive.** Ficha e índice en castellano (Irwin 1994): " + VOLL_URL + ". En inglés, 2.ª ed. (1988), en **préstamo en archive.org**: " + AO["voll88"]],
    ["Sessa, «Notas técnicas de cátedra» y apunte de Codificación", "**No está en el Drive ni online.** Pedirlo a la cátedra"],
    ["R. Morán, apunte de stocks («Elementos de Gestión de las Existencias (Stocks)», 2007, citado en su apunte de JIT)", "**No está en el Drive.** Solo aparece en un sitio de terceros y el autor prohíbe reproducirlo. Pedirlo a la cátedra o a la Escuela de Ingeniería Industrial (FCEIA-UNR)"],
    ["APICS", "No está en el Drive"],
]

def biblio_u6():
    return [
        H("4. Fuentes y bibliografía de la U6"),
        P("**Prioridad: el material del Drive.** Lo de internet solo complementa y va marcado como fuente externa."),
        T(["Material", "Dónde está", "Clases"], [
            ["Chase, Jacobs y Aquilano, 12a ed. (caps. 7, 7A, 16, 18, 19)", "Drive", "1–12"],
            ["Notas técnicas de R. Morán: plan agregado, capacidad, MRP, PAC, JIT", "Drive (cátedra)", "2, 3, 5–10, 12"],
            ["Resumen de alumnos de Monks (caps. 5, 10, 13)", "Drive (`Resumen_Monks.docx`)", "2, 4, 5, 6, 7, 10, 11"],
            ["Láminas de Bigatti (UTN FRRo, 2015) y TP 7 Odoo", "Drive (cátedra)", "2, 3, 10"],
            ["Láminas UNICEN «Planificación y Control de la Producción» (2003)", "**Fuente externa:** " + UNICEN_URL, "10"],
            ["Índice del Vollmann (catálogo UNDEF)", "**Fuente externa:** " + VOLL_URL, "10 (hipótesis MCP)"],
        ], "Qué se usó en la unidad"),
        T(["Lo que falta", "Estado y cómo conseguirlo"], FALTAN_ROWS, "Bibliografía del programa que no está en el Drive"),
        AVISO("**Resoluciones oficiales:** no hay, ni en el Drive ni online. Las resoluciones de esta unidad son del material cuando así se indica, y si no, **cálculo propio**. Los enunciados ilegibles (cédulas de manejo) tampoco aparecieron en internet. Relevamiento completo: " + HALL + "."),
    ]

def biblio_u5():
    return [
        H("5. Fuentes y bibliografía de la U5"),
        P("**Prioridad: el material del Drive.** Lo de internet solo complementa y va marcado como fuente externa."),
        T(["Material", "Dónde está", "Clases"], [
            ["Chase, Jacobs y Aquilano, 12a ed. (caps. 10, 11, 12, 17)", "Drive", "1–10"],
            ["R. Morán: «Planificación de la distribución» (2000) y «Producción Justo a Tiempo» (2012)", "Drive (cátedra)", "5, 8, 9"],
            ["Práctica «Repaso de conceptos estadísticos básicos» (tabla z de la cátedra)", "Drive (cátedra)", "5, 6"],
            ["Y. Reyes, «Control de inventarios» (PUCV)", "**Fuente externa:** " + REY1_URL, "3 (descuentos), 7 (ABC)"],
            ["Y. Reyes, «Inventarios de demanda aleatoria» (PUCV)", "**Fuente externa:** " + REY2_URL, "6 (período único)"],
        ], "Qué se usó en la unidad"),
        T(["Lo que falta", "Estado y cómo conseguirlo"], FALTAN_ROWS, "Bibliografía del programa que no está en el Drive"),
        AVISO("El resumen de Monks del Drive tiene los caps. 11 y 12 (compras y control de inventarios) **solo con el título**, así que para la U5 no aporta. **Resoluciones oficiales:** no hay, ni en el Drive ni online. Relevamiento completo: " + HALL + "."),
    ]

TEO['u6int'] = biblio_u6()
SRC['u6int'] = [RM, UNICEN, VOLL, HALL]
HX['u6int'] = [
    C('Fuentes', 'Primero el Drive.',
      'Chase, las notas de Morán y el resumen de Monks son del Drive. Lo de internet (láminas de UNICEN, índice del Vollmann) solo complementa y va marcado como fuente externa.',
      ejemplo='Monks y Vollmann en inglés: préstamo gratis en archive.org con cuenta propia. Sessa y el apunte de stocks de Morán: pedirlos a la cátedra.'),
]

# ---------------------------------------------------------------- U5
TEO['u5c3'] = [
    H("3. Otra forma de evaluar un descuento (fuente externa)"),
    AVISO("**Fuente externa, no es de la cátedra:** Y. Reyes Fernández, apunte docente PUCV, " + REY1_URL + ". El método de la cátedra y de Chase es el de la sección 2. Este sirve como control rápido."),
    P("El apunte dice que el descuento produce **tres efectos**: (1) una economía en el precio, igual a la reducción por unidad × el consumo del período; (2) menos pedidos por período, o sea, ahorro en costo de pedir; (3) más costo de mantener, porque el pedido es más grande. "
      "**Conviene aceptar si:** economía en precio + economía en pedidos − costo adicional de mantener > 0."),
    EJ("Ejemplo del apunte (Reyes): D = 2.000 u en 100 días, S = 100 por pedido, H = 10 por unidad en los 100 días", [
        F(r"Q^* = \sqrt{\frac{2 \cdot 2.000 \cdot 100}{10}} = 200"),
        P("Descuento del 10 % si se piden 250 (precio unitario 1)."),
        L(["Economía en precio: 0,10 × 2.000 = 200.",
           "Economía en pedidos: 2.000·100/200 − 2.000·100/250 = 1.000 − 800 = 200.",
           "Costo adicional de mantener: (250 − 200)/2 × 10 = 250.",
           "Neto: 200 + 200 − 250 = **150 > 0** → conviene el descuento."]),
        P("Verificación (cálculo propio) con el costo total de Chase: CT(200) = 2.000·1 + 1.000 + 1.000 = 4.000 y CT(250) = 2.000·0,9 + 800 + 1.250 = 3.850. La diferencia es la misma: 150."),
    ]),
]
SRC['u5c3'] = [REY1]
HX['u5c3'] = [
    C('Fuente externa · PUCV', 'Los tres efectos del descuento.',
      'Apunte de Reyes (PUCV): el descuento ahorra en precio y en cantidad de pedidos, pero aumenta el costo de mantener. Si la suma da positiva, conviene. Da lo mismo que comparar costos totales como en Chase.',
      ejemplo='Ejemplo del apunte: 200 + 200 − 250 = 150 a favor del descuento.'),
]

TEO['u5c6'] = [
    H("6. Período único con matriz de valor esperado (fuente externa)"),
    AVISO("**Fuente externa, no es de la cátedra:** Y. Reyes Fernández, «Inventarios de demanda aleatoria», PUCV, " + REY2_URL + ". En el Drive el período único se resuelve con el análisis marginal de Chase (sección 2). Esta es otra forma de plantearlo, con una tabla."),
    P("El método del **valor esperado** arma una matriz **inventario × demanda**, calcula la ganancia de cada celda y elige la alternativa de mayor beneficio esperado (fórmula de abajo). "
      "Distingue el **costo por exceso** (unidades que sobran: el apunte lo valúa con el costo de capital) y el **costo por defecto** (unidades que faltan: la utilidad que se pierde)."),
    F(r"VE(A_i) = \sum_{j} x_{ij} \cdot p_j", "x: resultado de cada alternativa con cada demanda; p: probabilidad de esa demanda"),
    T(["Stock / demanda", "D = 20 (p 0,40)", "D = 30 (p 0,30)", "D = 40 (p 0,30)", "Beneficio esperado"], [
        ["30", "45", "150", "100", "**93**"],
        ["40", "−10", "95", "200", "84,5"],
        ["50", "−65", "40", "145", "29,5"],
    ], "Matriz de beneficios del ejemplo del apunte (compra 5, venta 10, costo de capital 10 %). Se elige 30 unidades"),
    AVISO("**Ojo (cálculo propio):** el apunte, además de no registrar la venta que se pierde, resta el costo por defecto. Por eso sus ganancias con faltante son menores que ingreso − costo de compra: con 30 en stock y demanda 40, el apunte da 100, y la ganancia directa sería 300 − 150 = 150. "
          "En el final usá el **análisis marginal** de la cátedra y de Chase. La matriz sirve para ver el razonamiento."),
]
SRC['u5c6'] = [REY2]
HX['u5c6'] = [
    C('Fuente externa · PUCV', 'Período único con una matriz.',
      'Apunte de Reyes (PUCV): inventario × demanda, ganancia por celda y elegir el mayor valor esperado. En su ejemplo gana stockear 30 (93 contra 84,5 y 29,5). En el final, el método es el marginal de Chase.'),
]

TEO['u5c7'] = [
    H("9. Otro criterio de ABC y políticas por clase (fuente externa)"),
    AVISO("**Fuente externa, no es de la cátedra:** Y. Reyes Fernández, «Control de inventarios», PUCV, " + REY1_URL + ". El criterio del Drive y de Chase es el valor de uso anual (sección 2). Esto suma **qué hacer** con cada clase."),
    P("El apunte ordena 10 artículos por valor de consumo (cantidad × costo unitario) y llega a: **A** = 7 % de las unidades y 74 % del valor; **B** = 44 % y 19 %; **C** = 49 % y 7 %. "
      "Para fijar los cortes usa también el **costo unitario** («costo unitario de 25 o más, o consumo anual superior a 20.000» para la clase A, en la moneda del ejemplo). Fijate que mide el porcentaje sobre las **unidades usadas**, no sobre la cantidad de ítems."),
    T(["Clase", "Política de compra según el apunte"], [
        ["A", "existencias al mínimo; no recomienda stock de seguridad (sin arriesgar faltantes); la compra la aprueba algún nivel ejecutivo"],
        ["B", "depende de su peso: si son ~20 % del consumo, políticas de C; si son ~40 %, políticas de A con controles menos estrictos"],
        ["C", "procedimientos sencillos y rutinarios, reservas de emergencia; solo autoriza el jefe de compras"],
    ], "Políticas por clase (Reyes, PUCV)"),
    P("Las ventajas que da el apunte: economía de personal de planificación y control, menos faltantes por fallas internas y más eficiencia en el manejo de existencias."),
]
SRC['u5c7'] = [REY1]
HX['u5c7'] = [
    C('Fuente externa · PUCV', 'Qué hacer con cada clase.',
      'Apunte de Reyes (PUCV): A, mínimo stock y compra aprobada por un ejecutivo; B, según su peso; C, compra rutinaria con reservas de emergencia y firma del jefe de compras.',
      ejemplo='En su ejemplo: A = 7 % de las unidades y 74 % del valor.'),
]

TEO['u5int'] = biblio_u5()
SRC['u5int'] = [REY1, REY2, HALL]
HX['u5int'] = [
    C('Fuentes', 'Primero el Drive.',
      'Chase, Morán y la tabla z de la cátedra son del Drive. Los apuntes de PUCV entran solo como fuente externa, en descuentos, período único y ABC.',
      ejemplo='Falta el apunte de stocks de Morán: pedilo a la cátedra. Monks y Vollmann en inglés: préstamo en archive.org.'),
]

# ---------------------------------------------------------------- aplicar
def _fix_old(c):
    """Corrige textos viejos que quedaron desactualizados."""
    for b in c["teoria"]:
        if b.get("type") == "callout" and "«MCP» en el final 13/12/2012" in b.get("text", ""):
            b["text"] = "**«MCP»:** ver la sección «La sigla MCP» al final de esta clase (hipótesis, fuente externa)."
        if b.get("type") == "callout" and b.get("text", "").startswith("**Lo que no está en el Drive:** Monks"):
            b["text"] = b["text"].replace("**Lo que no está en el Drive:** Monks (el programa lo cita y los alumnos dicen que el hombre–máquina sale de ahí)",
                                          "**Lo que no está en el Drive:** el libro de Monks (el programa lo cita y los alumnos dicen que el hombre–máquina sale de ahí; sí está el resumen de alumnos)")
        if b.get("type") == "table":
            for r in b.get("rows", []):
                for i, cell in enumerate(r):
                    if isinstance(cell, str) and cell.startswith("**No está en el Drive.** El «Resumen Monks» de alumnos"):
                        r[i] = cell + ". Los caps. 5, 10 y 13 (capacidad, PMP, PRM/PRC) sí están y se usan en la U6"


def _num(text):
    m = re.match(r"^(\d+)\. ", text or "")
    return int(m.group(1)) if m else None


def apply(c):
    cid = c["id"]
    _fix_old(c)
    if cid in TEO:
        add = copy.deepcopy(TEO[cid])
        t = c["teoria"]
        gl = t[-1] if t and t[-1].get("type") == "glosario" else None
        nums = [_num(b.get("text")) for b in t if b.get("type") == "heading"] + [_num(b.get("title")) for b in t]
        nums = [x for x in nums if x]
        nxt = (_num(gl.get("title")) if gl and _num(gl.get("title")) else (max(nums) + 1 if nums else 1))
        for b in add:
            if b.get("type") == "heading" and _num(b["text"]):
                b["text"] = re.sub(r"^\d+\. ", f"{nxt}. ", b["text"]); nxt += 1
        if gl:
            if _num(gl.get("title")):
                gl["title"] = re.sub(r"^\d+\. ", f"{nxt}. ", gl["title"])
            c["teoria"] = t[:-1] + add + [gl]
        else:
            c["teoria"] = t + add
    if cid in SRC:
        if isinstance(c["source"], list):
            c["source"] += [x for x in SRC[cid] if x not in c["source"]]
        else:
            c["source"] = c["source"] + "; " + "; ".join(x for x in SRC[cid] if x not in c["source"])
    return c


def apply_hist(cid, h):
    h = list(h)
    for i, card in enumerate(h):
        rep = HREPL.get(cid, {}).get(card.get("title"))
        if rep: h[i] = rep
    if cid == "u6c0":
        for card in h:
            if card.get("title") == "Chase y las notas de Morán.":
                card["ejemplo"] = "El libro de Monks no está, pero sí un resumen de alumnos (caps. 5, 10 y 13). Vollmann y Sessa no están. Lo de internet entra solo como fuente externa."
            if card.get("title") == "Huecos del material.":
                card["text"] = card["text"].replace("«MCP» no aparece definido.", "«MCP» no aparece definido (en la Clase 10 está la hipótesis, como fuente externa).")
    extra = HX.get(cid, [])
    if extra:
        h = h[:-1] + extra + h[-1:]
    return h
