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

- **AlizIA Malena Clone v1** `dlkqIuF0zNKHDiz5ajTG` (IVC clonada de Mercedes).
- `model_id="eleven_multilingual_v2"`, `language_code="es"`.
- `stability=0.90`, `similarity_boost=0.75`, `style=0.15`, `use_speaker_boost=True`.
- **Estos settings NO cambian entre escenas del mismo video.**

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

### Estructura del `voice-board.md`

```markdown
# Voice-board — <producto>

> Producto: `Product-rules-<slug>.md` (vigente al <fecha>)
> Voz: AlizIA Malena Clone v1 `dlkqIuF0zNKHDiz5ajTG`
> Settings: `stability=0.90, sim=0.75, style=0.15, speaker_boost=true`, `eleven_multilingual_v2`, `es`
> Post: padding final 0.5 s (`apad=pad_dur=0.5`)
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

## Paso 2 — Generar audios + tracking inmediato

Por cada bloque del voice-board, llamar a ElevenLabs (Python). Aplicar `apad`
post-render. **Tracking inmediato** al Sheet — Regla #1 de `CLAUDE.md`.

```python
import os
from elevenlabs.client import ElevenLabs

client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
texto = "..."  # frase normalizada del voice-board
out_raw = "productos/<slug>/audio/workspace/vo-<escena>-v1-raw.mp3"

audio = client.text_to_speech.convert(
    voice_id="dlkqIuF0zNKHDiz5ajTG",
    text=texto,
    model_id="eleven_multilingual_v2",
    language_code="es",
    voice_settings={
        "stability": 0.90,
        "similarity_boost": 0.75,
        "style": 0.15,
        "use_speaker_boost": True,
    },
    output_format="mp3_44100_128",
)
with open(out_raw, "wb") as f:
    for chunk in audio:
        if chunk:
            f.write(chunk)
```

Padding final (mismo path final para todas las escenas):

```bash
ffmpeg -y -i "productos/<slug>/audio/workspace/vo-<escena>-v1-raw.mp3" \
  -af "apad=pad_dur=0.5" -c:a libmp3lame -b:a 192k \
  "productos/<slug>/audio/vo-<escena>-v1.mp3"
```

Tracking (después de cada job, antes de mostrar al usuario):

```bash
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE","range":"generations!A:K","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["<id>","<video_id>","vo-<escena>","audio","elevenlabs/eleven_multilingual_v2","<frase normalizada>","completed","local","","productos/<slug>/audio/vo-<escena>-v1.mp3","YYYY-MM-DD"]]}'
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

---

## Referencias

- Reglas globales: `CLAUDE.md`
- Skill paralela imágenes: `.claude/skills/product-images-generation/SKILL.md`
- Skill posterior: `.claude/skills/generate-video/SKILL.md`
- Drive root: https://drive.google.com/drive/folders/16rGUnSWWMtnlAumavbZtDoOpegKqalUv
- Sheet: `1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE`
