# Storyboard — Teclado Admouse ColorTec + Cobertor acrílico

> Producto: `Product-rules-teclado-admouse-colortec.md` (vigente al 2026-06-08)
> Hero canónico: pendiente — se generan en Paso 1.5 (DOS heros: keyboard-only + keyboard-with-keyguard)
> Guión pegado: 2026-06-08 por Federico
> Avatar: Mercedes (solo en E3-i) — `productos/_shared/avatars/mercedes/Avatar-rules-mercedes.md`
> Alumno: niño/a primario (~8-10 años) anónimo, mostrado de espaldas / costado / manos. No es personaje recurrente — solo identidad de "alumno".

---

## Fuente — guión

```
ESCENA 1 — EL DESAFÍO MOTOR
Visual: Aula. Un alumno trabaja frente a la computadora con el teclado Admouse. Se observa que al apoyar la mano, activa varias teclas al mismo tiempo sin intención. Se detiene, borra, vuelve a intentar.
Voz del avatar: "El teclado Admouse facilita la escritura. Pero para algunos alumnas o alumnos con dificultades motrices mayores, apoyar la mano o controlar con precisión cada pulsación puede ser un desafío mayor."

ESCENA 2 — LA DIFICULTAD ESPECÍFICA
Visual: Plano detalle de la mano del alumno sobre el teclado. Se ven pulsaciones involuntarias: varios dedos tocan teclas al mismo tiempo, o la mano cae sobre el teclado al buscar una letra.
Voz en off: "Los movimientos involuntarios, el temblor o la dificultad para sostener la mano en el aire mientras se escribe pueden generar pulsaciones no deseadas. Esto dificulta la tarea y puede volverse una fuente de frustración para el alumno o incluso impedirle la participación en la actividad."

ESCENA 3 — PRESENTACIÓN DEL MATERIAL
Visual i: Mercedes coloca el cobertor acrílico sobre el teclado Admouse. Plano detalle mostrando cómo los agujeros del cobertor coinciden con cada tecla. La mano se apoya con naturalidad sobre la superficie rígida.
Voz del avatar: "El cobertor acrílico es un complemento diseñado específicamente para el teclado Admouse. Es una superficie rígida y transparente que se coloca encima, con un agujero por cada tecla."
Visual ii: Plano detalle de un dedo ingresando con precisión en el agujero y presionando la tecla. La mano descansa sobre el cobertor entre pulsaciones.
Voz en off: "Permite apoyar la mano sobre el teclado sin activar teclas de forma involuntaria. El alumno o la alumna puede pulsar la tecla que elige, ingresando el dedo en el agujero correspondiente. Esto reduce las pulsaciones involuntarias y le da mayor control y precisión durante la escritura."

ESCENA 4 — EN USO
Visual: El alumno escribe con el cobertor colocado. Se observa la mano apoyada con estabilidad, pulsando tecla por tecla con mayor precisión. Completa la actividad junto a sus compañeros.
Voz en off: "Al poder apoyar la mano, el alumno no necesita sostenerla en el aire mientras busca cada tecla. Eso reduce el esfuerzo motor y le permite concentrar la energía en la tarea. Un ajuste simple que puede marcar una diferencia real en la participación y la autonomía durante las actividades digitales."

CIERRE
Visual: Teclado Admouse con el cobertor acrílico colocado, sobre fondo Alizia. La cámara recorre ambos productos como una unidad.
Placa: "Cobertor acrílico para teclado Admouse" / "Mayor precisión y control en la escritura digital." / "Encontralo en tu valija."
Voz avatar o texto: "No recomendado para alumnos con espasticidad. En esos casos, consultar con el especialista antes de su uso."
```

---

## Mapa de escenas → imágenes

| # | ID | Rol | Producto en cuadro | Avatar | Audio asociado | Output |
|---|---|---|---|---|---|---|
| 1 | `hero-keyboard-only` | producto puro | teclado puro | — | — | `workspace/hero/keyboard-only-v1.png` |
| 2 | `hero-keyboard-with-keyguard` | producto puro | teclado + cobertor | — | — | `workspace/hero/keyboard-with-keyguard-v1.png` |
| 3 | `E1` | escena | teclado puro (sin cobertor) | alumno (de espaldas) | VO1 (avatar) | `workspace/e1-v1.png` |
| 4 | `E2` | macro | teclado puro (close-up manos) | alumno (solo mano) | VO2 (off) | `workspace/e2-v1.png` |
| 5 | `E3-i` | escena con Mercedes | teclado + cobertor (siendo colocado) | Mercedes | VO3a (avatar) | `workspace/e3i-v1.png` |
| 6 | `E3-ii` | macro | teclado + cobertor (close-up dedo en agujero) | alumno (solo mano) | VO3b (off) | `workspace/e3ii-v1.png` |
| 7 | `E4` | escena | teclado + cobertor (en uso) | alumno (de costado) | VO4 (off) | `workspace/e4-v1.png` |
| 8 | `cierre` | producto + brand | teclado + cobertor sobre fondo Alizia | — | placa + VO5 | `workspace/cierre-v1.png` |

**Total: 8 imágenes** (2 heros + 5 escenas + 1 cierre). E3 del guión se desdobla en E3-i y E3-ii porque tiene dos VOs distintos y dos planos visuales distintos. Compacté lo que en otros videos sería E3-i / E3-ii / E3-iii en dos imágenes (la primera cubre "Mercedes coloca + agujeros que coinciden", la segunda cubre "dedo entra al agujero").

---

## hero-keyboard-only

- **Rol**: `producto_puro`
- **Modelo**: `product-photoshoot/conceptual_product`
- **Aspect / resolución**: `9:16` / `2k`
- **Refs (--image)**:
  - `referencias/ref-images/641052448_18571391659015740_1859984296843389714_n.jpg` (cenital limpio, mejor lectura del color por tecla)
  - `referencias/ref-images/442428136_899089812231608_2223775701284996178_n.jpg` (3/4 perspectiva, confirma forma de la carcasa y logo)
- **Prompt EN**:
  > `<§5 Product Rules — solo bloque base, SIN add-on keyguard>` + `on a pale neutral light-grey background, soft studio top-down catalog look, slight 5° tilt to read the keys clearly, the keyboard centered and isolated, no hands, no people, 9:16 vertical framing.`
- **Resumen ES**:
  > Teclado ColorTec puro, vista cenital ligeramente inclinada (~5°), sobre fondo gris pálido neutro estilo catálogo. Sin manos, sin contexto. Ref canónica para E1 / E2.
- **Constraints / QA**:
  - Paleta cromática FIEL (verde lima / rosa magenta vocales / rojo coral números / cian modificadores / azul intenso barra / naranja bordes)
  - Layout español (Ñ, ¿, ¡) sin numpad lateral
  - Logo "ColorTec by AdMouse" arriba-derecha (si no sale legible, omitir antes que garabato)
  - 1 sola unidad
- **Output**: `workspace/hero/keyboard-only-v1.png`

---

## hero-keyboard-with-keyguard

- **Rol**: `producto_puro`
- **Modelo**: `product-photoshoot/conceptual_product`
- **Aspect / resolución**: `9:16` / `2k`
- **Refs (--image)**:
  - `referencias/ref-images/641052448_18571391659015740_1859984296843389714_n.jpg` (teclado base)
  - `referencias/ref-images/admouse-keyguard-on-standard-keyboard-ciapat.jpg` (cobertor — ref oficial keyguard)
- **Prompt EN**:
  > `<§5 Product Rules — bloque base + add-on keyguard>` + `on a pale neutral light-grey background, soft studio top-down catalog look, slight 5° tilt, the keyboard centered and isolated WITH THE TRANSPARENT ACRYLIC KEYGUARD MOUNTED ON TOP, the colored keys visible through the keyguard holes, soft highlight on the acrylic surface confirming its glossy transparency, no hands, no people, 9:16 vertical framing.`
- **Resumen ES**:
  > Mismo encuadre que el hero anterior pero con el cobertor acrílico ya montado. Se ven los agujeros redondos del cobertor sobre cada tecla colorida del ColorTec, reflejos suaves del acrílico que confirman que es transparente y brillante. Ref canónica para E3-ii / E4 / cierre.
- **Constraints / QA**:
  - Cobertor TRANSPARENTE (las teclas coloridas se ven debajo)
  - Agujeros REDONDOS (excepto el de la barra, alargado)
  - Cobertor cubre SOLO el área de teclas, no la carcasa ni el apoyo de muñeca
  - Logo "AdMouse" en azul arriba-derecha del acrílico (o omitido si no sale limpio)
  - Reflejos suaves visibles para leer el material brillante
- **Output**: `workspace/hero/keyboard-with-keyguard-v1.png`

---

## E1 — El desafío motor (alumno escribiendo, problema visible)

- **Rol**: `escena_con_alumno`
- **Modelo**: `nano_banana_2`
- **Aspect / resolución**: `9:16` / `2k`
- **Refs (--image)**:
  - `product-hero-keyboard-only.png` (ref del producto — pendiente Paso 1.5)
- **Prompt EN** *(copy-paste al CLI)*:
  > A primary-school child (around 8-10 years old) sitting at a tidy school desk, seen from BEHIND-AND-SLIGHTLY-TO-THE-SIDE (over-the-shoulder angle) so that the keyboard, the computer screen, and the child's hand are all visible but the child's face is NOT shown (or only a partial profile). The child wears a simple school t-shirt. The desk is neat and orderly: a laptop / desktop monitor in front, the colored Admouse ColorTec keyboard between the child and the monitor, no clutter. The child's small hand rests flat on the keyboard with several fingers PRESSING DOWN MULTIPLE COLORED KEYS AT ONCE (3-4 keys depressed at the same time, clearly accidental — the hand has "fallen" onto the keys), the child's posture shows mild concentration and slight frustration. The computer screen visible in the background shows a clean simple text editor with a few correctly typed lines and then several garbled extra characters from the accidental presses. Shot on a modern smartphone, candid documentary photography style, natural ambient classroom light from a window (overcast / warm bulbs), slight motion blur, subtle film grain, true-to-life colors gently saturated and properly exposed (NOT washed-out, NOT cinematic graded), imperfect natural framing. Clean tidy classroom in the background (organized shelves, calm). 9:16 vertical. + <§5 Product Rules — bloque base keyboard ONLY, sin add-on keyguard>.
- **Resumen ES**:
  > Niño/a de primaria visto desde atrás-costado (sin cara). Escritorio prolijo en aula, monitor + teclado ColorTec. Mano apoyada plana sobre el teclado con 3-4 teclas pulsadas a la vez (claramente accidental). Pantalla detrás muestra unas líneas bien escritas y luego caracteres garabato de las pulsaciones involuntarias. Look documental, luz natural de aula.
- **Constraints / QA**:
  - Alumno SIN cara (de espaldas / profile parcial)
  - Teclado SIN cobertor (E1 es el problema antes del producto)
  - Mano CON varias teclas hundidas a la vez (es la lectura visual del problema)
  - Pantalla con texto SIMPLE legible + caracteres extra garabato visibles (no scribbles completos)
  - Entorno PROLIJO, no aula caótica
  - Anti-pattern: mirando a cámara, sonriendo, aula desordenada
- **Output**: `workspace/e1-v1.png`

---

## E2 — La dificultad específica (close-up mano sobre teclas)

- **Rol**: `escena_con_grip`
- **Modelo**: `nano_banana_2`
- **Aspect / resolución**: `9:16` / `2k`
- **Refs (--image)**:
  - `product-hero-keyboard-only.png` (ref del producto — pendiente Paso 1.5)
- **Prompt EN**:
  > Extreme close-up (macro) of a primary-school child's small hand resting on the colored Admouse ColorTec keyboard, shot from a low 3/4 angle nearly at desk level so the keys fill the frame and the hand reads large. The hand is flat, palm-down, with three or four fingers SIMULTANEOUSLY DEPRESSING separate colored keys (one finger pushes a green letter key, another pushes a pink vowel, another rests heavily on a coral red number key) — clearly accidental, not deliberate. The hand looks small against the oversized keys (each key approximately 2.2 cm). The remaining parts of the keyboard and a sliver of the wooden classroom desk are visible at the edges of the frame. Soft natural classroom light with a subtle warm cast. Shot on a modern smartphone, candid documentary photography style, slight motion blur on the depressed keys, subtle film grain, true-to-life colors gently saturated. 9:16 vertical. + <§5 Product Rules — bloque base keyboard ONLY, sin add-on keyguard>.
- **Resumen ES**:
  > Macro de la mano del alumno sobre el teclado, ángulo bajo 3/4 a nivel del escritorio. Mano chica contra teclas grandes, 3-4 dedos pulsando teclas distintas a la vez (verde, rosa, roja). Se lee el problema motor de un vistazo. Luz natural de aula.
- **Constraints / QA**:
  - SIN cobertor (E2 sigue siendo el problema)
  - Múltiples teclas hundidas simultáneamente (visible)
  - Mano de niño/a (no adulto)
  - Encuadre macro — el teclado llena el frame
  - Paleta cromática del teclado fiel
- **Output**: `workspace/e2-v1.png`

---

## E3-i — Mercedes coloca el cobertor

- **Rol**: `escena_con_avatar`
- **Modelo**: `nano_banana_2`
- **Aspect / resolución**: `9:16` / `2k`
- **Refs (--image)**:
  - `productos/_shared/avatars/mercedes/mercedes-base.webp` (Mercedes identity — OBLIGATORIO primero)
  - `product-hero-keyboard-with-keyguard.png` (ref del producto montado — pendiente Paso 1.5)
- **Prompt EN**:
  > <§5 Avatar Rules Mercedes — bloque EN completo> Mercedes is shown in a medium-close shot from a 3/4 high angle, leaning slightly forward at a school desk in a tidy inclusive classroom. Her hands hold the TRANSPARENT ACRYLIC KEYGUARD by its outer edges (both hands, fingers on the rim, NOT on the central acrylic surface) and she is lowering / placing it precisely on top of the Admouse ColorTec keyboard, the keyguard aligned over the colored keys with the round holes about to settle over each key. The colored keys (lime green, magenta pink, coral red, cyan, deep blue spacebar) read clearly through the transparent acrylic. Mercedes looks DOWN AT HER HANDS / at the keyguard, NOT at the camera, with a calm warm closed-mouth gentle smile (NOT speaking, NOT articulating words). The classroom in the background is soft-focus, tidy, with organized shelves and warm ambient daylight. Shot on a modern smartphone, candid documentary photography style, natural light from a window, subtle film grain, true-to-life colors gently saturated, imperfect natural framing. 9:16 vertical. + <§5 Product Rules — bloque base + add-on keyguard>.
- **Resumen ES**:
  > Mercedes en plano medio-corto, mostrada desde un ángulo 3/4 alto. Sostiene el cobertor acrílico transparente desde los bordes (no por la superficie central) y lo está bajando para apoyarlo sobre el teclado ColorTec, perfectamente alineado. Las teclas de colores se leen a través del acrílico. Mercedes mira sus manos, no a cámara, sonrisa cálida cerrada. Aula prolija detrás, luz natural.
- **Constraints / QA**:
  - Mercedes idéntica a `mercedes-base.webp` (pelo caramelo medio, sonrisa cerrada, NO articulando)
  - Mercedes mira sus manos / el teclado, NO a cámara
  - Cobertor sostenido desde los **bordes**, no desde el centro
  - Cobertor TRANSPARENTE, agujeros REDONDOS, teclas coloridas visibles abajo
  - El cobertor todavía no está completamente apoyado (está siendo colocado — gesto en proceso)
  - Aula prolija
- **Output**: `workspace/e3i-v1.png`

---

## E3-ii — Dedo entrando al agujero (macro de uso correcto)

- **Rol**: `escena_con_grip`
- **Modelo**: `nano_banana_2`
- **Aspect / resolución**: `9:16` / `2k`
- **Refs (--image)**:
  - `product-hero-keyboard-with-keyguard.png` (ref del producto montado — pendiente Paso 1.5)
- **Prompt EN**:
  > Extreme close-up (macro) of a primary-school child's small hand, palm-down, RESTING FLAT on the surface of the transparent acrylic keyguard mounted on top of the Admouse ColorTec keyboard. Four fingers stay flat and relaxed on the acrylic surface (NOT pressing anything, the keyguard supports their weight). The INDEX FINGER IS RAISED slightly and is just entering one of the round holes — the fingertip is inside a round hole and pressing down on a colored key (the key visible is a green letter key, slightly depressed). The other colored keys (pink vowels, red numbers, cyan modifiers) are clearly visible through the transparent acrylic around the active hole. Soft highlight reflections on the acrylic surface confirm the glossy transparent material. Low 3/4 angle near desk level, the keyguard and keys fill the frame. Soft natural classroom light with a warm cast. Shot on a modern smartphone, candid documentary photography style, subtle film grain, true-to-life colors gently saturated. 9:16 vertical. + <§5 Product Rules — bloque base + add-on keyguard>.
- **Resumen ES**:
  > Macro de la mano del alumno apoyada plana sobre el cobertor, 4 dedos relajados sobre la superficie acrílica (sin presionar nada). El índice se levanta levemente y entra en un agujero redondo, presionando una tecla verde debajo. Se ven los reflejos suaves del acrílico (lectura "transparente brillante"). Encuadre macro.
- **Constraints / QA**:
  - 4 dedos relajados sobre el acrílico, índice en el agujero (NO toda la mano dentro)
  - Cobertor TRANSPARENTE, agujeros REDONDOS visibles
  - Tecla activa visible y ligeramente hundida bajo el dedo
  - Reflejos en el acrílico (transparencia brillante)
  - Mano chica (niño/a)
- **Output**: `workspace/e3ii-v1.png`

---

## E4 — En uso (alumno escribiendo con cobertor)

- **Rol**: `escena_con_alumno`
- **Modelo**: `nano_banana_2`
- **Aspect / resolución**: `9:16` / `2k`
- **Refs (--image)**:
  - `product-hero-keyboard-with-keyguard.png` (ref del producto montado — pendiente Paso 1.5)
- **Prompt EN**:
  > A primary-school child (around 8-10 years old) seated at a tidy school desk in an inclusive classroom, seen from a SIDE PROFILE (3/4 side angle, face partly visible but the focus is on the hand and the keyboard, NOT on the face). The child wears a simple school t-shirt and looks down at the laptop / monitor screen with calm focused concentration. The child's hand rests FLAT and STABLE on the surface of the transparent acrylic keyguard mounted on the Admouse ColorTec keyboard, with the index finger inserted in one of the round holes pressing a colored key precisely — a deliberate, controlled keystroke. The screen visible in the background shows a clean readable line of simple Spanish text (for example "Hola mamá" or "casa sol mesa") with NO garbled extra characters. The body language is relaxed, autonomous, focused. In the soft-focus background, one or two other children sit at neighboring desks working on their own tasks. Tidy organized classroom, warm natural daylight from a window. Shot on a modern smartphone, candid documentary photography style, slight motion blur, subtle film grain, true-to-life colors gently saturated. 9:16 vertical. + <§5 Product Rules — bloque base + add-on keyguard>.
- **Resumen ES**:
  > Alumno/a sentado/a en aula inclusiva, plano de costado 3/4 (cara parcial, no protagónica). Mano apoyada estable sobre el cobertor, índice entra al agujero y presiona con precisión una tecla. Pantalla muestra texto SIMPLE legible bien escrito ("Hola mamá" / "casa sol mesa"), sin garabatos. Compañeros desenfocados detrás trabajando. Look documental, luz natural.
- **Constraints / QA**:
  - CON cobertor (transparente, redondos)
  - Cara parcial (no protagónica), foco en mano/teclado
  - Texto en pantalla simple y LEGIBLE, sin garabatos
  - Compañeros detrás (soft focus) — refuerza inclusión y autonomía
  - Mano estable, gesto controlado (no caos como E1/E2)
- **Output**: `workspace/e4-v1.png`

---

## cierre — Producto + brand

- **Rol**: `cierre_brand`
- **Modelo**: `product-photoshoot/conceptual_product`
- **Aspect / resolución**: `9:16` / `2k`
- **Refs (--image)**:
  - `product-hero-keyboard-with-keyguard.png` (ref canónica)
- **Prompt EN**:
  > The complete Admouse ColorTec keyboard with the transparent acrylic keyguard mounted on top, centered on a soft warm pale background with subtle AlizIA brand colors (very gentle gradient of soft warm beige to soft warm cream — NOT loud, NOT corporate-banner-style). 3/4 high angle, slight 10° tilt to read both the colored keys through the transparent keyguard AND the rounded holes of the keyguard. Soft directional studio light from the upper-left creating gentle highlights on the glossy acrylic surface to confirm transparency. Keyboard + keyguard read as a single unit. No hands, no people, no text overlays (text is added in post). Generous negative space above and below for placa overlays. 9:16 vertical. + <§5 Product Rules — bloque base + add-on keyguard>.
- **Resumen ES**:
  > Teclado + cobertor montado, centrado sobre fondo cálido pálido (gradiente suave estilo AlizIA, no banner ruidoso). Ángulo 3/4 alto con tilt suave, reflejos brillantes en el acrílico que confirman transparencia. Espacio negativo arriba y abajo para que después se superpongan las placas con texto ("Cobertor acrílico..." / "Mayor precisión..." / "Encontralo en tu valija" / disclaimer espasticidad).
- **Constraints / QA**:
  - SIN texto en la imagen — la placa se agrega en post (Pillow → overlay)
  - Espacio negativo arriba y abajo
  - Fondo AlizIA SUTIL (no banner saturado)
  - Cobertor + teclado leídos como UNIDAD
  - Reflejos suaves en el acrílico
- **Output**: `workspace/cierre-v1.png`

---

## Aprendizajes

> Se completa durante Paso 3 (QA por imagen). Notar acá qué cambió entre v1 y vN y por qué. Al cierre del flujo, separar aprendizajes generalizables (van a la skill) vs específicos del producto (van al Product Rules §3).
