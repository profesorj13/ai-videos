# ai-video — instrucciones del proyecto

Producción de videos cortos verticales (9:16) con modelos de IA, para productos
de inclusión educativa de AlizIA / Educabot. Stack restringido: **Higgsfield +
ElevenLabs + FFmpeg**. No usar HeyGen, Hedra, Runway, fal, Replicate u otros
proveedores externos a menos que el usuario lo pida explícitamente.

---

## Regla #1 — Toda generación se registra en el Sheet (NO EXCEPCIONES)

**Sheet**: `1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE` — "AV3 Videos Tracker"
**CLI**: `gws` (instalado, autenticado en la máquina).

Cada llamada a un modelo (Higgsfield, ElevenLabs, lo que sea que consuma crédito
o saldo) **se registra inmediatamente después** de que el job termina, esté
`completed`, `nsfw`, `failed` o `discarded`. **No al final de la sesión**, no
"luego lo cargo". Inmediatamente.

Por qué: queremos trazabilidad de costos, capacidad de auditar qué prompt
funcionó vs qué falló, y poder reproducir cualquier still o video con su
historia completa. Sin esto, el aprendizaje no se acumula.

### Estructura real del Sheet (4 tabs)

**`videos`** (`A:F`) — un row por proyecto de video:
| # | Columna | Ejemplo |
|---|---|---|
| A | `id` | `2` (auto-incremental) |
| B | `slug` | `safety-loop-scissors-mercedes-v1` |
| C | `producto` | `Safety Loop Easy Grip Scissors` |
| D | `titulo` | `Tijera adaptada — Mercedes v1` |
| E | `duracion_seg` | `40` |
| F | `formato` | `9:16` |

**`scripts`** (`A:F`) — un row por sub-escena del guión:
| # | Columna | Ejemplo |
|---|---|---|
| A | `video_id` | `2` (FK → videos.id) |
| B | `escena` | `E3-i`, `E5` |
| C | `t_inicio` | `0:08` |
| D | `t_fin` | `0:12` |
| E | `narracion` | texto del VO |
| F | `visual` | descripción del plano |

**`generations`** (`A:K`) — un row por CADA generación (la tabla principal):
| # | Columna | Ejemplo |
|---|---|---|
| A | `id` | `15` (auto-incremental, siguiente al máximo existente) |
| B | `video_id` | `2` (FK → videos.id) |
| C | `escena` | `E3-i`, `mercedes-bible-04`, `vo-e2i` |
| D | `tipo` | `image` · `video` · `audio` |
| E | `modelo` | `nano_banana_2`, `seedance_2_0`, `product-photoshoot/conceptual_product`, `elevenlabs/eleven_multilingual_v2` |
| F | `prompt` | el prompt enviado (intent corto si Product Photoshoot lo asembla) |
| G | `status` | `completed`, `nsfw`, `failed`, `discarded` |
| H | `job_id` | UUID Higgsfield, o `local` si no aplica |
| I | `url_resultado` | URL del CDN, vacío para audio local |
| J | `asset_local` | path relativo `data/assets/.../<archivo>` |
| K | `fecha` | `2026-05-18` (formato ISO `YYYY-MM-DD`) |

**`assets`** (`A:F`) — refs canónicas reutilizables:
| # | Columna | Ejemplo |
|---|---|---|
| A | `id`, B `slug`, C `tipo`, D `ruta_local`, E `descripcion`, F `fecha` | — |

### Comando estándar — append a `generations`

El helper `gws sheets +append` apunta por default a la **primera** tab (`videos`),
no a `generations`. Para `generations` usar el comando explícito:

```bash
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE","range":"generations!A:K","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["15","2","E3-i","image","nano_banana_2","Macro vertical 9:16 closeup ...","completed","ae79bc23-1e7c-4f94-883b-51093222a27a","https://d8j0ntlcm91z4.cloudfront.net/.../hf_....png","data/assets/products/safety-loop-scissors/generations/mercedes-v1/images/e3i-still-v5.png","2026-05-18"]]}'
```

> Para los otros tabs, cambiar `range` por `videos!A:F`, `scripts!A:F` o `assets!A:F`.

### Cómo saber el próximo `id`

`id` es el máximo existente + 1:

```bash
gws sheets +read --spreadsheet 1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE --range 'generations!A:A' \
  | python3 -c "import json,sys,re; raw=sys.stdin.read(); raw=re.sub(r'^Using keyring backend.*\n','',raw,flags=re.M); d=json.loads(raw); print(max(int(r[0]) for r in d['values'][1:] if r and r[0].isdigit())+1)"
```

### Cuándo registrar `discarded`

Si una imagen sale mal y se regenera (mala morfología, grip incorrecto, lipsync
roto, identidad cambiada, etc.), la versión descartada **también** entra al
Sheet con `status=discarded` y el detalle del problema en el prompt o como
asset_local apuntando a la carpeta `discarded/`. El descarte sin trazar es
deuda técnica.

### Bulk append

Cuando se generan N stills/videos seguidos, hacer un solo append con todas las
filas en `values`:

```bash
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE","range":"generations!A:K","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[
    ["15","2","E1","video","seedance_2_0","Static medium top-down...","completed","fd77c8f5-9999-48fb-beed-69382674d204","https://...","data/assets/.../videos/e1.mp4","2026-05-18"],
    ["16","2","E2-ii","video","seedance_2_0","Macro vertical...","completed","c5f86f61-326b-4105-9a8e-efc8ce69edae","https://...","data/assets/.../videos/e2ii.mp4","2026-05-18"]
  ]}'
```

### Crear row en `videos` antes de empezar a trackear

Si todavía no existe el `video_id` para el proyecto en curso, **primero**
crear el row en `videos` y usar ese `id` en todas las generaciones que sigan:

```bash
# 1) ver el último id
gws sheets +read --spreadsheet 1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE --range 'videos!A:A'

# 2) crear el row (helper +append apunta a la primera tab, que es videos)
gws sheets +append \
  --spreadsheet 1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE \
  --json-values '[["2","safety-loop-scissors-mercedes-v1","Safety Loop Easy Grip Scissors","Tijera adaptada — Mercedes v1","40","9:16"]]'
```

---

## Regla #2 — Workflow gated, una skill por etapa

El proceso global es:

```
guión (validado fuera) → imágenes (gate) → audios (gate) → videos (gate) → montaje (gate final)
```

Cada etapa vive en su propia skill. Cada **gate** requiere aprobación
explícita del usuario sobre el lote antes de avanzar. Nunca generar audios
sin imágenes aprobadas, nunca videos sin audios aprobados, nunca montar sin
videos aprobados.

Skills por etapa:

- **Imágenes** → `product-images-generation` (activa).
- **Audios** → `generate-audio` (futura).
- **Videos** → `generate-video` (futura).
- **Montaje** → todavía dentro de `ai-inclusion-videos` (legacy) hasta que se desmonte.

La skill `ai-inclusion-videos` queda como **referencia histórica** del workflow
completo end-to-end del piloto Mercedes-v1. Se va desmontando a medida que cada
etapa tenga su skill propia. No editarla salvo para corregir errores graves.

---

## Pre-flight (una vez por sesión)

Antes de arrancar cualquier skill del pipeline, verificar que el entorno
está listo. Si **algo** falla, parar y avisar al usuario — no improvisar.

```bash
# 1. Higgsfield autenticado + saldo
higgsfield account status   # plan activo + créditos disponibles

# 2. ElevenLabs API key cargada (la skill `generate-audio` la usa)
test -n "$ELEVENLABS_API_KEY" && echo "OK" || echo "FALTA cargar .env"

# 3. gws CLI para Sheets/Drive (Mac y Windows)
gws --version
gws sheets +read --spreadsheet 1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE --range 'videos!A1:A2'

# 4. FFmpeg + Pillow
ffmpeg -version
python3 -c "from PIL import Image; print('Pillow OK')"
```

> Paths del repo siempre relativos al root de `ai-video/` (donde está este
> `CLAUDE.md`). El equipo trabaja entre Mac y Windows — nada de hardcodear
> `/Users/...` ni `C:\Users\...` en skills, scripts o comandos.

Saldo mínimo recomendado al arrancar un video de ~30s: **300 créditos** Higgsfield.

La **creación de subcarpetas del proyecto** (workspace, descartes, etc.) es
responsabilidad de cada skill, no del pre-flight global.

---

## Estructura raíz `productos/`

Cada producto de inclusión vive en su carpeta bajo `productos/` en la raíz
del repo `ai-video/`. Esta convención es compartida por todo el equipo (Mac y
Windows). **Todos los paths son relativos al root del repo** — nunca
hardcodear `/Users/...` ni `C:\Users\...`.

**Hay un solo video por producto** — no hay subniveles de proyecto/versión.

```
productos/
├── _template/                              # plantilla — copiar para arrancar un producto nuevo
│   └── (mismo layout que abajo, con `Product-rules-TEMPLATE.md` y README)
└── <producto-slug>/
    ├── Product-rules-<producto-slug>.md    # contrato del producto (6 bloques, gate obligatorio)
    ├── product-hero.png                    # output `product-images-generation` (Paso 1.5)
    ├── storyboard.md                       # output `product-images-generation` (plan imágenes)
    ├── voice-board.md                      # output `generate-audio` (plan VO + normalización)
    ├── motion-board.md                     # output `generate-video` (plan motion + casos)
    ├── referencias/
    │   └── ref-images/                     # fotos reales/web del producto (input externo)
    ├── workspace/                          # `product-images-generation` — iteración de imágenes
    │   ├── hero/                           # versiones hero-v1.png, hero-v2.png…
    │   ├── logs/                           # JSON por job de Higgsfield
    │   └── discarded/                      # se llena al cierre del flujo
    ├── imagenes-aprobadas/                 # finales locales por escena
    ├── imagenes-a-validar/                 # espejo de lo que sube a Drive
    ├── audio/                              # `generate-audio` (ElevenLabs)
    │   ├── workspace/                      # versiones raw pre-padding
    │   ├── logs/                           # JSON por job
    │   ├── discarded/
    │   ├── aprobados/                      # finales con nombre limpio `vo-<escena>.mp3`
    │   └── vo-<escena>-v<N>.mp3            # archivos versionados durante iteración
    ├── videos/                             # `generate-video` (Seedance 2.0)
    │   ├── workspace/                      # `.mp4` silent por escena
    │   ├── logs/                           # JSON por job + plans
    │   ├── preview/                        # `.mp4` con audio overlay (validación)
    │   └── discarded/
    └── final/                              # render único (skill `ai-inclusion-videos` legacy)
```

### Arrancar un producto nuevo

```bash
cp -r productos/_template productos/<mi-slug>
mv productos/<mi-slug>/Product-rules-TEMPLATE.md \
   productos/<mi-slug>/Product-rules-<mi-slug>.md
# Subir 1-3 fotos reales del producto a productos/<mi-slug>/referencias/ref-images/
```

Después invocás la skill `product-images-generation <mi-slug>` y ella crea
todo lo que falte. Detalle en `productos/_template/README.md`.

El **`Product-rules-<slug>.md`** es el contrato del producto, gate
obligatorio antes de generar cualquier imagen. 6 bloques canónicos: qué es ·
anatomía · restricciones · uso · prompt base EN (exhaustivo) · product hero
(still del producto puro aprobada). Detalle en la skill
`product-images-generation` §"Paso 0.5".

> El guión **no vive en disco**. El equipo lo redacta en un Google Docs y lo
> pega al invocar la skill correspondiente. Cada skill lo embebe en el
> artefacto que produce (ej. `storyboard.md` lo conserva como sección "Fuente")
> para trazabilidad.

> ⚠️ La estructura anterior `data/assets/products/<slug>/generations/<proj>/`
> (vista en `ai-inclusion-videos`) está deprecada para productos nuevos. Solo
> se mantiene viva para el piloto Mercedes-v1 hasta que se cierre.

**Drive — root del equipo para assets a validar:**
`https://drive.google.com/drive/folders/16rGUnSWWMtnlAumavbZtDoOpegKqalUv`

Cada skill que publique assets a Drive debe colgarlos de
`<root>/<producto-slug>/<carpeta>/` (ej. `imagenes-a-validar/`).

---

## Regla #3 — Nunca pisar archivos

Cuando se regenera un asset, **NUNCA** se sobrescribe el archivo anterior.
Convención obligatoria:

- Sufijo descriptivo del problema: `e3i-still-v1.png`, `e3i-still-v2-grip-wrong.png`, `e3i-still-v3-soulFail.png`, `e3i-still-v5.png` (la aprobada).
- Versiones descartadas se mueven a `<carpeta>/discarded/` al final del flujo, no antes (mientras se itera, conviven en la carpeta principal para poder referenciarlas).
- El archivo principal se renombra solo cuando el usuario aprueba la versión final, no antes.

El usuario necesita poder señalar "el problema lo vi en la v2" en cualquier
momento. Si pisamos archivos, esa conversación es imposible.

---

## Regla #4 — Skills locales: solo las del pipeline modular

El pipeline está siendo desmontado de `ai-inclusion-videos` en una skill por
etapa (ver Regla #2). Las únicas skills locales válidas son las del pipeline
modular (`product-images-generation`, `generate-audio`, `generate-video`).

Las 3 skills externas de Higgsfield (`higgsfield-soul-id`,
`higgsfield-product-photoshoot`, `higgsfield-generate`) están instaladas
globalmente y se usan tal cual desde las skills locales.

No crear variantes locales adicionales sin pedido explícito.

---

## Regla #5 — Stack canónico

Tres proveedores cerrados: **Higgsfield + ElevenLabs + FFmpeg**.

Los detalles operativos (qué modelo para qué caso, IDs de voz, settings,
parámetros, decision trees, flags) **viven en la skill correspondiente**, no
acá. Se cargan solo cuando esa skill se activa:

- Imágenes (Nano Banana Pro, Product Photoshoot, estética visual) → [`product-images-generation`](.claude/skills/product-images-generation/SKILL.md).
- Audios (voz canónica, settings ElevenLabs, normalización de texto) → [`generate-audio`](.claude/skills/generate-audio/SKILL.md).
- Videos (Seedance 2.0, decision tree de casos, lockdowns) → [`generate-video`](.claude/skills/generate-video/SKILL.md).
- Montaje final (concat FFmpeg con map mixto, overlays con Pillow) → `ai-inclusion-videos` (legacy) hasta crear `montaje-final`.

Notas operativas mínimas que sí valen acá:

- `higgsfield account status` debe retornar plan activo y créditos. Saldo mínimo recomendado para un video ~30 s: **300 créditos**.
- `ELEVENLABS_API_KEY` cargada como env var antes de invocar `generate-audio` (ver §Pre-flight).
- FFmpeg local **sin libass**: overlays de texto van por Pillow → PNG → `overlay` filter, nunca `drawtext`/`subtitles`.

---

## Regla #6 — Hallazgos cross-cutting

Cada skill consolida sus propios hallazgos por etapa (ver §Paso 5 de cada
una). Acá viven solo los que aplican a **todas** las skills.

A. **Mostrar resultados al usuario con URL CDN / Drive, NUNCA con `Read` del archivo local.** El usuario no ve la imagen/video/audio que abrimos en local (ni en Mac ni en Windows). Pegar URL para que abra en el navegador.

B. **Prompts en español resumido al usuario antes de cada job; inglés completo solo al modelo.** El equipo decide sobre intención en español, no sobre prompt en inglés.

C. **Strategic reset si 3-4 iteraciones sin progreso.** Si el modelo se atasca en el mismo error, **parar** y replantear con el usuario (¿es el prompt? ¿las refs? ¿el Product Rules?). No iterar a ciegas.

D. **`Product-rules-<slug>.md` es contrato**, vive en `productos/<slug>/`. Toda corrección del usuario sobre el producto se anota ahí *en el momento*. Sin Product Rules vigente, no se genera nada (ver `product-images-generation` §Paso 0.5).

E. **Aprendizaje GENERALIZABLE > específico del producto.** Cada cierre de skill (Paso 5) revisa qué se incorpora a la skill (vale para todos los productos futuros) vs qué queda en el Product Rules del producto puntual. La meta es que cada video entre con menos retries que el anterior.

---

## Regla #7 — Repo Git: qué se comparte y qué queda local

El repo `git@github.com:profesorj13/ai-videos.git` es la **memoria colectiva
del equipo**: skills, guiones, product-rules, refs canónicas chicas. Todo
binario regenerable queda local. La regla mental es:

> Si lo puede regenerar otra persona corriendo la skill desde cero → no sube.
> Si es saber humano (texto, decisión, referencia visual canónica) → sube.

### Qué SÍ se commitea

| Categoría | Path | Por qué |
|---|---|---|
| Instrucciones | `CLAUDE.md`, `README.md` | Contrato del proyecto |
| Skills locales | `.claude/skills/**/SKILL.md` + soporte | Lo que estamos perfeccionando juntos |
| Skill legacy | `ebt/skills/inclusion-video-pipeline/SKILL.md` | Referencia histórica del piloto |
| Documentación | `ebt/docs/**/*.md`, `docs/**/*.md`, `docs/**/*.html` | Guiones, HANDOFFs, workflows |
| Texto del producto | `productos/<slug>/{storyboard.md, product-rules.md}` | Decisiones del producto |
| Refs canónicas chicas | `productos/<slug>/referencias/**` (`< 500 KB`) | Para arrancar reproducible sin pedir archivos |
| Estructura base | `.gitkeep` en carpetas vacías clave | Unifica el layout entre máquinas |

### Qué NO se commitea (cubierto por `.gitignore`)

| Categoría | Path/patrón | Cómo lo recupera el equipo |
|---|---|---|
| Video output | `*.mp4`, `*.mov`, `*.webm`, `*.mkv` | Regenerando con la skill |
| Audio output | `*.mp3`, `*.wav`, `*.opus`, `*.m4a` | Regenerando con ElevenLabs |
| PDFs regenerables | `*.pdf` | Re-exportando del HTML/source |
| Pilotos legacy pesados | `ebt/data/`, `beato/` | Cada uno tiene los suyos local |
| Workspace de iteración | `productos/*/workspace/` | Es ruido temporal |
| Outputs aprobados | `productos/*/{imagenes-aprobadas,imagenes-a-validar,audio,videos,final}/` | Drive + regenerable |
| Secretos | `.env*`, `*.key`, `*.pem`, `credentials*.json` | Cada uno tiene los suyos |
| OS / IDE | `.DS_Store`, `node_modules/`, `__pycache__/`, `.venv/` | Generables |
| Backups sueltos | `*.zip`, `*.tar.gz` | No queremos versionarlos |

### Las excepciones explícitas en `.gitignore`

Hay 3 patrones que **re-incluyen** archivos que la regla general ignoraría:

```gitignore
!productos/*/*.md                       # cualquier .md del producto
!productos/*/referencias/**/*.{png,jpg,jpeg,webp,svg,gif}
!**/.gitkeep
```

Si una imagen ref pesa > 500 KB:
1. **NO** la commitees igual "porque la negación lo permite".
2. Subila al Drive del equipo (`16rGUnSWWMtnlAumavbZtDoOpegKqalUv`).
3. Anotá el link en `productos/<slug>/referencias/README.md`.

### Workflow típico de contribución

```bash
# 1. Pull antes de arrancar (que llegue lo último del equipo)
git pull

# 2. Iterar local — todo lo pesado se ignora solo
# (correr skills, generar imágenes, audios, videos)

# 3. Si mejoraste una skill o aprendiste algo nuevo:
git status                                # debería mostrar SOLO .md o refs chicas
git add CLAUDE.md .claude/skills/...
git commit -m "skill(images): nueva regla de hand-on-grip"
git push
```

Si `git status` lista algún binario pesado, **parar** y revisar `.gitignore`
antes de seguir — algo se escapó.

### Cuando el `.gitignore` no alcanza

Si una skill nueva genera un tipo de artefacto que no está cubierto, **actualizar
ambos `.gitignore` y este CLAUDE.md** en el mismo commit. No dejar la
inconsistencia, es la única forma de que el equipo se mantenga alineado.

---

## Referencias

- Skill workflow gated end-to-end (legacy): `.claude/skills/ai-inclusion-videos/SKILL.md`
- Skill etapa imágenes (activa): `.claude/skills/product-images-generation/SKILL.md`
- Skills externas Higgsfield (instaladas globalmente):
  - `~/.claude/skills/higgsfield-soul-id/SKILL.md`
  - `~/.claude/skills/higgsfield-product-photoshoot/SKILL.md`
  - `~/.claude/skills/higgsfield-generate/SKILL.md`
