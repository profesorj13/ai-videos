---
name: generate-video
description: |
  Genera el lote de videos por escena (image-to-video) del producto AlizIA con
  Seedance 2.0, partiendo de imágenes y audios ya aprobados. Flujo: pre-check
  → motion-board.md (clasificación de casos + modelo + prompt extensivo) →
  canary one-shot → resto del lote → overlay audio → publicación del lote en
  Drive. Cada generación se trackea en `generations` con `tipo=video`.
  Optimiza para ONE-SHOT (cada generación es cara): prompt extensivo,
  modelo más económico que dé buena chance, decision tree por caso de escena.
  Cada retry mapea su causa raíz y consolida un lockdown en la skill.
  Depende de imágenes aprobadas + audios aprobados (no funciona si falta uno).
  Use cuando el usuario pida "generar videos del producto X", "armar los
  videos por escena", "motion-board", "image-to-video del producto X".
  NO usar para montaje final (queda en `ai-inclusion-videos` legacy), videos
  largos > 60s, ni para escenas que NECESITEN lipsync real (descartado por
  proyecto — ver caso A del decision tree).
argument-hint: "<producto-slug>"
allowed-tools: Bash, Read, Write, Edit, Skill, AskUserQuestion
---

# generate-video

Skill que transforma imágenes + audios aprobados en un **lote de videos por
escena aprobados y publicados para validación del equipo**. NO incluye el
montaje final del .mp4 único (eso vive en `ai-inclusion-videos` legacy hasta
crear `montaje-final`).

**Premisa central**: cada generación de video es cara. La skill optimiza para
**one-shot**:

- Prompt extensivo y causa-aware (con lockdowns ya aprendidos).
- Modelo más económico que dé buena chance para el caso.
- Canary obligatorio: primera escena se valida one-shot **antes** de lanzar el resto del lote.
- Cada retry se mapea (causa raíz) y se consolida como lockdown explícito en esta skill (Paso 5).

Las reglas globales viven en `CLAUDE.md`. Esta skill no las redefine.

---

## Plataforma

- Bash compatible (Mac, Linux, Git Bash o WSL en Windows). PowerShell para los bloques marcados.
- Paths **relativos al root del repo `ai-video/`**.
- Dependencias: `ffmpeg` (overlay audio, `ffprobe`), `python3` (Drive helper).

---

## Dependencias

- `Product-rules-<slug>.md` aprobado.
- **Imágenes aprobadas** en `productos/<slug>/imagenes-aprobadas/<escena>.png` (de `product-images-generation`).
- **Audios aprobados** en `productos/<slug>/audio/aprobados/vo-<escena>.mp3` (de `generate-audio`).
- Guión pegado por el usuario.

Si falta cualquiera de los tres, **parar** y avisar — esta skill no las genera.

---

## Paso 0 — Pre-check

```bash
SLUG="<producto-slug>"
ROOT="productos/$SLUG"

test -f "$ROOT/Product-rules-$SLUG.md"  || echo "FALTA: Product-rules-$SLUG.md"
test -d "$ROOT/imagenes-aprobadas"      || echo "FALTA: imagenes-aprobadas/"
test -d "$ROOT/audio/aprobados"         || echo "FALTA: audio/aprobados/"

mkdir -p "$ROOT"/videos/{workspace,logs,preview,discarded}
```

Para cada escena del guión, verificar que existen su `imagenes-aprobadas/<escena>.png` **y** `audio/aprobados/vo-<escena>.mp3`. Si falta alguno → parar.

---

## Casos canónicos de escena (clasificación obligatoria)

Cada bloque del motion-board declara su caso. **Esta clasificación define el
modelo, el prompt-pack y los lockdowns a aplicar.**

| Caso | Definición | Modelo | Justificación |
|---|---|---|---|
| **A — Avatar narrando (sin lipsync)** | Persona visible, VO en off (narración-sobre-gesto). Boca NO articula palabras. | `seedance_2_0` `--mode std` 720p, **silent** | Más barato. Lipsync real **descartado de proyecto** porque modelos con lipsync (Veo 3, etc.) imponen su propio TTS y se pierde la voz canónica Malena Clone v1. |
| **B — Avatar gestual (sin habla)** | Persona visible interactuando con el producto. El VO describe lo que se ve. Sonrisa cerrada permitida. | `seedance_2_0` `--mode std` 720p, **silent** | Idem A. Prompt declara `warm closed soft smile, NOT articulating words`. |
| **C — Producto puro / manos sin cara** | Sin persona visible (o solo manos). | `seedance_2_0` `--mode std` 720p, **silent** | Más barato. Micro-movimiento del objeto rígido + animación de cámara sutil. |
| **D — Cierre brand / kinetic** | Logo + texto, sin movimiento de actor. | **No generar** — still + transición FFmpeg basta. Skill **pregunta** antes de gastar créditos. | Lo más barato es no generar. |

**Regla absoluta para Seedance 2.0**: NUNCA pasar `--audio`. No hace
pass-through real: usa el MP3 como guía rítmica de animación pero sintetiza
su propio TTS al output. Generar **silent** y overlay con FFmpeg después.

---

## Paso 1 — `motion-board.md` + GATE 1

El motion-board es el **contrato de video**. Antes de tirar nada, el usuario
aprueba el board completo.

### Estructura por escena

```markdown
## E1

- **Caso**: A — Avatar narrando (sin lipsync)
- **Modelo**: `seedance_2_0 --mode std --resolution 720p` *(no pasar `--audio`)*
- **Duración** *(calculada con `ffprobe` sobre el VO)*: 5 s
  - VO `vo-e1.mp3` dura 4.3 s → `--duration 5` (cola ~0.7 s).
- **`--start-image`**: `productos/<slug>/imagenes-aprobadas/e1.png`
- **Prompt EN** *(causa-aware, copy-paste al CLI)*:
  > <bloque extenso — ver "Estructura del prompt EN" abajo>
- **Resumen ES** *(para el usuario antes del job)*:
  > <2-3 líneas en español describiendo el movimiento>
- **Lockdowns aplicados** *(de la sección "Lockdowns canónicos")*:
  - `[CAP-SLIDE]` `RIGID SOLID OBJECT — rigid parts stay FIXED, do NOT slide along the body`
  - `[CLOSED-MOUTH]` `warm closed soft smile throughout, NOT articulating words, NOT opening mouth`
  - `[IDENTITY]` `same person as in start-image, no facial restructuring`
  - `[PRODUCT-MULTIPLY]` `exactly ONE unit of the product on screen, do NOT duplicate or mirror`
- **Constraints / QA notes**:
  - Mantener fidelidad de la imagen de partida (no driftear identidad).
  - Movimiento sutil — no overshoot.
- **Output esperado**: `videos/workspace/e1-silent.mp4`
```

### Estructura del prompt EN (causa-aware)

5 bloques en orden:

1. **Subject**: qué se ve en la imagen de partida (resumido).
2. **Action**: qué movimiento sutil queremos.
3. **Camera**: estática / lento push-in / orbit corto / fija.
4. **Style**: continuar la estética documental "foto de celular" del still (ver `product-images-generation` §Estética visual).
5. **Constraints / Lockdowns**: cada lockdown de la sección "Lockdowns canónicos" que aplique al caso.

Plantilla:

```
[SUBJECT] <2-3 líneas describiendo el contenido de la start-image>.
[ACTION] <movimiento explícito — ej "subject slowly turns the product 15° clockwise">.
[CAMERA] <static / slow 5% push-in / fixed handheld microshake>.
[STYLE] continuous with smartphone-shot documentary look from the still — same lighting, same grain, no cinematic re-grading, no AI sheen.
[CONSTRAINTS]
- RIGID SOLID OBJECT — <piezas rígidas> stay FIXED, do NOT slide along <cuerpo>.
- <para caso A/B> warm closed soft smile throughout, NOT articulating words, NOT opening mouth, NOT speaking.
- IDENTITY LOCK — same person as in start-image, no facial restructuring, no age drift.
- EXACTLY ONE unit of <product> on screen, do NOT duplicate or mirror.
- NO objects appearing or disappearing.
```

### Lockdowns canónicos (crece con cada video — Paso 5)

| Tag | Causa de retry que evita | Bloque a pegar |
|---|---|---|
| `[CAP-SLIDE]` | Partes rígidas (cap, grip) "se deslizan" durante la animación | `RIGID SOLID OBJECT — <piezas> stay FIXED, do NOT slide along <cuerpo>` |
| `[CLOSED-MOUTH]` | Avatar abre la boca / articula palabras (descartado por proyecto) | `warm closed soft smile throughout, NOT articulating words, NOT opening mouth, NOT speaking` |
| `[IDENTITY]` | Drift de identidad facial entre escenas | `same person as in start-image, no facial restructuring, no age drift` |
| `[PRODUCT-MULTIPLY]` | Aparece 2+ unidades del producto | `EXACTLY ONE unit of <product> on screen, do NOT duplicate or mirror` |
| `[STATIC-BG]` | Fondo "vive" demasiado (otras personas se mueven raro) | `background stays static, no extra people moving, no objects appearing` |

*(Nuevos lockdowns se agregan acá tras cada retry mapeado en Paso 5.)*

### GATE 1 — Aprobación del motion-board

> "Motion-board listo en `<path>`. Te paso clasificación (caso A/B/C/D),
> modelo elegido, duración por escena, lockdowns aplicados y resumen ES por
> escena. Decime OK por escena o qué cambiar. No quemo créditos hasta tu OK."

---

## Paso 2 — Canary one-shot + lote

### Canary (obligatorio)

Tirar **una sola escena** primero (la primera del guión, o la que el usuario
indique). Validar one-shot. **No** lanzar el resto hasta validar.

```bash
higgsfield generate create seedance_2_0 \
  --prompt "<prompt EN del motion-board E1>" \
  --start-image "productos/$SLUG/imagenes-aprobadas/e1.png" \
  --duration 5 --aspect_ratio 9:16 --resolution 720p --mode std \
  --wait --wait-timeout 15m --json \
  > "productos/$SLUG/videos/logs/e1-v1.json"
```

Tracking inmediato a `generations` con `tipo=video`.

### Resultado del canary

- **OK one-shot** → tirar el resto del lote en paralelo (background).
- **Falla** → **Paso de causa raíz** (obligatorio antes de retry):
  1. Identificar exactamente qué falló (artefacto cap-slide, identity-drift, mouth-open, product-multiply, fondo movido, etc.).
  2. Mapear a un lockdown existente (si lo hay) o **proponer uno nuevo** al usuario.
  3. Anotar la causa en `## Aprendizajes` del motion-board.
  4. Trackear el descarte (`status=discarded`) con motivo en `prompt` y `asset_local` apuntando a `videos/discarded/`.
  5. Editar el bloque del motion-board con el lockdown aplicado.
  6. Recién entonces retry como `v2`.

> Si **dos canaries seguidos fallan por causas distintas**, aplicar
> *strategic reset* (ver `CLAUDE.md` §Regla #6.C). No iterar a ciegas.

### Resto del lote (post-canary OK)

Lanzar en paralelo, background. No spammear status — esperar y revisar logs:

```bash
for e in e2-i e2-ii e3-i e3-ii e4 e5; do
  higgsfield generate create seedance_2_0 \
    --prompt "<prompt del motion-board $e>" \
    --start-image "productos/$SLUG/imagenes-aprobadas/$e.png" \
    --duration $(jq -r ".duration" "productos/$SLUG/videos/logs/$e.plan.json") \
    --aspect_ratio 9:16 --resolution 720p --mode std \
    --wait --wait-timeout 15m --json \
    > "productos/$SLUG/videos/logs/$e-v1.json" 2>&1 &
done
wait
```

**Naming**: `<escena>-v<N>[-causa-retry].mp4`. Nunca pisar.

---

## Paso 3 — Overlay audio + GATE 2

Para cada `<escena>-silent.mp4` aprobado a nivel video, generar el preview
con audio:

```bash
ffmpeg -y \
  -i "productos/$SLUG/videos/workspace/<escena>-v1.mp4" \
  -i "productos/$SLUG/audio/aprobados/vo-<escena>.mp3" \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest \
  "productos/$SLUG/videos/preview/<escena>.mp4"
```

Subir cada `preview/<escena>.mp4` a Drive en `video-preview/` (igual que
audio en su Paso 3) y mostrar URL al usuario. **No mostrar `Read` local** —
no lo ve.

Decisión por escena: **OK** | **regenerar video** | **regenerar overlay**
(si el audio quedó corto/largo y hay que ajustar `-shortest` o `-t`).

Atender en QA:
- Identidad consistente del avatar entre escenas.
- Producto rígido (no cap-slide).
- Boca cerrada en casos A/B.
- Audio + video alineados en duración.

---

## Paso 4 — Publicar lote a Drive

Cuando **todos** los previews están aprobados:

```bash
ROOT_FOLDER_ID="16rGUnSWWMtnlAumavbZtDoOpegKqalUv"

PROD_FOLDER_ID=$(gws_find_or_create_folder "$SLUG" "$ROOT_FOLDER_ID")
VAL_FOLDER_ID=$(gws_find_or_create_folder "videos-a-validar" "$PROD_FOLDER_ID")

for mp4 in "productos/$SLUG/videos/preview/"*.mp4; do
  gws drive +upload "$mp4" --parent "$VAL_FOLDER_ID"
done

echo "https://drive.google.com/drive/folders/$VAL_FOLDER_ID"
```

> El helper `gws_find_or_create_folder` (bash + python3 cross-platform) está
> definido en `product-images-generation` §Paso 4.

---

## Paso 5 — Aprendizajes GENERALIZABLES + lockdowns

Esta es la sección **más importante** de esta skill. Cada retry que pasamos
en Paso 2/3 es una oportunidad de codificar un lockdown que evita el mismo
retry en el próximo producto.

Diferencia:

| Tipo | Dónde |
|---|---|
| Generalizable (vale para cualquier producto) | **A esta skill** — agregar fila a "Lockdowns canónicos" + ajustar plantilla del prompt EN |
| Específico del producto (terminología, partes únicas) | Al `Product-rules-<slug>.md` |
| Cross-skill (afecta también imágenes/audio) | A `CLAUDE.md` §Regla #6 |

Al cierre, revisar `## Aprendizajes` del motion-board y proponer al usuario:

- Qué filas nuevas se agregan a la tabla de Lockdowns canónicos.
- Qué cambios en la estructura del prompt EN (bloques, orden).
- Qué tag nuevo (`[XYZ]`) se acuña.

Aplicar tras OK del usuario. **El objetivo es que el próximo producto entre
con menos retries que este.**

---

## Anti-patterns

1. **Pasar `--audio` a Seedance 2.0.** No es pass-through. Genera su propio TTS y rompe la voz canónica. Siempre silent + overlay FFmpeg.
2. **Usar modelos con lipsync nativo** (Veo 3, etc.) para escenas con avatar. Imponen su TTS → pérdida de voz canónica. Caso A/B usan narración-sobre-gesto.
3. **Lanzar el lote completo antes de validar el canary.** Si la primera falla por una causa, las 7 siguientes probablemente también — y son créditos perdidos.
4. **Retry sin causa raíz mapeada.** Si no entendés por qué falló, no lo reintentes igual. Strategic reset.
5. **Prompt corto / sin lockdowns.** Cada generación es cara — el prompt extensivo es la inversión que paga el one-shot.
6. **Mostrar `Read` local al usuario.** No ve el video. Subir a Drive y pasar URL.
7. **Pisar archivos en regen.** `v<N+1>` siempre, sufijo con la causa.
8. **Saltarse el tracking de descartes.** Cada retry se trackea con motivo.
9. **Intentar montaje final acá.** Out of scope v1 — queda en `ai-inclusion-videos` legacy.

---

## Referencias

- Reglas globales: `CLAUDE.md`
- Skill previa imágenes: `.claude/skills/product-images-generation/SKILL.md`
- Skill paralela audio: `.claude/skills/generate-audio/SKILL.md`
- Skill legacy (incluye el montaje final por ahora): `.claude/skills/ai-inclusion-videos/SKILL.md`
- Drive root: https://drive.google.com/drive/folders/16rGUnSWWMtnlAumavbZtDoOpegKqalUv
- Sheet: `1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE`
