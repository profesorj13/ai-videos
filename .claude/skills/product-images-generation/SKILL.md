---
name: product-images-generation
description: |
  Genera el lote completo de imágenes (stills first-frame) del video de un
  producto AlizIA partiendo de un guión pegado por el usuario. Flujo:
  pre-check de la carpeta del producto → Product Rules gate (obligatorio) →
  storyboard.md → product hero gate → generación con Higgsfield → QA por
  imagen → publicación del lote en Drive para validación del equipo. Cada
  generación se trackea en el Sheet en `generations` con `tipo=image`.
  Reemplaza la Etapa 1 de la skill `ai-inclusion-videos`.
  Use cuando el usuario pida "generar imágenes del producto X", "armar el
  storyboard de imágenes", "stills del video de X", "imágenes para el video
  de X", "tirar las imágenes del guión", o cuando ya haya un guión validado
  y la próxima etapa sea producir las imágenes.
  NO usar para audios (skill futura `generate-audio`), videos image-to-video
  (skill futura `generate-video`), ni para imágenes sueltas sin guión
  (`higgsfield-generate` / `higgsfield-product-photoshoot`).
argument-hint: "<producto-slug>"
allowed-tools: Bash, Read, Write, Edit, Skill, AskUserQuestion
---

# product-images-generation

Skill que transforma un guión validado en un **lote de imágenes aprobadas y
publicadas para validación del equipo**. Hay **un solo video por producto** —
toda la generación cuelga directo de `productos/<producto-slug>/`, sin
subniveles.

El valor está en los gates (Product Rules → storyboard → product hero →
imágenes) y en cerrar el loop de aprendizaje: cada regeneración deja una
mejora candidata para la skill o para el `Product-rules-<slug>.md`.

Las reglas globales (tracking inmediato al Sheet, no pisar archivos, stack
cerrado, sin polling visible, hallazgos del piloto) viven en `CLAUDE.md`.
Esta skill las **respeta**, no las redefine.

---

## Plataforma

- Asume **bash compatible** (macOS, Linux, Git Bash o WSL en Windows). El
  equipo trabaja entre Mac y Windows: cuando un comando es Windows-tricky,
  hay alternativa PowerShell anotada.
- Paths siempre **relativos al root del repo `ai-video/`** (donde está este
  `CLAUDE.md`). No hardcodear `/Users/...` ni `C:\Users\...`.
- Dependencias del Paso 4 (Drive): `python3` (cross-platform). No usar `jq`
  (no nativo en Windows).

---

## Argumento

- `<producto-slug>` *(obligatorio)*: ej `safety-loop-scissors`. Debe existir como `productos/<producto-slug>/`.

---

## Paso 0 — Pre-check de carpeta del producto

Verificar que el usuario tiene la estructura mínima. Los paths son
relativos al root del repo.

```bash
SLUG="<producto-slug>"
ROOT="productos/$SLUG"

test -f "$ROOT/Product-rules-$SLUG.md"        || echo "FALTA: Product-rules-$SLUG.md"
test -d "$ROOT/referencias"                    || echo "FALTA: referencias/"
test -d "$ROOT/referencias/ref-images"         || echo "FALTA: referencias/ref-images/"
```

> `referencias/ref-images/` debe contener al menos una foto del producto
> tomada del mundo real (web del fabricante, foto del producto físico).
> No requerimos una `hero.png` externa preacordada — la imagen "manda visual"
> del producto la genera la skill en el Paso 1.5 (`product-hero.png`).

Si **algo** falta → parar, mostrar qué falta y la estructura esperada, y
ofrecerle al usuario crear los huecos vacíos (no inventar contenido).

Estructura esperada (sin subniveles de proyecto):

```
productos/<producto-slug>/
├── Product-rules-<producto-slug>.md   # contrato del producto (6 bloques, GATE 0.5)
├── referencias/                       # input externo (subido por el equipo)
│   └── ref-images/                    # fotos reales del producto, web, etc.
├── product-hero.png                   # output Paso 1.5 — ref canónica generada
├── storyboard.md                      # output Paso 1
├── workspace/                         # iteración + descartes + logs
│   ├── hero/                          # versiones hero-v1.png, hero-v2.png...
│   ├── logs/                          # JSON por job
│   └── discarded/                     # se llena solo al cierre del flujo
├── imagenes-aprobadas/                # finales locales por escena
└── imagenes-a-validar/                # espejo de lo que sube a Drive
```

Cuando el pre-check pasa, crear las subcarpetas de trabajo:

```bash
mkdir -p "$ROOT"/{workspace/{hero,logs,discarded},imagenes-aprobadas,imagenes-a-validar}
```

**PowerShell**: `New-Item -ItemType Directory -Force -Path "$ROOT/workspace/hero","$ROOT/workspace/logs","$ROOT/workspace/discarded","$ROOT/imagenes-aprobadas","$ROOT/imagenes-a-validar"`

---

## Paso 0.5 — Product Rules (gate obligatorio)

**Nada se genera sin un `Product-rules-<slug>.md` aprobado.** Ni el hero, ni
las escenas. Esta regla es dura: si la primera invocación a Higgsfield sale
antes del OK del usuario sobre este archivo, hay que regenerar todo el lote
después porque las stills no van a respetar la anatomía / restricciones.

### Estructura canónica del `Product-rules-<slug>.md` (6 bloques)

```markdown
# Product Rules — <Nombre del producto> (<slug>)

## 1. Qué es
<1 párrafo: qué objeto es, para qué inclusión sirve, contexto de uso típico>

## 2. Anatomía
<componentes del producto descritos uno a uno: forma, color, material, escala>
- componente A: ...
- componente B: ...

## 3. Restricciones
<lista de lo que NO debe verse en las stills: deformaciones, errores comunes
del modelo, anti-patterns visuales>
- no fusionar dos unidades en una forma simétrica (mariposa / pétalos / labios)
- no rotar más de 30°
- no mostrar piezas internas
- ...

## 4. Uso (grip / interacción)
<cómo se sostiene / usa el producto físicamente — explícito para el modelo>
- grip humano: dedos sobre <parte X>, pulgar <descripción>
- escala respecto a una mano adulta: ...

## 5. Prompt base — descripción exhaustiva del producto (EN)
<bloque en inglés copy-paste, listo para incrustar en cualquier prompt de
escena con el producto. Debe ser tan detallado que un modelo que solo lea
este bloque pueda reconstruir el producto sin ver ninguna imagen.>

```
<prompt en inglés, ~80-150 palabras>
```

## 6. Product Hero
- Path local: `product-hero.png`
- Job ID Higgsfield: `<uuid>`
- URL CDN: `<https://...cloudfront...png>`
- Versión aprobada: `v<N>` (anterior: descartadas en `workspace/hero/discarded/`)
- Fecha de aprobación: `YYYY-MM-DD`
```

### Cuándo existe ya el archivo

- Si lo tiene completo y al día → mostrarle al usuario los 6 bloques resumidos en español y pedir confirmación de "vigente" antes de seguir.
- Si está incompleto (faltan bloques, falta hero, etc.) → completar con él los bloques faltantes.

### Cuándo NO existe todavía

- Generar borrador a partir de:
  - Las `referencias/ref-images/*` (describir objetivamente componente por componente — NO desde memoria del modelo).
  - Lo que el usuario diga sobre uso/inclusión.
- Pedirle al usuario aprobación bloque por bloque (los 5 primeros).
- Bloque 6 (product hero) requiere generación (Paso 1.5).

### GATE 0.5 — Aprobación del Product Rules

> "`Product-rules-<slug>.md` listo en `<path>`. Te paso los 6 bloques
> resumidos en español para validar antes de tocar imágenes. Decime OK por
> cada bloque o qué cambiar."

**No avanzar a Paso 1 hasta tener los 5 primeros bloques aprobados.** El
bloque 6 (Product Hero) se completa en Paso 1.5.

---

## Paso 1 — Obtener el guión y generar `storyboard.md`

El guión **no vive en disco**. El equipo lo redacta en un Google Docs y lo
pega al invocar la skill.

- Si el usuario ya lo pegó en el prompt → usar ese.
- Si no → pedirlo con `AskUserQuestion`: *"Pegá el guión completo (escenas
  con narración y descripción visual)."*

El `storyboard.md` **es** el plan de generación. Si está bien, las imágenes
salen bien al primer intento.

### Inputs para escribir el storyboard

1. `productos/<slug>/Product-rules-<slug>.md` — contrato (los 6 bloques).
2. `productos/<slug>/referencias/ref-images/*` — refs visuales adicionales.
3. **El guión pegado por el usuario**.
4. **Si el guión incluye avatares humanos**: `productos/_shared/avatars/<avatar>/Avatar-rules-<avatar>.md` — contrato canónico del avatar (descripción física + ropa + sonrisa + mirada, leída desde la foto base, NO desde memoria). Para Mercedes: [`productos/_shared/avatars/mercedes/Avatar-rules-mercedes.md`](../../../productos/_shared/avatars/mercedes/Avatar-rules-mercedes.md). Si el avatar no tiene Avatar Rules todavía, **abrir su foto base, describirla bloque por bloque, y crear el archivo** antes de redactar el storyboard. La descripción del avatar incrustada en cada prompt de escena debe ser **copia exacta del §5 del Avatar Rules** — no improvisar variaciones por escena.

### Estética visual (v4 — "documental real")

**Las stills deben leerse como foto de celular, no como render IA.** Esto es
una decisión de proyecto, validada contra una foto real de aula AlizIA.

Bloque de prompt canónico (incluir o adaptar en cada escena con persona o
entorno visible):

```
Shot on a modern smartphone, candid documentary photography style, natural
ambient room light (overcast window or warm interior bulbs, no studio
lighting), slight motion blur, subtle film grain, true-to-life colors
gently saturated and properly exposed (NOT washed-out, NOT cinematic
graded), real everyday clothing, imperfect natural framing, subject looking
at the object they are using (NOT at camera). Clean, tidy, orderly
environment (shelves organized, desk clear) — NEVER cluttered or messy.
```

**Reglas estéticas duras**:
- Look documental de celular, NO render pulido.
- Entorno **ordenado y prolijo** (anti-pattern: caos, cables sueltos, mesa atestada).
- Colores **apenas vivos**, fieles a la vida — ni flat ni grading cinematográfico.
- **No atarse a "aula maker"**: el entorno es libre (escritorio, espacio neutro, aula). Lo que importa es la estética, no el lugar.
- **Primeros planos preferidos**: close-up / medium close-up esconden fondo y bajan el riesgo "IA". No hace falta ver mucho entorno.
- Gesto candid (mirando al objeto, NO a cámara).
- Avatares humanos: **smile cálido y cerrado, NOT articulating words** (porque el video después no tiene lipsync; ver hallazgos en `CLAUDE.md`).

### Estructura de `storyboard.md`

Un bloque por imagen. Embebé el **guión completo** al principio como sección
"Fuente" para que quede trazable junto al plan, ya que no vive en disco.

```markdown
# Storyboard — <producto>

> Producto: `Product-rules-<slug>.md` (vigente al <fecha>)
> Hero canónico: `product-hero.png` (job `<uuid>`, vN aprobada)
> Guión pegado: YYYY-MM-DD por <usuario>

## Fuente — guión

<pegar acá el texto completo del guión, tal cual lo entregó el usuario>

---

## E1 — <título de la escena>

- **Rol**: `producto_puro` | `escena_con_avatar` | `escena_con_grip` | `cierre_brand`
- **Modelo**: `nano_banana_2` | `product-photoshoot/conceptual_product` | `product-photoshoot/closeup_product_with_person`
- **Aspect / resolución**: `9:16` / `2k`
- **Refs (--image)**:
  - `product-hero.png` *(canonical — siempre que la escena tenga el producto)*
  - `referencias/ref-images/<otra>.jpg` *(si aplica, justificar por qué)*
- **Prompt EN** *(copy-paste al CLI)*:
  > <prompt completo en inglés, incluyendo el bloque de estética documental
  > y el "Prompt base" del Product Rules §5>
- **Resumen ES** *(para el usuario antes de tirar el job, regla v2)*:
  > <2-3 líneas en español describiendo qué se va a generar>
- **Constraints / QA**:
  - Respetar anatomía §2 del Product Rules
  - **1 producto único** cerca de la mano (nunca 2+; ver hallazgos)
  - Anclaje de escala explícito (ej "~length of two adult palms / ~14 cm")
  - Grip: `CRITICAL HAND-ON-GRIP — fingers grip DIRECTLY ON the product, NOT above it and NOT on the bare barrel`
  - Avatar: smile cálido cerrado, no articulando palabras
- **Output esperado**: `workspace/e1-v1.png`

---

## E2-i — ...
```

### GATE 1 — Aprobación del `storyboard.md`

> "Storyboard listo en `<path>`. Revisalo (prompts, refs, modelos por escena)
> y decime si arranco a generar. No quemo créditos hasta tu OK."

Si pide cambios → editar el storyboard, no empezar a generar.

---

## Paso 1.5 — Generar el Product Hero (cierra GATE 0.5)

Antes de generar **cualquier** escena, generar la still del producto puro
sobre fondo neutro: sin manos, sin avatar. Es la ref canónica que se va a
pasar como `--image` en TODAS las escenas con producto. Más confiable que
describir componentes a ciegas: el modelo copia una imagen ya validada.

```bash
# Subir las refs al CDN UNA SOLA VEZ y reusar los UUIDs (evita AccessDenied
# transitorio del uploader). Guardar los UUIDs en una sección al final del
# Product-rules-<slug>.md para no perderlos.
higgsfield generate create nano_banana_2 \
  --prompt "<prompt base §5 del Product Rules> on a neutral pale background, studio softbox catalog look, centered, isolated product, no hands, no people, 9:16 vertical" \
  --image "productos/$SLUG/referencias/ref-images/<best-ref>.jpg" \
  --aspect_ratio 9:16 --resolution 2k \
  --wait --wait-timeout 8m --json \
  > "productos/$SLUG/workspace/logs/hero-v1.json"
```

- Output a `workspace/hero/hero-v1.png` (luego v2, v3 si hay regen).
- Trackear inmediatamente en `generations` con `escena=hero`, `tipo=image`.
- Mostrar URL CDN al usuario (Read local NO sirve — el usuario no la ve).

### GATE Hero — Aprobación del Product Hero

> "Hero v1: <URL CDN>. ¿La uso como ref canónica de todas las escenas, o
> regeneramos?"

Cuando aprueba: copiar a `productos/<slug>/product-hero.png` (path canónico)
y completar el bloque §6 del `Product-rules-<slug>.md` con job_id, URL CDN,
versión y fecha.

---

## Paso 2 — Generar las imágenes de escena

Ejecutar los bloques del storyboard en el orden del guión. Por defecto, una
imagen a la vez (la primera fija el "look": identidad del avatar, paleta).
Una vez aprobada la primera, paralelizar el resto en background.

### Convenciones

- Output a `workspace/<escena>-v<N>.png`. Nunca pisar: `v1`, `v2-grip-wrong`, `v3-identity-drift`, ...
- Logs JSON a `workspace/logs/<escena>-v<N>.json`.
- Refs siempre con **paths relativos al root del repo** (`productos/<slug>/...`) o **UUIDs del CDN** ya subidos.

### Decision tree de modelo

| Rol de la imagen | Modelo |
|---|---|
| Producto puro / catalog look | `higgsfield product-photoshoot create --mode conceptual_product` |
| Escena con producto (con o sin manos) | `nano_banana_2` con `product-hero.png` + 1 ref de uso si aplica |
| Avatar humano desde 1 foto base | `nano_banana_2` + foto base como `--image` |

### Hallazgos de prompt-craft (consolidados — incluir en el prompt si aplica)

1. **1 producto único cerca de la mano**. Con 2+ unidades NB Pro las fusiona en formas simétricas deformes (mariposa, pétalos, labios). Si el guión pide "varios", priorizar fidelidad del producto y bajar a 1.
2. **Anclaje de escala explícito**. "Tamaño real" no alcanza. Anclar a una medida humana: `"~length of two adult palms / ~14 cm, thin like an ordinary BIC pen"`.
3. **Hand-on-grip explícito**. El modelo por default agarra al lado, no sobre. Forzar: `CRITICAL HAND-ON-GRIP — fingers grip DIRECTLY ON the product, NOT above it and NOT on the bare barrel`.
4. **Texto manuscrito en hojas**. Pedir palabras reales simples (`"Hola/mamá/casa/sol/mesa" + lined practice rows a-a-a`), explícito `"tidy and legible, NOT random scribbles"`, acotar tamaño (`"fits within two lined rows"`). Evita glifos-garabato falsos.
5. **Refs como UUIDs CDN reusables**. Subir cada ref UNA SOLA VEZ y reusar el UUID en toda la skill (evita `AccessDenied` transitorio del uploader). Guardar UUIDs en una tabla al pie del Product Rules.
6. **Edición manual del usuario en Photoshop** es una ref canónica válida. Si el usuario edita una still en Photoshop para fixear un problema, subir esa al CDN y reusarla como `--image` en regeneraciones.

### Comunicación con el usuario — antes de tirar el job

Regla v2: **prompts en español resumido al usuario, inglés completo solo al
modelo**. Antes de cada llamada, mostrar:

- 2-3 líneas de resumen en español de qué se va a generar.
- Bloque ` ```en ` con el prompt en inglés colapsado/citado (no esperar OK por texto — ver "generate-and-show").

### Generate-and-show (durante iteración post-GATE 1)

Para prompts visuales concretos (post-GATE 1 del storyboard), **generar
directo y adjuntar prompt + URL del resultado en el mismo turno**, en vez
de esperar OK del texto del prompt. Ahorra un turno; el usuario juzga mejor
sobre la imagen que sobre el texto.

Pre-aprobación SOLO cuando hay ambigüedad real (qué producto, qué slug,
decisión de pipeline, cambio de modelo, regeneración masiva).

### Tracking (obligatorio, inmediato — Regla #1 de `CLAUDE.md`)

Después de **cada** job que retorna, **antes** de mostrar el resultado al
usuario, append a `generations` con `tipo=image`. Bulk-append si lanzaste N
jobs en paralelo. Ver `CLAUDE.md` §"Estructura real del Sheet".

Mínimo a registrar por imagen: `escena` (E1, hero, etc.), `modelo`, `prompt`
exacto enviado al CLI, `status`, `job_id`, `url_resultado`, `asset_local`
(`productos/<slug>/workspace/e1-v1.png`).

---

## Paso 3 — QA por imagen y decisión

Por cada imagen generada:

1. Mostrarle al usuario la **URL CDN** + path local + la nota de constraints del bloque del storyboard correspondiente. **Nunca asumir que el usuario ve el archivo local** (`Read` / `Invoke-Item` no le muestran nada — siempre URL CDN compartible).
2. Pedir decisión: **OK** | **regenerar** | **descartar y reescribir bloque**.

### Si OK

- Copiar a `imagenes-aprobadas/<escena>.png` (nombre limpio). El original queda en `workspace/` por trazabilidad.
- Marcar el bloque del storyboard como ✅ aprobado con el path final.

### Si regenerar

- Identificar el problema (grip incorrecto, identidad drift, fondo equivocado, NSFW falso positivo, etc.).
- **Antes de regenerar**, decidir si el problema es del prompt (editar el bloque del storyboard) o del muestreo (mismo prompt, nueva seed).
- Tirar `v<N+1>` con sufijo descriptivo (`-grip-wrong`, `-identity-drift`).
- Trackear la descartada en el Sheet con `status=discarded` y motivo.
- Anotar el motivo en `## Aprendizajes` al final del storyboard.

### Si descartar y reescribir

- Editar el bloque del storyboard antes de tirar otro prompt. El bloque queda con `# DESCARTADO — motivo` arriba y el nuevo debajo.

### Strategic reset (v2 — anti-pattern)

Si llevamos **3-4 iteraciones sin progreso** sobre la misma escena, **parar
y reiniciar limpio**. Síntomas: el modelo se atasca en el mismo error, las
correcciones del prompt no cambian el output, estamos probando lo mismo
desde 3 ángulos distintos. Acciones:

- Parar.
- Replantear con el usuario: ¿es problema del prompt, del modelo, de las refs, del Product Rules?
- Si es del Product Rules → actualizar §2/§3 con el aprendizaje y rearmar el bloque del storyboard desde cero.
- Si es de las refs → ver si una edición manual del usuario en Photoshop puede destrabar.
- Si es del modelo → probar el otro modelo del decision tree (NB Pro ↔ product-photoshoot).

**No iterar 5+ veces sobre el mismo modelo mental que falla.**

---

## Paso 4 — GATE 2 + publicación a Drive

Cuando **todas** las imágenes del storyboard tienen su `v<N>` aprobada en
`imagenes-aprobadas/`:

1. Copiar el lote a `imagenes-a-validar/`.
2. Subir a Drive en una subcarpeta del root del equipo.

### Estructura en Drive

Root del equipo: `16rGUnSWWMtnlAumavbZtDoOpegKqalUv` (carpeta "videos-ia / productos").

```
<root>/
└── <producto-slug>/
    └── imagenes-a-validar/
        ├── E1.png
        ├── E2-i.png
        └── ...
```

### Comandos reales (cross-platform: bash + python3, NO jq)

Sintaxis verificada (`gws drive --help`):
- Crear carpeta: `gws drive files create --json '{...}'` (no existe `+mkdir`).
- Subir archivo: `gws drive +upload <file> --parent <ID>`.

Helper bash idempotente — usa `python3` (cross-platform) para parsear JSON:

```bash
ROOT_FOLDER_ID="16rGUnSWWMtnlAumavbZtDoOpegKqalUv"
SLUG="<producto-slug>"
LOCAL_DIR="productos/$SLUG/imagenes-a-validar"

gws_find_or_create_folder() {
  local name="$1" parent="$2"
  # Buscar
  local found
  found=$(gws drive files list --params "$(python3 -c "
import json, sys
print(json.dumps({
  'q': f\"name = '{sys.argv[1]}' and '{sys.argv[2]}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false\",
  'fields': 'files(id,name)'
}))" "$name" "$parent")" \
    | python3 -c "import json,sys; d=json.load(sys.stdin); print((d.get('files') or [{}])[0].get('id',''))")
  if [[ -n "$found" ]]; then
    echo "$found"; return
  fi
  # Crear
  gws drive files create --json "$(python3 -c "
import json, sys
print(json.dumps({
  'name': sys.argv[1],
  'mimeType': 'application/vnd.google-apps.folder',
  'parents': [sys.argv[2]]
}))" "$name" "$parent")" \
    | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])"
}

PROD_FOLDER_ID=$(gws_find_or_create_folder "$SLUG" "$ROOT_FOLDER_ID")
VAL_FOLDER_ID=$(gws_find_or_create_folder "imagenes-a-validar" "$PROD_FOLDER_ID")

for img in "$LOCAL_DIR"/*.png; do
  gws drive +upload "$img" --parent "$VAL_FOLDER_ID"
done

echo "https://drive.google.com/drive/folders/$VAL_FOLDER_ID"
```

**Windows / PowerShell** (mismo `gws` CLI, sintaxis nativa para el loop):

```powershell
$RootFolderId = "16rGUnSWWMtnlAumavbZtDoOpegKqalUv"
$Slug = "<producto-slug>"
$LocalDir = "productos/$Slug/imagenes-a-validar"

function Get-OrCreateFolder($Name, $Parent) {
  $q = "name = '$Name' and '$Parent' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
  $params = @{ q = $q; fields = "files(id,name)" } | ConvertTo-Json -Compress
  $found = gws drive files list --params $params | ConvertFrom-Json
  if ($found.files.Count -gt 0) { return $found.files[0].id }
  $body = @{ name = $Name; mimeType = "application/vnd.google-apps.folder"; parents = @($Parent) } | ConvertTo-Json -Compress
  return (gws drive files create --json $body | ConvertFrom-Json).id
}

$ProdId = Get-OrCreateFolder $Slug $RootFolderId
$ValId  = Get-OrCreateFolder "imagenes-a-validar" $ProdId

Get-ChildItem "$LocalDir/*.png" | ForEach-Object {
  gws drive +upload $_.FullName --parent $ValId
}

"https://drive.google.com/drive/folders/$ValId"
```

### Mensaje al usuario al cerrar el gate

> "Subido a Drive: <URL>. Equipo puede comentar/aprobar ahí. Cuando tengas
> feedback, lo aplicamos como otra ronda (Paso 3). Si todo queda firme,
> cerramos con el Paso 5 (aprendizajes a la skill / Product Rules)."

---

## Paso 5 — Aprendizajes GENERALIZABLES

Énfasis: el conocimiento que sale de **este** video debe aplicar a **todos
los productos futuros**. La meta es que el próximo producto entre con menos
retries que este.

Diferencia clara:

| Tipo de aprendizaje | Dónde se anota |
|---|---|
| **Generalizable** (vale para cualquier producto) | **A esta skill** — Estética visual, decision tree, hallazgos de prompt-craft, anti-patterns |
| Específico del producto (anatomía, terminología, partes únicas) | Al `Product-rules-<slug>.md` (en el momento, no al final) |
| Cross-skill (afecta también audio/video) | A `CLAUDE.md` §Regla #6 |

Ejemplos típicos que van a **esta skill** (no a un producto puntual):

- "Para producto con bucle continuo, `all fingers external, no thumb inside the loop` siempre al prompt." → bloque "Hallazgos de prompt-craft".
- "NB Pro falla con la palabra `Y` → reemplazar por `Z`." → bloque idem.
- "Plano cenital sobre mesa muestra mejor el grip que ¾ profile." → "Estética visual".

Al cierre, revisar `## Aprendizajes` del storyboard y proponer al usuario
qué filas/notas se incorporan a la skill. Aplicar tras OK.

---

## Anti-patterns específicos de esta skill

1. **Empezar a generar antes de tener el `Product-rules-<slug>.md` aprobado.** Gate dura.
2. **Empezar a generar escenas antes de tener el `product-hero.png` aprobado.** Las escenas necesitan el hero como `--image`.
3. **Empezar a generar antes de tener el `storyboard.md` aprobado.** El storyboard es el contrato del lote.
4. **Mover archivos descartados a `discarded/` durante la iteración.** Quedan en `workspace/` hasta que el flujo cierre — el usuario puede necesitar referenciar la v2 para explicar un problema.
5. **Subir a Drive sin tener el lote completo aprobado localmente.** El equipo no debería ver versiones mixtas.
6. **Saltarse el tracking de descartes.** Cada `v<N>` regenerada implica un row con `status=discarded` en `generations`. Sin excepción.
7. **Asumir que el guión está en disco.** No existe `guion.md`. Si el usuario no lo pegó, pedirlo con `AskUserQuestion`.
8. **Reinventar subniveles tipo `generacion/<proyecto>/`.** Hay un solo video por producto; todo cuelga de `productos/<slug>/`.
9. **Iterar 5+ veces sobre el mismo modelo mental que falla.** Aplicar strategic reset (Paso 3).
10. **Tirar prompts a ciegas sin describir las refs objetivamente.** Antes del primer prompt de cada escena, describir las refs componente por componente (alimenta el Product Rules §2).
11. **Re-subir refs cada vez al CDN.** Subir UNA SOLA VEZ y reusar UUIDs.
12. **Describir el producto desde memoria del modelo cuando hay refs.** Las refs son el ground truth.
12-bis. **Describir el avatar humano desde memoria / desde el nombre.** Si la escena tiene un avatar (Mercedes u otro), abrir su `mercedes-base.webp` (o equivalente) y leer la ref antes de redactar el bloque de avatar en el prompt. Describir avatares "de cabeza" desde el nombre lleva a errores como pelo del color equivocado, edad imprecisa, ropa que no es. Para el avatar Mercedes hay un contrato canónico en [`productos/_shared/avatars/mercedes/Avatar-rules-mercedes.md`](../../../productos/_shared/avatars/mercedes/Avatar-rules-mercedes.md) — incrustar su §5 (Prompt base EN) en todas las escenas con Mercedes. Para avatares nuevos, copiar ese archivo como plantilla bajo `productos/_shared/avatars/<slug>/`.
13. **Subestimar la edición manual en Photoshop del usuario** como ref canónica válida.
14. **Mostrar al usuario `Read` del archivo local.** El usuario NO ve la imagen así (ni en Mac ni en Windows). SIEMPRE pegar URL CDN.
15. **Pre-aprobar prompts en texto** cuando ya tenemos el storyboard aprobado. Para iteración, generate-and-show (mostrar resultado + prompt en el mismo turno).

---

## Referencias

- Reglas globales del proyecto: `CLAUDE.md`
- Skill legacy (referencia histórica del workflow completo): `.claude/skills/ai-inclusion-videos/SKILL.md` — Etapa 1 desmontada por esta skill.
- Skills externas Higgsfield:
  - `higgsfield-generate` — wrapper general
  - `higgsfield-product-photoshoot` — modos `conceptual_product`, `closeup_product_with_person`
  - `higgsfield-soul-id` — solo si hay 15+ fotos reales del avatar
- Drive root del equipo: https://drive.google.com/drive/folders/16rGUnSWWMtnlAumavbZtDoOpegKqalUv
- Sheet: `1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE`

---

## Lo que NO está en esta skill

El changelog del equipo (v3, v6) incluye decisiones de **audio** y **video**
que NO aplican acá:

- Voz canónica **AlizIA Malena Clone v1** `aKtTSeLwi8u4QiEEtGZ0` (re-clonada 2026-06-08 con 3 samples), settings
  `stability=0.70, similarity_boost=0.75, style=0.50, use_speaker_boost=True`,
  cierre de frase con punto, sin `<break>`, sin filler `Listo.` (la voz nueva cierra
  frases sola), padding 0.5s con `apad` → skill `generate-audio`.
- Seseo rioplatense (`lápiz`→`lápis`, `precisión`→`presisión`, etc.) → futura `generate-audio`.
- Seedance 2.0 no hace lipsync — decisión "narración-sobre-gesto" → futura `generate-video`.
- Artefacto cap-slide en Seedance, declarar producto como `RIGID SOLID OBJECT` → futura `generate-video`.

Lo único que **sí** afecta a imágenes de esos hallazgos es el avatar con
**smile cálido cerrado, NOT articulating words** (porque el video después no
le va a poner lipsync). Ya está incluido en "Estética visual" (Paso 1).
