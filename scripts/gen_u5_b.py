from u5lib import *

def c2():
    t = [
        P("**Sistemas de Gestión (UTN FRRo) · Unidad 5 · Bloque A · Clase 2 · Lote económico (EOQ / LEC) y punto de pedido**"),
        AVISO("**De dónde sale esta clase.** El modelo y sus supuestos: **Chase cap. 17**, ecuaciones [17.2] a [17.4]. En el Resumen V6 las fórmulas son imagen y no se leen; las escribo en la notación estándar de Chase con las definiciones que sí están en el texto. Los ejercicios son de finales (SG!EVA, EjerciciosFinalesResueltos, SG1.doc). **Las resoluciones con la etiqueta «cálculo propio» son mías**; cuando hay hoja manuscrita, lo digo y comparo."),
        IDEA("**Idea central:** pedir mucho de una vez baja el costo de pedir y sube el de mantener. El **lote económico** $Q^*$ es el tamaño que hace mínima la suma. Con demanda y entrega ciertas, se pide $Q^*$ cada vez que el stock baja al **punto de pedido** $R = \\bar d \\cdot L$."),
        H("1. Supuestos del modelo básico"),
        P("Chase los da como «irreales, pero representan un punto de partida»:"),
        L(["La demanda del producto es **constante y uniforme** durante todo el período.",
           "El **tiempo de entrega** es constante.", "El **precio por unidad** es constante.",
           "El costo de mantener se basa en el **inventario promedio**.", "Los costos de pedido o preparación son **constantes**.",
           "Se cubren **todas** las demandas (no se permiten pedidos acumulados, o sea faltantes)."]),
        S("u5_sierra.svg", "El efecto sierra: se pide Q al llegar a R y el pedido llega L después (esquema propio)"),
        H("2. Costo total anual"),
        P("Costo anual total = costo de compra + costo de pedidos + costo de mantenimiento (Chase [17.2]):"),
        F("CT = D\\,C + \\frac{D}{Q}\\,S + \\frac{Q}{2}\\,H", "[17.2] Chase · H = i·C"),
        L(["$D\\,C$: costo de compra anual (no depende de $Q$ mientras el precio sea fijo).",
           "$\\frac{D}{Q}S$: costo anual de pedidos = cantidad de pedidos al año por el costo de cada uno.",
           "$\\frac{Q}{2}H$: costo anual de mantener = inventario promedio ($Q/2$) por el costo de mantener una unidad un año."]),
        S("u5_costos.svg", "Las tres curvas con los datos de BIT-Kaffee (gráfico propio)"),
        H("3. El lote óptimo"),
        P("Chase deriva el costo total respecto de $Q$ y lo iguala a cero:"),
        F("\\frac{dCT}{dQ} = -\\frac{DS}{Q^2} + \\frac{H}{2} = 0 \\quad\\Rightarrow\\quad Q^* = \\sqrt{\\frac{2DS}{H}}", "[17.3] Chase"),
        P("En las **resoluciones manuscritas** la misma fórmula aparece con la otra notación ($L$ = costo de pedido, $c$ = precio, $i$ = tasa):"),
        F("Q^* = \\sqrt{\\frac{2\\,D\\,L}{c\\,i}}", "notación de las hojas resueltas (EFR, SG1.doc)"),
        P("Consecuencias útiles (**complemento**, salen de la misma fórmula): en $Q^*$ el costo de pedir es igual al de mantener; el costo anual de pedir + mantener en el óptimo vale $\\sqrt{2DSH}$; la cantidad de pedidos al año es $N = D/Q^*$ y el tiempo entre pedidos $T = Q^*/\\bar d$."),
        H("4. Punto de pedido"),
        P("Como el modelo supone demanda y entrega constantes, «no es necesario tener inventario de seguridad y el punto de volver a pedir, R, simplemente es» (Chase [17.4]):"),
        F("R = \\bar d \\cdot L", "[17.4] · d̄ = demanda diaria promedio · L = tiempo de entrega en días"),
        P("En las hojas: $PP = D_{LT} = \\bar d \\cdot LT$. Con incertidumbre se le suma el stock de seguridad (Clase 5)."),
        H("5. El costo por unidad que usan las resoluciones"),
        P("Varias hojas de la cátedra comparan alternativas con el **costo total por unidad** (dividen [17.2] por $D$):"),
        F("CT(Q) = c + \\frac{L}{Q} + \\frac{c\\,i\\,Q}{2D}", "por unidad · SG1 Lu Final 2; EFR p.2, 3 y 16"),
        P("Da el mismo óptimo y ordena igual las alternativas. Para pasar a pesos por año, multiplicás por $D$."),
        H("6. Ejemplos resueltos"),
        EJ("Ejemplo 1 · BIT-Kaffee (final, EFR p.16)", [
            P("«BIT-Kaffee consume anualmente **7500 cajas** de vasos descartables de 100cc. Los costos de ordenar son de **$15** y el anual de manejo (almacenamiento, etc.) **30%** del precio de compra. Cada caja cuesta **$12**, y se sabe que el tiempo de demora de la entrega es de **5 días**. Establezca una política y programa de abastecimiento óptimo.» La hoja toma **250 días hábiles** por año."),
            F("H = 0{,}30 \\cdot 12 = 3{,}6 \\qquad Q^* = \\sqrt{\\frac{2 \\cdot 7500 \\cdot 15}{3{,}6}} = \\sqrt{62\\,500} = 250 \\text{ cajas}"),
            F("\\bar d = \\frac{7500}{250} = 30 \\text{ cajas/día} \\qquad PP = 30 \\cdot 5 = 150 \\text{ cajas} \\qquad T = \\frac{250}{30} \\approx 8 \\text{ días}"),
            F("CT = 12 + \\frac{15}{250} + \\frac{3{,}6 \\cdot 250}{2 \\cdot 7500} = 12{,}12 \\ \\$/\\text{caja}"),
            P("**Política** (así cierra la hoja): «se realiza un pedido de 250 ítems cuando el PP sea = 150 ítems». Son unos 30 pedidos por año. *(Los números coinciden con la hoja; el costo anual de pedir + mantener, $900, es cálculo propio: 30 pedidos × $15 + 125 × $3,6.)*"),
        ]),
        EJ("Ejemplo 2 · El bar (final, EFR p.17)", [
            P("«Un bar consume anualmente **730 cajas** de vasos descartables de 200cc. Los costos de ordenar es **$15** y el de manejo **30%** del costo. Cada caja cuesta **$12**, y se sabe que el tiempo de demora de la entrega es de **5 días**. Se desea establecer una política óptima de abastecimiento.»"),
            F("Q^* = \\sqrt{\\frac{2 \\cdot 730 \\cdot 15}{12 \\cdot 0{,}3}} \\approx 78 \\text{ cajas} \\qquad PP = \\frac{730}{250} \\cdot 5 \\approx 15 \\text{ cajas}"),
            P("La hoja: «se debe realizar un pedido de 78 cajas cuando el stock llegue a 15 cajas»; tiempo entre pedidos $T = Q^*/D = 78/730 \\approx 0{,}1$ año (unos 27 días hábiles, cálculo propio)."),
        ]),
        EJ("Ejemplo 3 · Hospital: precio implícito y LEC (final, EFR p.30)", [
            P("«Un hospital desea comprar **500 kg** de algodón por año, el costo de ordenar es **$10** c/u, el de mantener en stock es **$0,25 por unidad y por año**. La tasa de interés aplicable a estos bienes de cambio es de **12%** anual. 1.1 ¿Cuál es el precio de cada kg de algodón? 1.2 ¿Cuál es su LEC?»"),
            F("H = c\\,i \\Rightarrow c = \\frac{0{,}25}{0{,}12} \\approx \\$2{,}08 \\text{ por kg} \\qquad Q^* = \\sqrt{\\frac{2 \\cdot 500 \\cdot 10}{0{,}25}} = 200 \\text{ kg}"),
            P("Lo mismo da la hoja manuscrita ($c$ ≈ 2,08; $Q = 200$)."),
        ]),
        H("7. Sensibilidad: ¿cuánto cuesta no pedir el óptimo?"),
        P("La curva de costo total es **chata cerca del mínimo**: equivocarse un poco en $Q$ cuesta poco. Pero pedir el doble o la mitad ya se nota. El final de IMBA lo pregunta directamente."),
        EX("8. EJERCICIO — IMBA / TT: variación respecto del óptimo (SG!EVA 09/03/2006 y otros; EFR p.2; SG1 Lu Final 14)", [
            P("«La empresa IMBA tiene un contrato con la firma DBA para la venta de **150000 items** al año. IMBA ordena materia prima a su proveedor para **40.000 items**. Colocar el pedido cuesta **$40.-** y los costos de almacenar se calculan el **20%** del costo del ítem **$0,15** c/u. IMBA desea conocer el porcentaje de variación de la cantidad pedida con respecto a la óptima y determinar el importe de esta variación.» (En EFR la empresa se llama TT y la consigna dice «y cuánto le cuesta esta variación, si es que le cuesta».)"),
        ], [
            AVISO("**Fuente:** resolución manuscrita de EjerciciosFinalesResueltos p.2 (y SG1.doc, Final 14, que llega al mismo $Q^*$). Los porcentajes y el costo anual están verificados con cálculo propio."),
            F("Q^* = \\sqrt{\\frac{2 \\cdot 150\\,000 \\cdot 40}{0{,}15 \\cdot 0{,}20}} = \\sqrt{400\\,000\\,000} = 20\\,000 \\text{ ítems}"),
            P("**Variación de la cantidad:** IMBA pide 40.000, el doble del óptimo: **+100%** respecto de $Q^*$ (dicho al revés, el óptimo es 50% menos que lo que pide; la hoja anota «50%»)."),
            P("**Costo por unidad** con la fórmula de las hojas:"),
            F("CT(20\\,000) = 0{,}15 + \\frac{40}{20\\,000} + \\frac{0{,}15 \\cdot 0{,}2 \\cdot 20\\,000}{2 \\cdot 150\\,000} = 0{,}154 \\qquad CT(40\\,000) = 0{,}155"),
            F("(0{,}155 - 0{,}154) \\cdot 150\\,000 = \\$150 \\text{ por año}"),
            P("**Cálculo propio, en pesos por año** (pedir + mantener): con 20.000 son $300 + $300 = **$600**; con 40.000 son $150 + $600 = **$750**. La política actual cuesta **$150 más por año (+25%)**."),
            AVISO("**Error a no copiar:** en SG1.doc (Final 14) el costo se calcula como $c\\cdot i\\cdot Q$ ($8000 vs. $600). Eso no es el costo de la política: le falta dividir por 2 el inventario y le falta el costo de pedir. La respuesta correcta es la de EFR: **$150/año**."),
            P("**Política de compras sugerida:** pedir 20.000 ítems, 7,5 pedidos por año (uno cada 7 semanas aprox., cálculo propio). Si el proveedor exige lotes de 40.000, la penalidad es de $150/año."),
        ]),
        H("9. Modelo con faltantes permitidos (pedidos pendientes)"),
        P("Un final (EFR p.30) trae un caso donde **sí** se permite faltar, con un costo por faltante. El modelo no está en el resumen de Chase."),
        P("**Complemento (no está en el material):** si cada unidad que falta y se entrega después cuesta $B$ por unidad y por año, el modelo EOQ con pedidos pendientes da:"),
        F("Q^* = \\sqrt{\\frac{2DS}{H}\\cdot\\frac{H+B}{B}} \\qquad S_{max} = Q^*\\,\\frac{B}{H+B}", "complemento · S_max = existencia máxima justificada"),
        EX("10. EJERCICIO — EOQ con faltantes (EFR p.30)", [
            P("«Una Empresa tiene una demanda anual de **1000 u/año**, costo de ordenar **$10** c/orden y costo de mantener **$10** c/u. año. Los costos de faltante son calculados en aprox. **$40** cada vez que la empresa tiene un faltante. Indicar qué cantidad de existencia está justificada.»"),
        ], [
            AVISO("**Cálculo propio con el modelo complemento.** La hoja manuscrita de EFR solo anota «40 = 10·x ⇒ x = 4», sin desarrollo; no la puedo usar como clave. Interpreto los $40 como costo por unidad faltante y por año."),
            F("Q^* = \\sqrt{\\frac{2\\cdot 1000 \\cdot 10}{10}\\cdot\\frac{10+40}{40}} = \\sqrt{2500} = 50 \\qquad S_{max} = 50\\cdot\\frac{40}{50} = 40"),
            P("**Existencia justificada: 40 unidades** como máximo; se piden 50 y se dejan acumular hasta 10 pendientes. Sin faltantes el lote sería $\\sqrt{2000} \\approx 45$."),
        ], estado="cálculo propio"),
        EX("11. EJERCICIO — Ingap SA: sistema actual vs. óptimo (EFR p.34)", [
            P("«El comedor de una empresa industrial (Ingap SA) utiliza **120 vasos** de 250 cc. de papel por día. Estos se compran **cada 30 días**. Ingap SA trabaja **360 días** al año, dichos vasos cuestan **10 $/la docena**, los costos de cada orden es de **$5** c/u y **50%** del precio de compra el de mantenimiento anual. Ingap SA quiere determinar cuál de las alternativas de abastecimiento es más conveniente, para ello indicar: 1.1 La relación o diferencia cuantificable entre el sistema de compra actual y otro propuesto de minimización de costos. 1.2 Si la entrega demora dos días, sugerir un plan de gestión de inventarios. 1.3 Dado que el comedor pertenece a la empresa (considerado como un centro de costo más), decir cómo y quién genera el pedido de estos vasos y qué sector es el encargado de adquirirlos.»"),
        ], [
            AVISO("**Cálculo propio.** La hoja manuscrita llega a $Q \\approx 1021$, $PP = 240$ y «gestión de stock y compras», pero su comparación de costos está ilegible."),
            F("D = 120 \\cdot 360 = 43\\,200 \\text{ vasos/año} \\quad c = \\frac{10}{12} = 0{,}833 \\quad H = 0{,}5 \\cdot 0{,}833 = 0{,}417"),
            F("Q^* = \\sqrt{\\frac{2 \\cdot 43\\,200 \\cdot 5}{0{,}417}} \\approx 1018 \\text{ vasos} \\ (\\approx 85 \\text{ docenas})"),
            P("**1.1** Hoy pide 120 × 30 = 3600 vasos. Pedir + mantener: actual = 12 × 5 + 1800 × 0,417 ≈ US$ 810 por año; óptimo = √(2·D·S·H) ≈ US$ 424 por año. **Diferencia ≈ 386 por año** a favor de la política óptima (la actual cuesta 1,9 veces más)."),
            P("**1.2** $PP = 120 \\cdot 2 = 240$ vasos: cuando quedan 240, se piden ≈1020 (unos 42 pedidos al año, uno cada ~8,5 días)."),
            P("**1.3** El pedido de reposición lo genera **gestión de stock / almacén** al llegar al PP; lo adquiere **Compras**. El comedor, como centro de costo, recibe el cargo."),
        ], estado="cálculo propio"),
        G("12. Glosario de símbolos", "Notación de Chase; entre paréntesis, la de las hojas resueltas.", [
            ["D", "demanda anual", "Unidades por año"], ["S (L)", "costo de pedido", "$ por pedido"],
            ["C (c)", "precio unitario", "$ por unidad"], ["i", "tasa de mantenimiento", "% anual del valor"],
            ["H = iC", "costo de mantener", "$ por unidad y por año"], ["Q*", "lote económico", "EOQ / LEC"],
            ["R (PP)", "punto de pedido", "R = d̄·L sin incertidumbre"], ["N = D/Q*", "pedidos por año", ""],
            ["T = Q*/d̄", "tiempo entre pedidos", "En días si d̄ es diaria"], ["B", "costo de faltante", "Complemento: $ por unidad pendiente y por año"],
        ]),
    ]
    src = [V6, EVA, EFR(2, "TT/IMBA"), EFR(16, "BIT-Kaffee"), EFR(17, "bar 730 cajas"), EFR(30, "hospital algodón; EOQ con faltantes"),
           EFR(34, "Ingap SA"), LU(16, "Final 14, IMBA"), PAT]
    return clase("u5c2", "Clase 2 · Lote económico (EOQ / LEC) y punto de pedido", "Lote económico y punto de pedido", "A",
                 "El modelo básico de cantidad fija: supuestos, costo total, la fórmula del lote económico y el punto de pedido. Con los ejercicios de final BIT-Kaffee, el bar, el hospital, IMBA e Ingap.",
                 src, t, "Clase 3 · EOQ con descuentos por cantidad", ["u5/img/u5_sierra.svg", "u5/img/u5_costos.svg"])


def c3():
    t = [
        P("**Sistemas de Gestión (UTN FRRo) · Unidad 5 · Bloque A · Clase 3 · EOQ con descuentos por cantidad**"),
        AVISO("**De dónde sale esta clase.** El procedimiento: **Chase cap. 17, «Modelos de precio descontado»**. El ejercicio: el **caso librería**, que aparece varias veces en SG!EVA (con variantes) y tiene dos resoluciones manuscritas (EFR p.3 y SG1.doc Final 2). El Documento Maestro lo marca con ★."),
        IDEA("**Idea central:** si el precio baja al comprar más, ya no alcanza con $Q^*$. Hay que calcular el lote económico **con cada precio**, quedarse con los que caen dentro de su tramo, sumar los **puntos de quiebre** del precio y elegir el de **menor costo total, incluida la compra**."),
        H("1. El problema"),
        P("Chase: «el precio de venta de una pieza varía según el tamaño del pedido. Se trata de un cambio **discreto** en lugar de unitario». Su ejemplo: tornillos para madera a 0,02 dólares cada uno de 1 a 99, 1,60 por 100 y 13,50 por 1000. El EOQ calculado con el precio de 1,60 podría dar 75 tornillos, pero 75 tornillos cuestan 0,02 cada uno: **no es factible**."),
        P("Ahora el costo de compra $D\\,C$ **sí depende de Q**, porque $C$ cambia con el tramo. Entonces se compara el costo total completo:"),
        F("CT(Q) = D\\,C(Q) + \\frac{D}{Q}\\,S + \\frac{Q}{2}\\,i\\,C(Q)"),
        H("2. Procedimiento de dos pasos (Chase)"),
        P("Vale cuando el costo de mantener es un **porcentaje del precio** ($H = iC$), como en todos los ejercicios del libro y de la cátedra:"),
        L(["**Paso 1.** Ordenar los precios del más bajo al más alto y, empezando por el más bajo, calcular el EOQ de cada precio **hasta encontrar uno factible** (que caiga dentro de su rango).",
           "**Paso 2.** Si el primer EOQ factible es el del precio más bajo, ese es el óptimo. Si no, calcular el costo total de ese EOQ factible **y** el costo total en **cada cantidad de quiebre** de los precios más bajos (la cantidad mínima con la que se accede a cada descuento). La $Q$ óptima es la de menor costo."], True),
        P("Chase agrega una advertencia práctica: el descuento por volumen «casi siempre hace que resulte económico pedir cantidades superiores a $Q_{opt}$», así que hay que estimar bien la **obsolescencia** y los **costos de almacenamiento** antes de aceptar."),
        S("u5_descuentos.svg", "Caso librería: una curva por precio; el óptimo cae en el quiebre de 100 cajas (gráfico propio)"),
        EX("3. EJERCICIO — La librería (SG!EVA; EFR p.3; SG1 Lu Final 2)", [
            P("«Una librería pide un determinado ítem en cajas de 1000 unidades. La demanda anual es constante a lo largo del año, y se sabe con certeza que es de **600 cajas**, también se conoce con certeza que el tiempo de reaprovisionamiento es exactamente **un mes**. El costo de ordenar es de **$16** y los costos anuales de manejo son de **36%**. El mayorista ofrece este descuento por volumen:»"),
            T(["Cant. de cajas", "Precio / caja"], [["1 – 49", "$7,50"], ["50 – 99", "$7,35"], ["100 o más", "$7,00"]]),
            P("«2.1 Establecer una política económica (óptima) de abastecimiento.»"),
        ], [
            AVISO("**Fuente:** resoluciones manuscritas de SG1.doc (Final 2) y EFR p.3, que llegan al mismo resultado. Repito el procedimiento y lo verifico (cálculo propio)."),
            P("**Paso 1**, del precio más bajo al más alto:"),
            F("Q_{7{,}00} = \\sqrt{\\frac{2\\cdot 600\\cdot 16}{7{,}00\\cdot 0{,}36}} \\approx 87{,}3 \\Rightarrow \\text{no factible (necesita } \\geq 100)"),
            F("Q_{7{,}35} = \\sqrt{\\frac{19\\,200}{7{,}35\\cdot 0{,}36}} \\approx 85{,}2 \\Rightarrow \\text{factible (50–99)}"),
            P("(El de $7,50 da ≈ 84,3, tampoco factible; las hojas lo calculan igual.)"),
            P("**Paso 2.** Comparar el EOQ factible (85) con el quiebre del precio más bajo (100). Con el costo por caja de las hojas:"),
            F("CT(85) = 7{,}35 + \\frac{16}{85} + \\frac{7{,}35\\cdot 0{,}36\\cdot 85}{2\\cdot 600} \\approx 7{,}73"),
            F("CT(100) = 7{,}00 + \\frac{16}{100} + \\frac{7{,}00\\cdot 0{,}36\\cdot 100}{1200} = 7{,}37"),
            P("Las hojas calculan también $CT(49)$ al precio de $7,50 ≈ 7,94 (el máximo de ese tramo); no hace falta según el procedimiento de Chase, pero no cambia nada."),
            T(["Alternativa", "Precio", "$/caja", "$/año (×600, cálculo propio)"], [
                ["Q = 49", "$7,50", "7,94", "≈ 4762"], ["Q = 85", "$7,35", "7,73", "≈ 4635"], ["**Q = 100**", "**$7,00**", "**7,37**", "**4422**"]]),
            P("**Política óptima: pedir 100 cajas por vez**, 6 pedidos al año (uno cada 2 meses). Como el reaprovisionamiento es de un mes y la demanda es cierta, el **punto de pedido** es la demanda de un mes: $600/12 = 50$ cajas (cálculo propio; las hojas no lo escriben)."),
        ]),
        EX("4. VARIANTE B — librería con manejo TEA 20% (SG!EVA)", [
            P("La misma librería (cajas de una gruesa, 600 cajas/año, reaprovisionamiento de un mes, $16 por orden, misma tabla de precios) pero con «costos anuales de manejo de **TEA 20%**»."),
        ], [
            AVISO("**Cálculo propio** (no hay resolución en el material)."),
            F("Q_{7{,}00} = \\sqrt{\\frac{2\\cdot 600\\cdot 16}{7{,}00\\cdot 0{,}20}} \\approx 117 \\Rightarrow \\text{factible (100 o más)}"),
            P("Es el precio más bajo y su EOQ es factible: el procedimiento **termina en el paso 1**. Política: **pedir 117 cajas** (≈5 pedidos al año), punto de pedido 50 cajas; costo total ≈ $4364/año. Con un manejo más barato conviene pedir más."),
        ], estado="cálculo propio"),
        EX("5. VARIANTE A — librería con 95% de confianza (SG!EVA 27/02/2003)", [
            P("«Una librería pide un determinado cuaderno en cajas de **una gruesa**. La demanda anual es constante a lo largo del año, y se sabe con certeza que es de 600 cajas, también se conoce que el tiempo de reaprovisionamiento es de un mes, **durante este período se desea mantener un 95% de confianza en el suministro**. El costo de ordenar es de $16 y los costos anuales de manejo son de 36%.» Misma tabla (allí dice «precio / unidad»)."),
        ], nota="Para resolver. El lote sale igual que en el ejercicio 3 (100 cajas). Para el 95% hace falta el desvío de la demanda en el mes de reaprovisionamiento, y el enunciado no lo da (dice que la demanda es «constante»). Con un σ, el punto de pedido sería 50 + 1,64·σ (Clase 5). Hay que confirmar con la cátedra qué dato falta.", estado="para resolver"),
        EXAM("**Cómo escribirlo en el examen:** 1) definir variables y la función de precio por tramos; 2) EOQ por precio, marcando factible / no factible; 3) costo total del EOQ factible y de los quiebres más baratos; 4) elegir y **enunciar la política** (cuánto pedir, cada cuánto, punto de pedido)."),
        G("6. Glosario", "", [
            ["C(Q)", "precio por tramos", "El precio depende de la cantidad pedida"],
            ["Quiebre", "cantidad mínima del descuento", "50 y 100 cajas en la librería"],
            ["Factible", "Q dentro de su tramo", "Un EOQ calculado con un precio que no le corresponde no sirve"],
            ["Gruesa", "doce docenas", "144 unidades (variante del enunciado)"],
        ]),
    ]
    src = [V6, EVA, "texto/examenes/Ejercicios posibles.txt (librería)", EFR(3, "librería"), LU(4, "Final 2, librería"), DM, PAT]
    return clase("u5c3", "Clase 3 · EOQ con descuentos por cantidad", "EOQ con descuentos", "A",
                 "Cuando el precio baja por volumen: el procedimiento de dos pasos de Chase y el caso librería de los finales, resuelto y con sus variantes.",
                 src, t, "Clase 4 · Perpetuo y periódico", ["u5/img/u5_descuentos.svg"])
