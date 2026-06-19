---
name: ai-inclusion-videos
description: |
  Workflow gated para producir un video corto vertical (9:16, ~25-45s) sobre un
  producto de inclusión educativa de AlizIA, partiendo de un guión escrito.
  El flujo es estrictamente secuencial con QA gates humanos entre etapas:
  guión → imágenes (gate) → audios (gate) → videos (gate) → montaje (gate) → assembly post-final (intro+outro+música, gate final).
  Stack: Higgsfield (Nano Banana Pro, Product Photoshoot, Seedance 2.0) +
  ElevenLabs (Paola Blasi) + FFmpeg. Cada generación se registra en el Sheet
  `1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE`.
  Use cuando el usuario pida "armar un video del producto X", "video inclusivo
  con Mercedes", "video estilo Logitech para AlizIA", "producir reel del producto",
  "video vertical 9:16 con avatar" en este proyecto.
  NO usar para edición de video genérico, ni para videos largos > 60s, ni para
  videos que NO sigan el formato vertical 9:16 educativo.
argument-hint: "[ruta-al-guion.md]"
allowed-tools: Bash, Read, Write, Edit, Skill
---

# ai-inclusion-videos

Workflow probado en producción para videos AlizIA. **El valor de esta skill
está en los QA gates, no en los prompts**. Cada gate es un punto donde el
usuario aprueba el lote antes de que avancemos. Saltearlos es caro: cualquier
asset mal aprobado se propaga aguas abajo y multiplica el retrabajo.

---

## Reglas firmes (no negociables)

1. **Toda generación se trackea en el Sheet inmediatamente** (ver sección "Tracking").
2. **Nunca pisar archivos**: convención `v1`, `v2`, `v3` + sufijo descriptivo (`-grip-wrong`, `-ttsloop`, `-soulFail`).
3. **No avanzar de etapa sin aprobación explícita del usuario** del lote previo.
4. **Stack cerrado**: Higgsfield + ElevenLabs + FFmpeg. Nada más.
5. **Sin polling visible**: cuando un job tarda 2-5 min, programar wakeup / agente en background; no spammear status updates.

---

## Pipeline (5 etapas + gates)

```
                  ┌──────────────────────────────┐
   guión.md  ───▶ │  Etapa 1 — Imágenes (stills) │
                  └──────┬───────────────────────┘
                         ▼                                ◀── GATE 1: usuario aprueba cada still
                  ┌──────────────────────────────┐
                  │  Etapa 2 — Audios VO         │
                  └──────┬───────────────────────┘
                         ▼                                ◀── GATE 2: usuario aprueba todos los MP3
                  ┌──────────────────────────────┐
                  │  Etapa 3 — Videos por escena │
                  └──────┬───────────────────────┘
                         ▼                                ◀── GATE 3: usuario aprueba cada video
                  ┌──────────────────────────────┐
                  │  Etapa 4 — Montaje per-escena│
                  └──────┬───────────────────────┘
                         ▼                                ◀── GATE 4: usuario aprueba el concat
                  ┌──────────────────────────────────────────┐
                  │  Etapa 5 — Assembly post-final           │
                  │  (intro + outro + bed musical canónico)  │
                  └──────┬───────────────────────────────────┘
                         ▼                                ◀── GATE FINAL: usuario aprueba el .mp4
                       final.mp4
```

---

## Etapa 0 — Pre-flight (una vez por sesión)

Antes de generar cualquier asset, verificar:

```bash
# 1. Higgsfield autenticado + saldo
higgsfield account status   # debe retornar plan activo + créditos disponibles

# 2. ElevenLabs API key cargada
set -a && source /Users/ivi/Desktop/repos-educabot/av3-inclusion/.env && set +a
echo "${ELEVENLABS_API_KEY:0:8}..."   # confirma que está

# 3. gws CLI para Sheets (autenticado)
gws --version
gws sheets +read --spreadsheet 1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE --range 'videos!A1:A2' | head -10

# 4. FFmpeg + Pillow
ffmpeg -version | head -1
python3 -c "from PIL import Image; print('Pillow OK')"
```

Si **algo** falta, parar y avisar al usuario. No improvisar.

### Carpetas

Crear si no existen, **antes** de la etapa 1:

```bash
PROJECT_SLUG="<slug-del-producto>-<vN>"   # ej: safety-loop-scissors-mercedes-v1
BASE="/Users/ivi/Desktop/ai-video/data/assets/products/<product-slug>/generations/$PROJECT_SLUG"
mkdir -p "$BASE"/{images/discarded,audio,videos/{logs,discarded,preview},overlays,final}
```

### Row del proyecto en el Sheet `videos`

Si el proyecto es nuevo, agregar **una sola vez** un row a `videos` y guardar
el `video_id` devuelto — todas las generaciones lo van a referenciar.

```bash
# ver id máximo actual
gws sheets +read --spreadsheet 1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE --range 'videos!A:A'

# agregar el row (helper +append apunta por default a videos = tab 0)
gws sheets +append \
  --spreadsheet 1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE \
  --json-values '[["<next_id>","<slug>","<producto>","<titulo>","<duracion_estimada>","9:16"]]'
```

---

## Etapa 1 — Imágenes (stills first-frame)

Una still por sub-escena del guión. Cada still es el primer frame del video
que se generará en Etapa 3, así que la calidad acá determina la calidad del
video.

### Decision tree de modelo

| Caso | Modelo | Por qué |
|---|---|---|
| Avatar humano partiendo de 1 foto base | `nano_banana_2` + foto base como `--image` | Preserva identidad sin training; **NO** usar Soul ID con < 15 fotos. |
| Producto puro sobre fondo limpio (macro, cierre brand) | `higgsfield product-photoshoot create --mode <conceptual_product\|closeup_product_with_person>` | Backend asembla prompt brand-quality con GPT Image 2. |
| Escena con manos humanas + producto | `nano_banana_2` con 2 refs del producto + prompt quirúrgico del grip | Más control que Product Photoshoot, identidad consistente con avatar. |

### Comandos

```bash
# Avatar: expandir 1 foto a 6-8 ángulos (bible de Mercedes / etc.)
higgsfield generate create nano_banana_2 \
  --prompt "Same person as in reference, three-quarter profile, soft window light, mid-30s, ..." \
  --image /path/to/<avatar>.jpeg \
  --aspect_ratio 9:16 --resolution 2k \
  --wait --wait-timeout 8m --json > images/logs/<avatar>-M01.log

# Producto puro
higgsfield product-photoshoot create \
  --mode conceptual_product \
  --prompt "cyan rigid plastic loop scissors levitating on pastel pink AlizIA background, premium product reveal" \
  --image refs/<canonical>.jpg \
  --aspect_ratio 9:16 --timeout 8m

# Escena con grip humano (la más difícil — ver Aprendizajes #4)
higgsfield generate create nano_banana_2 \
  --prompt "Top-down view of young hand wrapping the continuous cyan plastic loop from OUTSIDE, all fingers external, no thumb inside the loop, ..." \
  --image refs/61KlzOKGpjL.jpg \
  --image refs/61-8ViFVZaL.jpg \
  --aspect_ratio 9:16 --resolution 2k \
  --wait --wait-timeout 8m --json
```

### Naming

- `<escena>-<rol>-v<N>[-<descriptor>].png` ej: `e3i-still-v1.png`, `e3i-still-v2-grip-wrong.png`, `e3i-still-v5.png` (final).
- El sufijo `-vN` se incrementa **cada** regeneración aunque la anterior sea solo subóptima. No reusar el mismo nombre.

### Tracking (obligatorio inmediato)

Después de cada job que retorna, **antes** de mostrarlo al usuario:

```bash
# Schema generations: id | video_id | escena | tipo | modelo | prompt | status | job_id | url_resultado | asset_local | fecha
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE","range":"generations!A:K","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["<id>","<video_id>","<escena>","<tipo>","<modelo>","<prompt>","<status>","<job_id>","<url>","<asset_local>","<fecha YYYY-MM-DD>"]]}'
```

Si el job sale `nsfw`, `failed`, o lo descartamos por calidad → también se
trackea con `status=nsfw|failed|discarded`. El motivo del descarte va anidado
en el `prompt` o se referencia en el `asset_local` apuntando a `discarded/`.

### GATE 1 — Aprobación del usuario

Cuando todas las stills planeadas están generadas:

> "Tengo `N` imágenes listas para la Etapa 2. Te las paso una por una para QA.
> Decime OK / regenerar / cambiar para cada una. Recién cuando todas estén
> aprobadas paso a audios."

Mostrar URL + descripción breve + paths locales. **No** pasar a Etapa 2 hasta
que el usuario diga "todas OK" o equivalente.

Si pide regenerar alguna: regenerar, trackear el descarte y el reemplazo, y
volver a pedir aprobación de **esa**. No batch-regenerar sin confirmación.

---

## Etapa 2 — Audios VO

Una pista por sub-escena. Todas con la misma voz canónica, mismos parámetros.

### Voz canónica

- **Paola Blasi** `PoLFkTquRWtbexdwW3Xa` (español rioplatense, AlizIA-aligned).
- `model_id=eleven_multilingual_v2`, `language_code=es`.
- Voice settings: `stability=0.65, similarity_boost=0.75, style=0.30, use_speaker_boost=True`.

### Comando (Python)

```python
import os
from elevenlabs.client import ElevenLabs
client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

texto = "..."  # del guión
audio = client.text_to_speech.convert(
    voice_id="PoLFkTquRWtbexdwW3Xa",
    text=texto,
    model_id="eleven_multilingual_v2",
    language_code="es",
    voice_settings={"stability":0.65,"similarity_boost":0.75,"style":0.30,"use_speaker_boost":True},
    output_format="mp3_44100_128",
)
with open(out_path, "wb") as f:
    for chunk in audio:
        if chunk: f.write(chunk)
```

### Trucos de pronunciación

Cuando ElevenLabs pronuncia mal una palabra técnica en español, probar
**en este orden**, parando al primer ajuste que funciona:

1. **Acentuar** la sílaba que se quiere que diga bien: `bucle` → `buclé`, `vínculo` → `vínculo`.
2. **Separar con guión**: `bucle` → `bu-cle`.
3. **Reescribir la palabra**: `bucle` → `lazo` / `asa cerrada`.

ElevenLabs es no-determinista: si solo cambia el seed, una segunda generación
del mismo texto puede pronunciar bien (probar 2-3 veces antes de cambiar texto).

### Tracking

```bash
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE","range":"generations!A:K","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["17","2","vo-e2i","audio","elevenlabs/eleven_multilingual_v2","Esta es la solución. La tijera adaptada tiene un asa en buclé continuo.","completed","local","","data/assets/products/safety-loop-scissors/generations/mercedes-v1/audio/vo-e2i-paola-v2.mp3","2026-05-18"]]}'
```

### GATE 2 — Aprobación del usuario

> "Tengo `N` audios listos. ¿Los escuchás y me decís OK uno por uno o
> regenerás alguno? Cuando todos estén OK paso a videos."

**No** pasar a Etapa 3 hasta tener todos los audios validados.

---

## Etapa 3 — Videos por escena (image-to-video)

Cada still aprobada se anima con `seedance_2_0`. La duración del video se elige
en función de la duración del audio correspondiente.

### Decision tree de `--audio`

| Tipo de escena | `--audio` | Por qué |
|---|---|---|
| **Sin avatar** (producto puro, manos, escenas grupales) | NO pasar `--audio` | El VO se pisará en FFmpeg desde el MP3 externo. |
| **Con avatar** (Mercedes hablando) | **NO pasar `--audio`** | Seedance 2.0 con `--audio` NO hace pass-through: usa el MP3 como guía rítmica para animar la boca pero **sintetiza su propio TTS** al output (en piloto Mercedes-v1, E4 con prompt en inglés terminó hablando en inglés). Generar silent + pisar MP3 en FFmpeg. Se pierde el lipsync exacto, se gana voz consistente. |

> Si en el futuro Higgsfield publica un modelo con audio pass-through real, esta regla cambia. Revisar `higgsfield model list` antes de cada proyecto nuevo.

### Duración

Seedance 2.0 acepta `--duration` entre 4 y 10 segundos. Elegir el entero más
chico que cubra el VO + ~0.5-1s de cola:

| VO (s) | duration |
|---|---|
| ≤ 3.5 | 4 |
| 3.5–4.5 | 5 |
| 4.5–5.5 | 6 |
| 5.5–6.5 | 7 |
| 6.5–7.5 | 8 |
| 7.5–8.5 | 9 |
| 8.5–9.5 | 10 |

Si el VO supera 9.5s, partir la escena en dos sub-clips de 5s c/u.

### Comando

```bash
higgsfield generate create seedance_2_0 \
  --prompt "<prompt corto: subject + action + camera + style + constraints>" \
  --start-image images/<scene>-still.png \
  --duration <N> --aspect_ratio 9:16 --resolution 720p --mode std \
  --wait --wait-timeout 15m --json \
  > videos/logs/<scene>.log 2>&1 &
```

Lanzar todos los videos del lote en paralelo (cada uno como background con
`&` o como agente). El proceso típico tarda 2-5 min por video. **No spammear
status updates** — esperar y revisar logs al final.

### Overlay del MP3 (post-Seedance, pre-aprobación)

Cuando un video silent termina, generar inmediatamente el preview con audio
para que el usuario lo evalúe con voz:

```bash
ffmpeg -y -i videos/<scene>-silent.mp4 -i audio/vo-<scene>-paola.mp3 \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest \
  videos/preview/<scene>-overlay.mp4
```

(Para escenas en las que el video es más largo que el audio, eliminar `-shortest` o usar `-t <duración exacta>`.)

### Tracking

```bash
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE","range":"generations!A:K","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["18","2","E3-i","video","seedance_2_0","Macro top-down zoom-in toward cutting hand...","completed","ae79bc23-1e7c-4f94-883b-51093222a27a","https://d8j0ntlcm91z4.cloudfront.net/.../hf_....mp4","data/assets/products/safety-loop-scissors/generations/mercedes-v1/videos/e3i.mp4","2026-05-18"]]}'
```

### GATE 3 — Aprobación del usuario

> "Tengo `N` videos listos. Acá los URLs de cada preview con audio pegado.
> Me decís OK / regenerar / ajustar uno por uno. Cuando todos estén OK pasamos al montaje."

Atención a:
- Identidad del avatar consistente entre las escenas con persona.
- Producto con morfología correcta en cada toma.
- Grip correcto en escenas con manos cortando.
- Audio + boca razonablemente alineados (no lipsync perfecto, pero no descalabro).

**No** pasar a Etapa 4 sin el visto bueno completo del lote.

---

## Etapa 4 — Montaje per-escena (FFmpeg)

Concatenar todos los videos en orden, con el map mixto correcto.

### Regla del map mixto

> Importante: en piloto Mercedes-v1 todas las escenas se generan **silent**, por lo que el audio siempre se pisa con el MP3 externo. Si en un futuro proyecto se usa un modelo con audio embebido real (no Seedance 2.0), esa escena va con `-map 0:a` y NO se pisa.

```bash
ffmpeg -y \
  -i videos/e1.mp4         -i audio/vo-e1-paola.mp3 \
  -i videos/e2i.mp4        -i audio/vo-e2i-paola-v2.mp3 \
  -i videos/e2ii.mp4       -i audio/vo-e2ii-paola.mp3 \
  -i videos/e3i.mp4        -i audio/vo-e3i-paola.mp3 \
  -i videos/e3ii.mp4       -i audio/vo-e3ii-paola.mp3 \
  -i videos/e3iii.mp4      -i audio/vo-e3iii-paola.mp3 \
  -i videos/e4.mp4         -i audio/vo-e4-paola.mp3 \
  -i videos/e5.mp4 \
  -filter_complex "
    [0:v]setpts=PTS-STARTPTS[v0]; [1:a]asetpts=PTS-STARTPTS[a0];
    [2:v]setpts=PTS-STARTPTS[v1]; [3:a]asetpts=PTS-STARTPTS[a1];
    [4:v]setpts=PTS-STARTPTS[v2]; [5:a]asetpts=PTS-STARTPTS[a2];
    [6:v]setpts=PTS-STARTPTS[v3]; [7:a]asetpts=PTS-STARTPTS[a3];
    [8:v]setpts=PTS-STARTPTS[v4]; [9:a]asetpts=PTS-STARTPTS[a4];
    [10:v]setpts=PTS-STARTPTS[v5]; [11:a]asetpts=PTS-STARTPTS[a5];
    [12:v]setpts=PTS-STARTPTS[v6]; [13:a]asetpts=PTS-STARTPTS[a6];
    [14:v]setpts=PTS-STARTPTS[v7]; anullsrc=channel_layout=stereo:sample_rate=44100[a7];
    [v0][a0][v1][a1][v2][a2][v3][a3][v4][a4][v5][a5][v6][a6][v7][a7]concat=n=8:v=1:a=1[v][a]
  " \
  -map "[v]" -map "[a]" \
  -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 192k \
  final/<project-slug>.mp4
```

### Overlays con Pillow + FFmpeg

PNGs transparentes generados con Pillow + DM Sans (skill `front-alizia` da la paleta y tipografía). Para animar entrada/salida:

```bash
-i overlays/e5-title.png \
-filter_complex "[14:v][15:v]overlay=enable='between(t,33,38)':alpha=0.95[outv]"
```

### Tracking del render final

```bash
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE","range":"generations!A:K","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["99","2","final","render","ffmpeg/concat","8 clips + 7 vos + overlays, duración 40s","completed","local","","data/assets/products/safety-loop-scissors/generations/mercedes-v1/final/<slug>.mp4","2026-05-18"]]}'
```

### Normalizar channels antes del concat (regla anti-morse)

> Lección de `safety-loop-scissors-v3` (2026-06-18). Tras varias horas de
> debug por un golpeteo rítmico tipo morse a partir del segundo 41 del final
> compilado.

**Antes** del concat, verificar specs de audio de cada clip por escena:

```bash
for f in productos/<slug>/videos/preview/*.mp4; do
  ffprobe -v error -select_streams a -show_entries stream=codec_name,sample_rate,channels -of csv=p=0 "$f"
done
```

Si hay **mismatch de channels** (mono vs stereo) entre clips — Seedance 2.0
devuelve `channels` que dependen del audio que le pases (clip silent o VO mono
→ mono; clip con audio stereo → stereo), **no asumir uniformidad** — normalizar
a stereo 44.1k 192k AAC en un directorio `preview-norm/` previo al concat:

```bash
mkdir -p productos/<slug>/videos/preview-norm
for SRC in productos/<slug>/videos/preview/*.mp4; do
  ffmpeg -y -i "$SRC" -c:v copy -c:a aac -ac 2 -ar 44100 -b:a 192k \
    productos/<slug>/videos/preview-norm/$(basename "$SRC")
done
```

Después concatenar desde `preview-norm/` con `-c:a copy` (sin re-encode
adicional — los clips ya están alineados). El concat con `intro` + `outro` y
el mix del bed musical también deben forzar `-c:a aac -ac 2 -ar 44100 -b:a
192k` explícitamente.

**Causa raíz**: cuando ffmpeg re-encoda AAC en una transición mono↔stereo,
mete artefactos rítmicos en el clip siguiente al cambio de channel layout. El
"morse" arranca EXACTAMENTE en esa transición. El clip standalone suena
limpio — el morse aparece sólo al concatenar clips con channel layouts mixtos.

**Si reportan morse en un final ya compilado** (síntoma típico: "código
morse" / "golpeteo rítmico" / "tipo punteo"), antes de tocar nada más, correr
el `ffprobe` de arriba sobre los clips fuente. Caminos descartados (verificados
en `safety-loop-scissors-v3`, no perder tiempo ahí): bed musical, sidechain
compress agresivo, concat con intro/outro, regeneración del clip individual.

### GATE 4

> "Acá el concat per-escena sin intro/outro ni música. Reproducilo y decime:
> aprobado / iteración / cambio mayor. Si aprobás, pasamos a Etapa 5 (assembly
> post-final)."

---

## Etapa 5 — Assembly post-final (intro + outro + bed musical canónico)

Brandeo AlizIA — **todos** los videos del equipo cierran igual: intro y outro
compartidos + bed musical canónico con ducking sobre la VO. Esta etapa es
mecánica (no hay creatividad), aplica para cada producto sin tocar parámetros.

### Assets canónicos compartidos

Viven en `productos/_compartidos/` (todos binarios — bajada local una vez
por máquina desde Drive, instrucciones en [`productos/_compartidos/README.md`](../../../productos/_compartidos/README.md)).

| Archivo | Duración / specs | Drive ID |
|---|---|---|
| `intro.mp4` | 7.8s · 720×1280 · 23.976 fps · sin audio | [`1rU80YQAjoFog47jFZWYkxSfWxBFtzBav`](https://drive.google.com/file/d/1rU80YQAjoFog47jFZWYkxSfWxBFtzBav/view) |
| `outro.mp4` | 5.05s · 720×1280 · 23.976 fps · sin audio | [`1dSck-x8FUVC_6bS_FH0Oovm7BVHwEGH0`](https://drive.google.com/file/d/1dSck-x8FUVC_6bS_FH0Oovm7BVHwEGH0/view) |
| `bed-canonico-the-mountain.mp3` | 145s · 44.1 kHz · stereo · instrumental cálido | [`1VQEQdTSohE8DAZfKQ4Ci2nv3KGgMLKNl`](https://drive.google.com/file/d/1VQEQdTSohE8DAZfKQ4Ci2nv3KGgMLKNl/view) |
| `educabot-logo-overlay.png` | 720×1280 · RGBA · logo "EDUCABOT — TECNOLOGÍA EDUCATIVA" en top 8-14%, resto transparente · 38 KB | [`1_Dp0W-_cNNaaGDYji3A7-UGBkkhwZrVU`](https://drive.google.com/file/d/1_Dp0W-_cNNaaGDYji3A7-UGBkkhwZrVU/view) |

Antes de arrancar, **pre-check**:

```bash
ls productos/_compartidos/intro.mp4 productos/_compartidos/outro.mp4 \
   productos/_compartidos/bed-canonico-the-mountain.mp3 || \
  echo "FALTA bajar assets canónicos — ver productos/_compartidos/README.md"
```

### Paso 5.1 — Concat intro + final + outro

Los finales suelen ir a 24 fps (Seedance) y los intro/outro a 23.976. Hay que
normalizar a 24 fps **y** inyectar audio silencioso en intro/outro (con
`anullsrc`) para que el concat tenga audio continuo.

```bash
SLUG=safety-loop-scissors           # ejemplo
VN=v3                                # versión del final per-escena aprobado en GATE 4
FINAL="productos/$SLUG/final/$SLUG-$VN-final.mp4"
OUT="productos/$SLUG/final/$SLUG-$VN-final-with-intro-outro.mp4"

ffmpeg -y \
  -i productos/_compartidos/intro.mp4 \
  -i "$FINAL" \
  -i productos/_compartidos/outro.mp4 \
  -f lavfi -t 8.3  -i "anullsrc=channel_layout=mono:sample_rate=44100" \
  -f lavfi -t 5.05 -i "anullsrc=channel_layout=mono:sample_rate=44100" \
  -filter_complex "[0:v]fps=24,setsar=1[v0];[1:v]fps=24,setsar=1[v1];[2:v]fps=24,setsar=1[v2];[v0][3:a][v1][1:a][v2][4:a]concat=n=3:v=1:a=1[outv][outa]" \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 128k -movflags +faststart \
  "$OUT"
```

### Paso 5.1b — Overlay logo Educabot sobre el contenido principal

El logo Educabot (`educabot-logo-overlay.png`) se aplica **solo al contenido
principal** — entre intro y outro, NUNCA encima de intro/outro (las placas
ya traen su branding propio y aplicarles el logo encima genera ruido visual).

Opciones:

- **A (recomendado para videos nuevos)**: aplicar el overlay al `$FINAL` del
  concat per-escena (antes del paso 5.1). Resultado: el logo queda en cuadro
  durante todo el contenido principal del 5.1.
- **B**: aplicar al output del 5.1 con `enable='between(t,T_VO_START,T_VO_END)'`
  para que el overlay solo aparezca durante el contenido principal (no en los
  segmentos del intro/outro). Útil si el `$FINAL` ya fue aprobado y no querés
  re-renderearlo.

El PNG ya está dimensionado a 720×1280 con el logo en la zona superior y el
resto transparente — no requiere scale ni position, se aplica full-frame con
`overlay=0:0:format=auto`:

```bash
# Opción A: overlay sobre el $FINAL antes del concat con intro/outro
FINAL_WITH_LOGO="productos/$SLUG/final/$SLUG-$VN-final-with-logo.mp4"
ffmpeg -y \
  -i "$FINAL" \
  -i productos/_compartidos/educabot-logo-overlay.png \
  -filter_complex "[0:v][1:v]overlay=0:0:format=auto" \
  -c:v libx264 -crf 18 -preset slow -c:a copy \
  "$FINAL_WITH_LOGO"
# después usar $FINAL_WITH_LOGO como input en el paso 5.1
```

```bash
# Opción B: overlay condicional en el output del 5.1, encendido solo durante
# el contenido principal (después del intro, antes del outro).
T_LOGO_END=$(python3 -c "print(8.3 + $FINAL_DUR)")     # cambia a 7.8 si intro nuevo
OUT_WITH_LOGO="${OUT%.mp4}-with-logo.mp4"
ffmpeg -y \
  -i "$OUT" \
  -i productos/_compartidos/educabot-logo-overlay.png \
  -filter_complex "[0:v][1:v]overlay=0:0:format=auto:enable='between(t,8.3,$T_LOGO_END)'" \
  -c:v libx264 -crf 18 -preset slow -c:a copy \
  "$OUT_WITH_LOGO"
```

> **No** aplicar el overlay sobre intro/outro completos: las placas tienen
> branding propio y el logo encima genera ruido visual. Si usás Opción B
> verificá los timestamps — un off-by-one que tape la placa de cierre rompe
> el cierre brand.

### Paso 5.2 — Mix con bed musical (ducking automático)

Música al 70% en intro/outro, ducked al 10% bajo la VO. Fades de 0.6s en
transiciones, fade-out 1.0s al cierre. `T_VO_START = intro_dur (8.3s)`,
`T_VO_END = T_VO_START + dur(final)`.

```bash
# Inputs
WITH_IO="$OUT"                                                  # del paso 5.1
TOTAL=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$WITH_IO")
FINAL_DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$FINAL")
T_VO_START=8.3
T_VO_END=$(python3 -c "print(8.3 + $FINAL_DUR)")
T_FADEOUT_START=$(python3 -c "print($TOTAL - 1.0)")
FINAL_OUT="productos/$SLUG/final/$SLUG-$VN-final-with-music.mp4"

ffmpeg -y \
  -i "$WITH_IO" \
  -i productos/_compartidos/bed-canonico-the-mountain.mp3 \
  -filter_complex "[0:a]aformat=channel_layouts=stereo,aresample=44100[vo];[1:a]atrim=0:$TOTAL,aresample=44100,afade=t=in:st=0:d=1.0,afade=t=out:st=$T_FADEOUT_START:d=1.0,volume='if(lt(t,$(python3 -c "print($T_VO_START-0.3)")),0.7,if(lt(t,$(python3 -c "print($T_VO_START+0.3)")),0.7-(t-$(python3 -c "print($T_VO_START-0.3)"))/0.6*0.6,if(lt(t,$(python3 -c "print($T_VO_END-0.3)")),0.10,if(lt(t,$(python3 -c "print($T_VO_END+0.3)")),0.10+(t-$(python3 -c "print($T_VO_END-0.3)"))/0.6*0.6,0.7))))':eval=frame[music];[vo][music]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[mixed]" \
  -map 0:v -map "[mixed]" \
  -c:v copy -c:a aac -b:a 192k -ar 44100 -movflags +faststart \
  "$FINAL_OUT"
```

Tips:
- `-c:v copy` — solo se re-encodea audio, render en ~2s.
- Si el usuario reporta "la música tapa la VO" o "no se escucha la música" en
  intro/outro, ajustar los dos floats (`0.10` y `0.7`) y regenerar como nueva
  versión `-v<N+1>`. Nunca pisar.
- Override de bed musical por video puntual: pasar otra ruta como `-i` en lugar
  del canónico. No reemplaces el archivo canónico salvo acuerdo de equipo.

### Paso 5.3 — Publicación en Drive `videos-a-validar/`

```bash
PARENT=$(gws drive files list --params "{\"q\":\"name='$SLUG' and trashed=false\",\"fields\":\"files(id,name)\"}" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['files'][0]['id'])")
VAL_FOLDER=$(gws drive files list --params "{\"q\":\"name='videos-a-validar' and '$PARENT' in parents\",\"fields\":\"files(id)\"}" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['files'][0]['id'])")
gws drive +upload "$FINAL_OUT" --parent "$VAL_FOLDER"
```

### Tracking del assembly

Cada paso 5.1 y 5.2 se registra en `generations` con `tipo=assembly`:

```bash
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE","range":"generations!A:K","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[
    ["<next_id>","<video_id>","intro-outro","assembly","ffmpeg/concat","intro.mp4 + final + outro.mp4 + anullsrc","completed","local","<drive_url_si_subido>","productos/<slug>/final/<slug>-vN-final-with-intro-outro.mp4","<fecha>"],
    ["<next_id+1>","<video_id>","music","assembly","ffmpeg/amix-ducking","bed-canonico-the-mountain.mp3, ducking 0.7/0.10/0.6s","completed","local","<drive_url>","productos/<slug>/final/<slug>-vN-final-with-music.mp4","<fecha>"]
  ]}'
```

### GATE FINAL

> "Acá el .mp4 con intro/outro y música. Reproducilo y decime:
> aprobado / iteración (ajustar niveles) / cambio mayor.
> Si aprobás, registro los dos assemblies en el Sheet, archivo descartes y cierro."

---

## Tracking — pegar al Sheet (regla #1 absoluta)

Sheet: `1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE` — 4 tabs (`videos`, `scripts`, `generations`, `assets`).

### Schema real

**`videos`** (`A:F`): `id | slug | producto | titulo | duracion_seg | formato`
**`scripts`** (`A:F`): `video_id | escena | t_inicio | t_fin | narracion | visual`
**`generations`** (`A:K`): `id | video_id | escena | tipo | modelo | prompt | status | job_id | url_resultado | asset_local | fecha`
**`assets`** (`A:F`): `id | slug | tipo | ruta_local | descripcion | fecha`

### Comando canónico (target = `generations`)

```bash
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE","range":"generations!A:K","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[[<11 columnas>], [<11 columnas>], ...]}'
```

> El helper `gws sheets +append` apunta solo a la primera tab (`videos`).
> Para `generations` (la operativa) usar la forma explícita con `--params --json`.

### Pre-flight de Sheet (una vez por proyecto)

```bash
# 1) Próximo id disponible en generations
gws sheets +read --spreadsheet 1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE --range 'generations!A:A' \
  | python3 -c "import json,sys,re; r=sys.stdin.read(); r=re.sub(r'^Using keyring backend.*\n','',r,flags=re.M); d=json.loads(r); print(max(int(x[0]) for x in d['values'][1:] if x and x[0].isdigit())+1)"

# 2) Próximo video_id (si el proyecto NO existe todavía)
gws sheets +read --spreadsheet 1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE --range 'videos!A:B'

# 3) Crear el row del proyecto en videos (si NO existe)
gws sheets +append \
  --spreadsheet 1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE \
  --json-values '[["<video_id>","<slug>","<producto>","<titulo>","<duracion_seg>","9:16"]]'
```

A partir de ahí, todas las generaciones referencian `video_id` y se incrementan
el `id`.

### Cuándo pegar al Sheet

- Inmediatamente después de cada job que retorna (cualquier status).
- Antes de mostrarle al usuario el output, no después.
- Bulk-append cuando se lanzaron N jobs en paralelo y terminaron.
- Versiones descartadas (`status=discarded`) también van — con `asset_local` apuntando a la carpeta `discarded/`.
- El render final también va (`tipo=render`, `modelo=ffmpeg/concat`).

### Cuándo NO pegar al Sheet

- Nunca dejar de pegar. La regla es absoluta. Si no podés (gws no autenticado, etc.), parar y avisar al usuario.

---

## Anti-patterns (cosas que ya nos costaron tiempo)

1. **Generar el siguiente lote antes de tener aprobación del lote actual.** Esto se llamaba "ahorrar tiempo" y termina costando 3× en regeneraciones.
2. **Pisar archivos en regen.** Convención v1/v2/v3 + sufijo descriptivo. SIEMPRE.
3. **Pasar `--audio` a Seedance 2.0 para lipsync.** No funciona como pass-through. Generar silent + overlay.
4. **Soul ID con < 15 fotos.** Falla. Usar Nano Banana Pro con foto base como `--image`.
5. **Olvidarse de trackear los descartes.** Equivalente a quemar la trazabilidad.
6. **Decirle al usuario "ya está, próxima etapa".** Esperar OK explícito por cada gate.
7. **Crear una nueva skill local "para esta vez nomás".** No. Esta skill es la base. Si algo nuevo se gana, se documenta acá.
8. **Polling visible**: status spam cada 30s. Usar background + wakeup, o esperar en silencio.

---

## Costo de referencia

Video vertical 9:16, ~40s, 8 sub-escenas (piloto Mercedes-v1 + correcciones):

- Imágenes: ~30 créditos Higgsfield (8 finales + retries).
- Audios: ~1k chars ElevenLabs (~$0.30).
- Videos: ~200 créditos Higgsfield (8 finales + retries).
- Total: **~230 créditos Higgsfield + ~$0.50 ElevenLabs + tiempo FFmpeg gratis**.

Saldo mínimo recomendado al arrancar: **300 créditos**.

---

## Referencias

- Sheet: https://docs.google.com/spreadsheets/d/1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE
- HANDOFF activo del piloto: `<repo>/docs/videos/scripts/HANDOFF-mercedes-v1.md`
- Skills externas usadas (instaladas globalmente):
  - `higgsfield-generate` — wrapper general
  - `higgsfield-product-photoshoot` — modos product_shot, conceptual_product, etc.
  - `higgsfield-soul-id` — solo si hay 15+ fotos reales del avatar
- Diseño visual (cuando hay que producir docs/PDF del proceso): skill `front-alizia` (DM Sans + paleta `#735fe3`/`#01ceaa`).
