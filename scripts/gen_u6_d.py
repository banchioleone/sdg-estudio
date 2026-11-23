from u6lib import *


def c11():
    t = [
        P("**Unidad 6 · Bloque D · Clase 11 · Balanceo de línea**"),
        IDEA("**Idea central:** en una línea, la demanda fija el **tiempo de ciclo** (cada cuánto tiene que salir una unidad). Balancear es repartir las tareas en estaciones, respetando las precedencias, para que ninguna estación supere el ciclo y el tiempo ocioso total sea mínimo."),
        H("1. El problema y las fórmulas (Chase cap. 7A)"),
        P("Chase: el balanceo «consiste en asignar todas las tareas a una serie de estaciones de trabajo de modo que cada una de ellas no tenga más de lo que se puede hacer en el tiempo del ciclo de la estación de trabajo y que el tiempo no asignado (es decir, inactivo) de todas las estaciones de trabajo sea mínimo». Lo complica la **relación de precedencia**, que «especifica el orden en que se deben realizar las tareas»."),
        F(r"C = \frac{\text{tiempo de producción por día}}{\text{producción requerida por día}} \qquad N_t = \frac{T}{C} \;(\text{redondear hacia arriba}) \qquad \text{Eficiencia} = \frac{T}{N_a \cdot C}", "C = tiempo de ciclo; T = suma de los tiempos de las tareas; N_t = estaciones mínimas teóricas; N_a = estaciones reales"),
        L(["Diagrama de precedencias (círculos = tareas, flechas = orden).", "Tiempo de ciclo C.", "Estaciones mínimas N_t.",
           "Elegir una regla de asignación y otra para desempatar.", "Asignar tareas de a una a la estación 1 hasta llenar C o quedarse sin tareas viables; seguir con la 2, etc.",
           "Calcular la eficiencia.", "Si no satisface, rebalancear con otra regla."], True),
        H("2. Ejemplo resuelto de Chase: camioneta modelo J (ejemplo 7A.1)"),
        EJ("500 camionetas por día en 420 minutos", [
            T(["Tarea", "Tiempo (s)", "Precede"], [["A", "45", "—"], ["B", "11", "A"], ["C", "9", "B"], ["D", "50", "—"], ["E", "15", "D"], ["F", "12", "C"], ["G", "12", "C"], ["H", "12", "E"], ["I", "12", "E"], ["J", "8", "F, G, H, I"], ["K", "9", "J"], ["**T**", "**195**", ""]], "Chase, ilustración 7A.9"),
            F(r"C = \frac{60 \cdot 420}{500} = 50{,}4 \text{ s} \qquad N_t = \frac{195}{50{,}4} = 3{,}87 \rightarrow 4"),
            P("**Reglas:** (a) primero la tarea con **más tareas subsiguientes** (A 6; B o D 5; C o E 4; F, G, H o I 2; J 1; K 0); (b) para desempatar, la de **mayor tiempo**."),
            T(["Estación", "Tareas", "Tiempo", "Ocioso"], [["1", "A", "45", "5,4"], ["2", "D", "50", "0,4"], ["3", "B, E, C, F", "47", "3,4"], ["4", "G, H, I, J", "44", "6,4"], ["5", "K", "9", "41,4"]], "Chase, ilustración 7A.11"),
            F(r"\text{Eficiencia} = \frac{195}{5 \cdot 50{,}4} = 0{,}77"),
            P("77% quiere decir 23% de inactividad: 57 segundos ociosos por ciclo, casi todos en la estación 5. Chase agrega que con la regla (b) primero y (a) para desempatar se consigue un balance viable de **cuatro** estaciones."),
        ]),
        S("u6_precedencias_j.svg", "Diagrama de precedencias de la camioneta J con las 5 estaciones de Chase (redibujo propio de la ilustración 7A.11B)"),
        H("3. Cuando una tarea es más larga que el ciclo"),
        P("Ejemplo de Chase: tareas de 40, 30, 15, 25, 20, 18 y 15 s; 7,5 h por día y 750 unidades → C = 27.000 / 750 = **36 s**, pero hay una tarea de 40 s. Opciones:"),
        L(["**Dividir la tarea** entre dos estaciones que procesen unidades completas.", "**Compartir la tarea** con una estación contigua que ayuda.",
           "**Estaciones en paralelo**: dos estaciones hacen la misma tarea.", "**Trabajador más capacitado**: la tarea excede el ciclo solo 11%.",
           "**Horas extra**: a 40 s por unidad salen 675 por día, 75 menos; producirlas lleva 75 × 40 / 60 = **50 minutos** extra.", "**Rediseñar** el producto."], True),
        P("Chase también trata las líneas de **modelo mixto** (varios modelos en la misma línea) y las líneas **flexibles en U**, donde los operarios pueden intercambiar elementos del trabajo y se pueden sumar o restar operarios según el ritmo."),
        H("4. Ejercicios de final"),
        EX("EJERCICIO — Montaje con estaciones en paralelo (Ejercicios posibles; 22/05/2003)", [
            P("«Se necesita implementar una tarea de montaje que producirá **80 unidades en un turno de 8 horas**.» OP 01 montaje mecánico **12 minutos**; OP 02 montaje eléctrico **16 minutos**; OP 03 prueba **3 minutos**. «2.1- ¿Cuántas estaciones de trabajo en paralelo se requieren en cada OP? 2.2- Estimando que los trabajadores de cada estación no pueden ser utilizados para otras actividades en la planta, ¿cuál es el tiempo ocioso para esta tarea?»"),
        ], [
            P("**Cálculo propio** (no hay resolución en el material)."),
            F(r"C = \frac{480 \text{ min}}{80} = 6 \text{ min}"),
            T(["Operación", "Tiempo", "Estaciones = tiempo / C", "Capacidad por ciclo", "Ocioso por ciclo"], [
                ["OP 01", "12", "12 / 6 = **2**", "2 × 6 = 12", "0"], ["OP 02", "16", "16 / 6 = 2,67 → **3**", "18", "2"], ["OP 03", "3", "3 / 6 = 0,5 → **1**", "6", "3"],
                ["**Total**", "31", "**6 estaciones**", "36", "**5 min**"],
            ]),
            P("**Tiempo ocioso:** 5 min por unidad × 80 unidades = **400 min por turno** (equivale a 6 × 480 − 80 × 31 = 2.880 − 2.480). Eficiencia = 31 / (6 × 6) = **86,1%**."),
        ], estado="cálculo propio"),
        EX("EJERCICIO — Las otras dos versiones del montaje (06/05/2004 y 09/03/2006)", [
            P("**06/05/2004:** 80 unidades en 8 horas con OP 01 = **72 min**, OP 02 = **48 min**, OP 03 = **6 min**. **09/03/2006:** **800 unidades** en 8 horas con 12, 16 y 3 minutos."),
        ], [
            P("**Cálculo propio.** 06/05/2004: C = 6 min → 72/6 = **12**, 48/6 = **8**, 6/6 = **1** estaciones; las divisiones son exactas, así que **no hay tiempo ocioso** (eficiencia 100%)."),
            P("09/03/2006: C = 480/800 = **0,6 min** → 12/0,6 = **20**; 16/0,6 = 26,7 → **27**; 3/0,6 = **5** estaciones (52 en total). Ocioso: solo OP 02, 27 × 0,6 − 16 = 0,2 min por unidad → **160 min por turno**. Eficiencia 31 / (52 × 0,6) = 99,4%."),
        ], estado="cálculo propio"),
        EX("EJERCICIO — Línea de ventanas de aluminio (Ejercicios posibles; 22/05/2003)", [
            P("«Un fabricante está diseñando una planta que producirá ventanas de aluminio reforzadas. La capacidad de producción mínima necesaria es de **640 u/día**. […] El fabricante desea saber todos los comentarios técnicos que se pueden realizar a este proyecto (buen diseño de planta, si se puede mejorar, capacidad ociosa, eficiencia, capacidad adecuada, etc.).» Diseño propuesto: estación 1 A; 2 B; 3 C y D; 4 E y F; 5 G; 6 H."),
            T(["Actividad", "Descripción", "Predecesoras", "Tiempo (s)"], [
                ["A", "Ensamblado de marco", "—", "70"], ["B", "Instalar molduras", "A", "80"], ["C", "Introducir tornillos", "A", "40"], ["D", "Instalar seguro en marco", "A", "20"],
                ["E", "Instalar manija", "A", "40"], ["F", "Colocar cristal", "B, C", "30"], ["G", "Cubrir tornillos", "C", "50"], ["H", "Embalar", "D, E, F, G", "50"], ["", "**Total**", "", "**380**"],
            ]),
        ], [
            AVISO("**Qué hay en el material.** La resolución manuscrita (EFR p. 19) trabaja con un ciclo de **90 s**, estaciones mínimas 380/90 = 4,22 → **5** y eficiencia **84,44%**; usa 320 u/día en un turno, que da el mismo ciclo que 640 u/día en **dos turnos** (57.600 s / 640 = 90 s). El análisis del diseño propuesto y el balance de 5 estaciones son **cálculo propio**."),
            P("**1. ¿Alcanza un turno?** Con 8 h: C = 28.800 / 640 = **45 s**, menor que la tarea más larga (B, 80 s). Imposible sin **estaciones en paralelo** o sin más turnos. Con dos turnos: C = **90 s**."),
            P("**2. El diseño propuesto** (6 estaciones): tiempos 70, 80, 60, 70, 50, 50. Respeta las precedencias. La estación más cargada (80 s) fija el ritmo: con 2 turnos salen 57.600 / 80 = 720 u/día ≥ 640. Eficiencia con C = 90: 380 / (6 × 90) = **70,4%**; aun midiéndola contra el cuello de botella, 380 / (6 × 80) = 79,2%. Sobra una estación."),
            P("**3. Mejor balance con C = 90 s** (5 estaciones = el mínimo):"),
            T(["Estación", "Tareas", "Tiempo", "Ocioso"], [["1", "A, D", "90", "0"], ["2", "B", "80", "10"], ["3", "C, E", "80", "10"], ["4", "F, G", "80", "10"], ["5", "H", "50", "40"]]),
            S("u6_ventanas.svg", "Precedencias de la línea de ventanas y el balance de 5 estaciones con C = 90 s (cálculo propio)"),
            P("Precedencias: F necesita B (estación 2) y C (estación 3), G necesita C, H necesita D, E, F y G: todo se cumple. Eficiencia = 380 / (5 × 90) = **84,4%**, la de la hoja manuscrita. **Comentario técnico:** el diseño propuesto funciona pero tiene una estación de más (capacidad ociosa); con 5 estaciones se gana eficiencia y se sigue cumpliendo la demanda en dos turnos."),
        ], estado="cálculo propio", nota="El ciclo de 90 s y el 84,44% están en la hoja; el balance concreto es propio"),
        EX("EJERCICIO — Turnos para cédulas de manejo (final 14/03/2013, transcripción de alumno)", [
            P("Según el alumno: «la dirección de tránsito desea implementar un sistema de turnos para tramitar cédulas de manejo en donde se entregan **50 números por día**, y trabajan de **8 a 16 hs**. Luego daba un cuadro en donde había **10 actividades** […] con su predecesora y su duración. Se pedía: a) dibujar el diagrama de red de la línea y calcular el tiempo de ciclo total (por número eran unos **36 min**); b) balancear la línea y calcular la eficiencia; c) ¿cuántas cédulas puede entregar la red balanceada?»"),
        ], [
            AVISO("**Falta la tabla de las 10 actividades**: no está en el Drive. Con lo que hay se puede plantear el arranque (cálculo propio)."),
            F(r"C = \frac{480 \text{ min}}{50} = 9{,}6 \text{ min} \qquad N_t = \frac{36}{9{,}6} = 3{,}75 \rightarrow 4 \text{ estaciones}"),
            P("Los «36 min por número» son la suma T de las tareas (el alumno lo llama «tiempo de ciclo total»; en Chase, el ciclo es C). Para la c): si el balance da una estación más cargada de, por ejemplo, 9 min, la red entrega 480 / 9 = 53 cédulas por día: **la capacidad la fija la estación más lenta**."),
        ], estado="para resolver", nota="Falta la tabla de actividades"),
        AVISO("**Hombre–máquina:** los finales del 01/08/2002 y del 13/12/2012 traen un ejercicio de gráfica hombre–máquina (ciclo, tiempo ocioso, eficiencia y costo horario). Según la transcripción del alumno es «la misma que está en la página 129 del Monks», y Monks no está en el Drive. No es tema de esta unidad en el material de la U6; acá solo lo dejamos anotado."),
    ]
    return clase("u6c11", "Clase 11 · Balanceo de línea", "Balanceo de línea", "D",
                 "Tiempo de ciclo, estaciones mínimas, eficiencia y reglas de asignación con la camioneta J de Chase; tareas más largas que el ciclo; y los ejercicios de final: montaje en paralelo, ventanas y cédulas.",
                 "; ".join([CH("7A", "228–232", "balanceo de la línea de ensamble, ejemplo 7A.1"), EPOS, EVA + " — 22/05/2003, 06/05/2004, 09/03/2006", EFR(19, "ventanas: ciclo 90 s, 84,44%"), "texto/examenes/Preguntas de teoria del final de SG1.txt (14/03/2013, cédulas)"]), t)


def c12():
    t = [
        P("**Unidad 6 · Bloque D · Clase 12 · Control de las actividades de producción**"),
        IDEA("**Idea central:** el PAC es la parte que **ejecuta** el plan: libera las órdenes con su documentación, decide qué se hace primero en cada centro (prioridades y secuencia) y recoge datos de planta para saber cómo van las órdenes y la capacidad."),
        H("1. Qué es el PAC"),
        P("Morán: el objetivo del PAC «es realizar el lanzamiento, la programación y el control del progreso de las órdenes de producción, es decir administrar el trabajo en curso de ejecución». También se llama **control del taller** (SFC: Shop Floor Control). Sus entradas son las salidas del MPS, del MRP y del CRP, y los datos de ingeniería del producto y del proceso."),
        T(["Función (Morán §1)", "Qué hace"], [
            ["**Asignación y control de prioridades**", "adapta la ejecución a los cambios: adelantar una orden, atrasar otra; las prioridades se revisan semanal o diariamente; después viene la **carga de máquinas** y el **secuenciamiento**"],
            ["**Información sobre trabajos en curso**", "compara cantidades y fechas reales con las del MRP y corrige discrepancias"],
            ["**Control del estado de las órdenes**", "informe de estado de cada orden e informes de excepción"],
            ["**Datos para el control de la capacidad**", "información de planta para ajustar mano de obra y equipos"],
        ]),
        P("Ningún sistema es un control automático: «aún los sistemas más evolucionados cierran el bucle de control con un decisor humano»."),
        S("u6_pac.svg", "Las tres fases del PAC y sus documentos (esquema según Morán, figura 1)"),
        H("2. Fase 1: liberación o lanzamiento de las órdenes"),
        T(["Documento", "Para qué (Morán)"], [
            ["**Hoja de ruta**", "secuencia de operaciones, equipos y herramental"], ["**Requisición de materiales**", "vales para sacar materia prima o componentes del almacén"],
            ["**Vales de trabajo**", "uno por operación de la ruta, para informar lo realizado"], ["**Vales de movimiento**", "para mover e informar los traslados entre centros"],
            ["**Lista de piezas**", "para armado o montaje"],
        ]),
        P("Con más automatización estos papeles se reemplazan por información en línea. **La cátedra:** «Planeamiento y control lanza las OF **cada viernes para la semana siguiente** y reprograma las OF que tuvieron problema»; horizonte de planificación mensual, de programación semanal, períodos de días o turnos, revisión diaria (banco, pregunta 8). La programación puede ser centralizada o distribuida; para activar una orden atrasada el banco elige la distribuida «ya que sirve como colchón para la recuperación» (pregunta 10)."),
        EXAM("**«¿Qué es una hoja de ruta?»** (17/03/2011). Respuesta: el documento que define la **secuencia de operaciones** de cada ítem fabricado, con el centro o máquina, el herramental y los tiempos (Morán, PAC §2.1). En la cátedra sale del **análisis del proceso** («origina la hoja de ruta del proceso (secuencia de operaciones)», pregunta 33) y su archivo tiene `nro_componente + nro_ruta + lef + nro_operacion + scrap` (pregunta 16). La hoja de ruta tiene una ruta por cada ítem padre; la estructura de producto, los ítems que tienen padre (pregunta 34)."),
        H("3. Fase 2: programación de las órdenes"),
        P("Asigna las órdenes liberadas a los centros y emite la **lista de despacho** (por día o por turno): qué trabajos hacer en cada centro, con orden, cantidad, centro anterior y posterior, fechas de comienzo y entrega, y horas remanentes. Objetivos de la programación de operaciones (Morán): cumplir las fechas de entrega, **minimizar el stock en proceso** reduciendo lead times y **maximizar la utilización** de equipos y personal. En un taller (job shop) se hace en dos fases: **carga de máquinas** y **secuenciamiento**."),
        P("Para modificar la capacidad en el corto plazo: horas extras, **rutas alternativas**, **superposición** (lote de transferencia), **división de operaciones** y **división del lote**. Con capacidad finita se usa simulación."),
        H("4. Reglas de prioridad (Chase cap. 19)"),
        T(["Regla", "Qué hace"], [
            ["FCFS", "primero en llegar, primero en atenderse"], ["SOT (SPT)", "primero el tiempo de operación más breve"], ["EDD", "primero el plazo más próximo"],
            ["STR", "menor tiempo ocioso restante = tiempo hasta el vencimiento − procesamiento restante"], ["STR/OP", "STR dividido por las operaciones restantes"],
            ["CR", "proporción crítica: (fecha de vencimiento − fecha actual) / días hábiles que quedan; primero la menor"], ["LCFS", "último en llegar, primero en atenderse"], ["Aleatorio", "a criterio del supervisor u operador"],
        ], "Chase, ilustración 19.3"),
        EJ("Chase, ejemplo 19.1: cinco trabajos en una fotocopiadora", [
            T(["Trabajo", "A", "B", "C", "D", "E"], [["Procesamiento (días)", "3", "4", "2", "6", "1"], ["Plazo (días)", "5", "6", "7", "9", "2"]]),
            T(["Regla", "Secuencia", "Tránsito total", "Tránsito promedio", "Retardo promedio"], [
                ["FCFS", "A B C D E", "50", "10,0", "4,6"], ["**SOT**", "E C A B D", "**36**", "**7,2**", "**2,4**"], ["EDD", "E A B C D", "39", "7,8", "2,4"],
                ["LCFS", "E D C B A", "46", "9,2", "4,0"], ["Aleatorio", "D C A E B", "53", "10,6", "5,4"], ["STR", "E A B D C", "43", "8,6", "3,2"],
            ], "Chase, ejemplo 19.1"),
            P("SOT da el menor tiempo de tránsito; FCFS es «justa» pero más lenta. Para varios trabajos en **dos máquinas en secuencia** se usa la **regla de Johnson**, que Chase desarrolla en el mismo capítulo."),
        ]),
        S("u6_reglas.svg", "Tiempo de tránsito promedio con cada regla (Chase, ejemplo 19.1; gráfico propio)"),
        H("5. Fase 3: control del progreso"),
        P("Cada vez que se completa un proceso de la hoja de ruta se registran cantidad de piezas, rechazo, operador, operación, centro y tiempo; se mantiene el archivo de **órdenes abiertas**. Informes: **estado de las órdenes** (dónde está, cuánto falta, si está atrasada, prioridad), **progreso** (cuántas se completaron en el período y cuántas no), **excepción** (atrasos, cantidades insuficientes; pueden ser diarios) y **consultas en línea**. El **control de la capacidad** compara entradas y salidas en horas (8 h al 80% = 6,40 h de salida planificada; Clase 6)."),
        H("6. Recolección de datos de planta"),
        T(["Método (Morán §3.2)", "A favor", "En contra"], [
            ["a) Hoja de recorrido (job traveler)", "el más simple; historia completa de la orden", "datos al final; sin control de errores; «el menos conveniente»"],
            ["b) Tarjeta de tiempos del operario", "simple; datos al fin de cada turno", "hay que sumarizar por departamento; informes días después; errores de anotación"],
            ["c) Vales por operación (arrancables)", "datos al terminar cada operación", "se pierden; carga manual; demora hasta el ingreso"],
            ["d) Terminal por departamento o planta", "muy usada en plantas por lotes; on-line u off-line", "el operario pierde tiempo yendo (colas); requiere validación"],
            ["e) Terminal por centro de trabajo", "estado frecuente; adaptada al centro", "costo de instalación; solo se justifica on-line"],
            ["f) Ingreso oral (voz)", "manos libres", "secuencias rígidas, pocas voces, vocabulario chico"],
            ["g) Monitoreo por computadora", "conexión directa con sensores; rastreo multinivel", "solo seguimiento: la decisión sigue siendo humana"],
        ]),
        P("**Identificación automática:** códigos de barras, cintas magnéticas, reconocimiento óptico, visión artificial. El más usado es el **código de barras**: reduce los errores de ingreso «en el orden de 1/3.000.000 con respecto al ingreso manual» y acelera la carga. (Se conecta con la codificación de la U3: el dígito verificador.)"),
    ]
    return clase("u6c12", "Clase 12 · Control de las actividades de producción", "Control de la producción (PAC)", "D",
                 "Funciones del PAC, lanzamiento de órdenes y sus documentos, hoja de ruta, lista de despacho, reglas de prioridad de Chase, control del progreso y métodos de recolección de datos de planta.",
                 "; ".join([PACN, CH(19, "627–631", "reglas de prioridad, ejemplo 19.1"), REPASO + " — preguntas 8, 10, 16, 33, 34", "texto/examenes/17_03_2011.txt (hoja de ruta)"]), t)


def integ():
    t = [
        P("**Unidad 6 · Cierre · Integrador · Ejercicios tipo examen**"),
        IDEA("**Idea central:** los ejercicios de la U6 son de cinco familias y cada una tiene un molde fijo. Reconocé la familia por el enunciado, escribí datos y unidades, seguí el molde y **cerrá interpretando** (los criterios de corrección piden «interpretación de los resultados» y «fundamentación»)."),
        T(["Familia", "Cómo la reconocés", "Molde", "Clase"], [
            ["**MRP**", "tabla ítem / padre / cantidad / stock / LT / scrap / LEC y un programa de entregas", "estructura y niveles → registro nivel por nivel → brutos (padres + independiente) → netos → lote → scrap → lanzamiento; informar atrasos", "7, 8, 9"],
            ["**Balanceo**", "unidades por turno, tareas con tiempos y predecesoras u operaciones en paralelo", "C → N_t → asignar con regla → eficiencia → ocioso; si una tarea > C, paralelo", "11"],
            ["**Plan agregado**", "demanda por período, capacidad normal, costos de extra, inventario y pendientes, stock inicial", "unidades extra inevitables → ubicarlas comparando costos → planilla → costo total → subsistemas", "2, 3"],
            ["**MPS**", "ventas confirmadas y pronóstico por mes", "demanda = pedidos + pronóstico (cátedra) → discutir el pronóstico → restricciones de tiempo → revisión", "4"],
            ["**Capacidad**", "máquinas en serie con factor de actividad y scrap, o una estación con turnos y rendimientos", "cantidades hacia atrás por scrap → tiempos efectivos → cuello de botella → acumulación y tiempo total; o CDT/CDR", "5, 6"],
        ]),
        S("u6_familias.svg", "Peso de cada familia de práctica de la U6 en los 19 finales fechados (conteos de patrones_examenes.md)"),
        H("1. Chequeo rápido por familia"),
        L(["**MRP:** ¿sumaste la demanda independiente a los brutos? ¿El componente común se neteó una sola vez, en su nivel más bajo? ¿Agrandaste por scrap **antes** de explotar? ¿Escribiste la convención de LEC y scrap? ¿Hay órdenes que caen antes del período 1?",
           "**Balanceo:** ¿C en las mismas unidades que las tareas? ¿Redondeaste N_t hacia arriba? ¿La eficiencia usa N reales? ¿El ocioso se pide por ciclo o por turno?",
           "**Plan agregado:** ¿el plan cumple la condición de cierre (stock final nulo)? ¿Justificaste por qué cada unidad extra va en ese período?",
           "**MPS:** ¿explicaste de dónde sale la demanda y qué hacés con un pronóstico viejo?",
           "**Capacidad:** ¿dividiste por el factor de actividad (o el RGE) para pasar de tiempo estándar a tiempo real?"]),
        H("2. Ejercicios para practicar (enunciados del material)"),
        EX("EJERCICIO — MRP de la mesa 30/04/2003", [
            P("Producto A y sus componentes (semanas):"),
            T(["Ítem", "Padre", "Cant.", "Stock", "Scrap", "LT", "Entregas"], [
                ["A", "—", "—", "90", "2%", "1", "340 semana 1"], ["B", "A", "1", "300", "2%", "2", "—"], ["C", "B", "2", "600", "3%", "2", "—"],
                ["D", "A y B", "1 y 2", "300", "3%", "2", "450 semana 1"], ["E", "A", "2", "600", "2,5%", "1", "—"],
            ], "SG!EVA, Examen 30/4/03 (tal cual el compilado)"),
            T(["Semana", "1", "2", "3", "4", "5", "6", "7", "8"], [["D (independiente)", "", "", "100", "", "", "100", "", ""], ["E (independiente)", "", "250", "", "550", "", "", "500", "750"]]),
        ], [
            P("**Pistas (no hay resolución en el material):** las entregas de la semana 1 no se pueden fabricar a tiempo (LT ≥ 1): se cubren con stock y lo que falta se **informa como atraso**. D es común (A × 1, B × 2) y además tiene demanda independiente y una entrega propia de 450. Aplicá la convención de scrap de la Clase 8 y escribila."),
        ], estado="para resolver"),
        EX("EJERCICIO — MRP mensual con «solo los primeros 400 B» (Ejercicios posibles)", [
            T(["Ítem", "Stock", "LEC", "Lead time", "Scrap"], [["A", "150", "400", "1 mes", "3%"], ["B", "200", "600", "2 meses", "2,5%"], ["D", "400", "800", "1 mes", "3%"], ["E", "80", "—", "—", "1,5%"]]),
            P("«Nota: Solo los primeros 400 B se armarán con la componente E. Se requiere producir 400 A en Octubre y 600 A para Diciembre. Además se requieren órdenes de 60 unidades de la componente D para Septiembre, 40 para Octubre y 50 para Noviembre. 2.1- Realizar el Plan de Requerimiento de Materiales, con stock de cierre.»"),
        ], [
            P("**Pistas:** el dibujo de la estructura no se conserva en el Drive (solo las marcas N=0, N=1, N=2 al costado de la tabla): escribí la estructura que suponés. «Solo los primeros 400 B» quiere decir que E tiene brutos **solo** por esos 400 (una efectividad o un cambio de ingeniería): después, B se arma sin E. Pedí siempre el **stock de cierre** de cada ítem."),
        ], estado="para resolver"),
        EX("EJERCICIO — Examen tipeado sin fecha (EFR p. 36; 45 minutos)", [
            P("«Dada la siguiente estructura de producto y la información asociada confeccionar el MRP.» En el árbol escaneado: **A** y **B** arriba; debajo, **2C** y **1D**; debajo de C, **−1E** (cantidad negativa); debajo de D, **2F** y **1E**."),
            T(["Ítem", "Stock", "Lead time", "LEC", "Scrap"], [["A", "50", "2", "150", "—"], ["B", "100", "1", "200", "2,5%"], ["C", "100", "2", "150", "1,5%"], ["D", "100", "1", "100", "—"], ["E", "200", "1", "100", "1,5%"], ["F*", "100", "2", "200", "4%"]], "EFR p. 36 (lead time en semanas)"),
            P("«*Solo para los primeros 400 productos independientes.» Requerimientos: **150 A para la semana 7 y 300 para la 9; 200 B para la 8 y 200 para la 10**. Ingresos programados: **250 C para la semana 6**. Teoría del mismo examen: productos tangibles y no tangibles; factor α del suavizado exponencial; inventario periódico; potencialidad de un código alfanumérico; cómo se usa la BOM."),
        ], [
            P("**Pistas:** las líneas del árbol escaneado no dejan claro si C cuelga solo de A o de A y B: escribí cuál suponés. El **−1E** es una cantidad negativa (C devuelve un E, como el «B × −2» de 2015): resta de los brutos de E. El ingreso de 250 C entra en el disponible de la semana 6. F se necesita solo para los primeros 400 productos finales: después deja de explotarse. No hay resolución en el material."),
        ], estado="para resolver"),
        EX("EJERCICIO — Dos máquinas, 3000 ítems y una línea para 5000 u/día (09/03/2006)", [
            P("M1 → depósito Q1-2 → M2. Factor combinado de actividad 0,80 y 0,80; tiempo estándar 19\" y 15\"; scrap 2,5% y 3,5%. «1- La cantidad máxima de semielaborados que se encontrarían en el depósito Q1-2, si se necesitan entregar 3000 ítems. […] 2- El tiempo de entrega para las 1000 unidades. 3- Cómo diseñaría la línea de producción para procesar 5000 unidades/día trabajando solo un turno de 8:00 hs.»"),
        ], [
            P("**Cálculo propio para arrancar:** M2 procesa 3000 / 0,965 = 3108,8 → **3109**; M1, 3109 / 0,975 = 3188,7 → **3189**. Tiempos efectivos 19/0,80 = **23,75 s** y 15/0,80 = **18,75 s**: M2 es más rápida, así que con transferencia unitaria el depósito casi no acumula; el máximo de diseño es el lote completo si M2 espera (3109). Para 5000 u/día en 8 h: C = 28.800/5000 = **5,76 s** → M1 necesita 23,75/5,76 = 4,1 → **5 máquinas en paralelo** y M2 18,75/5,76 = 3,3 → **4** (sin contar el scrap, que agrega 2,5% y 3,5% de carga)."),
        ], estado="cálculo propio"),
        H("3. Teoría de la U6 que cayó (para repasar en voz alta)"),
        T(["Pregunta", "Dónde está"], [
            ["Definir mediante una fórmula la capacidad de una estación de trabajo (2011, 2014)", "Clase 5"], ["Determinar la capacidad para una empresa (2012)", "Clases 5 y 6"],
            ["Variables que definen la capacidad de producción tangible (2013, 2015)", "Clase 5"], ["Hipótesis de listas de capacidad y perfiles de recursos (2018)", "Clase 6"],
            ["¿Qué es una hoja de ruta? (2011)", "Clase 12"], ["Sintetizar el algoritmo de MRP; módulos de un ERP (mesa de octubre)", "Clases 7 y 10"],
            ["Qué es MRP, MCP, ERP (2012); información de la BOM en un ERP (2014)", "Clases 7 y 10"], ["¿Cuándo una empresa JIT necesita MRP? (2018)", "Clase 10"],
            ["Hipótesis del TBO; demanda del MPS; subsistema que construye el PRM (bancos)", "Clases 9, 4 y 10"],
        ]),
        EXAM("**Para el día del examen:** el MRP es lo más probable (42% de los finales con fecha y vigente en 2013 y 2015). Practicá con tiempo: la consigna 2018 da 40 minutos para el ejercicio. Si te falta un dato o el enunciado es ambiguo (scrap, LEC, una cantidad negativa), **escribí el supuesto** y seguí."),
    ]
    return clase("u6int", "Integrador · Ejercicios tipo examen", "Integrador", "E",
                 "Las cinco familias de práctica de la U6 con su molde de resolución, el chequeo rápido, ejercicios de final para practicar y la teoría que cayó.",
                 "; ".join([PAT, EVA, EPOS, EFR(36, "examen tipeado sin fecha"), "texto/examenes/examen_2018_transcripcion.md"]), t)
