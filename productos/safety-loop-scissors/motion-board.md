# Motion-board — Tijera adaptada (safety-loop-scissors v3)

> Producto: [`Product-rules-safety-loop-scissors.md`](Product-rules-safety-loop-scissors.md)
> Imágenes aprobadas: `imagenes-aprobadas/E*.png` (v2 post-feedback equipo, 2026-06-09)
> Audios aprobados: `audio/aprobados/vo-*.mp3` (voz re-clonada `aKtTSeLwi8u4QiEEtGZ0`, sin filler)
> Video ID Sheet: `7` · Formato `9:16` · Modelo principal: `seedance_2_0 --mode std --resolution 720p`
> **Regla absoluta**: NUNCA pasar `--audio` a Seedance (no es pass-through real — sintetiza su propio TTS). Generar silent, overlay con FFmpeg después.

---

## Decisión de duración (Seedance acepta 4-10s)

| # | Audio VO | Duración Seedance | Estrategia |
|---|---|---|---|
| **E1** | 12.16s | `--duration 10` | VO supera 9.5s — `tpad=stop_mode=clone:stop_duration=2.16` en post para congelar último frame y cubrir audio |
| **E2-i** | 2.26s | `--duration 4` | mín Seedance, audio termina a 2.26 + apad, video corre 4s con cola visual |
| **E2-ii** | 10.11s | `--duration 10` | VO ~apenas pasado — `tpad clone +0.11s` en post |
| **E3-i** | 4.08s | `--duration 5` | Apenas mayor que VO, da cola natural |
| **E3-ii** | 4.77s | `--duration 6` | Cola natural |
| **E3-iii** | 6.12s | `--duration 7` | Cola natural |
| **E4** | 10.25s | `--duration 10` | `tpad clone +0.25s` en post |
| **E5** | sin VO | `--duration 4` | Mínimo, cierre brand micro-motion + overlays texto en post |

Costo estimado: ~200 créditos Seedance (10s × 8 ≈ 200 cr).

---

## Clasificación de casos por escena

| # | Caso | Avatar visible | Habla | Lockdowns a aplicar |
|---|---|---|---|---|
| **E1** | C — Manos sin cara | No | — | `[CAP-SLIDE]`, `[PRODUCT-MULTIPLY]`, `[STATIC-BG]` |
| **E2-i** | B — Mercedes presenta producto | Sí | No | `[CLOSED-MOUTH]`, `[IDENTITY]`, `[CAP-SLIDE]`, `[PRODUCT-MULTIPLY]`, `[STATIC-BG]` |
| **E2-ii** | C — Close-up grip sin cara | No | — | `[CAP-SLIDE]`, `[PRODUCT-MULTIPLY]` |
| **E3-i** | C — Manos cortando aula | No | — | `[CAP-SLIDE]`, `[PRODUCT-MULTIPLY]`, `[STATIC-BG]` |
| **E3-ii** | B — Mercedes gesticulando | Sí | No | `[CLOSED-MOUTH]`, `[IDENTITY]`, `[CAP-SLIDE]`, `[PRODUCT-MULTIPLY]`, `[STATIC-BG]` |
| **E3-iii** | C — Grupo niños manualidades | No (caras parciales) | — | `[CAP-SLIDE]`, `[PRODUCT-MULTIPLY]`, `[STATIC-BG]` |
| **E4** | A — Mercedes narrando aula | Sí | No | `[CLOSED-MOUTH]`, `[IDENTITY]`, `[CAP-SLIDE]`, `[PRODUCT-MULTIPLY]`, `[STATIC-BG]` |
| **E5** | D — Cierre brand | — | — | `[CAP-SLIDE]`, `[PRODUCT-MULTIPLY]` (micro-motion catalog) |

---

## E1 — El problema (manos con tijera común)

- **Caso**: C — Manos sin cara
- **Modelo**: `seedance_2_0 --mode std --resolution 720p` (silent)
- **Duración**: `5` — `vo-e1.mp3` dura 12.16s → tpad clone +2.16s en post para extender video al audio completo (último frame congela). Actualizo `--duration 10` para tener más video real antes del freeze.
- **`--start-image`**: `productos/safety-loop-scissors/imagenes-aprobadas/E1.png`
- **Resumen ES**: cámara cenital estática, sutil micro-shake de smartphone, las manos del niño hacen pequeño forcejeo recurrente con la tijera común (mover dedos hacia los aros sin lograr meterlos), el papel cuadriculado se desliza un poquito por la inestabilidad. Sin avatar visible. Transmite "dificultad".
- **Prompt EN**:
  > [SUBJECT] Top-down vertical 9:16 view of a child's small hands (white classroom smock cuffs visible) on a light wood school desk, struggling with a CONVENTIONAL traditional scissor (two royal-blue plastic finger rings, sharp pointed steel blades, ~17 cm long). A sheet of white squared-grid school paper lies on the desk.
  > [ACTION] The child's fingers are subtly trying to thread into the conventional scissor's finger rings — small recurring attempts and pulls. The paper shifts a tiny bit on the desk from the instability. NOT smooth cutting. The motion shows hesitation and lack of fine motor control. The conventional scissor stays in approximately the same position but at a slightly unstable angle.
  > [CAMERA] Top-down static smartphone shot with very subtle handheld micro-shake. NO push-in, NO orbit.
  > [STYLE] Continuous with the smartphone documentary look from the start-image — same warm natural classroom lighting, same subtle grain, same true-to-life colors. NO cinematic regrade, NO AI sheen.
  > [CONSTRAINTS]
  > - RIGID SOLID OBJECT — the conventional scissor's metal blades and plastic rings stay FIXED in proportion, do NOT slide or morph.
  > - EXACTLY ONE conventional scissor on screen, do NOT duplicate.
  > - Background (other children's hands and edges of pencils visible in the periphery) stays static, no extra people appearing.
  > - NO face, NO body — only hands and forearms in frame.
  > - The scissor is the TRADITIONAL one with two finger rings, NOT the adaptive Safety Loop.
- **Output esperado**: `videos/workspace/e1-silent-v1.mp4`

---

## E2-i — Mercedes presenta la tijera adaptada

- **Caso**: B — Mercedes gestual sin habla
- **Modelo**: `seedance_2_0 --mode std --resolution 720p` (silent)
- **Duración**: `4` — `vo-e2i.mp3` dura 2.26s. Video tiene cola natural de ~1.7s.
- **`--start-image`**: `productos/safety-loop-scissors/imagenes-aprobadas/E2-i.png`
- **Resumen ES**: Mercedes sentada en aula presenta sutilmente la tijera verde con su mano — pequeño movimiento de elevar o acercar el producto a la cámara unos centímetros. Sonrisa cerrada cálida, mira el producto (no a cámara). Cámara estática con micro-shake.
- **Prompt EN**:
  > [SUBJECT] Vertical 9:16 medium shot of the same woman as in the start-image (Mercedes, mid-30s Argentine teacher, warm caramel-brown wavy long hair, simple light blouse / grey t-shirt) seated at a school table in an Argentine classroom (cream walls, windows on the left, green chalkboard at back, pedagogical posters, light-wood desks, students with white guardapolvo smocks blurred in background). She holds the adaptive Safety Loop scissor (single lime-green silicone teardrop loop, two thick lime-green plastic handles, open V-blades, silver pivot) in her right hand at chest height.
  > [ACTION] Mercedes very subtly raises the scissor a few centimeters toward the camera (small presenting gesture, ~3 cm of vertical lift over 4 seconds). She keeps her gaze gently directed at the scissor (not at camera). Her smile stays warm and closed.
  > [CAMERA] Static smartphone medium shot with very subtle handheld micro-shake. NO push-in.
  > [STYLE] Continuous with the smartphone documentary look from the start-image — natural classroom light, subtle grain, true-to-life colors.
  > [CONSTRAINTS]
  > - WARM CLOSED SOFT SMILE throughout, NOT articulating words, NOT opening mouth, NOT speaking.
  > - IDENTITY LOCK — same person as start-image, same caramel hair, no facial restructuring, no age drift.
  > - RIGID SOLID OBJECT — the green silicone teardrop loop and rigid plastic handles stay FIXED in proportion, do NOT slide or morph mid-shot.
  > - EXACTLY ONE adaptive Safety Loop scissor on screen, do NOT duplicate or mirror.
  > - Background stays static — students in background do NOT move dramatically.
  > - The scissor is the ADAPTIVE Safety Loop (single teardrop loop), NOT a conventional scissor.
- **Output esperado**: `videos/workspace/e2i-silent-v1.mp4`

---

## E2-ii — Manos demostrando el mecanismo (squeeze + cuchillas cerradas)

- **Caso**: C — Close-up grip sin cara
- **Modelo**: `seedance_2_0 --mode std --resolution 720p` (silent)
- **Duración**: `10` — `vo-e2ii.mp3` dura 10.11s → `tpad clone +0.11s` en post para cubrir el audio entero.
- **`--start-image`**: `productos/safety-loop-scissors/imagenes-aprobadas/E2-ii.png`
- **Resumen ES**: close-up de la mano del niño sobre fondo neutro beige. Demuestra el mecanismo: la mano aprieta el bucle de silicona (apenas comprime) → las cuchillas cerradas se mantienen apretadas. Movimiento sutil de squeeze, sin abrir. Educativo.
- **Prompt EN**:
  > [SUBJECT] Vertical 9:16 close-up of a single child's small hand (white classroom smock cuff visible at the wrist) on a clean uncluttered light beige neutral background. The hand grips the adaptive Safety Loop scissor with the canonical grip: thumb extended along the upper rigid plastic handle pressing it from outside, four fingers inside the lime-green silicone teardrop loop. The two stainless V-blades at the top are CLOSED, touching each other as a single thin closed edge pointing upward (this is the "squeezed" position of the mechanism).
  > [ACTION] The hand subtly re-applies pressure — barely visible tightening of the grip (small breathing-like compression of the loop, ~1-2mm motion). The blades stay CLOSED throughout. NO opening of the blades. The product stays in approximately the same position.
  > [CAMERA] Static close-up with very subtle handheld micro-shake. NO push-in.
  > [STYLE] Continuous with the smartphone documentary look from the start-image — natural light, subtle grain.
  > [CONSTRAINTS]
  > - RIGID SOLID OBJECT — the silver pivot, rigid plastic handles, and blades stay FIXED in proportion, do NOT slide or morph.
  > - EXACTLY ONE adaptive Safety Loop scissor on screen.
  > - BLADES STAY CLOSED throughout (touching), do NOT open. This is the "compressed" position demonstrating the mechanism.
  > - NO face, NO body — only one hand and forearm in frame.
- **Output esperado**: `videos/workspace/e2ii-silent-v1.mp4`

---

## E3-i — Aula manos cortando

- **Caso**: C — Manos cortando aula
- **Modelo**: `seedance_2_0 --mode std --resolution 720p` (silent)
- **Duración**: `5` — `vo-e3i.mp3` dura 4.08s, cola ~0.92s.
- **`--start-image`**: `productos/safety-loop-scissors/imagenes-aprobadas/E3-i.png`
- **Resumen ES**: vista lateral del niño cortando papel cuadriculado en aula. Movimiento sutil de avance de la tijera adaptada cortando el papel (squeeze + slide horizontal). El papel se separa apenas en el borde de corte. Otros niños trabajando blurred al fondo.
- **Prompt EN**:
  > [SUBJECT] Vertical 9:16 detail shot of a child's hands (white classroom smock cuffs visible) cutting a sheet of white squared-grid school paper on a light wood school desk. The child uses the adaptive Safety Loop scissor (single lime-green silicone teardrop loop, rigid plastic handles, silver pivot, open V-blades). The canonical grip is in place: thumb along upper rigid handle, four fingers inside the silicone loop. Other children's hands and white smocks blurred in the background.
  > [ACTION] The scissor advances forward along the paper edge with a subtle squeeze-cut motion: the V-blades close briefly (1-2 cm advance) cutting the paper, then re-open slightly. Small repeating squeeze cycles, the hand advancing 1-2 cm horizontally along the cut line. The paper subtly separates at the cut edge.
  > [CAMERA] Static lateral smartphone shot with subtle handheld micro-shake. NO push-in.
  > [STYLE] Continuous with the smartphone documentary look from start-image — bright Argentine classroom daylight, subtle grain.
  > [CONSTRAINTS]
  > - RIGID SOLID OBJECT — the green silicone teardrop loop, rigid plastic handles, silver pivot stay FIXED in proportion, do NOT slide along each other or morph.
  > - EXACTLY ONE adaptive Safety Loop scissor in frame.
  > - The OTHER children in the background stay static, no dramatic movement, no extra people appearing.
  > - NO face, NO body — only hands and forearms in foreground.
  > - The scissor blades are CUTTING ALONG the paper (lateral cut), NOT stabbing down.
- **Output esperado**: `videos/workspace/e3i-silent-v1.mp4`

---

## E3-ii — Mercedes confiada gesticulando

- **Caso**: B — Mercedes gestual sin habla
- **Modelo**: `seedance_2_0 --mode std --resolution 720p` (silent)
- **Duración**: `6` — `vo-e3ii.mp3` dura 4.77s, cola ~1.23s.
- **`--start-image`**: `productos/safety-loop-scissors/imagenes-aprobadas/E3-ii.png`
- **Resumen ES**: Mercedes en aula, gesticulando con la mano libre mientras sostiene la tijera con la otra. Movimiento natural de "explicación con manos" — pequeña apertura de palma o mover dedos en aire. Sonrisa cerrada cálida, no mira a cámara.
- **Prompt EN**:
  > [SUBJECT] Vertical 9:16 medium shot of the same woman as start-image (Mercedes, mid-30s Argentine teacher, caramel-brown wavy hair, simple light blouse / grey t-shirt) seated at a school desk in an Argentine classroom (cream walls, windows on left, green chalkboard at back, pedagogical posters, students with white guardapolvo blurred in background). She holds the adaptive Safety Loop scissor in her right hand at table level; her left hand is in mid-gesture (palm open or fingers moving slightly).
  > [ACTION] Mercedes performs a small natural teaching hand-gesture with her LEFT hand — slight palm opening, small flexion of fingers, ~3 seconds of subtle motion. The right hand (holding the scissor) stays mostly stationary. She looks gently down at the scissor or her left hand, with her warm closed smile staying soft.
  > [CAMERA] Static medium shot with subtle handheld micro-shake.
  > [STYLE] Continuous with smartphone documentary look from start-image.
  > [CONSTRAINTS]
  > - WARM CLOSED SOFT SMILE throughout, NOT articulating words, NOT opening mouth, NOT speaking.
  > - IDENTITY LOCK — same person as start-image, same caramel hair, no facial restructuring.
  > - RIGID SOLID OBJECT — the green silicone loop, rigid handles, silver pivot stay FIXED.
  > - EXACTLY ONE adaptive Safety Loop scissor in frame.
  > - Background students stay static.
- **Output esperado**: `videos/workspace/e3ii-silent-v1.mp4`

---

## E3-iii — Grupo niños manualidades + uno cortando

- **Caso**: C — Grupo niños (caras parciales / blurred)
- **Modelo**: `seedance_2_0 --mode std --resolution 720p` (silent)
- **Duración**: `7` — `vo-e3iii.mp3` dura 6.12s, cola ~0.88s.
- **`--start-image`**: `productos/safety-loop-scissors/imagenes-aprobadas/E3-iii.png`
- **Resumen ES**: vista general de mesa de aula con varios niños haciendo manualidades. El niño en primer plano corta papel con la tijera adaptada (squeeze cut sutil avanzando). Los otros niños siguen pegando papeles (manos blurred). Atmósfera grupal natural.
- **Prompt EN**:
  > [SUBJECT] Vertical 9:16 three-quarter shot of three to four children (~7-9 years old, white classroom smocks guardapolvo blanco) around a wooden school desk in an Argentine classroom. One child in the foreground is cutting a colored paper strip with the adaptive Safety Loop scissor (single lime-green silicone teardrop, rigid handles, silver pivot, open V-blades) — canonical grip: thumb along upper handle, four fingers inside silicone loop. Other children are gluing small colored paper pieces into a notebook (glue stick, colored paper triangles/squares visible on desk).
  > [ACTION] The foreground child performs a subtle lateral squeeze-cut motion along the paper edge (1-2 squeeze cycles, ~2 cm advance horizontally). The other children continue their gluing activity with tiny natural hand motions (small placements of paper pieces, no dramatic movement). Background classroom (other tables, students at far distance) stays calm and static.
  > [CAMERA] Static smartphone shot with subtle handheld micro-shake.
  > [STYLE] Continuous with the smartphone documentary look from start-image — same Argentine classroom morning light, subtle grain.
  > [CONSTRAINTS]
  > - RIGID SOLID OBJECT — the adaptive scissor stays rigid in proportion.
  > - EXACTLY ONE adaptive Safety Loop scissor in the whole frame.
  > - Background students stay calm and static, no extra people appearing.
  > - The scissor blades are CUTTING ALONG the paper laterally, NOT stabbing down.
  > - NO heroic posing — natural group craft activity.
- **Output esperado**: `videos/workspace/e3iii-silent-v1.mp4`

---

## E4 — Mercedes en aula con fondo alumnos

- **Caso**: A — Mercedes narrando aula (sin lipsync)
- **Modelo**: `seedance_2_0 --mode std --resolution 720p` (silent)
- **Duración**: `10` — `vo-e4.mp3` dura 10.25s → `tpad clone +0.25s` en post.
- **`--start-image`**: `productos/safety-loop-scissors/imagenes-aprobadas/E4.png`
- **Resumen ES**: close-up portrait de Mercedes mostrando la tijera diminuta junto a su cara. Movimiento sutil: la otra mano puede acompañar con un mini-gesto, o Mercedes inclina apenas la cabeza. Estudiantes blurred al fondo siguen trabajando con micro-motion. Sonrisa cerrada cálida.
- **Prompt EN**:
  > [SUBJECT] Vertical 9:16 close-up portrait of the same woman as start-image (Mercedes, mid-30s Argentine teacher, caramel-brown wavy hair, white classroom smock). Her face occupies the upper 60% of the frame. She holds the TINY adaptive Safety Loop scissor (children's miniature, ~1/8 of her face height, lime-green silicone teardrop + rigid handles + silver pivot + open V-blades) near her chin with the canonical grip. Background: out-of-focus students at distant tables in the Argentine classroom (cream walls, windows on left, green chalkboard).
  > [ACTION] Mercedes performs a very subtle natural facial micro-motion (small blink, soft smile shift) and her holding hand may slightly turn the scissor 5-10° to present it from a marginally different angle. The background students stay calm and barely move (depth-of-field blurred, micro-motion only). She continues to look down/sideways at the tiny scissor (NOT at camera).
  > [CAMERA] Static close-up portrait with very subtle handheld micro-shake. NO push-in.
  > [STYLE] Continuous with the smartphone documentary look from start-image.
  > [CONSTRAINTS]
  > - WARM CLOSED SOFT SMILE throughout, NOT articulating words, NOT opening mouth, NOT speaking.
  > - IDENTITY LOCK — same person as start-image, same caramel hair, same warm presence, no facial restructuring, no age drift.
  > - RIGID SOLID OBJECT — green silicone teardrop, rigid handles, silver pivot stay FIXED in proportion.
  > - EXACTLY ONE adaptive Safety Loop scissor on screen, the SAME tiny size as in the start-image.
  > - Background students stay calm, no dramatic movement.
  > - The scissor stays TINY (children's miniature, fitting in her hand near her chin), do NOT enlarge it.
- **Output esperado**: `videos/workspace/e4-silent-v1.mp4`

---

## E5 — Cierre brand AlizIA

- **Caso**: D — Cierre brand (¿generar o still + transición?)
- **Modelo propuesto**: `seedance_2_0 --mode std --resolution 720p` (silent) si se genera. Alternativa: still + crossfade FFmpeg con un ken-burns muy sutil.
- **Duración**: `4` (mínimo Seedance). Sin VO — solo overlays de texto en post con Pillow.
- **`--start-image`**: `productos/safety-loop-scissors/imagenes-aprobadas/E5.png`
- **Resumen ES**: la tijera flota sobre el fondo coral rosado AlizIA. Micro-motion catalog: rotación lentísima 3-5° o pequeño bobbing vertical. Sin texto en el video (los títulos "Tijera adaptada / Encontrala en tu valija" se overlayean en post con Pillow).
- **Prompt EN**:
  > [SUBJECT] Vertical 9:16 catalog product hero shot of a single adaptive Safety Loop scissor (lime-green silicone teardrop loop, rigid plastic handles, silver pivot, open V-blades with rounded safety-blunt tips) levitating slightly tilted ~10-15° from vertical at the center of the frame. Background is a soft warm coral-pink studio gradient (AlizIA brand aesthetic).
  > [ACTION] Very subtle catalog micro-motion: the scissor SLOWLY rotates 3-5 degrees clockwise OR gently bobs up and down ~3 pixels over 4 seconds. Cinematic minimal product reveal motion. NO dramatic motion.
  > [CAMERA] Static catalog studio shot, NO camera movement.
  > [STYLE] Continuous with the catalog studio look from the start-image — soft pink gradient, gentle shadow, premium product reveal aesthetic.
  > [CONSTRAINTS]
  > - RIGID SOLID OBJECT — the scissor stays rigid in proportion as it rotates.
  > - EXACTLY ONE adaptive Safety Loop scissor on screen.
  > - NO text appearing (titles will be overlaid in post with Pillow).
  > - NO hands, NO people, NO other objects.
  > - Background stays as solid soft coral-pink gradient, no extra elements appearing.
- **Output esperado**: `videos/workspace/e5-silent-v1.mp4`

> **Decisión a confirmar con el usuario**: ¿generamos E5 con Seedance o solo
> usamos la still + crossfade FFmpeg con Ken Burns sutil? Generación cuesta
> ~20-30 cr y da micro-motion real; alternativa es 0 cr y se ve casi igual a
> esta resolución / duración. **Recomendación: solo still + Ken Burns en
> post**, es lo más eficiente y la diferencia visual a 4s es despreciable.

---

## Plan de generación

1. **Canary**: tirar `E1` solo. Validar one-shot.
2. Si E1 OK → tirar `E2-i, E2-ii, E3-i, E3-ii, E3-iii, E4` en paralelo (background).
3. `E5` se decide post-canary (generar o usar still + Ken Burns).
4. Por cada video: trackear inmediato en Sheet `generations` con `tipo=video`.
5. Por cada video terminado: overlay FFmpeg con el VO (`-map mixto`) + subir preview a Drive.

Costo estimado total: ~150-180 créditos Seedance (sin contar reintentos).
Saldo actual: 1803 créditos ✓.

---

## Aprendizajes (se llenan al cierre del lote)

*(reservado — al cierre del Paso 5, mover acá lo generalizable a la skill vs lo específico de este producto que va al Product Rules. Lockdowns nuevos detectados aquí se agregan a la tabla "Lockdowns canónicos" de la skill `generate-video`.)*
