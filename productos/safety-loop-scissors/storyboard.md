# Storyboard — Tijera adaptada (safety-loop-scissors v3)

> Producto: [`Product-rules-safety-loop-scissors.md`](Product-rules-safety-loop-scissors.md) (vigente al 2026-05-28)
> Hero canónico: [`product-hero.png`](product-hero.png) — job `f750ccf3-b3b2-425d-85c7-4ddbec59749f`, v4 aprobada 2026-05-28
> Avatar canónico: Mercedes — ref base `referencias/ref-images/ref-avatar-mercedes-base.webp`
> Guión pegado: 2026-05-28 por usuario (v3 — reemplaza v1/v2 del piloto Mercedes)
> Video ID en Sheet: `7` (slug `safety-loop-scissors-v3`)

---

## Fuente — guión v3

**Tijeras adaptadas**

**1. El problema**

Visual: Plano cerrado sobre una mesa de trabajo escolar. Se ven únicamente las manos de un alumno intentando utilizar una tijera común. Los movimientos muestran dificultad para introducir los dedos en los aros, sostener la tijera y coordinar el corte. El papel se mueve y la tijera pierde estabilidad.

Voz en off: *"Hay alumnos y alumnas que tienen dificultades para usar este tipo de tijera. A veces cuesta entender qué está pasando realmente. Pero podríamos estar frente a una dificultad motriz que podemos acompañar."*

**2. La presentación del material**

2.i) Visual: El avatar Mercedes levanta la tijera adaptada de la mesa y la muestra para la cámara, que hace un zoom medio al objeto.
Voz del avatar: *"Esta es la tijera adaptada."*

2.ii) Visual: Sobre un fondo limpio, unas manos con baja coordinación motriz interactúan con la tijera adaptada. Se muestra cómo el mango continuo acompaña el movimiento de apertura y cierre mediante una presión suave y controlada.
Voz en off: *"Está diseñada para que el movimiento de corte sea mucho más simple. En lugar de tener dos aros separados, tiene un mango continuo que solo necesita presión para abrir y cerrar."*

**3. El uso en el aula**

3.i) Visual: Plano general de un aula genérica argentina con alumnos trabajando alrededor de una mesa, todos con guardapolvo blanco. La cámara se acerca lentamente hacia un alumno que utiliza la tijera adaptada junto a sus compañeros. En plano detalle, se ven únicamente las manos con baja coordinación motriz utilizando la tijera para cortar papel con mayor estabilidad y acompañamiento en el movimiento.
Voz en off: *"No requiere coordinar los dedos ni ejercer fuerza para cortar."*

3.ii) Visual: El avatar Mercedes mostrándose segura frente a cámara, gesticulando para acompañar su frase.
Voz del avatar: *"Con esta tijera, el movimiento de corte es más accesible para quien la usa."*

3.iii) Visual: Varios niños haciendo manualidades, un niño con esta tijera cortando un papel mientras otros pegan papeles en un cuaderno alrededor de la mesa.
Voz en off: *"Así, logramos que el alumno o la alumna pueda participar de la actividad junto al resto del grupo."*

**4. El resultado**

Visual: El avatar Mercedes sostiene la tijera adaptada mientras habla a cámara dentro del aula. De fondo, desenfocado, se ven alumnos con guardapolvo blanco trabajando en distintas actividades.
Avatar / voz en off: *"Es una herramienta pensada para alumnos y alumnas que pueden presentar dificultades en la motricidad fina, en la fuerza de agarre o en la coordinación de ambas manos."*

**5. Cierre de producto**

Visual: La tijera sobre el fondo rosado de AlizIA, con un título llamativo "Tijera adaptada" / "Encontrala en tu valija." — estilo hipermotion.

---

## Plan de imágenes — 8 stills

| # | Escena | Rol | Modelo | Refs principales |
|---|---|---|---|---|
| E1 | El problema — manos con tijera COMÚN | escena_con_grip (sin avatar, sin producto adaptado) | `nano_banana_2` | (sin product-hero — usa tijera común) |
| E2-i | Mercedes levanta la tijera adaptada | escena_con_avatar + producto | `nano_banana_2` | `ref-avatar-mercedes-base.webp` + `product-hero.png` |
| E2-ii | Manos sobre fondo limpio interactuando con la tijera adaptada | escena_con_grip | `nano_banana_2` | `product-hero.png` + `ref-real-grip-hand-loop-side.jpg` |
| E3-i | Aula argentina + plano detalle manos cortando | escena_con_grip + entorno aula | `nano_banana_2` | `product-hero.png` + `ref-real-action-cutting-paper.png` |
| E3-ii | Mercedes segura frente a cámara, gesticulando | escena_con_avatar | `nano_banana_2` | `ref-avatar-mercedes-base.webp` + `product-hero.png` |
| E3-iii | Grupo de niños haciendo manualidades | escena_con_grip + grupo | `nano_banana_2` | `product-hero.png` |
| E4 | Mercedes en aula sostiene tijera, fondo alumnos desenfocados | escena_con_avatar + producto | `nano_banana_2` | `ref-avatar-mercedes-base.webp` + `product-hero.png` |
| E5 | Cierre brand AlizIA fondo rosado hipermotion | cierre_brand | `product-photoshoot/conceptual_product` | `product-hero.png` |

> Orden de generación: **estricto del guión** (E1 → E2-i → E2-ii → E3-i → E3-ii → E3-iii → E4 → E5). Primero E1 (fija el look documental). Una vez aprobada, paralelizar el resto.

---

## Bloque estético canónico (incluir en E1-E4)

```
Shot on a modern smartphone, candid documentary photography style, natural
ambient light (overcast window or warm interior bulbs, no studio lighting),
slight motion blur, subtle film grain, true-to-life colors gently saturated
and properly exposed (NOT washed-out, NOT cinematic graded), real everyday
clothing, imperfect natural framing. Clean, tidy, orderly environment
(shelves organized, desk clear) — NEVER cluttered or messy. Subject looking
at the object they are using (NOT at camera, unless explicitly noted).
```

Para escenas con avatar: añadir `warm closed-mouth gentle smile, NOT articulating words, NOT speaking — mouth closed and soft`. (Razón: el video no tendrá lipsync; ver hallazgos `CLAUDE.md`).

---

## E1 — El problema (manos con tijera común)

- **Rol**: `escena_con_grip` (sin producto adaptado — esta escena muestra la tijera tradicional como contraste)
- **Modelo**: `nano_banana_2`
- **Aspect / resolución**: `9:16` / `2k`
- **Refs (`--image`)**: ninguna específica del producto adaptado (es tijera común). Opcionalmente subir una ref genérica si hace falta — por ahora generar sin `--image` o con la ref documental de Mercedes para fijar estilo.
- **Resumen ES**:
  > Plano cerrado top-down sobre mesa escolar de madera clara. Manos de niño (~8 años, guardapolvo blanco) intentando usar una tijera común tradicional (con dos aros plásticos azules separados). Dedos forcejeando para entrar en los aros, papel blanco cuadriculado moviéndose, tijera ladeada. Comunica dificultad motriz. Estética documental celular.
- **Prompt EN**:
  > Shot on a modern smartphone, candid documentary photography style, natural ambient classroom light from a window (no studio lighting), slight motion blur, subtle film grain, true-to-life colors gently saturated. Top-down vertical 9:16 close-up shot of a child's small hands (~8 years old, wearing the cuffs of a white classroom smock "guardapolvo blanco") struggling to use a CONVENTIONAL TRADITIONAL SCISSOR with two separate plastic finger rings (royal blue plastic rings, sharp pointed steel blades, ~17 cm long — a standard school scissor, NOT an adaptive scissor). The child's fingers are awkwardly trying to enter the rings, the scissor is tilted at an unstable angle, a sheet of white squared-grid school paper is shifting slightly on the light wood desk surface. Show the difficulty and lack of stability. Clean tidy school desk (no clutter — just the paper, the scissor, maybe a pencil to the side). Imperfect natural framing. NO face, NO full body — just the hands and forearms in frame. NO adaptive Safety Loop scissor in this shot — this scene shows the conventional scissor problem.
- **Constraints / QA**:
  - **Tijera convencional, NO adaptiva**. Dos aros separados azules, hojas largas.
  - Solo manos (no cara, no cuerpo).
  - Mesa limpia y ordenada (anti-pattern: caos).
  - Estética foto-celular documental.
- **Output esperado**: `workspace/e1-v1.png`

---

## E2-i — Mercedes levanta la tijera adaptada

- **Rol**: `escena_con_avatar` + producto
- **Modelo**: `nano_banana_2`
- **Aspect / resolución**: `9:16` / `2k`
- **Refs (`--image`)**:
  - `referencias/ref-images/ref-avatar-mercedes-base.webp` (identidad Mercedes)
  - `product-hero.png` (canónico — define la morfología del producto)
- **Resumen ES**:
  > Mercedes (~30s, pelo castaño largo, remera/blusa clara) sentada en una mesa de aula, levantando la tijera adaptada verde lima hacia la cámara con la mano derecha. Plano medio (de cintura para arriba), cámara ligeramente abajo. Sonrisa cálida cerrada, mirando el producto, no a cámara. Estética documental celular, luz cálida de aula.
- **Prompt EN**:
  > `[BLOQUE ESTÉTICO]` Medium shot, vertical 9:16, of the same woman as in the reference image (mid-30s, warm medium-brown wavy long hair with subtle natural highlights (NOT dark, NOT black — softly sun-lit caramel brown), calm warm Argentine teacher/psychopedagogist energy, simple light-colored cotton blouse or grey t-shirt). She is seated at a school table in a tidy classroom, light wood desk, soft overcast window light from the side. She is HOLDING UP the adaptive Safety Loop scissor with her right hand, presenting it toward the camera at chest height. **The scissor MUST match the product-hero reference EXACTLY**: one single Safety Loop adapted scissor, RIGID SOLID OBJECT ~14 cm, OPEN V-shaped stainless blades at the top with rounded safety-blunt tips, silver pivot screw, two THICK lime-green plastic handles diverging in inverted-V from the pivot, and one continuous lime-green silicone teardrop loop at the bottom — NOT a conventional scissor, NOT two finger rings. Single product only, lime-green color only. She looks at the scissor (NOT at the camera) with a warm closed-mouth gentle smile, NOT articulating words, mouth closed and soft. Imperfect natural framing, smartphone documentary look.
- **Constraints / QA**:
  - Identidad Mercedes preservada (refs).
  - Producto = hero canónico (no inventar otra morfología).
  - Sonrisa cerrada, NO articulando palabras.
  - Mira el producto, no a cámara.
  - Una sola tijera, verde lima.
- **Output esperado**: `workspace/e2i-v1.png`

---

## E2-ii — Manos sobre fondo limpio interactuando con la tijera adaptada

- **Rol**: `escena_con_grip` (close-up manos + producto, sin avatar)
- **Modelo**: `nano_banana_2`
- **Aspect / resolución**: `9:16` / `2k`
- **Refs (`--image`)**:
  - `product-hero.png`
  - `referencias/ref-images/ref-real-grip-hand-loop-side.jpg` (grip canónico)
- **Resumen ES**:
  > Close-up vertical 9:16 sobre fondo limpio (mesa clara o paño claro neutro). Una sola mano de niño (~8 años) agarra el bucle continuo verde lima DESDE AFUERA — todos los dedos por fuera del bucle, pulgar también por fuera. Aprieta suavemente para que las cuchillas se abran y cierren. La tijera no corta papel todavía: solo muestra el mecanismo de squeeze. Estética documental celular.
- **Prompt EN**:
  > `[BLOQUE ESTÉTICO]` Close-up vertical 9:16, clean uncluttered light wood or pale neutral fabric background, soft natural ambient light. A single child's small hand (~8 years old, guardapolvo blanco cuff visible) holding the adaptive Safety Loop scissor. **CRITICAL HAND-ON-LOOP — fingers WRAP the continuous flexible lime-green silicone loop from OUTSIDE: all fingers (index, middle, ring, pinky) external, NO thumb inside the loop, NO fingers threaded through holes like a conventional scissor.** The whole hand gently squeezes the loop, demonstrating the simple low-force open/close motion of the blades at the top. **The scissor MUST match the product-hero reference EXACTLY** (RIGID SOLID OBJECT ~14 cm, open V-blades with rounded safety-blunt tips, silver pivot, thick lime-green handles diverging in inverted-V, continuous lime-green silicone teardrop loop). Single product only, lime-green only. NO paper being cut in this shot — focus on the squeeze grip mechanism. NO face, NO full body — just the hand and forearm in frame. Smartphone documentary look.
- **Constraints / QA**:
  - Grip canónico (todos dedos POR FUERA del bucle, pulgar también).
  - Una sola tijera, no inventar morfología.
  - No hay papel cortándose (eso es E3-i).
  - Solo mano, no cara.
- **Output esperado**: `workspace/e2ii-v1.png`

---

## E3-i — Aula argentina + manos cortando papel

- **Rol**: `escena_con_grip` + entorno aula (compone wide → detail)
- **Modelo**: `nano_banana_2`
- **Aspect / resolución**: `9:16` / `2k`
- **Refs (`--image`)**:
  - `product-hero.png`
  - `referencias/ref-images/ref-real-action-cutting-paper.png` (acción de corte real)
- **Resumen ES**:
  > Plano detalle vertical 9:16 de las manos de un niño (~8 años, guardapolvo blanco) usando la tijera adaptada verde para cortar una hoja blanca cuadriculada sobre una mesa escolar. Otros niños alrededor (apenas visibles en bordes, fuera de foco) trabajando. Aula argentina genérica luminosa. La hoja se mantiene estable, el corte avanza con control. Estética documental.
- **Prompt EN**:
  > `[BLOQUE ESTÉTICO]` Vertical 9:16 detail shot of a child's hands (~8 years old, white classroom smock "guardapolvo blanco" cuffs visible) cutting a sheet of white squared-grid school paper on a light wood school desk. The child uses the adaptive Safety Loop scissor with the canonical grip — **fingers WRAP the continuous lime-green silicone loop from OUTSIDE, all fingers external, NO thumb inside the loop**. The hand squeezes gently, the open V-blades at the top of the scissor are cutting the paper with stability and control. The non-dominant hand holds the paper flat on the desk. In the soft out-of-focus background, edges of other children's hands and smocks working alongside on the same table — bright Argentine classroom ambient daylight from windows, tidy organized environment. **The scissor MUST match the product-hero reference EXACTLY** (single Safety Loop scissor, lime-green only, open V-blades with safety-blunt tips, silver pivot, thick handles diverging in inverted-V, continuous teardrop loop). Single product only. NO face, NO full body. Smartphone documentary look.
- **Constraints / QA**:
  - Grip canónico (mismo que E2-ii).
  - Papel se mantiene estable (contraste con E1 donde se movía).
  - Compañeros visibles solo en bordes desenfocados.
  - Una sola tijera.
- **Output esperado**: `workspace/e3i-v1.png`

---

## E3-ii — Mercedes segura frente a cámara

- **Rol**: `escena_con_avatar`
- **Modelo**: `nano_banana_2`
- **Aspect / resolución**: `9:16` / `2k`
- **Refs (`--image`)**:
  - `referencias/ref-images/ref-avatar-mercedes-base.webp`
  - `product-hero.png` (puede sostener la tijera o tenerla en la mesa al costado — opcional)
- **Resumen ES**:
  > Mercedes (~30s, identidad consistente con E2-i y E4) en aula, plano medio. Postura segura, gesticulando con las manos para acompañar lo que dice. Mira hacia abajo a la tijera o ligeramente fuera de cámara (NO a cámara), sonrisa cálida cerrada. Tijera adaptada visible en una mano o sobre la mesa frente a ella. Estética documental celular.
- **Prompt EN**:
  > `[BLOQUE ESTÉTICO]` Medium shot, vertical 9:16, of the same woman as in the reference (mid-30s, warm medium-brown wavy long hair with subtle natural highlights (NOT dark, NOT black — softly sun-lit caramel brown), calm warm Argentine teacher energy, simple light blouse or grey t-shirt). She is seated at a tidy school table in a bright but soft-lit classroom. Confident open posture, hands moving slightly mid-gesture to accompany her speech. She holds the adaptive Safety Loop scissor in one hand or has it resting on the desk in front of her. She looks DOWN at the scissor / at the desk (NOT at the camera), warm closed-mouth gentle smile, NOT articulating words, mouth closed and soft. **The scissor (if visible) MUST match the product-hero reference EXACTLY** (single lime-green Safety Loop scissor, open V-blades with safety-blunt tips, silver pivot, thick handles diverging in inverted-V, continuous lime-green silicone teardrop loop). Single product. Imperfect natural framing, smartphone documentary look.
- **Constraints / QA**:
  - Misma identidad que E2-i y E4.
  - NO mira a cámara.
  - Sonrisa cerrada.
  - Una sola tijera si está visible.
- **Output esperado**: `workspace/e3ii-v1.png`

---

## E3-iii — Niños haciendo manualidades en grupo

- **Rol**: `escena_con_grip` + grupo (varios niños alrededor de mesa)
- **Modelo**: `nano_banana_2`
- **Aspect / resolución**: `9:16` / `2k`
- **Refs (`--image`)**:
  - `product-hero.png`
- **Resumen ES**:
  > Plano vertical 9:16 desde ¾ alto sobre mesa de aula. Tres-cuatro niños (~7-9 años, guardapolvo blanco) haciendo manualidades alrededor de la mesa: uno (en el centro o un costado claro) cortando con la tijera adaptada verde, los otros pegando papelitos en un cuaderno. Cabezas inclinadas al trabajo, conversación tranquila implícita. Inclusión visible. Estética documental celular.
- **Prompt EN**:
  > `[BLOQUE ESTÉTICO]` Vertical 9:16 three-quarter overhead shot of a tidy school desk with three or four children (~7-9 years old, all wearing white classroom smocks "guardapolvo blanco") doing arts-and-crafts together. One child uses the adaptive Safety Loop scissor to cut a colored paper strip — **canonical grip: fingers WRAP the lime-green silicone loop from OUTSIDE, all fingers external, NO thumb inside**. The other children are gluing small colored paper pieces into a notebook. Heads bent toward the work, calm focused group activity, soft Argentine classroom light from windows. **Only ONE adaptive Safety Loop scissor in the frame, matching the product-hero exactly** (single lime-green unit, open V-blades with safety-blunt tips, silver pivot, thick handles diverging in inverted-V, continuous teardrop loop) — NO multiple adaptive scissors, NO conventional scissors. Tidy organized classroom desk (papers, glue stick, notebook — no clutter). Smartphone documentary look, faces softly visible at angles (not posed to camera).
- **Constraints / QA**:
  - SOLO 1 tijera adaptada en frame (riesgo de duplicación si menciona "varios niños").
  - Grip canónico en el niño que la usa.
  - Inclusión grupal visible.
- **Output esperado**: `workspace/e3iii-v1.png`

---

## E4 — Mercedes en aula sostiene tijera, fondo alumnos desenfocados

- **Rol**: `escena_con_avatar` + producto + entorno aula
- **Modelo**: `nano_banana_2`
- **Aspect / resolución**: `9:16` / `2k`
- **Refs (`--image`)**:
  - `referencias/ref-images/ref-avatar-mercedes-base.webp`
  - `product-hero.png`
- **Resumen ES**:
  > Mercedes (~30s, misma identidad que E2-i y E3-ii) en aula argentina, plano medio. Sostiene la tijera adaptada verde lima frente a ella, acompañando con la otra mano un gesto natural. De fondo desenfocado se ven alumnos con guardapolvo blanco trabajando en distintas mesas. Foco en Mercedes y la tijera. Sonrisa cálida cerrada, mirando la tijera (no a cámara). Estética documental celular, luz cálida de aula.
- **Prompt EN**:
  > `[BLOQUE ESTÉTICO]` Medium shot, vertical 9:16, same woman as in the reference (mid-30s, warm medium-brown wavy long hair with subtle natural highlights (NOT dark, NOT black — softly sun-lit caramel brown), calm warm Argentine teacher/psychopedagogist energy, simple light blouse or grey t-shirt). She stands or sits in a bright tidy Argentine classroom, holding the adaptive Safety Loop scissor visibly in her front hand, the other hand gently accompanying with a natural mid-gesture. In the soft out-of-focus background, several students (~7-9 years old) in white classroom smocks "guardapolvo blanco" are visible working at different tables — heads down, focused, depth-of-field blur on them so Mercedes and the scissor remain crisp in foreground. She looks at the scissor (NOT at the camera) with a warm closed-mouth gentle smile, NOT articulating words, mouth closed and soft. **The scissor MUST match the product-hero reference EXACTLY** (single lime-green Safety Loop scissor, open V-blades with safety-blunt tips, silver pivot, thick handles diverging in inverted-V, continuous teardrop loop). Single product, lime-green only. Imperfect natural framing, smartphone documentary look.
- **Constraints / QA**:
  - Identidad Mercedes consistente (E2-i, E3-ii, E4 deben verse como la misma persona).
  - Producto = hero.
  - Sonrisa cerrada.
  - Fondo con alumnos pero desenfocado.
- **Output esperado**: `workspace/e4-v1.png`

---

## E5 — Cierre brand AlizIA fondo rosado hipermotion

- **Rol**: `cierre_brand`
- **Modelo**: `product-photoshoot/conceptual_product` (Higgsfield)
- **Aspect / resolución**: `9:16` / `2k`
- **Refs (`--image`)**: `product-hero.png`
- **Resumen ES**:
  > Tijera adaptada verde lima sobre fondo rosado AlizIA (rosa coral/pastel #F4B7C8 aprox), composición catalog vertical 9:16, levitación estilo "premium product reveal" / hipermotion. Texto del cierre se overlayea en post (Pillow) — el still **no incluye** el texto. La still solo tiene el producto sobre el fondo rosado dramático, listo para que en post se sumen los títulos.
- **Prompt EN**:
  > A single adaptive Safety Loop Easy Grip scissor (lime-green), RIGID SOLID OBJECT, levitating slightly tilted (~10-15° from vertical) at the center of a vertical 9:16 frame. Background is a soft warm coral-pink studio gradient (premium brand background, slight radial lighting), AlizIA brand aesthetic. Dramatic catalog studio softbox lighting from above-left, gentle soft shadow on the background plane behind the product. Premium e-commerce / product-reveal hero shot. **The scissor MUST match the product-hero reference EXACTLY** (single Safety Loop scissor, open V-blades with safety-blunt tips, silver pivot, thick lime-green handles diverging in inverted-V from pivot, continuous lime-green silicone teardrop loop at bottom). Single product only, lime-green only. NO text in the image (titles will be overlaid in post). NO hands, NO people, NO other objects. Clean, no clutter.
- **Constraints / QA**:
  - Producto = hero (misma morfología).
  - Fondo rosado AlizIA (coral suave).
  - SIN texto en la imagen (se overlayea después).
  - Solo producto, sin manos.
- **Output esperado**: `workspace/e5-v1.png`

---

## Aprendizajes (se llenan al cierre del lote)

*(reservado — al cierre del Paso 5, mover acá lo generalizable a la skill vs lo específico de este producto que va al Product Rules)*
