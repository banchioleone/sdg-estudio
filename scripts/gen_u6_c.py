from u6lib import *

W12 = [str(i) for i in range(1, 13)]


def c7():
    t = [
        P("**Unidad 6 · Bloque C · Clase 7 · MRP: la lógica del registro**"),
        IDEA("**Idea central:** el MRP toma el MPS, la estructura del producto, los lead times, el stock y las órdenes en curso, y calcula **para cada pieza y cada período**: necesidades brutas → stock proyectado → necesidades netas → órdenes planificadas adelantadas el lead time. Después baja un nivel y repite."),
        H("1. Qué es y cuándo sirve"),
        P("Morán: el MRP «obtiene las necesidades de cada una de las partes (conjuntos, subconjuntos, piezas o materias primas), en cada período de planificación, para cumplir con las cantidades de los productos finales fijadas en el Plan Maestro de Producción». Es «un sistema de gestión de las existencias para la **demanda dependiente**»: las necesidades no se pronostican, se **calculan** a partir del MPS. Es útil cuando el producto es compuesto, y «tanto más importante cuanto más compleja sea la estructura» y más amplia la variedad. Es aplicable a la **producción por lotes**."),
        L(["El **período** (semana, día) es la unidad de los lead times.", "El **horizonte** debe ser por lo menos igual al plazo acumulado de provisión y producción del artículo que más tarda.",
           "Se actualiza **período a período con horizonte deslizante**. El primer período es el **período de acción**: solo se liberan las órdenes de ese período."]),
        T(["Entradas (Morán)", "Salidas (Morán)"], [
            ["Programa maestro de producción", "órdenes de producción y compra del período de acción"],
            ["Estructura de los productos", "órdenes para períodos futuros"],
            ["Lead times de provisión y fabricación, en períodos", "reprogramaciones (cambios de fecha de órdenes emitidas)"],
            ["Existencias disponibles de cada parte", "cancelaciones por cambios en el MPS"],
            ["Órdenes de producción y compra en curso, con fecha", "informes de estado, de resultados y de excepción; existencias futuras"],
        ]),
        H("2. La estructura del producto (BOM)"),
        P("Especifica, por niveles: **nivel 0** producto terminado; niveles 1 a n−2 subconjuntos; nivel n−1 piezas de producción propia; **nivel n** partes compradas, y la cantidad con que cada componente entra en su **padre** (el nivel inmediato superior). Se expresa con la **lista de materiales** (BOM: Bill of Materials), indentada o en forma padre–componente–cantidad, o como **árbol**."),
        S("u6_bom_x.svg", "Ejemplo de Morán: X = 1 A + 2 B; A = 1 C + 3 D (todas las piezas se compran). Dibujo propio con los datos de la nota técnica"),
        T(["Ítem", "Padre", "Cantidad en el padre"], [["A", "X", "1"], ["B", "X", "2"], ["C", "A", "1"], ["D", "A", "3"]], "Lista de materiales padre–componente (Morán)"),
        H("3. El registro MRP y sus fórmulas"),
        T(["Fila", "Definición (Morán)"], [
            ["**Requerimientos brutos** $Q_{t,j}$", "demanda del ítem j en el período t. Para productos finales salen del MPS; para los demás, de las órdenes planificadas de los padres"],
            ["**Ingresos programados** $P_{t,j}$", "cantidad ya ordenada que ingresa al comienzo del período t (una orden ya liberada)"],
            ["**Disponible** $S_{t,j}$", "existencia esperada al final del período t; si es negativa, hay faltante"],
            ["**Requerimientos netos** $N_{t,j}$", "lo que hay que proveer al comienzo de t"],
            ["**Órdenes planificadas** $R_{t,j}$", "los netos adelantados el lead time; se pueden agrandar a un lote"],
        ]),
        F(r"Q_{t,j} = R_{t,k} \cdot q_{j,k} \qquad S_{t,j} = S_{t-1,j} + P_{t,j} - Q_{t,j} \qquad R_{t,j} = N_{t+L_j,\,j}", "q_{j,k} = cantidad del ítem j en una unidad del padre k; L_j = lead time de j"),
        P("Los **netos** se calculan acumulando: en cada período, si el disponible es negativo y lo ya pedido no alcanza, el neto es lo que falta: $N_t = -S_t - Nacum_{t-1}$. Así no se pide dos veces el mismo faltante. Cuando una orden planificada **se libera**, se convierte en ingreso programado en el período de la necesidad."),
        L(["Determinar los requerimientos brutos de cada ítem en cada período.", "Determinar los netos, con las existencias y los ingresos programados.",
           "Con los lead times, determinar las órdenes planificadas.", "Pasar al nivel inferior y repetir.", "Liberar las órdenes del período de acción."], True),
        P("Esos son los cinco pasos de Morán. La mesa especial de octubre preguntó justamente «Sintetizar el algoritmo de cálculo de MRP»."),
        H("4. Ejemplo resuelto de Morán: producto X"),
        EJ("Planificación al comienzo del período 1", [
            P("Lead times: X 1 semana; A, B, C y D 2 semanas. Stock inicial: X 20, A 10. Ingresos programados en la semana 1: X 50, C 30, D 100. El MPS pide X: 50 en la semana 1, 50 en la 4 y 60 en las semanas 6, 8, 10 y 12."),
            T(["Producto X (LT 1)", *W12], [
                ["Brutos", "50", "", "", "50", "", "60", "", "60", "", "60", "", "60"],
                ["Ingr. programados", "50", "", "", "", "", "", "", "", "", "", "", ""],
                ["Disponible (S₀ = 20)", "20", "20", "20", "−30", "−30", "−90", "−90", "−150", "−150", "−210", "−210", "−270"],
                ["Netos", "", "", "", "30", "", "60", "", "60", "", "60", "", "60"],
                ["**Órd. planificadas**", "", "", "**30**", "", "**60**", "", "**60**", "", "**60**", "", "**60**", ""],
            ]),
            T(["Conjunto A (1 por X, LT 2)", *W12], [
                ["Brutos", "", "", "30", "", "60", "", "60", "", "60", "", "60", ""],
                ["Disponible (S₀ = 10)", "10", "10", "−20", "−20", "−80", "−80", "−140", "−140", "−200", "−200", "−260", "−260"],
                ["Netos", "", "", "20", "", "60", "", "60", "", "60", "", "60", ""],
                ["**Órd. planificadas**", "**20**", "", "60", "", "60", "", "60", "", "60", "", "", ""],
            ]),
            P("Los brutos de A son las órdenes de X (× 1). Los de B son las órdenes de X × 2 (60, 120, 120, 120, 120 en las semanas 3, 5, 7, 9, 11) y, sin stock, B planifica **60 en la semana 1**. Los brutos de C son las órdenes de A × 1 (20 en la semana 1) y los de D, × 3 (60 en la semana 1)."),
            T(["Pieza", "Brutos sem. 1", "Ingr. sem. 1", "Disponible sem. 1", "Primer neto", "Orden a liberar en la sem. 1"], [
                ["C (1 por A)", "20", "30", "10", "50 en la sem. 3 (60 − 10)", "**50**"],
                ["D (3 por A)", "60", "100", "40", "140 en la sem. 3 (180 − 40)", "**140**"],
            ]),
            P("**Órdenes del período de acción:** A 20, B 60, C 50 y D 140. Al liberarlas, pasan a ingresos programados (A 20 en la semana 3, B 60 en la 3, C 50 en la 3, D 140 en la 3) y el resto sigue como planificado hasta la próxima corrida."),
        ]),
        S("u6_registro_mrp.svg", "Cómo se lee el registro: brutos, disponible, netos y la orden adelantada el lead time (esquema con el producto X de Morán)"),
        H("5. Ejemplo resuelto de Chase: focos de Juno (ejemplo 18.1)"),
        EJ("Dos focos y un casquillo común", [
            P("VH1: stock 85, lote 200, LT 1. VH2: stock 358, lote 400, LT 1. Casquillo (1 por foco): stock 425, compra de 500, LT 3, stock de seguridad 20, ingreso programado de 500 en la semana 1."),
            T(["", "1", "2", "3", "4", "5", "6", "7", "8"], [
                ["VH1 brutos", "34", "37", "41", "45", "48", "48", "48", "48"],
                ["VH1 disponible", "51", "14", "173", "128", "80", "32", "184", "136"],
                ["VH1 expedición", "", "**200**", "", "", "", "**200**", "", ""],
                ["VH2 brutos", "104", "134", "144", "155", "134", "140", "141", "145"],
                ["VH2 disponible", "254", "120", "376", "221", "87", "347", "206", "61"],
                ["VH2 expedición", "", "**400**", "", "", "**400**", "", "", ""],
                ["Casquillo brutos", "", "600", "", "", "400", "200", "", ""],
                ["Casquillo disponible (− SS)", "905", "305", "305", "305", "405", "205", "205", "205"],
                ["Casquillo expedición", "", "**500**", "", "", "", "", "", ""],
            ], "Chase, ejemplo 18.1"),
            P("Fijate en el casquillo: sus brutos son las **expediciones** de VH1 y VH2 (600 = 200 + 400 en la semana 2). El disponible arranca en 425 + 500 − 20 = 905 porque Chase descuenta el stock de seguridad. En la semana 5 faltan 95 → se recibe un lote de 500 en la 5 y, con LT 3, se pide en la **semana 2**."),
            AVISO("**Errata del libro:** la tabla de la solución dice «OH = 385» para VH2, pero el enunciado da **358** y el disponible de la semana 1 (358 − 104 = 254) confirma 358."),
        ]),
        G("Vocabulario del registro", "Cómo nombran lo mismo Morán, Chase y la cátedra.", [
            ("Brutos", "requerimientos brutos", "Chase: necesidades brutas"),
            ("Ingr. prog.", "ingresos programados", "Chase: entradas programadas; órdenes ya liberadas"),
            ("Disponible", "existencia proyectada", "Chase: saldo disponible proyectado"),
            ("Netos", "requerimientos netos", "Chase: necesidades netas"),
            ("Órd. planif.", "órdenes planificadas", "Chase: expedición de pedidos planeados (y la «entrada» es la recepción)"),
            ("PMCC / PMCF", "plan maestro de componentes compradas / fabricadas", "lo que la cátedra llama salida de la primera explosión (Clase 10)"),
        ]),
        EXAM("**Teoría que se toma con esto:** «Sintetizar el algoritmo de cálculo de MRP» (mesa especial de octubre); «Qué es y para qué se usa la Estructura del Producto» (13/12/2012); «En ERP, qué información tiene la BOM» (17/02/2014); «Cómo se utiliza la BOM» (EFR p. 36); «Explosión sumarizada vs. indentada» y «componentes alternativos vs. accesorios» (el final de Lu). La estructura del producto es U3 (datos de ingeniería): acá la usás."),
    ]
    return clase("u6c7", "Clase 7 · MRP: la lógica del registro", "MRP básico", "C",
                 "Qué es el MRP, la estructura del producto, el registro (brutos, ingresos, disponible, netos, órdenes), sus fórmulas y dos ejemplos resueltos: el producto X de Morán y los focos de Juno de Chase.",
                 "; ".join([MRPN + " §1–§2", CH(18, "593–603", "ejemplo 18.1 Juno Lighting"), PAT + " (mesa especial de octubre, 2012, 2014, Lu, EFR p.36)"]), t)


def c8():
    meses = ["Jun", "Jul", "Ago", "Sep", "Oct", "Nov"]
    t = [
        P("**Unidad 6 · Bloque C · Clase 8 · MRP de examen: scrap, repuestos y componentes comunes**"),
        IDEA("**Idea central:** el MRP de final agrega cuatro complicaciones al registro básico: **lote económico** (LEC), **scrap** (hay que lanzar más de lo que se necesita), **demanda independiente** de un componente (repuestos) y **componentes comunes** a varios padres. Todo se resuelve en el mismo orden: nivel por nivel, sumando todos los brutos antes de netear."),
        H("1. Las cuatro complicaciones según Morán"),
        T(["Caso", "Qué dice Morán", "Cómo se hace en la planilla"], [
            ["**Componentes comunes**", "los brutos de un ítem común salen de las órdenes de **todos** sus padres; con **códigos de nivel** se procesa cada nivel en todos los árboles antes de bajar", "ubicá cada ítem en su nivel más bajo y sumá los brutos de todos sus padres"],
            ["**Repuestos**", "son «una demanda independiente que se debe agregar» a la dependiente", "brutos = (órdenes del padre × cantidad) + demanda independiente"],
            ["**Defectuosos (scrap)**", "si r es la fracción de defectuosos, para obtener x hay que empezar con x′ = x / (1 − r)", "se agranda la orden **antes** de explotar al nivel inferior"],
            ["**Lote económico**", "con EOQ, la cantidad a pedir es la del MRP o la del EOQ, «la que sea mayor»; la cátedra agrupa en **múltiplos enteros del LEC**", "redondeá el neto al múltiplo de LEC que lo cubre"],
        ]),
        F(r"x'_{i,j} = \frac{x_{i,j}}{1 - r_{i,j}}", "Corrección por defectuosos (Morán, §2.2)"),
        P("Morán advierte que el scrap fijo en el sistema «también puede generar stocks en exceso», porque sigue cargado aunque el proceso haya mejorado, hasta que se lo revise."),
        H("2. Stock de seguridad y tiempo de seguridad"),
        L(["El **stock de seguridad** se usa normalmente en **productos finales**, que son los expuestos a la demanda independiente. En componentes de demanda dependiente «no es recomendable», salvo incertidumbre en cantidades (repuestos, rechazos) o en plazos de proveedores; lo que hay que hacer es mejorar el sistema productivo.",
           "El **tiempo de seguridad** es un lead time adicional para liberar la orden: «comenzar antes y terminar antes». Sirve, por ejemplo, con proveedores poco confiables en las fechas, y es mejor que un stock de seguridad."]),
        P("En Chase (Juno, Clase 7) el stock de seguridad del casquillo se descuenta del disponible: la orden salta cuando el disponible bajaría de 20, no de 0."),
        H("3. Convención para el scrap y el LEC en esta página"),
        AVISO("**Hipótesis de trabajo (cálculo propio):** (1) el **neto** se cubre con un **lote en piezas buenas** que es múltiplo del LEC; (2) la **cantidad a lanzar** es lote / (1 − scrap), redondeada hacia arriba; (3) los componentes explotan desde la cantidad **lanzada**. La cátedra permite pasarse hasta 20% del lote («se permite un incremento del 20% del lote», banco de preguntas, 15); no lo usé para no cambiar los resultados. Si en el examen usás otra convención, **escribila**: es lo que se corrige."),
        H("4. Final 03/12/2015 (y Ejercicios posibles, 06/05/2004)"),
        EX("EJERCICIO — Producto A con scrap, LEC y demanda independiente de E (final 03/12/2015)", [
            P("«La siguiente tabla muestra la información de un producto A y la de todos sus componentes. […] El ítem E tiene además una demanda independiente que se muestra a continuación, junto con los pedidos para el pto. A. 1.1- Graficar la estructura del pto. A. 1.2- Determinar el MRP.»"),
            T(["Ítem", "Padre", "Cant. en el padre", "Stock inicial", "LT (mes)", "Scrap", "LEC"], [
                ["A", "—", "—", "90", "1", "1%", "120"], ["B", "A", "1", "300", "2", "—", "200"],
                ["C", "B", "−2 (ver aviso)", "600", "2", "—", "—"], ["D", "A y B", "1 y 2", "300", "1", "—", "100"],
                ["E", "A", "2", "600", "1", "1,5%", "150"],
            ], "Datos de la planilla del alumno final03-12.xlsx: la foto del enunciado es ilegible en la tabla"),
            T(["", "Sep", "Oct", "Nov"], [["Pedidos de A", "180", "310", "250"], ["Demanda independiente de E", "", "500", "150"]]),
        ], [
            AVISO("**Qué es del material y qué es propio.** Los datos salen de `final03-12.xlsx` (resolución de un alumno) porque la foto del 03/12/2015 no se lee. La planilla resuelve **sin scrap** y mi motor de cálculo coincide con ella en todas las filas. La versión con scrap es **cálculo propio** con la convención de la sección 3. La cantidad **−2** de C figura así en la planilla: C se comporta como un ítem que **aparece** con cada B (subproducto o recupero), y su saldo crece; no lo pude confirmar con el enunciado."),
            P("**1. Estructura:** nivel 0 A; nivel 1 B, D y E (hijos de A); nivel 2 C y D (hijos de B). **D es común** a A y a B: va a su nivel más bajo (2) y se netea una sola vez, después de tener las órdenes de A y de B."),
            P("**2. A** (LT 1, LEC 120, stock 90). Sin scrap:"),
            T(["A", *meses], [
                ["Brutos", "", "", "", "180", "310", "250"], ["Disponible", "90", "90", "90", "30", "80", "70"],
                ["Netos", "", "", "", "90", "280", "170"], ["Recepción (múltiplo de 120)", "", "", "", "120", "360", "240"],
                ["**Lanzamiento**", "", "", "**120**", "**360**", "**240**", ""],
            ]),
            P("**3. B** (LT 2, LEC 200, stock 300): brutos = lanzamientos de A × 1 → 120 (ago), 360 (sep), 240 (oct). Netos 180 (sep) y 220 (oct) → recepciones 200 y 400 → **lanza 200 en julio y 400 en agosto**."),
            P("**4. E** (LT 1, LEC 150, stock 600): brutos = A × 2 + independiente → 240 (ago), 720 (sep), 480 + 500 = 980 (oct), 150 (nov). Netos 360, 890, 140 → recepciones 450, 900, 150 → **lanza 450 (ago), 900 (sep), 150 (oct)**."),
            P("**5. D** (LT 1, LEC 100, stock 300): brutos = A × 1 + B × 2 → 400 (jul, de B 200), 120 + 800 = 920 (ago), 360 (sep), 240 (oct). Netos 100, 920, 280, 220 → **lanza 100 (jun), 1000 (jul), 300 (ago), 300 (sep)**."),
            P("**6. C:** con la cantidad −2 de la planilla, cada lanzamiento de B **suma** 2 C: 600 → 1.000 (jul) → 1.800 (ago). No genera órdenes."),
            T(["Ítem", "Lanzamientos sin scrap (planilla)", "Lanzamientos con scrap (cálculo propio)"], [
                ["A (1%)", "ago 120 · sep 360 · oct 240", "ago **122** · sep **364** · oct **243**"],
                ["B", "jul 200 · ago 400", "jul 200 · ago 400 (netos 186 y 229: siguen entrando en un lote)"],
                ["E (1,5%)", "ago 450 · sep 900 · oct 150", "ago **457** · sep **1.066** · oct **153** (el neto de oct pasa de 890 a 908 y ya no entra en 900: el lote sube a 1.050)"],
                ["D", "jun 100 · jul 1000 · ago 300 · sep 300", "igual: los netos (100, 922, 286, 229) entran en los mismos múltiplos de 100"],
            ]),
            P("Ejemplo del cálculo con scrap: A en septiembre necesita recibir 120 buenas → lanza 120 / 0,99 = 121,2 → **122**. E en septiembre: brutos 2 × 364 = 728; neto 728 − 356 = 372 → lote 450 → lanza 450 / 0,985 = 456,9 → **457**."),
        ], estado="cálculo propio", nota="Sin scrap coincide con la planilla del alumno; con scrap es convención propia"),
        AVISO("**La versión 06/05/2004 y la de Ejercicios posibles** usan el mismo esquema A/B/C/D/E (A 90, B 300, C 600, D 300, E 600; D común a A y B; E con demanda independiente) pero en **semanas**, con scrap en todos los ítems (A 2%, B 2%, C 3%, D 3%, E 2,5% en el 30/04/2003) y entregas de A en la semana 1. Con lead times de 2 semanas aparecen **órdenes vencidas** (habría que lanzar antes de la semana 1): en el examen se **informa el atraso**, no se borra."),
        H("5. Final 08/08/2013: dos productos y componentes comunes"),
        S("u6_arbol_2013.svg", "Estructura de A y S del final 08/08/2013 con los componentes comunes resaltados (dibujo propio)"),
        EX("EJERCICIO — Entregar 70 A y 50 S en 12 semanas (final 08/08/2013)", [
            P("«Una empresa tiene que cumplir una orden de entrega de 70 productos del tipo A y 50 productos del tipo S dentro de 12 semanas.»"),
            T(["Ítem", "Lead time", "Predecesora", "Cantidad", "Disponible"], [
                ["A", "4", "—", "", "0"], ["S", "2", "—", "", "0"], ["B", "3", "A", "2", "0"], ["C", "4", "A", "2", "150"], ["C", "4", "T", "3", "150"],
                ["D", "2", "B", "3", "0"], ["E", "2", "B", "2", "0"], ["E", "2", "S", "1", "0"], ["F", "4", "S", "4", "150"], ["F", "4", "B", "1", "150"], ["T", "1", "S", "1", "0"],
            ], "Enunciado transcripto por un alumno: «Los Lead Times y las cantidades pueden no ser exactamente los tomados en el examen»"),
            P("«1. Confeccionar la estructura de los productos A y S. 2. ¿De qué forma puede mejorarse el contenido de la tabla anterior? 3. Confeccionar el MRP. 4. Luego de programada la producción a la empresa se le solicitan 50 unidades más del producto S. Se desea saber si la empresa puede entregar la producción requerida 11 semanas o antes. La empresa es de ensamblado y las operaciones de ensamblado pueden hacerse de forma inmediata si están disponibles las piezas.»"),
        ], [
            AVISO("**Resolución propia.** Hay una planilla de alumno (`Final 1.xlsx`) que encaja con este final, pero tiene errores: pone el stock de 150 en E en lugar de F y calcula el requerimiento de C desde T como 50 en lugar de 150 (T × 3). Lo de abajo es cálculo propio, verificado con el mismo motor de la sección 4."),
            P("**1. Estructura.** A (nivel 0) = 2 B + 2 C; B = 3 D + 2 E + 1 F. S (nivel 0) = 1 E + 4 F + 1 T; T = 3 C. Comunes: **C** (de A y de T), **E** (de B y de S), **F** (de B y de S)."),
            P("**2. Mejorar la tabla:** repite filas por cada padre (C, E y F aparecen dos veces con el mismo disponible), mezcla stock con estructura y no tiene LEC ni scrap ni nivel. Lo prolijo es separar el **maestro de ítems** (ítem, LT, stock, lote, nivel) del **maestro de estructura** (padre, componente, cantidad), como en los datos de ingeniería de la U3."),
            P("**3. MRP** (sin lotes ni scrap, recepción en la semana 12):"),
            T(["Ítem", "Brutos", "Netos", "Lanzamiento"], [
                ["A (LT 4)", "70 (sem 12)", "70", "**sem 8: 70**"], ["S (LT 2)", "50 (sem 12)", "50", "**sem 10: 50**"],
                ["B (LT 3) = 2 × A", "140 (sem 8)", "140", "**sem 5: 140**"], ["T (LT 1) = 1 × S", "50 (sem 10)", "50", "**sem 9: 50**"],
                ["C (LT 4) = 2 × A + 3 × T", "140 (sem 8) + 150 (sem 9)", "stock 150 cubre la sem 8 → 140 en la sem 9", "**sem 5: 140**"],
                ["D (LT 2) = 3 × B", "420 (sem 5)", "420", "**sem 3: 420**"],
                ["E (LT 2) = 2 × B + 1 × S", "280 (sem 5) + 50 (sem 10)", "280 y 50", "**sem 3: 280 · sem 8: 50**"],
                ["F (LT 4) = 1 × B + 4 × S", "140 (sem 5) + 200 (sem 10)", "stock 150 cubre la sem 5 → 190 en la sem 10", "**sem 6: 190**"],
            ]),
            P("**4. ¿50 S más en 11 semanas o antes?** Para entregar 50 S adicionales en la semana k hay que lanzar S en k − 2, T en k − 3, E en k − 4 y **F en k − 6** (F es el camino más largo: 4 + 2). Con el stock de F ya usado, la orden de F tiene que liberarse **en la semana 1 o después**: k − 6 ≥ 1 → **k ≥ 7**. Probado con el motor: para k = 11, 10, 9, 8 y 7 todas las órdenes caen en la semana 1 o más; para k = 6, F tendría que lanzarse en la semana 0. **Respuesta: sí, se pueden entregar en la semana 11 y hasta en la semana 7**, si hay capacidad (el MRP no la mira: eso es CRP, Clase 6). La frase «el ensamblado puede hacerse de forma inmediata» invita a discutir si el LT de S (2) se puede acortar, lo que adelantaría todavía más."),
        ], estado="cálculo propio", nota="La planilla del alumno tiene errores; esta resolución es propia"),
        H("6. Actualización del registro (Morán)"),
        EJ("Pieza X, lead time 2, lotes de 50", [
            P("**Al comienzo del período 1:** stock 10, brutos 30, 20, 20, 0, 45; ingreso programado de 50 en el período 1. Disponible 30, 10, −10, −10, −55 → netos 10 (per. 3) y 45 (per. 5) → órdenes de 50 en los períodos 1 y 3."),
            P("**Lo que pasó en el período 1:** se liberó la orden de 50 para el período 3; la salida real fue 20 (no 30); del ingreso programado entraron 45 netas (5 rechazadas); el bruto del período 5 se adelanta al 4; comercialización pide 5 para muestra en el período 2; aparece un bruto de 25 en el período 6."),
            T(["Comienzo del período 2", "2", "3", "4", "5", "6"], [
                ["Brutos", "25", "20", "45", "0", "25"], ["Ingr. programados", "", "50", "", "", ""],
                ["Disponible (S₀ = 10 + 45 − 20 = 35)", "10", "40", "−5", "−5", "−30"], ["Netos", "", "", "5", "", "25"],
                ["Órd. planificadas", "5 → lote 50", "", "25", "", ""],
            ], "Morán §3"),
            P("Un solo lote de 50 cubre los dos netos (5 + 25 = 30). Morán: las diferencias entre lo planificado y lo real «conducen a reprogramaciones permanentes» y el sistema emite **mensajes de excepción**."),
        ]),
    ]
    return clase("u6c8", "Clase 8 · MRP de examen: scrap, repuestos y componentes comunes", "MRP con scrap y comunes", "C",
                 "Componentes comunes, demanda independiente, scrap, lote económico, stock y tiempo de seguridad, y la actualización del registro; con los finales 03/12/2015 y 08/08/2013 resueltos.",
                 "; ".join([MRPN + " §2–§3", "texto/examenes/final03-12-15.txt + final03-12.xlsx (planilla de alumno)", "texto/examenes/Final SG1 - 8 Agosto de 2013.txt + Final 1.xlsx", EVA + " — 30/04/2003, 06/05/2004", EPOS, REPASO + " — pregunta 15"]), t)


def c9():
    t = [
        P("**Unidad 6 · Bloque C · Clase 9 · Tamaño de lote en el MRP**"),
        IDEA("**Idea central:** el neto de cada período puede ser una cantidad «antieconómica». Agrupar netos ahorra preparaciones pero genera stock. Todos los métodos buscan el equilibrio entre **costo de pedir o preparar** y **costo de mantener**, con distintas reglas."),
        P("Morán: la determinación del tamaño del lote «debe ser hecha nivel por nivel, dada la propagación de las cantidades a los niveles inferiores»."),
        H("1. Los métodos"),
        T(["Método", "Regla", "Cuándo sirve"], [
            ["**Lote por lote (L4L)**", "pedir exactamente el neto de cada período", "minimiza el stock; ignora las preparaciones (las tiene todas)"],
            ["**EOQ / LEC**", "lote fijo del modelo clásico; se pide el mayor entre el neto y el EOQ", "demanda «poco variable» período a período"],
            ["**TBO / POQ**", "período fijo, cantidad variable: cada TBO períodos se pide lo que suman los netos", "la demanda «no varía mucho»; genera menos stock que el EOQ"],
            ["**PPB** (balance cantidad–período)", "agrupar netos minimizando el costo unitario total (producción + mantener, con medio período de stock)", "demanda variable"],
            ["**Silver-Meal**", "igual que PPB pero con costo fijo + mantener completo en los períodos en que no se usa", "heurística simple con muy buenos resultados (Morán)"],
            ["**Costo total mínimo (CTM)**", "agrupar hasta que mantener ≈ pedir (Chase)", "costo de pedir constante"],
            ["**Costo unitario mínimo (CUM)**", "agrupar hasta minimizar (pedir + mantener) / unidades (Chase)", "cuando el costo de pedir cambia con el tamaño"],
            ["**Wagner-Whitin**", "evalúa todas las combinaciones, como programación dinámica", "óptimo, pero «muy engorroso» (Morán)"],
        ]),
        F(r"EOQ_j = \sqrt{\frac{2 D_j W_j}{H_j}} \qquad TBO_j = \left[\frac{T}{D_j / EOQ_j}\right] = \left[\frac{T \cdot EOQ_j}{D_j}\right]", "D_j demanda media por período (EOQ) o total del horizonte T (TBO); W_j costo fijo de la orden; H_j costo de mantener por unidad y período; [ ] parte entera"),
        F(r"CM_{t,j} = \frac{S_{t-1,j} + S_{t,j}}{2}\, H_j", "Costo de mantenimiento de cada período con existencia media (convención de Morán para comparar)"),
        H("2. Ejemplo de Morán: conjunto X y piezas Y y Z"),
        EJ("Datos", [
            P("X = 3 Y + 2 Z (ambas compradas). MPS de X para 12 semanas: 0, 60, 10, 90, 80, 0, 40, 80, 20, 70, 0, 90 (total 540); stock de X 90; LT 1; EOQ de X 90."),
            P("**Y:** sin stock, ingreso programado de 500 en la semana 1, LT 2, W = 100, H = 0,20 por unidad y semana. **Z:** sin stock, **demanda independiente de 300 por semana**, ingreso de 700 en la semana 1, LT 1, W = 150, H = 0,30."),
            P("Las órdenes de X (90 en las semanas 3, 4, 6, 8 y 11 con EOQ) generan brutos de Y = 3 × 90 = 270 y de Z = 2 × 90 = 180 más 300 de demanda propia."),
        ]),
        T(["Método", "Y: órdenes", "Y: costo OC + mant. = total", "Z: costo total"], [
            ["EOQ (Y 340, Z 610, redondeados a decenas)", "3 × 340", "300 + 489 = **789**", "1.050 + 785 = **1.835**"],
            ["TBO/POQ (X 2, Y 3, Z 1)", "370, 210, 270", "300 + 382 = **682**", "1.500 + 150 = **1.650**"],
            ["Silver-Meal", "310, 270, 270", "300 + 354 = **654**", "900 + 672 = **1.572**"],
        ], "Morán §2.1; costo de mantener con existencia media"),
        P("Verificación propia de los EOQ: Y → D = 1.350/12 = 112,5 por semana, $\\sqrt{2 \\cdot 112{,}5 \\cdot 100/0{,}20} = 335{,}4$ → 340. Z → D = 4.500/12 = 375, $\\sqrt{2 \\cdot 375 \\cdot 150/0{,}30} = 612{,}4$ → 610. TBO de Y: [12 × 340 / 1.350] = [3,02] = 3; de Z: [12 × 610 / 4.500] = [1,63] = 1; de X: [12 × 90 / 540] = 2."),
        P("La lección de Morán: el EOQ «puede conducir a valores de existencias excesivamente altos en los niveles inferiores por la propagación de excesos», y «en general la aplicación del lote óptimo dinámico genera menos stocks que los otros modelos»."),
        S("u6_loteo_moran.svg", "Costo total de la pieza Z con cada método (datos de Morán; gráfico propio)"),
        H("3. PPB y Silver-Meal paso a paso (Morán)"),
        EJ("Netos 40, 50, 60, 70; costo fijo 5; costo unitario 1; mantener 2% por período", [
            T(["Lote", "Cubre", "PPB: costo unitario", "Silver-Meal: costo por unidad"], [
                ["40", "1 período", "1,135", "5/40 = 0,125"], ["90", "2 períodos", "1,077", "(5 + 50 × 0,02)/90 = 0,067"],
                ["**150**", "3 períodos", "**1,066**", "**(5 + 110 × 0,02 + 60 × 0,02)/150 = 0,055**"], ["220", "4 períodos", "1,067", "0,057"],
            ]),
            P("PPB considera que lo que se usa en un período está «almacenado la mitad del tiempo» y todo el tiempo en los demás. Silver-Meal solo carga mantenimiento completo en los períodos en que la pieza no se usa. Aquí ambos eligen **150**, pero «en general los dos criterios conducen a lotes de distinto tamaño»."),
        ]),
        H("4. Ejemplo de Chase: cuatro métodos con los mismos netos"),
        EJ("Netos 50, 60, 70, 60, 95, 75, 60, 55; preparación 47; pieza 10; mantener 0,5% por semana", [
            P("EOQ: D = 525/8 × 52 = 3.412,5 por año; H = 0,5% × 10 × 52 = 2,60; $EOQ = \\sqrt{2 \\cdot 3412{,}5 \\cdot 47/2{,}60} \\approx 351$. Chase carga el mantenimiento sobre el **inventario final** de cada semana (no el promedio)."),
            T(["Método", "Pedidos", "Costo total 8 semanas"], [
                ["Lote por lote", "8 pedidos", "**376,00**"], ["EOQ 351", "351 en la sem 1 y en la sem 6", "**171,05**"],
                ["Costo total mínimo", "335 (sem 1–5) y 190 (sem 6–8)", "**140,50** (el más bajo)"], ["Costo unitario mínimo", "410 (sem 1–6) y 115 (sem 7–8)", "**153,50**"],
            ], "Chase, ilustraciones 18.19 a 18.22"),
            P("CTM elige 335 porque es donde mantener (38) y pedir (47) quedan más parecidos. CUM elige 410 porque ahí el costo por unidad es mínimo (0,2530). Chase: si el costo de pedir es constante, CTM «es más atractivo porque es más simple»; y la duración del horizonte influye en ambas técnicas."),
        ]),
        S("u6_loteo_chase.svg", "Costo total de 8 semanas con cada método (Chase, ilustraciones 18.19 a 18.22; gráfico propio)"),
        H("5. Hipótesis del TBO (pregunta de los bancos)"),
        P("La cátedra pregunta: «¿Cuáles son las hipótesis implícitas del método TBO en el MRP?». Con Morán: (1) la demanda **no varía mucho** de un período a otro («si la demanda es muy despareja de un período a otro este procedimiento tampoco es bueno»); (2) el lote **se hace al comienzo** de los períodos que cubre el TBO; (3) el EOQ en el que se basa supone costos de pedir y mantener **constantes** y una demanda media representativa del horizonte T; (4) el TBO es un **número entero** de períodos (parte entera)."),
        AVISO("**Una observación de Morán que se puede usar en teoría:** lo ideal es que el lote óptimo sea **menor** que los requerimientos por período. Si es mayor, se acumula stock, y entonces hay que revisar el proceso para **reducir el costo fijo** de la orden (el tiempo de puesta a punto). Es la puerta al JIT."),
    ]
    return clase("u6c9", "Clase 9 · Tamaño de lote en el MRP", "Tamaño de lote", "C",
                 "Lote por lote, EOQ, TBO/POQ, PPB, Silver-Meal, costo total mínimo y costo unitario mínimo, con los ejemplos de Morán (Y y Z) y de Chase; y las hipótesis del TBO.",
                 "; ".join([MRPN + " §2.1", CH(18, "607–611", "tamaño del lote, ilustraciones 18.19 a 18.22"), REPASO + " — hipótesis TBO"]), t)


def c10():
    t = [
        P("**Unidad 6 · Bloque C · Clase 10 · MRP de ciclo cerrado, MRP II, ERP y programación por armado final**"),
        IDEA("**Idea central:** el MRP solo no mira la capacidad. Cuando se le agrega el CRP con retroalimentación es **MRP de ciclo cerrado**; cuando se integran compras, finanzas, ventas e ingeniería es **MRP II**; y cuando abarca toda la empresa es **ERP**. La cátedra lo describe como un subsistema de cinco etapas."),
        H("1. El planificador y el ciclo cerrado"),
        P("Morán: un MRP «requiere la permanente participación del Planificador MRP, de lo contrario sería un sistema muy rígido». Sus funciones: liberar OP y OC; analizar la capacidad adicional; **reprogramar** fechas de órdenes emitidas; decidir lotes, stocks de seguridad y lead times; corregir errores eliminando sus causas; resolver faltantes **dentro** de las reglas del MRP; sugerir mejoras."),
        T(["Herramienta", "Qué hace (Morán)"], [
            ["**Señalamiento (pegging)**", "relaciona cada bruto con las órdenes de los niveles inferiores; permite subir por la estructura y ver el impacto de un problema hasta el producto final"],
            ["**Replanificación hacia arriba**", "con el señalamiento, verifica si se puede cumplir el producto final; si no, cambia fecha o cantidad, o acorta lead times"],
            ["**Órdenes planificadas en firme (FPO)**", "cantidades y fechas fijadas por el planificador; no las cambia la actualización automática"],
            ["**Regeneración / cambio neto**", "recalcular todos los registros o solo los que cambiaron (Chase: el cambio neto refleja el estado «en tiempo real»)"],
        ]),
        P("**MRP de ciclo cerrado** (Morán §4): «Cuando el MRP tiene retroalimentación del CRP se llama MRP de ciclo cerrado», y la información de capacidad insuficiente vuelve al sistema para reprogramar. Chase lo define como un sistema que incluye además la planeación de ventas y operaciones, el MPS y el CRP, y las funciones de ejecución (control de entradas/salidas, despacho, informes de demora), con retroalimentación «de modo que se pueda mantener válida la planeación en todo momento»."),
        S("u6_ciclo_cerrado.svg", "MRP de ciclo cerrado: plan → MPS → MRP → CRP → ¿es realista? → ejecución (esquema según Chase, ilustración 18.17)"),
        H("2. MRP II y ERP"),
        P("Chase: el sistema se expandió a compras y a la planta, y el nombre planeación de requerimiento de materiales «ya no era adecuado». **MRP II** (planeación de recursos de manufactura) refleja que participan cada vez más áreas. La «ecuación fundamental de manufactura» de Wight: **¿Qué vamos a hacer? ¿Qué se necesita para lograrlo? ¿Qué tenemos? ¿Qué debemos obtener?** La intención era planear y monitorear todos los recursos (manufactura, marketing, finanzas, ingeniería) en ciclo cerrado, generando cifras financieras, y simular el sistema de manufactura."),
        T(["Sistema", "Alcance"], [
            ["MRP", "materiales: qué, cuánto y cuándo pedir o fabricar"], ["MRP de ciclo cerrado", "MRP + CRP + MPS + ejecución, con retroalimentación"],
            ["MRP II", "ciclo cerrado + compras, finanzas, ingeniería, marketing; cifras financieras y simulación"],
            ["ERP", "sistema integrado de toda la empresa con una base de datos común (Chase cap. 14)"],
        ]),
        P("En la práctica de la cátedra (**TP N.º 7 «MRP», Odoo, 2015**) el MRP se usa **dentro de un ERP**. El caso es **Muebles Ros** (Rosario), que fabrica sillas de caño en dos modelos que solo difieren en el color del asiento. Datos del TP: la estructura de caño se fabrica contra orden en **4 días** (cortado, plegado, soldado y pintura) y el armado lleva **1 día** más; los asientos se compran en packs de 6 con **5 días** de entrega; el caño, con 2 días de flete; regatones y pintura se gestionan con **punto de pedido y lote** (no por MRP); preparar la planta cuesta 150. La empresa planifica **cada semana**: carga los pedidos, arma el plan y, si el stock proyectado da negativo, emite órdenes de abastecimiento. Es el registro MRP de la Clase 7 corriendo en un sistema real, mezclado con gestión de stock de la U5."),
        AVISO("**«MCP» en el final 13/12/2012** («Qué es MRP, MCP, ERP»): no aparece definido en el material del Drive. No lo invento: si te lo toman, aclará que no lo encontraste en la bibliografía y respondé MRP y ERP."),
        H("3. El subsistema MRP según la cátedra (banco «La gestión de producción»)"),
        T(["Etapa", "Qué hace", "Entradas → salida"], [
            ["**1. Primera explosión**", "descompone el producto y calcula las cantidades mes a mes", "PMP + estructura del producto + gestión de stocks → **PMCC** (componentes compradas) y **PMCF** (fabricadas), «agrupadas en función de un número entero de LEC o del LEF (se permite un incremento del 20% del lote), y desplazadas en el tiempo en función del LT»"],
            ["**2. Segunda explosión**", "calcula la carga **a capacidad infinita**", "PMCF + centros de máquinas + hoja de ruta + métodos y tiempos → horas máquina y horas hombre"],
            ["**3. Nivelación**", "ajusta la carga a lo disponible en cada centro", "CDT y CDR (Clase 5), sobre 4 meses"],
            ["**4. Emisión de órdenes de fabricación**", "desde la fecha de terminación más tardía (FT+T) calcula la de comienzo más tardía (FC+T) de cada operación", "registro de operaciones; si la nivelación adelantó, FC+t desde FT+t"],
            ["**5. Clasificación de las OF**", "ordena por centro de trabajo y fecha de comienzo", "lotes semanales a Planeamiento y Control; los avisos anticipados van a almacenes"],
        ], "Preguntas de repaso, 1, 3, 13 y 15 (respuestas de alumnos)"),
        L(["El pedido de reposición de ítems directos se genera en la **primera explosión** (PMCC); revisión trimestral, horizonte de seis meses (pregunta 28).",
           "Al subsistema de **compras** se transfiere el plan de componentes unitarias en la primera explosión y el de materias primas en la segunda (pregunta 4).",
           "**Inventarios** aporta al MRP II los saldos, el LEF y el lead time de fabricación (pregunta 43).",
           "Fechas: FT+T en la 2ª explosión; FT+t en la nivelación; FC+t y FC+T en la emisión de OF. Puede faltar FC+t si la nivelación no adelantó nada (pregunta 19)."]),
        EXAM("**Pregunta típica:** «¿Qué subsistema construye el PRM?» o «¿En qué etapa ocurre la primera explosión, qué programa la genera, a qué archivos recurre y qué produce?». Contestá con la tabla de arriba: MRP, PMP + estructura + stocks, PMCC/PMCF agrupados por LEC y desplazados por LT."),
        H("4. MRP y JIT"),
        P("Chase: MRP y JIT juntos forman un **sistema híbrido**; los proveedores de software llaman **manufactura de flujo** a los módulos que combinan su lógica. El MRP ayuda a crear el MPS y a planear materiales; el JIT ejecuta en la planta con kanban, sin órdenes de trabajo detalladas. Morán (Capacidad §4): en JIT «CRP es innecesaria (ni siquiera hay órdenes de producción)» y «sólo se justifica si se usa MRP»."),
        EXAM("**Final 2018:** «Explique en qué caso una empresa que produce con metodología JIT llega a necesitar trabajar con MRP.» Respuesta armada con el material: cuando tiene **estructuras de producto complejas con muchos componentes comprados con lead times largos** o **demanda variable que no permite una tasa nivelada**, necesita el MRP para planificar materiales a mediano plazo y para el MPS; la ejecución diaria puede seguir siendo JIT (sistema híbrido, manufactura de flujo, Chase cap. 18). Chase también señala que el MRP «tiene más provecho» cuando varios productos se hacen en lotes con el mismo equipo (Clase 1)."),
        H("5. Programación por armado final"),
        AVISO("**Complemento (no está en el material):** el programa lo nombra, pero no hay apunte de la cátedra. Lo que sí está: Morán dice que el MPS fija los productos finales «o los conjuntos mayores en el caso de producción para armado sobre pedido», y Chase marca que el MRP da beneficios grandes en **ensamble a pedidos** (ilustración 18.3). La idea general (Vollmann, citado en la bibliografía de Morán, no está en el Drive): en el **armado sobre pedido** el MPS se hace a nivel de **módulos u opciones** (que se fabrican para stock con el MRP) y un **programa de armado final** (FAS) arma el producto específico cuando llega el pedido, con un horizonte corto. Usalo así, aclarando que es complemento."),
    ]
    return clase("u6c10", "Clase 10 · MRP de ciclo cerrado, MRP II, ERP y armado final", "MRP II y ERP", "C",
                 "El planificador, señalamiento y órdenes en firme; MRP de ciclo cerrado, MRP II y ERP; el subsistema MRP de la cátedra en cinco etapas; MRP y JIT; y la programación por armado final.",
                 "; ".join([MRPN + " §3–§5", CAPN + " §4", CH(18, "604–607", "MRP de ciclo cerrado, MRP II, manufactura de flujo"), REPASO + " — preguntas 1–4, 13, 15, 19, 28, 43", ODOO, "texto/examenes/examen_2018_transcripcion.md (teoría 2)"]), t)
