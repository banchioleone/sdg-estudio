from u5lib import *
from gen_u5_e import V10, V11, V7, V12

def c10():
    t = [
        P("**Sistemas de Gestión (UTN FRRo) · Unidad 5 · Bloque C · Clase 10 · Cadena de suministro y ubicación de plantas**"),
        AVISO("**De dónde sale esta clase.** **Chase cap. 10** (estrategia de la cadena de suministro) y **cap. 11** (logística y ubicación de instalaciones), más los formatos de distribución del **cap. 7**. El Documento Maestro asigna «almacenes, trazabilidad, ubicaciones y distribución de plantas, logística del abastecimiento, satisfacción del cliente» a Chase cap. 11 y a **Monks**; Monks no está en el material. Todo está **verificado contra el libro completo** (Chase 12a ed., del Drive), del que salen la fórmula del centroide (ilegible en el V6) y los Ejemplos 10.2, 11.1, 11.2 y 11.3. **No hay ejemplos con datos inventados.**"),
        IDEA("**Idea central:** la **logística integral** mira toda la cadena, desde la materia prima hasta el cliente final, como un solo sistema. En cada eslabón hay inventario y cada eslabón le cuesta a la empresa: hay que **sincronizarlos**, ubicar bien las plantas y almacenes y elegir cómo transportar."),
        H("1. La cadena de suministro y su medición"),
        P("Chase: el inventario «sirve como amortiguador, permitiendo que cada paso funcione de manera independiente de los demás», pero en cada etapa representa un costo, «por lo tanto, es importante que las operaciones estén sincronizadas para minimizar el tamaño de los inventarios de protección». La eficiencia de la cadena se mide por la **inversión en inventario** respecto del costo de lo que se suministra: **rotación** y **semanas de suministro** (fórmulas en la Clase 6)."),
        P("«El objetivo es tener la cantidad de inventario apropiada y en los lugares correctos de la cadena de suministro.»"),
        H("2. El efecto látigo"),
        P("Chase muestra (pañales descartables de Procter & Gamble) que los pedidos del detallista al mayorista varían más que las ventas al consumidor y los del mayorista a sus proveedores son los más volátiles. «Este fenómeno del aumento de la variabilidad al moverse del cliente al productor en la cadena de suministro se conoce a menudo como **efecto látigo**.» Indica **falta de sincronía**: en unas etapas se acumula inventario y en otras hay demoras y escasez."),
        S("u5_latigo.svg", "Efecto látigo (esquema propio)"),
        P("Una práctica que lo agrava: las **compras adelantadas** por promociones de precio (el detallista compra el suministro de un año en enero y la planta del proveedor hace horas extra desde octubre). Una que lo reduce: el **reabastecimiento continuo** de Campbell Soup: EDI con los detallistas, «precio bajo todos los días» sin promociones, reposición diaria entre límites de inventario pactados. Bajó el inventario del detallista de **4 a 2 semanas de suministro**; como al detallista mantener cuesta al menos 25% al año, ahorra ~1% de las ventas, sobre una ganancia típica de 2%."),
        H("3. Producto funcional o innovador, y la estrategia de la cadena"),
        T(["", "Productos funcionales", "Productos innovadores"], [
            ["Ejemplos (Chase)", "lo que se compra en supermercados y gasolinerías; necesidades básicas", "ropa de moda, computadoras personales"],
            ["Demanda", "estable y predecible", "impredecible"], ["Ciclo de vida", "largo", "unos pocos meses"], ["Margen", "bajo", "más alto"]],
            "Fisher, según Chase cap. 10"),
        P("Hau Lee agrega el lado del **suministro**: estable (tecnología madura, base de proveedores establecida) o evolutivo (tecnología temprana, proveedores poco confiables). Combinando demanda y suministro define cuatro estrategias:"),
        L(["**Eficientes:** máxima eficiencia de costos, sin actividades que no agregan valor, economías de escala.",
           "**Con riesgos compartidos:** reunir recursos y compartir, por ejemplo, el **inventario de seguridad** de un componente clave entre varias empresas o tiendas.",
           "**Responsivas:** flexibles ante necesidades cambiantes; fabricación sobre pedido y personalización masiva.",
           "**Ágiles:** responsivas y, a la vez, con riesgos compartidos."]),
        P("Herramientas para la incertidumbre que trata el capítulo: **subcontratación** (Clase 8), subcontratación globalizada, **producción en masa personalizada** y **aplazamiento** (postergar la diferenciación del producto hasta el último punto de la red: HP adaptaba las impresoras DeskJet en su centro de distribución de Alemania y no en la fábrica de Singapur)."),
        H("4. Decisiones de logística y transporte"),
        P("Chase cap. 11 (p. 385): decidir cómo transportar los bienes de las plantas a los clientes afecta el **costo**, la **velocidad de entrega** y la **flexibilidad**. Ahí da **seis** medios:"),
        T(["Medio", "Característica (Chase)"], [
            ["Carretera (camión)", "mucha flexibilidad; casi cualquier lugar no separado por agua"], ["Agua (barco)", "capacidad muy alta, costo muy bajo, tránsito lento; voluminosos (petróleo, carbón, químicos)"],
            ["Aire", "rápido pero costoso; artículos pequeños, livianos y caros"], ["Vías férreas", "bajo costo, tránsito largo y variable; depende de la infraestructura"],
            ["Ductos", "líquidos, gases y sólidos suaves; alto costo inicial, bajo costo por milla"], ["Entrega a mano", "último paso; lento y caro por la mano de obra"]]),
        AVISO("**¿Cinco o seis modos?** El mismo libro cuenta distinto: en el **cap. 10** (p. 370) dice «Hay **cinco** modos básicos de transporte: carretera, ferrocarril, agua, tubería y aire»; en el **cap. 11** (p. 385) suma la **entrega a mano** («el último paso en muchas cadenas de suministro») y son **seis**. Si te lo preguntan, nombrá los cinco y aclará que Chase agrega la entrega a mano como sexto."),
        P("Lo común son las soluciones **multimodales** con contenedores estandarizados. Para elegir, Chase usa la **densidad de valor** (valor por unidad de peso): para Intel, el envío aéreo de microprocesadores se justifica si el ahorro en tiempo de tránsito y en inversión en inventario compensa el mayor flete."),
        EJ("Ejemplo del libro · Chase, Ejemplo 10.2: ¿aéreo o terrestre? (cap. 10, p. 371–372)", [
            P("Envío de Bloomington (Indiana) a Littleton (Massachusetts). Costo de tener inventario: **30% al año** del valor del producto. **UPS terrestre tarda 8 días** y **FedEx aéreo, 2**: el aéreo ahorra **6 días** de inventario en tránsito."),
            F("\\text{Ahorro costo embarque} = \\text{Costo aéreo} - \\text{Costo terrestre} = \\frac{\\text{Valor artículo}\\times 0{,}30\\times 6}{365} \\;\\Rightarrow\\; \\text{Valor artículo} = \\frac{365\\times\\text{Ahorro}}{0{,}30\\times 6}", "punto de equilibrio (Chase)"),
            T(["Peso (libras)", "UPS 8 días", "FedEx 2 días", "Ahorro con UPS", "Valor de equilibrio", "Por libra"], [
                ["1", "3,30", "18,25", "14,95", "3031,53", "3031,53"],
                ["5", "4,30", "26,75", "22,45", "4552,36", "910,47"],
                ["10", "5,00", "36,75", "31,75", "6438,19", "643,82"]], "Chase, ilustración 10.10 (filas 1, 5 y 10 de 1 a 10 libras; dólares)"),
            P("Lectura: un paquete de 1 libra conviene mandarlo por aire si vale más de **3031,53 dólares**; uno de 10 libras, si vale más de 643,82 por libra. «Los artículos caros se envían por vía aérea … mientras que los de poco valor se mandan con el servicio más barato de vía terrestre.»"),
        ]),
        H("5. Ubicación de plantas y almacenes: criterios"),
        P("Criterios que lista Chase para ubicar una planta o un almacén:"),
        L(["**Proximidad con los clientes**.", "**Clima de negocios** (empresas similares, legislación, apoyo del gobierno local).",
           "**Costos totales**: regionales (terreno, construcción, mano de obra, impuestos, energía), de distribución interna y externa, y costos ocultos (mover material entre ubicaciones, perder capacidad de respuesta por lejanía).",
           "**Infraestructura** (transporte, energía, telecomunicaciones).", "**Calidad de la mano de obra**.", "**Proveedores** competitivos y cercanos (apoyan la manufactura esbelta).",
           "**Otras instalaciones** de la misma compañía.", "**Zonas de libre comercio**.", "**Riesgo político**.", "**Barreras gubernamentales**.", "**Bloques comerciales**.",
           "**Regulaciones ambientales**.", "**Comunidad anfitriona**.", "**Ventaja competitiva** (dónde poner la sede de cada negocio, según Porter)."]),
        H("6. Métodos de ubicación"),
        P("Chase presenta tres técnicas (y una cuarta para servicios):"),
        L(["**Sistema de calificación de factores:** a cada factor se le asigna un rango de puntos, se califica cada sitio y se elige el de más puntos. Ejemplo de una refinería: combustibles en la región 0–330, energía 0–200, clima laboral 0–100, condiciones de vida 0–100, transportes 0–50, agua 0–10, clima 0–50, suministro 0–60, políticas y leyes fiscales 0–20. Problema: no refleja cuánto difieren los **costos** de un factor a otro; Chase sugiere ponderar con los desvíos estándar de los costos.",
           "**Método de transporte de la programación lineal:** minimizar el costo de enviar n unidades a m destinos (o maximizar la utilidad). Se resuelve con Solver de Excel.",
           "**Método del centroide:** ubica almacenes intermedios o de distribución (y torres de comunicación) considerando las instalaciones existentes, sus distancias y los volúmenes a enviar. Supone costos de entrada y salida iguales.",
           "**Servicios:** se usan técnicas estadísticas (regresión múltiple) para maximizar el potencial de utilidades de cada sitio, no para minimizar costos."], True),
        F("C_x = \\frac{\\sum d_{ix}\\,V_i}{\\sum V_i} \\qquad C_y = \\frac{\\sum d_{iy}\\,V_i}{\\sum V_i}", "centroide (Chase) · d = coordenada de la i-ésima ubicación · V = volumen enviado"),
        P("Donde (Chase, p. 394): $C_x$, $C_y$ = coordenadas del centroide; $d_{ix}$, $d_{iy}$ = coordenadas de la i-ésima ubicación; $V_i$ = «volumen de los bienes movidos a o de la i-ésima ubicación»."),
        EJ("Ejemplo del libro · Chase, Ejemplo 11.2: HiOctane Refining Company (p. 394)", [
            P("HiOctane necesita ubicar una instalación intermedia entre su refinería de **Long Beach** y sus principales distribuidores. Coordenadas y volumen enviado (millones de galones de gasolina al mes):"),
            T(["Ubicación", "x", "y", "V"], [["Long Beach (planta)", "325", "75", "1500"], ["Anaheim", "400", "150", "250"], ["La Habra", "450", "350", "450"], ["Glendale", "350", "400", "350"], ["Thousand Oaks", "25", "450", "450"]], "Chase, ilustración 11.5"),
            F("C_x = \\frac{325\\cdot 1500 + 400\\cdot 250 + 450\\cdot 450 + 350\\cdot 350 + 25\\cdot 450}{3000} = \\frac{923\\,750}{3000} = 307{,}9"),
            F("C_y = \\frac{75\\cdot 1500 + 150\\cdot 250 + 350\\cdot 450 + 400\\cdot 350 + 450\\cdot 450}{3000} = \\frac{650\\,000}{3000} = 216{,}7"),
            P("El centroide queda cerca de **(308, 217)**: «un punto de inicio para buscar un nuevo sitio». Chase agrega que quizá convenga enviar directo de Long Beach a Anaheim y recalcular el centroide sin Anaheim."),
            AVISO("En la tabla de la ilustración 11.5 el volumen de Thousand Oaks figura como **45**, pero la cuenta del libro usa **450** (por eso el total es 3000). Me quedo con 450, que es lo que cierra."),
        ]),
        EJ("Ejemplo del libro · Chase, Ejemplo 11.1: U. S. Pharmaceutical, método de transporte (p. 390–392)", [
            P("Cuatro fábricas surten los almacenes de cuatro clientes; se busca el programa de envíos de **costo mínimo** para la producción mensual. Costo de envío por caja (dólares), suministro y demanda:"),
            T(["De / A", "Columbus", "St. Louis", "Denver", "Los Ángeles", "Suministro"], [
                ["Indianápolis", "25", "35", "36", "60", "15"], ["Phoenix", "55", "30", "25", "25", "6"],
                ["Nueva York", "40", "50", "80", "90", "14"], ["Atlanta", "30", "40", "66", "75", "11"],
                ["Demanda", "10", "12", "15", "9", "46"]], "Chase, ilustraciones 11.2 y 11.3"),
            P("Chase lo plantea en una hoja de cálculo y lo resuelve con **Solver**: celda objetivo = costo total (**mínimo**); celdas cambiantes = cantidades enviadas; restricciones: lo enviado a cada cliente **=** su demanda y lo enviado desde cada fábrica **≤** su capacidad."),
            P("*Solución (cálculo propio; en el libro el resultado está en una pantalla de Excel que no se lee en el texto):* Indianápolis → Denver 15; Phoenix → Los Ángeles 6; Nueva York → Columbus 9 y St. Louis 5; Atlanta → Columbus 1, St. Louis 7 y Los Ángeles 3. **Costo mínimo: 1835 dólares** (puede haber otra asignación con el mismo costo)."),
        ]),
        EJ("Ejemplo del libro · Chase, Ejemplo 11.3: ubicar hoteles con regresión (p. 395–396)", [
            P("Una cadena hotelera juntó datos de **57 sitios existentes** y buscó qué variables se correlacionan con la utilidad operativa a dos años. El modelo de regresión final:"),
            F("\\text{Utilidad} = 39{,}05 - 5{,}41\\,(\\text{población del estado por hotel}) + 5{,}86\\,(\\text{precio del hotel}) - 3{,}91\\,\\sqrt{\\text{ingreso mediano del área}} + 1{,}75\\,(\\text{universitarios a cuatro millas})", "Chase, Ejemplo 11.3 (población e ingreso en miles)"),
            P("Lectura de Chase: la utilidad baja con la **penetración de mercado**, sube con el **precio**, baja con **ingresos altos** («los hoteles funcionan mejor en áreas con ingresos medianos bajos») y sube con **universidades cercanas**. Es la **regresión múltiple de la U2** aplicada a ubicación: en servicios se maximiza la utilidad del sitio, no se minimiza el costo."),
        ]),
        H("7. Distribución de planta (formatos)"),
        P("La distribución **dentro** de la instalación la define el patrón de flujo del trabajo. Chase (cap. 7) da cinco estructuras básicas:"),
        T(["Formato", "Cómo es (Chase)", "Ejemplos"], [
            ["**Proyecto** (posición fija)", "el producto queda fijo por su volumen o peso; el equipo va al producto", "obras, casas, caminos, sets de filmación"],
            ["**Centro de trabajo** (taller, por proceso)", "se agrupan equipos o funciones similares; la pieza pasa de un centro a otro", "todas las perforadoras en un área, las troqueladoras en otra"],
            ["**Celda de manufactura**", "área dedicada a productos con procesamiento similar; produce «conforme se necesita»", "familias de piezas"],
            ["**Línea de ensamble** (por producto)", "procesos ordenados según los pasos sucesivos; ritmo controlado", "juguetes, electrodomésticos, autos"],
            ["**Proceso continuo**", "como una línea pero con flujo continuo; muy automatizado, 24 horas", "petróleo, químicos, fármacos"]]),
        P("Se eligen con la **matriz producto-proceso** (volumen y estandarización). El balanceo de líneas (estaciones en paralelo, tiempo ocioso) se ve en la U4."),
        H("8. Logística del abastecimiento y logística integral"),
        P("**Complemento (síntesis propia del material):** la **logística del abastecimiento** (o de entrada) cubre lo que va del proveedor a la planta: compras, transporte de entrada, recepción, almacén de materias primas y la reposición con los modelos de stock. La **logística interna** mueve el material dentro de la planta (distribución en planta, WIP). La **logística de distribución** (de salida) va de la planta al cliente: almacenes, CD, DRP y transporte. La **logística integral** las trata como un único sistema, que es lo que pide el objetivo del programa."),
        G("9. Glosario", "", [
            ["Efecto látigo", "", "Aumento de la variabilidad de los pedidos aguas arriba de la cadena"],
            ["Semanas de suministro", "", "Inventario promedio / costo de lo vendido × 52"],
            ["Aplazamiento", "", "Diferenciar el producto lo más tarde posible en la red"],
            ["Densidad de valor", "", "Valor por unidad de peso; guía el modo de transporte"],
            ["Centroide", "", "Ubicación que minimiza el costo de transporte ponderado por volumen"],
            ["Matriz producto-proceso", "", "Relaciona volumen y estandarización con el formato de distribución"],
        ]),
    ]
    src = [CH(10, "360–372", "medición, Fisher y Lee, densidad de valor, Ejemplo 10.2"), CH(11, "385–396", "modos de transporte, métodos de ubicación, Ejemplos 11.1–11.3"), V10, V11, V7, V12, PROG, DM]
    return clase("u5c10", "Clase 10 · Cadena de suministro y ubicación de plantas", "Cadena de suministro y ubicación de plantas", "C",
                 "La logística integral: medir la cadena, el efecto látigo, qué cadena le conviene a cada producto, modos de transporte, criterios y métodos para ubicar plantas y almacenes, y los formatos de distribución de planta.",
                 src, t, "Integrador · Ejercicios tipo examen", ["u5/img/u5_latigo.svg"])


def integ():
    t = [
        P("**Sistemas de Gestión (UTN FRRo) · Unidad 5 · Cierre · Integrador · Ejercicios tipo examen**"),
        AVISO("**Qué es esta página.** Una guía para practicar: **todas las familias de ejercicios de inventarios** que aparecen en el material, con la consigna resumida, el **camino de resolución** y dónde está resuelta en estas clases. Los resultados son los verificados en cada clase (resoluciones manuscritas corregidas o cálculo propio, según se indica allí)."),
        IDEA("**Idea central:** casi todo ejercicio de inventarios se resuelve con cinco preguntas: **¿qué modelo?** (perpetuo/periódico, con o sin incertidumbre, con o sin descuento), **¿cuánto pedir?** ($Q^*$), **¿cuándo?** (PP o T), **¿cuánto de seguridad?** (z·σ) y **¿quién lo hace?** (subsistemas)."),
        H("1. Mapa de decisión"),
        T(["Si el enunciado dice…", "Usá", "Clase"], [
            ["demanda anual constante y entrega cierta", "EOQ $Q^* = \\sqrt{2DS/H}$ y $R = \\bar d L$", "2"],
            ["«ordena X unidades… porcentaje de variación respecto de la óptima»", "EOQ + comparar costos de pedir y mantener", "2"],
            ["tabla de precios por cantidad", "EOQ por precio + factibilidad + quiebres", "3"],
            ["demanda diaria normal N(μ, σ), nivel de servicio", "perpetuo con SS: $R = \\bar d L + z\\sigma_d\\sqrt L$", "5"],
            ["«se revisa cada…», «cada T días»", "periódico: $q = \\bar d (T+L) + z\\sigma_{T+L} - I$", "6"],
            ["compra única, costo de sobrar y de faltar", "período único: $P \\leq C_u/(C_o+C_u)$", "6"],
            ["clases A/B/C y frecuencias de conteo", "plan de conteo: Σ(ítems × veces)/días", "7"],
            ["«mayor incidencia de…», «X% del capital»", "ABC con el criterio pedido y % acumulado", "7"],
            ["«indicar subsistemas participantes»", "gestión de stock / almacenes, compras, recepción, calidad, contable", "1 y 5"]]),
        H("2. Familias de práctica"),
        EX("A · Sistema perpetuo con stock de seguridad (el más tomado)", [
            P("Demanda diaria N(50,10), LT 3 días, $6 por pedido, 20% TEA, $1,2, NS 85%, 200 días (variantes: N(60,10) 90% 200 días; N(85,10) 85% 240 días). «Definir, confeccionar y calcular» + subsistemas."),
        ], [
            T(["Variante", "Q*", "z (tabla)", "SS", "PP"], [["N(50,10), 85%, 200 d", "≈707", "1,04", "18", "168"], ["N(60,10), 90%, 200 d", "≈775", "1,28", "22", "202"], ["N(85,10), 85%, 240 d", "≈1010", "1,04", "18", "273"]]),
            P("Desarrollo completo y comparación con las hojas en la **Clase 5** (ojo con el error de unidades de algunas hojas en $Q^*$)."),
        ]),
        EX("B · EOQ con descuentos (librería)", [
            P("600 cajas/año, $16 por orden, 36% anual, precios $7,50 / $7,35 / $7,00 con quiebres en 50 y 100."),
        ], [P("Óptimo en el quiebre: **Q = 100 cajas**, CT ≈ $7,37 por caja; PP = 50 cajas. Variante con 20%: Q ≈ 117. Desarrollo en la **Clase 3**.")]),
        EX("C · Variación respecto del óptimo (IMBA / TT)", [
            P("150.000 ítems/año, pide 40.000, $40 por pedido, 20% de $0,15."),
        ], [P("$Q^* = 20.000$; pide el doble (+100%); cuesta **$150/año más** (+25%). **Clase 2**.")]),
        EX("D · Política de abastecimiento (BIT-Kaffee, bar, hospital, Ingap)", [
            P("Datos de consumo anual, costo de orden, % de manejo, precio y demora de entrega."),
        ], [T(["Caso", "Q*", "PP", "Otro"], [["BIT-Kaffee (7500 cajas)", "250", "150", "T ≈ 8 días"], ["Bar (730 cajas)", "78", "15", ""], ["Hospital (500 kg)", "200 kg", "—", "precio ≈ $2,08/kg"], ["Ingap SA (120 vasos/día)", "≈1018", "240", "ahorro ≈ $386/año vs. comprar cada 30 días"]]),
            P("Desarrollo en la **Clase 2**.")]),
        EX("E · EOQ con faltantes", [P("1000 u/año, $10 por orden, $10 mantener, $40 por faltante. ¿Qué existencia está justificada?")],
           [P("Con el modelo de pedidos pendientes (complemento): Q = 50, **existencia máxima 40**. **Clase 2**.")], estado="cálculo propio"),
        EX("F · Plan de conteo ABC", [P("EBS 6400 artículos (400 A ×5, 1000 B ×2, 5000 C ×1, 250 días); plan de 6300 elementos con dos operarios (95% y 80%, 6 h); despejar las veces de las A.")],
           [P("EBS: **36 artículos/día** (3 h con 5 min c/u). Plan 6300: **90/día**, capacidad 126/día, **3 h ociosas**. Veces de las A con 36/día y 200 días: **0,5 por año**. **Clase 7**.")]),
        EX("G · ABC por incidencia de mano de obra", [P("Vender el 50% del capital inmovilizado tomando los ítems de mayor incidencia de MO (tabla de 20 ítems).")],
           [P("Ordenar por MO/costo primo y acumular cantidad × costo primo: **12 ítems** (003, 004, 041, 036, 020, 051, 002, 040, 021, 038, 035, 037) = 50,5%. **Clase 7**.")]),
        H("3. Teoría y multiple choice"),
        EX("H · Preguntas de teoría que circulan", [
            L(["«Analice la aplicación de un sistema de gestión de inventarios periódicos y ejemplifique» (EFR p.36) → **Clase 4**.",
               "Tipo de control para alimentos frescos, diario, combustible, medicamentos, papel moneda (multiple choice; lo tomó Feraboli el 14/03/2013) → **Clase 4**. Es casi igual a la **pregunta de repaso 9 de Chase** (ejercicio I).",
               "«Cada tipo de material requiere un método de gestión…» (independientes con MRP / indirectos solo perpetuo / críticos con periódico / consumibles con orden abierta) → **Clase 4** (ojo con la marca que circula).",
               "Materiales directos e indirectos, órdenes abiertas y cerradas, etapas de compras, archivos, evaluación de proveedores (Examen 2005) → **Clase 8**.",
               "«EOQ en multiple choice» (SG-PreguntasTeoria-V1.0: «3 Múltiple Choice, uno sobre EOQ otro sobre BOM y otro sobre JIT»): no está el enunciado; repasá supuestos y fórmula → **Clase 2**.",
               "Concepto de inventario según TOC → **Clase 1** (sin definición de la cátedra en el material)."]),
        ], nota="Las respuestas están desarrolladas en las clases indicadas. No hay claves oficiales en el material.", estado="ver clases"),
        H("4. Práctica extra con el libro (Chase cap. 17, p. 578–587)"),
        P("El libro completo (Chase 12a ed., del Drive) trae **11 preguntas de repaso** y **33 problemas** al final del capítulo de inventarios. No son de la cátedra, pero sirven para practicar los mismos modelos. Los que más se parecen a lo que se tomó: la **pregunta 9** y los **problemas 9 y 18**."),
        EX("I · ★ Pregunta de repaso 9 (es el multiple choice de la cátedra)", [
            P("«¿Qué tipo de sistema de inventarios utilizaría en las situaciones siguientes? a) Abastecer su cocina con alimentos frescos. b) Obtener un periódico todos los días. c) Comprar gasolina para su auto. ¿A cuál de estas piezas le asigna el costo de faltantes más elevado?»"),
        ], nota="Es casi la misma consigna del multiple choice de «tipo de control» que tomó Feraboli (14/03/2013). Resolvelo con la Clase 4 (perpetuo o periódico, y por qué) y la Clase 6 (período único para el diario). El libro no da la respuesta.", estado="para resolver"),
        EX("J · Las otras preguntas de repaso (p. 578)", [
            L(["1. Demanda dependiente e independiente en un McDonald's, un fabricante de copiadoras y una compañía de suministros farmacéuticos → Clase 1.",
               "2. Inventario en proceso, de seguridad y estacional → Clases 1 y 5.", "3. Naturaleza de los costos que afectan el tamaño del inventario → Clases 1 y 2.",
               "4. ¿Cuándo elegir cantidad fija en lugar de período fijo? Desventajas del período fijo → Clase 4.",
               "5. Procedimiento con reducciones de precio; ¿cambia si el costo de mantener es un porcentaje del precio? → Clase 3.",
               "6. Preguntas básicas que responde una regla de decisión de inventarios → Clase 0 (cuándo y cuánto pedir).",
               "7. Supuestos de los costos de preparación, pedido y manejo; ¿qué tan válidos son? → Clase 2.",
               "8. «Lo bueno de los modelos de inventarios es que puede tomar uno predeterminado y aplicarlo siempre…» Comente → Clases 2 y 4.",
               "10. ¿Por qué clasificar en grupos, como en el ABC? → Clase 7.", "11. Política para mejorar los inventarios de una tienda departamental → Clase 6 (servicios)."]),
        ], nota="Respuestas en las clases indicadas; el libro no trae clave.", estado="para resolver"),
        EX("K · ★ Problema 9: EOQ y descuento por pedido (p. 579–580)", [
            P("«La demanda de una pieza es de 1000 unidades al año. Cada pedido hecho cuesta 10 dólares; el costo anual de manejar las piezas en el inventario es de 2 dólares cada uno. a) ¿Qué cantidad se debe pedir? b) Suponiendo que hay un descuento de 100 dólares por pedido si se piden 500 unidades o más. ¿Se deben hacer pedidos de 500 piezas o es necesario apegarse a la decisión tomada en a)?»"),
        ], [
            AVISO("**Cálculo propio** (el libro no publica la respuesta). Interpreto el descuento como 100 dólares menos **por cada pedido** de 500 o más."),
            F("a)\\; Q^* = \\sqrt{\\frac{2\\cdot 1000\\cdot 10}{2}} = 100 \\qquad \\frac{1000}{100}\\cdot 10 + \\frac{100}{2}\\cdot 2 = 100 + 100 = 200 \\text{ dólares/año}"),
            F("b)\\; Q = 500:\\; \\frac{1000}{500}\\cdot 10 + \\frac{500}{2}\\cdot 2 - 2\\cdot 100 = 20 + 500 - 200 = 320 \\text{ dólares/año}"),
            P("Pedir 500 cuesta más (320 contra 200): **conviene seguir pidiendo 100**. Es el mismo razonamiento que la familia IMBA (Clase 2) y la librería (Clase 3): comparar costos totales del óptimo y de la alternativa."),
        ], estado="cálculo propio"),
        EX("L · ★ Problema 18: período fijo con 98% (p. 581)", [
            P("«La demanda diaria de un producto es de 60 unidades con una desviación estándar de 10 unidades. El periodo de revisión es de 10 días y el tiempo de entrega de dos días. En el momento de la revisión, hay 100 unidades en existencia. Si se desea una probabilidad de servicio de 98%, ¿cuántas unidades hay que pedir?»"),
        ], [
            AVISO("**Cálculo propio** (el libro no publica la respuesta)."),
            F("\\sigma_{T+L} = 10\\sqrt{12} = 34{,}64 \\qquad z_{98\\%} = 2{,}05 \\qquad q = 60\\cdot 12 + 2{,}05\\cdot 34{,}64 - 100 \\approx 691 \\text{ unidades}"),
            P("Es la familia «demanda normal» de los finales (Clase 5) pero con revisión periódica (Clase 6): misma media diaria de 60 y desvío de 10 que la variante N(60,10)."),
        ], estado="cálculo propio"),
        EX("M · Otros problemas del capítulo con respuesta en el libro (Apéndice A, p. 739)", [
            L(["**5.** Charlie's Pizza: pedido cada 4 semanas, entrega 3 semanas, 150 libras/semana con desvío 30, 98%, hay 500 libras → respuesta del libro: **q = 713**.",
               "**8.** Jill's Job Shop: Tegdiws por punto de pedido y Widgets cada 3 semanas → respuestas del libro: **a) Q = 1225, R = 824; b) q = 390 − existencias en inventario**.",
               "**12.** Elemento X: 2000 unidades/año, 25 dólares cada una, almacenamiento 5 dólares por unidad, pedido 10 dólares → respuestas del libro: **a) Q = 89; b) 224,72 dólares; c) 222,50 dólares**.",
               "**14.** Materia prima a 20, 19 o 18 dólares por libra (menos de 100, 100 a 1000, más de 1000), pedido 40 dólares, demanda 3000, manejo 25% → descuentos, Clase 3 (sin respuesta en el libro)."]),
        ], nota="Usá las respuestas del libro para autocorregirte. Los enunciados completos están en drive_u5/txt/cap17_chase12.txt.", estado="para resolver"),
        EXAM("**Cómo se presenta un ejercicio de inventarios en el final:** 1) datos y supuestos (unidades: días/año, i anual); 2) modelo elegido y por qué; 3) cálculos con fórmula escrita; 4) **política** en una frase («pedir Q cuando la posición llegue a R»); 5) subsistemas y qué hace cada uno. Las hojas resueltas de la cátedra siguen ese orden."),
    ]
    src = [EVA, PAT, "texto/ocr/INVENTARIO_OCR.md", PA, MC, "texto/examenes/SG-PreguntasTeoria-V1.0.txt", "texto/examenes/Preguntas de teoria del final de SG1.txt (final de Feraboli del 14/03/2013)",
           EFR(36, "examen tipeado"), CH(17, "578–587", "preguntas de repaso y problemas"), "drive_u5/txt/administracionOperaciones.txt — Apéndice A, p. 739 (respuestas a problemas seleccionados del cap. 17)"]
    return clase("u5int", "Integrador · Ejercicios tipo examen", "Integrador de la U5", "D",
                 "Todas las familias de ejercicios de inventarios que cayeron en finales, con la consigna, el camino de resolución, los resultados y la clase donde está desarrollado cada uno.",
                 src, t, None)
