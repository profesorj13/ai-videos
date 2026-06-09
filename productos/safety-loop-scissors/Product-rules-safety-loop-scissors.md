# Product Rules — Tijera adaptada Safety Loop (safety-loop-scissors)

> Contrato vivo del producto. Lo lee la skill `product-images-generation` en el
> **GATE 0.5** (obligatorio). Toda corrección del usuario sobre el producto se
> anota acá *en el momento*, no al final.
>
> Aprendizajes consolidados del piloto Mercedes-v1/v2 (videos id=1, id=2 en
> el Sheet) embebidos en §3 y §4.

---

## 1. Qué es

Tijera adaptada **Safety Loop Easy Grip Scissors** (marca *Special Supplies*).
Tijera de inclusión escolar pensada para alumnos con dificultades de motricidad
fina, fuerza de agarre débil o problemas de coordinación bimanual. **No tiene
los dos aros separados** de una tijera tradicional: tiene **un único bucle
continuo de silicona/plástico flexible** que conecta los dos mangos plásticos
rígidos por debajo. El usuario agarra **los dos mangos rígidos** con la mano
(4 dedos contra un mango, pulgar contra el otro mango) y **aprieta
lateralmente** — los mangos se acercan, las cuchillas se cierran y cortan. Al
soltar, el **bucle de silicona actúa como resorte elástico** y devuelve la
tijera a posición abierta. El bucle NO se agarra: cuelga libre por debajo de
la mano y es el mecanismo de retroceso. Forma general: **lágrima / gota / pera** (estrecha arriba en
las cuchillas, ancha abajo en el bucle).

## 2. Anatomía

- **Bucle continuo (loop / asa)**: silicona o plástico flexible, sección cilíndrica delgada (~5-7 mm de grosor), forma de lágrima cerrada vista de perfil. Es lo que sustituye a los dos aros tradicionales. **Color del equipo: verde lima/manzana brillante** (las refs físicas usan este color; el catálogo trae también azul cyan, rosa, naranja, rojo, amarillo, pero el canónico para este video es VERDE).
- **Posición canónica del producto (hero / escenas estáticas)**: tijera **ABIERTA**, lista para cortar — las dos cuchillas separadas formando una V de ~25-35° entre sí (NO cerradas, NO juntas en una sola hoja vertical). Pivot plateado en el centro-arriba del producto.
- **Cuchillas de acero inoxidable (en V abierta)**: dos cuchillas cortas, ~3-4 cm de largo cada una, **redondeadas en la punta** (safety blunt tip — no acaban en pico afilado), acero plateado/satinado. **Apuntan hacia arriba divergiendo en V** desde el pivot. Conectadas con un **tornillo plateado pequeño** en el pivot.
- **Mango plástico rígido (dos piezas, DIVERGENTES en V invertida)**: a continuación del pivot, hacia abajo, cada cuchilla se prolonga en una pieza plástica rígida del mismo color que el bucle (~4-5 cm de largo, ~1.5-2 cm de ancho — **gruesas, no finitas**). Cada mango **sigue el ángulo natural de su cuchilla** y se inclina hacia afuera/abajo: los extremos superiores (al pivot) están **CERCA entre sí**; los extremos inferiores (al bucle) están **MÁS SEPARADOS**. **Los mangos NO son paralelos verticales — divergen suavemente formando una "V invertida ancha"** o trapecio. Llevan relieve antideslizante y texto "SPECIAL SUPPLIES" en relieve pequeño (no necesariamente legible). La transición al bucle silicona es directa.
- **Bucle continuo (silicona, conecta los mangos abajo)**: silicona flexible color verde lima/manzana, sección cilíndrica ~6 mm de grosor. **Arranca de los extremos inferiores divergentes de los mangos** y baja describiendo una **gota / oval / pera alargada vertical**, cerrándose suavemente abajo. El ancho del bucle hereda la separación de los extremos inferiores de los mangos (más ancho arriba que un círculo perfecto). **Color del equipo: verde lima/manzana brillante** (el catálogo trae también azul, rosa, naranja, rojo, amarillo, pero el canónico para este video es VERDE).
- **Silueta global del producto**: pensala como una **pera alargada / hoja de árbol / escudo medieval invertido**: cuchillas en V abierta arriba, pivot plateado en el cuello, mangos divergentes en V invertida (continuando el ángulo de las cuchillas), bucle gota cerrando abajo. **NO es un palito vertical con un círculo colgando**: es una silueta continua que se ensancha del pivot hacia el bucle.
- **Escala**: largo total del producto ~14 cm — comparable a "two adult palms end-to-end" o "la longitud de un lápiz BIC común".
- **Material global**: las cuchillas son metal frío, el resto es plástico/silicona del color elegido. Sin partes negras, sin partes transparentes.

## 3. Restricciones

Lo que **NO** debe verse en las stills (errores recurrentes del modelo
documentados en el piloto Mercedes-v1/v2):

- **NO fusionar dos unidades en una forma simétrica** tipo mariposa / pétalos / labios / corazón. Esto pasa especialmente con NB Pro cuando el prompt menciona "scissors" sin anclar la morfología del bucle.
- **NO mostrar dos aros separados estilo tijera convencional**. Es un único bucle cerrado en forma de lágrima.
- **NO mostrar dos mangos VISUALMENTE SEPARADOS** que parezcan dos piezas independientes (como aros). La silueta del mango debe leerse como **UNA SOLA PIEZA CONTINUA EN FORMA DE GOTA** — los dos lados verticales de la gota están UNIDOS por la silicona inferior, formando una silueta cerrada única. Si en la imagen se ven dos formas separadas en lugar de una silueta continua → ERROR.
- **NO inventar elementos internos en la gota**. El interior de la gota (el hueco encerrado por la silueta cerrada) está **COMPLETAMENTE VACÍO** de cualquier parte del producto: NO barras transversales, NO travesaños, NO refuerzos diagonales, NO apoyos internos, NO segundo aro pequeño dentro del grande, NO grip de plástico cruzando el medio. Solo se ve **lo que está DETRÁS de la gota** a través del hueco (mesa, mano, papel — pero NO algo del producto mismo).
- **NO mostrar la mano con dedos METIDOS DENTRO del bucle** como si fueran aros tradicionales.
- **NO mostrar la mano agarrando / envolviendo el bucle de silicona**. El bucle NO se agarra: cuelga libre por debajo. La mano agarra los DOS MANGOS RÍGIDOS arriba (4 dedos en uno, pulgar en el otro), squeeze lateral tipo alicate.
- **NO mostrar ningún dedo, pulgar, mano o muñeca PASANDO POR DENTRO del aro de silicona**. El hueco del bucle queda vacío, se debe ver aire a través del hueco. Si la silicona pasa visiblemente por encima de un dedo o del dorso de la mano → ERROR.
- **NO mostrar dos o más unidades de la tijera cerca de la mano**. Una sola tijera por escena cuando hay grip. (Si el guión pide "varios", priorizar fidelidad y mostrar 1.)
- **NO mostrar cuchillas largas, puntiagudas o estilo cocina**. Son cortas (~3-4 cm) y redondeadas.
- **NO inventar resortes, bisagras visibles ni piezas internas** del mecanismo plástico. El bucle es liso y continuo.
- **NO rotar más de ~30°** respecto al plano natural (cuchillas hacia abajo / hacia adelante).
- **NO cambiar el color del bucle entre escenas**. Verde lima/manzana canónico en TODAS las escenas con producto.
- **NO mostrar el bucle desinflado, doblado en V o quebrado** — debe leerse como forma de gota / pera alargada vertical, continua.
- **NO pellizcar el bucle en una "cintura" tipo jarrón / reloj de arena / vasija**. Silueta del bucle: gota / oval / pera alargada vertical, sin pellizcos.
- **NO mostrar las cuchillas CERRADAS / juntas formando una sola hoja vertical**. La tijera se renderiza en **posición ABIERTA / lista para cortar**: las dos cuchillas separadas en V de ~25-35° entre sí, divergiendo hacia arriba desde el pivot.
- **NO mostrar los mangos plásticos PARALELOS VERTICALES**. Los mangos **divergen** desde el pivot hacia abajo, siguiendo el ángulo natural de las cuchillas — los extremos inferiores (donde se conectan al bucle) están más separados que los extremos superiores (donde se unen al pivot). Es una **V invertida**, no dos columnas paralelas.
- **NO mostrar la silueta como "palito vertical con círculo colgando abajo"**. La silueta es continua y se ensancha del pivot hacia el bucle: pera alargada / escudo invertido.
- **NO mostrar mangos finitos ni en forma de palillos**. Son piezas robustas, ~1.5-2 cm de ancho cada una.

## 4. Uso (grip / interacción)

> **CORRECCIÓN MAYOR 2026-06-09**: el grip que veníamos modelando estaba MAL.
> Después de varias rondas con feedback del equipo, el grip canónico real es:
> **pulgar arriba del mango plástico superior + 4 dedos METIDOS DENTRO del bucle
> de silicona** (el bucle envuelve los 4 dedos). Se aprieta empujando el pulgar
> hacia abajo y tirando los 4 dedos hacia arriba.

Cómo se sostiene y se usa el producto, explícito para el modelo:

- **Grip canónico (squeeze vertical)**:
  - **EL PULGAR va APOYADO POR ARRIBA del mango plástico rígido superior** (justo debajo del pivot/cuchillas). El pulgar presiona hacia abajo, NO atraviesa nada.
  - **LOS 4 DEDOS (índice, mayor, anular, meñique) van METIDOS DENTRO DEL BUCLE de silicona** — el bucle continuo envuelve a los 4 dedos como un aro grande que entra en el puño. Los dedos curvados quedan dentro del bucle.
  - La mano queda en posición de "puño abierto" con el bucle alrededor de los 4 dedos y el pulgar separado por arriba apoyado en el mango rígido superior.
- **Movimiento de corte**: el pulgar empuja el mango rígido superior hacia ABAJO, mientras los 4 dedos (dentro del bucle) tiran hacia ARRIBA. Esto comprime el mecanismo y las cuchillas se cierran.
- **Ref canónica visual**: foto del producto rojo con grip humano correcto (ver §7 — guardar como `ref-real-grip-canonico.jpg`).
- **El bucle de silicona NO se agarra**. Es un **resorte elástico** que conecta los extremos inferiores de los mangos por debajo: cuelga libre por debajo de la mano, devuelve la tijera a posición abierta cuando se suelta el squeeze. **El bucle queda visible POR DEBAJO de la mano** en la mayoría de los planos con grip.
- **El hueco INTERIOR del bucle queda VACÍO**. Nada pasa por adentro del aro de silicona — ni pulgar, ni dedos, ni mano, ni muñeca, ni manga, ni papel. Se debe ver **aire visible** a través del hueco. Si en la imagen la silicona del bucle pasa POR ENCIMA / POR DELANTE de un dedo o de la palma → el dedo/mano está atravesando el aro → **ERROR**. El bucle queda **DEBAJO y POR FUERA de toda la mano**, como si estuviera colgando de los mangos al aire libre.
- **Frase quirúrgica para el prompt (anti-error — VERSIÓN CORRECTA 2026-06-09)**: `CRITICAL GRIP — the hand grips the scissor with this exact pose: the THUMB rests ON TOP of the upper rigid plastic handle (just below the pivot/blades, pressing down). The FOUR FINGERS (index, middle, ring, pinky) ARE INSIDE the silicone loop — the green silicone loop wraps AROUND the four fingers like a large ring entering the fist. The loop is held by the four fingers from inside it (fingers curled, loop around them). To close the blades, the thumb pushes the upper handle DOWN while the four fingers pull the loop UP. The grip is NOT lateral squeeze of two rigid handles — it is vertical squeeze: thumb on top handle pressing down, four fingers inside the loop pulling up.`
- **Movimiento de corte**: squeeze lateral de los dos mangos (igual que apretar unos alicates chiquitos). Al soltar, el bucle de silicona elástico devuelve los mangos a posición abierta y las cuchillas se reabren.
- **Orientación típica**: cuchillas hacia adelante (alejándose del cuerpo) o hacia abajo (top-down sobre la mesa). Bucle colgando hacia abajo / hacia el cuerpo.
- **Visibilidad del bucle según ángulo de cámara**: la gota PUEDE quedar parcial o totalmente oculta detrás del dorso de la mano según el ángulo de cámara (ej. cámara del lado del dorso → el dorso tapa la gota). **No es regla que la gota tenga que verse siempre**. Lo que SÍ es regla: que la silueta del producto visible se lea como **UNA SOLA pieza continua**, no como dos aros separados.
- **Posición del pulgar según ángulo de cámara** (regla crítica):
  - **Cámara del lado de la PALMA** (palma hacia cámara, dorso atrás): el **PULGAR queda VISIBLE ARRIBA, apoyado por AFUERA sobre el lado superior del mango** (encima del extremo superior derecho o izquierdo de la gota — según mano dominante). Los 4 dedos van por DETRÁS del producto (se ven nudillos / no se ven). La gota cuelga visible. **NO el pulgar atravesando el aro** — el pulgar va ENCIMA del mango, no a través.
  - **Cámara del lado del DORSO** (dorso hacia cámara, palma atrás): el dorso de la mano tapa parte del producto. Los 4 dedos pueden verse del costado agarrando un lado de la gota. El pulgar queda atrás. La gota puede quedar oculta total o parcialmente.
- **Anti-error frecuente**: cuando la palma está hacia la cámara, el modelo tiende a meter la mano DENTRO del aro de la gota (la silicona termina envolviendo la muñeca). ERROR. La gota debe colgar libre **por debajo y por afuera** de toda la mano; el pulgar va **encima del lado superior del mango**, no dentro del aro.
- **Escala vs mano**: la mano abarca los mangos rígidos (~4-5 cm cada uno). El bucle es proporcional pero no se aferra. Para mano de niño, los mangos llenan bien el puño.
- **Anclaje de escala obligatorio en el prompt**: `~14 cm total length / about the length of an adult BIC pen / fits inside a closed adult fist`.

## 5. Prompt base — descripción exhaustiva del producto (EN)

Bloque copy-paste listo para incrustar en cualquier prompt de escena con
producto. Si el modelo solo lee esto, debe poder reconstruir el producto sin
ver imagen.

```
A single Safety Loop Easy Grip adapted scissor for inclusive classroom use,
RIGID SOLID OBJECT, ~14 cm total length (about the length of an ordinary
BIC pen). OVERALL SILHOUETTE — an elongated pear / shield / tree-leaf shape
standing vertically: open V-shaped blades at the top, silver pivot screw at
the neck, two outward-angled plastic handles below the pivot, and a closed
silicone loop at the bottom. NOT a vertical stick with a circle hanging
below — it is a single continuous, gently widening silhouette from blades
to loop bottom.

TOP — two short stainless-steel blades (~3-4 cm each) with ROUNDED
SAFETY-BLUNT tips, satin-silver finish, joined by a small silver pivot
screw. The blades are shown OPEN, separated in a ~25-35° V, pointing
upward / outward — NEVER closed together as a single vertical knife.

MIDDLE — two THICK rigid lime-green plastic handle pieces (~4 cm long,
~1.5-2 cm wide each — chunky, NOT thin sticks). Each handle continues the
angle of its blade: they DIVERGE downward from the pivot in an inverted-V,
so the top of the handles (at the pivot) are CLOSE together and the bottom
of the handles (at the loop) are SEPARATED WIDER. Subtle embossed antislip
grip texture, faint "SPECIAL SUPPLIES" relief (not legible).

BOTTOM — one single continuous flexible silicone loop, glossy lime-green /
apple-green, ~6 mm cross-section, connecting the lower ends of the two
divergent handles. The loop describes an ELONGATED VERTICAL TEARDROP /
oval / pear shape, smoothly closing at the bottom. NOT a perfect round
circle. NO hourglass waist, NO pinch, NO break — continuous and smooth.

ABSOLUTE NO: NO conventional finger holes, NO closed/vertical-knife blade
position, NO parallel-vertical handles (they MUST diverge), NO thin
stick-like handles, NO multiple units in frame. Single product only.
Lime-green color ONLY.
```

## 6. Product Hero

- Path local: `product-hero.png` (copia canónica de `workspace/hero/hero-v4.png`)
- Job ID Higgsfield: `f750ccf3-b3b2-425d-85c7-4ddbec59749f`
- URL CDN: https://d8j0ntlcm91z4.cloudfront.net/user_3DzyY4cDXpkrQIt3tqQtvaDRiew/hf_20260528_192649_f750ccf3-b3b2-425d-85c7-4ddbec59749f.png
- Versión aprobada: `v4` (anteriores: v1 waist-pinched, v2 thin-handles-vshape, v3 blades-closed-handles-parallel — todas en `workspace/hero/` con sufijo descriptivo)
- Fecha de aprobación: `2026-05-28`

---

## Tabla de refs canónicas (UUIDs CDN reusables)

> Subir cada ref UNA SOLA VEZ y reusar el UUID. Evita `AccessDenied` transitorio.

| Slug | Path local | UUID CDN | Uso |
|---|---|---|---|
| hero | `product-hero.png` | *(pendiente — Paso 1.5)* | Ref canónica de todas las escenas con producto |
| ref-catalog-6colors | `referencias/ref-images/ref-product-catalog-6colors.jpg` | *(pendiente)* | Vista catalog 6 colores — muestra morfología bucle clara |
| ref-catalog-stack | `referencias/ref-images/ref-product-catalog-stack.jpg` | *(pendiente)* | Apilados — vista lateral de la silueta |
| ref-real-grip-blades-open | `referencias/ref-images/ref-real-grip-hand-blades-open.jpg` | *(pendiente)* | Foto real verde — vista de muñeca con producto (NO usar como ref del grip — confunde) |
| ref-real-grip-loop-side | `referencias/ref-images/ref-real-grip-hand-loop-side.jpg` | *(pendiente)* | Foto real verde — vista lateral del producto en mano |
| ref-real-action-cutting | `referencias/ref-images/ref-real-action-cutting-paper.png` | *(pendiente)* | Foto real cortando papel — referencia de acción |
| **ref-real-grip-canonico** ⭐ | `referencias/ref-images/ref-real-grip-canonico-2026-06-09.png` | *(pendiente)* | **REF CANÓNICA DEL GRIP** (tijera roja, mano adulta, pulgar extendido a lo largo del mango plástico superior + 4 dedos adentro del bucle de silicona). **Usar SIEMPRE como ref del grip** en escenas con manos. |
| **ref-real-grip-fist-cutting** ⭐ | `referencias/ref-images/ref-real-grip-fist-cutting-pose.jpg` | *(pendiente)* | **REF CANÓNICA POSE DE CORTE**: puño firme cerrado dorso a cámara, solo asoman las cuchillas arriba. Usar cuando la escena muestra al niño USANDO la tijera (cortando algo en posición natural). |
