---
name: generate-audio
description: |
  Genera el lote de audios (VO por escena) del video de un producto AlizIA con
  ElevenLabs (voz canónica AlizIA Malena Clone v1). Flujo: pre-check de la
  carpeta del producto → voice-board.md (revisión humana) → generación →
  QA por audio → publicación del lote en Drive para validación del equipo.
  Cada generación se trackea en el Sheet en `generations` con `tipo=audio`.
  NO depende de las imágenes — puede correr en paralelo a
  `product-images-generation`.
  Use cuando el usuario pida "generar audios del producto X", "armar la voz
  del video", "VO del producto X", "audios para el video de X", "voice-board".
  NO usar para imágenes (`product-images-generation`), videos por escena
  (`generate-video`), ni para clonar voces nuevas (ya hay voz canónica).
argument-hint: "<producto-slug>"
allowed-tools: Bash, Read, Write, Edit, Skill, AskUserQuestion
---

# generate-audio

Skill que transforma un guión validado en un **lote de audios aprobados y
publicados para validación del equipo**. Hay un solo video por producto;
todo cuelga de `productos/<producto-slug>/`.

El valor está en los dos gates (uno sobre el `voice-board.md`, otro sobre los
audios generados) y en consolidar **lockdowns generalizables** que mejoran
todos los videos futuros (Paso 5).

Las reglas globales viven en `CLAUDE.md`. Esta skill no las redefine.

---

## Plataforma

- Bash compatible (Mac, Linux, Git Bash o WSL en Windows). PowerShell para los bloques marcados.
- Paths **relativos al root del repo `ai-video/`**. No hardcodear `/Users/...` ni `C:\Users\...`.
- Dependencias: `python3` (ElevenLabs SDK + Drive helper), `ffmpeg` (padding `apad`).

---

## Dependencias

- `Product-rules-<slug>.md` aprobado (lo deja listo `product-images-generation` §Paso 0.5).
- Guión pegado por el usuario (no vive en disco — se pega en el prompt o vía `AskUserQuestion`).
- `ELEVENLABS_API_KEY` en el entorno (ver `CLAUDE.md` §"Pre-flight").
- **NO requiere imágenes**. Audio e imágenes pueden ir en paralelo.

---

## Paso 0 — Pre-check

```bash
SLUG="<producto-slug>"
ROOT="productos/$SLUG"

test -f "$ROOT/Product-rules-$SLUG.md" || echo "FALTA: Product-rules-$SLUG.md"
test -n "$ELEVENLABS_API_KEY"           || echo "FALTA: ELEVENLABS_API_KEY"

mkdir -p "$ROOT"/audio/{workspace,logs,discarded}
```

**PowerShell**: `New-Item -ItemType Directory -Force -Path "$ROOT/audio/workspace","$ROOT/audio/logs","$ROOT/audio/discarded"`

---

## Paso 1 — `voice-board.md` + GATE 1

El `voice-board.md` es el **contrato de audio** (paralelo conceptual al
`storyboard.md` de imágenes). Antes de llamar a ElevenLabs, el usuario lo
aprueba completo.

### Voz canónica fija

- **AlizIA Malena Clone v1** `dlkqIuF0zNKHDiz5ajTG` (IVC clonada de Mercedes, ~2 min de audio fuente).
- `model_id="eleven_multilingual_v2"`, `language_code="es"`.
- **Settings canónicos (v2 — consolidados con safety-loop-scissors-v3, 2026-05)**:
  `stability=0.70`, `similarity_boost=0.75`, `style=0.50`, `use_speaker_boost=True`.
- **Estos settings NO cambian entre escenas del mismo video.**
- *Historia*: el piloto Mercedes-v1 usaba `stab=0.90 / style=0.15`. Esos valores sonaban
  monótonos y sin cierre de frase. Bajar a `0.70 / 0.50` dio inflexiones naturales con
  cierre de frase. Probado en safety-loop-scissors-v3. **NO bajar `stability` < 0.65** —
  la voz empieza a meter letras inventadas. **NO subir `style` > 0.55** — el modelo
  inventa fonemas al inicio del audio. La banda segura es `stab∈[0.65, 0.75]`,
  `style∈[0.40, 0.55]`.

### Limitación inherente de la voz IVC (importante)

La voz se clonó con ~2 min de audio fuente (IVC, no PVC). Esto tiene dos consecuencias
permanentes hasta que se re-clone con más material:

1. **Cierres internos entre oraciones de una misma frase quedan "abiertos"**.
   Una frase con 3 oraciones encadenadas tiene las 2 primeras sin bajada de tono
   final. NO se resuelve con split por oración (duplica costo y suena igual).
2. **Cierre final de frase**: la última oración queda "colgando" sin tono descendente.
   Se compensa con el truco **"Listo." filler** (ver §Paso 2 — Pipeline canónico).

**Plan de mejora a mediano plazo**: regrabar a Mercedes con 5-10 min de audio
variado (cierres firmes, entonación pedagógica explícita, varias emociones) y
crear `AlizIA Malena Clone v2` en ElevenLabs. Hasta entonces, el truco "Listo."
es la solución oficial.

### Reglas de normalización de texto (aplicar antes de meter al voice-board)

1. **Cerrar cada frase con punto.** No dejar frase suelta sin puntuación final.
2. **Prohibido `<break>`** y cualquier tag SSML. La voz IVC no los respeta y mete artefactos.
3. **Seseo rioplatense** — el modelo a veces pronuncia z/c(e,i) con ceceo peninsular. Reescribir a `s`:

   | Original | Forzado |
   |---|---|
   | lápiz | lápis |
   | precisión | presisión |
   | confianza | confiansa |
   | esfuerzo | esfuerso |
   | difícil | difísil |
   | posicionar | posisionar |
   | facilitando | fasilitando |
   | necesitan | nesesitan |

   *(La lista crece con uso real — ver Paso 5.)*

4. **Acento forzado** en palabras técnicas que el modelo pronuncia mal: `buclé` (no `bucle`), etc. Probar antes de reescribir; ElevenLabs es no-determinista (2-3 generaciones del mismo texto pueden variar).

5. **`. Listo.` al final de la frase como cierre de entonación**. La voz IVC actual
   (ver §"Limitación") no cierra frases con bajada de tono naturalmente. El truco:
   - Agregar `. Listo.` al final del texto que se pasa a ElevenLabs
   - El modelo cierra la frase real con tono descendente porque "Listo." pasa a ser
     la última palabra (la caída de entonación cae sobre "Listo.")
   - **El "Listo." se CORTA del audio en post** (ver §Paso 2 — Pipeline canónico)
   - Aplica a **TODAS** las frases del voice-board sin excepción

### Estructura del `voice-board.md`

```markdown
# Voice-board — <producto>

> Producto: `Product-rules-<slug>.md` (vigente al <fecha>)
> Voz: AlizIA Malena Clone v1 `dlkqIuF0zNKHDiz5ajTG`
> Settings (canónicos v2): `stability=0.70, sim=0.75, style=0.50, speaker_boost=true`, `eleven_multilingual_v2`, `es`
> Post: agregar `. Listo.` al texto, cortar el filler en post (`atrim total-0.7s`), padding final 0.5 s (`apad`)
> Guión pegado: YYYY-MM-DD por <usuario>

## Fuente — guión

<texto completo del guión, tal cual lo entregó el usuario>

---

## vo-e1

- **Frase normalizada**:
  > Hola, soy Mercedes. Hoy te muestro una herramienta que cambió mi día a día en el aula.
- **Notas de pronunciación**: ninguna / `confianza→confiansa` aplicado.
- **Instrucciones extra al prompt** *(si aplica — tono/énfasis)*: ninguna.
- **Output esperado**: `audio/vo-e1-v1.mp3`

---

## vo-e2-i
...
```

### GATE 1 — Aprobación del voice-board

> "Voice-board listo en `<path>`. Te paso las frases normalizadas y notas de
> pronunciación por escena. Decime OK o qué ajustar. No quemo créditos hasta
> tu OK."

---

## Paso 2 — Generar audios — pipeline canónico + tracking inmediato

**Para cada bloque del voice-board**, el pipeline es **4 pasos atómicos**:

1. **Texto enviado a ElevenLabs** = `<frase normalizada del voice-board> + " Listo."`
2. **Generar** con voz + settings canónicos → guardar en `audio/workspace/<slug>-v<N>-raw.mp3`
3. **Cortar el "Listo."** con `atrim=0:{total-0.7}, apad=pad_dur=0.5` → guardar en `audio/<slug>-v<N>.mp3`
4. **Trackear** inmediato al Sheet (regla #1 de `CLAUDE.md`) — antes de mostrar al usuario

### Script canónico reutilizable: [`scripts/audio_pipeline.py`](scripts/audio_pipeline.py)

El helper está versionado al lado de la skill. Lo invocás con el voice-board ya
aprobado:

```bash
python3 .claude/skills/generate-audio/scripts/audio_pipeline.py \
  --slug "<producto-slug>" \
  --video-id <id_del_sheet> \
  --voice-board "productos/<slug>/voice-board.md"
```

El script:
- Parsea el voice-board (extrae cada bloque `## vo-<escena>` con su frase normalizada).
- Por cada track:
  1. Agrega `. Listo.` al final de la frase (si no termina ya con punto, le agrega `. Listo.`).
  2. Llama a ElevenLabs con los settings canónicos.
  3. Corta el filler con `atrim=0:total-0.7s` y aplica `apad=0.5s`.
  4. Trackea al Sheet `generations` (`tipo=audio`).
- Es **idempotente** por versión: si `audio/<slug>-v1.mp3` existe, salta. Para forzar
  regenerar, usar `--regen <slug>` (que toma `v<N+1>`).

### Si llamás manual (sin el script — para debug o retry puntual)

```python
import os, subprocess
from elevenlabs.client import ElevenLabs

client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
SETTINGS = {"stability": 0.70, "similarity_boost": 0.75, "style": 0.50, "use_speaker_boost": True}

# 1. Texto + filler
text = "<frase normalizada>. Listo."

# 2. Generar
raw = "productos/<slug>/audio/workspace/vo-<escena>-v1-raw.mp3"
audio = client.text_to_speech.convert(
    voice_id="dlkqIuF0zNKHDiz5ajTG",
    text=text,
    model_id="eleven_multilingual_v2",
    language_code="es",
    voice_settings=SETTINGS,
    output_format="mp3_44100_128",
)
with open(raw, "wb") as f:
    for chunk in audio:
        if chunk: f.write(chunk)

# 3. Cortar el "Listo." + apad (CRÍTICO: usar atrim+apad en filter, NUNCA -t + apad)
total = float(subprocess.run(
    ["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",raw],
    capture_output=True, text=True
).stdout.strip())
cut_at = total - 0.7  # fijo: "Listo." dura ~0.7s en contexto
out = "productos/<slug>/audio/vo-<escena>-v1.mp3"
subprocess.run([
    "ffmpeg","-y","-i",raw,
    "-af", f"atrim=0:{cut_at},apad=pad_dur=0.5",
    "-c:a","libmp3lame","-b:a","192k",
    out
], capture_output=True)
```

### Reglas duras del corte (lección aprendida)

- **Fallback fijo: `total - 0.7s`**. Funciona para la mayoría (~6 de 7 escenas).
- **Si todavía queda "Listo." audible**: usar `total - 0.8s` (más agresivo). Caso típico:
  frases largas donde el modelo dice "Listo." más lento.
- **Si el modelo "tropieza" en el medio** (artifact tipo "se traba y dice dos veces"):
  **regenerar** (ElevenLabs es no-determinista, otra seed lo arregla).
- **NUNCA usar `silencedetect`** para encontrar el corte. Detecta silencios INTERNOS
  de la frase (entre oraciones) y corta ahí, dejando el "Listo." después. Probado y falla.
- **NUNCA usar `-t {cut} -af apad`** en ffmpeg — el `-t` trunca el padding del filter
  graph. El padding queda en 0. Usar siempre `atrim=0:{cut},apad=pad_dur=0.5` en `-af`.

### Tracking (después de cada job, antes de mostrar al usuario)

```bash
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE","range":"generations!A:K","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["<id>","<video_id>","vo-<escena>","audio","elevenlabs/eleven_multilingual_v2","<frase>. Listo. [stab=0.70 sim=0.75 style=0.50 apad=0.5s cut=total-0.7s]","completed","local","","productos/<slug>/audio/vo-<escena>-v1.mp3","YYYY-MM-DD"]]}'
```

**Naming**: nunca pisar archivos. `vo-<escena>-v1.mp3`, `vo-<escena>-v2-pronunciacion-bucle.mp3`, etc. (ver `CLAUDE.md` Regla #3).

---

## Paso 3 — QA por audio + GATE 2

Por cada audio generado:

1. **Subir el MP3 al CDN para preview**. El usuario **no escucha un `Read` local** (ni en Mac ni en Windows). Subir a Drive en `audio-preview/` y pasar URL:

   ```bash
   # Reusa el helper gws_find_or_create_folder de product-images-generation §Paso 4
   PREVIEW_ID=$(gws_find_or_create_folder "audio-preview" "$PROD_FOLDER_ID")
   gws drive +upload "productos/$SLUG/audio/vo-$ESCENA-v1.mp3" --parent "$PREVIEW_ID"
   ```

2. Mostrar URL + frase normalizada + notas.
3. Decisión: **OK** | **regenerar (mismo texto, otra seed)** | **reescribir texto y regenerar**.

### Si OK

- El archivo `audio/vo-<escena>-v1.mp3` queda como "aprobado" (no se mueve, se referencia desde el voice-board con ✅).

### Si regenerar / reescribir

- Tirar `v<N+1>` con sufijo descriptivo del problema (`-pronunciacion-bucle`, `-tono-frio`).
- Trackear el descarte (`status=discarded`) con motivo en el campo `prompt` o `asset_local` apuntando a `audio/discarded/`.
- Anotar en `## Aprendizajes` del voice-board.

### Al cierre del QA — mover versiones descartadas a `audio-preview/descartados/`

Mientras iteramos, las versiones descartadas se acumulan en `audio-preview/` y
confunden al equipo cuando entra a aprobar (¿cuál es la versión final?).

**Antes de avisar al equipo que pueden revisar**, mover las versiones descartadas
a una subcarpeta `descartados/` dentro de `audio-preview/`. En la raíz de
`audio-preview/` queda solo **un archivo por escena** (el que está aprobado).

```bash
PREVIEW_ID="<id_de_audio-preview>"
DISCARDED_ID=$(gws drive files create --params '{"supportsAllDrives":true}' \
  --json "$(python3 -c 'import json; print(json.dumps({"name":"descartados","mimeType":"application/vnd.google-apps.folder","parents":["'$PREVIEW_ID'"]}))')" \
  | sed '/^Using keyring backend/d' | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")

# Listar y mover. Las APROBADAS las definís vos por nombre (ej. "vo-e1-v10.mp3"):
APROBADAS="vo-e1-v10.mp3 vo-e2i-v10.mp3 vo-e2ii-v12.mp3 ..."

gws drive files list --params "$(python3 -c "import json,sys; print(json.dumps({'q':f\"'$PREVIEW_ID' in parents and mimeType != 'application/vnd.google-apps.folder' and trashed = false\",'fields':'files(id,name)','pageSize':100}))")" \
  | sed '/^Using keyring backend/d' \
  | python3 -c "import json,sys; aprob=set(sys.argv[1].split()); d=json.load(sys.stdin); [print(f['id'], f['name']) for f in d['files'] if f['name'] not in aprob]" "$APROBADAS" \
  | while read FILE_ID NAME; do
    gws drive files update --params "$(python3 -c "import json,sys; print(json.dumps({'fileId':sys.argv[1],'addParents':sys.argv[2],'removeParents':sys.argv[3],'supportsAllDrives':True}))" "$FILE_ID" "$DISCARDED_ID" "$PREVIEW_ID")" --json '{}'
    echo "  moved: $NAME"
done
```

> El equipo abre `audio-preview/` y solo ve N archivos (uno por escena) + la
> carpeta `descartados/` que pueden inspeccionar si tienen curiosidad sobre la
> iteración. No se borra nada — la trazabilidad queda intacta.

---

## Paso 4 — Publicar lote a Drive

Cuando **todos** los audios tienen su `v<N>` aprobada:

1. Copiar los `vo-<escena>-v<N>.mp3` aprobados a `audio/aprobados/` con nombre limpio (`vo-<escena>.mp3`).
2. Subir el lote a `<root>/<producto-slug>/audios-a-validar/`.

Root del equipo: `16rGUnSWWMtnlAumavbZtDoOpegKqalUv`.

```bash
ROOT_FOLDER_ID="16rGUnSWWMtnlAumavbZtDoOpegKqalUv"

PROD_FOLDER_ID=$(gws_find_or_create_folder "$SLUG" "$ROOT_FOLDER_ID")
VAL_FOLDER_ID=$(gws_find_or_create_folder "audios-a-validar" "$PROD_FOLDER_ID")

for mp3 in "productos/$SLUG/audio/aprobados/"*.mp3; do
  gws drive +upload "$mp3" --parent "$VAL_FOLDER_ID"
done

echo "https://drive.google.com/drive/folders/$VAL_FOLDER_ID"
```

> El helper `gws_find_or_create_folder` (bash + python3 cross-platform) está
> definido en `product-images-generation` §Paso 4. Bloque PowerShell idem.

---

## Paso 5 — Aprendizajes GENERALIZABLES

Énfasis: el conocimiento que sale de **este** video tiene que aplicar a
**todos los productos futuros**. Diferencia clara:

| Tipo de aprendizaje | Dónde se anota |
|---|---|
| Generalizable (vale para cualquier producto) | **A esta skill** (sección Reglas de normalización, tabla de seseo, settings) |
| Específico del producto (terminología, pronunciaciones de su jerga) | Al `Product-rules-<slug>.md` |

Ejemplos típicos que van a la **skill**:

- "Palabra `X` mal pronunciada con seseo → reemplazo `Y` consolidado." → agregar fila a la tabla de seseo.
- "Tono frío en escenas emocionales → probar `style=0.20`." → nota en la sección de settings.
- "Padding inicial también necesario cuando la frase arranca con consonante explosiva." → ajustar el filtro `ffmpeg`.

Cierre del Paso 5: proponer al usuario qué filas/notas se agregan a esta skill (y a `CLAUDE.md` §Regla #6 si es cross-cutting), y aplicarlas tras OK.

---

## Anti-patterns

1. **Generar antes de tener el voice-board aprobado.** El voice-board es el contrato.
2. **Asumir que el guión está en disco.** No existe. Pedirlo con `AskUserQuestion` si el usuario no lo pegó.
3. **Pasar tags `<break>` u otros SSML.** Prohibidos — la voz IVC mete artefactos.
4. **Mostrar al usuario el archivo con `Read` / `Invoke-Item`.** No lo escucha. Subir al CDN y pasar URL.
5. **Cambiar settings entre escenas del mismo video.** La voz tiene que sonar idéntica de escena a escena.
6. **Pisar archivos en regeneración.** `v<N+1>` siempre.
7. **Saltar el tracking de descartes.** Cada regen trackea la descartada con motivo.
8. **Olvidar el `. Listo.` filler al final del texto.** Sin filler, la voz IVC no cierra frases — la última oración queda "abierta" / colgando. Aplica a TODAS las frases.
9. **Usar `silencedetect` para encontrar el punto de corte del "Listo.".** Detecta silencios INTERNOS de la frase (entre oraciones) y corta ahí, dejando el "Listo." en el output final. **Usar fallback fijo `total - 0.7s` (o 0.8s si la voz dice "Listo" lento).**
10. **Usar `-t {cut} -af apad` en ffmpeg.** El `-t` trunca el padding del filter. Usar siempre `atrim=0:{cut},apad=pad_dur=0.5` dentro de `-af`.
11. **Bajar `stability` < 0.65 o subir `style` > 0.55.** Fuera de la banda `stab∈[0.65,0.75]` × `style∈[0.40,0.55]`, la voz IVC mete letras inventadas o fonemas erróneos.
12. **Split por oración + concatenar para "arreglar" cierres internos.** No funciona — duplica costo y suena igual. Los cierres internos son limitación de la voz IVC. Aceptar.
13. **Asumir determinismo en ElevenLabs.** El mismo texto + settings da audios distintos. Si una generación tiene un artifact (trabón, palabra repetida), **regenerar** con misma seed.

---

## Referencias

- Reglas globales: `CLAUDE.md`
- Skill paralela imágenes: `.claude/skills/product-images-generation/SKILL.md`
- Skill posterior: `.claude/skills/generate-video/SKILL.md`
- Drive root: https://drive.google.com/drive/folders/16rGUnSWWMtnlAumavbZtDoOpegKqalUv
- Sheet: `1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE`
