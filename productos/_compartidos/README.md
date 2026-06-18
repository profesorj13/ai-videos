# productos/_compartidos/

Assets canónicos compartidos por **todos** los videos AlizIA — intro/outro de
brandeo y bed musical estándar. Esta carpeta vive bajo `productos/` pero **no
es un producto**: es la librería del equipo.

Los binarios están gitignored (mp4/mp3). El repo guarda solo este README con
los IDs Drive para que cualquier miembro del equipo (Mac o Windows) reproduzca
la carpeta local antes de correr el assembly post-final.

## Layout esperado local

```
productos/_compartidos/
├── README.md                                 (este archivo, en git)
├── intro.mp4                                 (descargar de Drive)
├── outro.mp4                                 (descargar de Drive)
└── bed-canonico-the-mountain.mp3             (descargar de Drive)
```

## Assets

| Archivo | Specs | Drive ID |
|---|---|---|
| `intro.mp4` | 720×1280, 23.976 fps, 8.3s, **sin audio** | [`1N_ZpyKY8954RqLTOneEIWeA2gjA743Sp`](https://drive.google.com/file/d/1N_ZpyKY8954RqLTOneEIWeA2gjA743Sp/view) |
| `outro.mp4` | 720×1280, 23.976 fps, 5.05s, **sin audio** | [`1dSck-x8FUVC_6bS_FH0Oovm7BVHwEGH0`](https://drive.google.com/file/d/1dSck-x8FUVC_6bS_FH0Oovm7BVHwEGH0/view) |
| `bed-canonico-the-mountain.mp3` | 145s, 44.1 kHz stereo, instrumental cálido | [`1VQEQdTSohE8DAZfKQ4Ci2nv3KGgMLKNl`](https://drive.google.com/file/d/1VQEQdTSohE8DAZfKQ4Ci2nv3KGgMLKNl/view) |

Drive folder: [`_compartidos/`](https://drive.google.com/drive/folders/1LnZsVuLXKqNF2DLsngRYDiuWNnECiuTO) (dentro del root del equipo `16rGUnSWWMtnlAumavbZtDoOpegKqalUv`).

## Bajada local (una vez por máquina)

### Opción A — Browser

Abrí los 3 links Drive de arriba, "Descargar" en cada uno, mové los archivos a
`productos/_compartidos/`.

### Opción B — `gws` CLI

```bash
mkdir -p productos/_compartidos
gws drive files get --params '{"fileId":"1N_ZpyKY8954RqLTOneEIWeA2gjA743Sp","alt":"media"}' --output productos/_compartidos/intro.mp4
gws drive files get --params '{"fileId":"1dSck-x8FUVC_6bS_FH0Oovm7BVHwEGH0","alt":"media"}' --output productos/_compartidos/outro.mp4
gws drive files get --params '{"fileId":"1VQEQdTSohE8DAZfKQ4Ci2nv3KGgMLKNl","alt":"media"}' --output productos/_compartidos/bed-canonico-the-mountain.mp3
```

### Opción C — `rclone`

```bash
rclone copy "gdrive:_compartidos/" productos/_compartidos/
```

(El remote `gdrive:` debe estar configurado apuntando al Drive del equipo.)

## Verificación

```bash
ffprobe -v error -show_entries format=duration productos/_compartidos/intro.mp4
# duration=8.299958

ffprobe -v error -show_entries format=duration productos/_compartidos/outro.mp4
# duration=5.046708

ffprobe -v error -show_entries format=duration productos/_compartidos/bed-canonico-the-mountain.mp3
# duration=145.084063
```

## Cuándo se usan

En la **Etapa 5 — Post-final assembly** de la skill
[`ai-inclusion-videos`](../../.claude/skills/ai-inclusion-videos/SKILL.md).
Concretamente:

1. `intro.mp4` + `<final>.mp4` + `outro.mp4` → concat con FFmpeg
2. `bed-canonico-the-mountain.mp3` → mix con ducking automático bajo la VO

Si querés cambiar el bed musical para un video puntual, pasarlo como override
local — pero **no** reemplaces el canónico sin acuerdo del equipo: la
coherencia de marca depende de que todos los videos suenen igual.

## Actualizar un asset

Si rehacemos intro/outro o cambiamos el bed canónico:

1. Subir nueva versión a Drive `_compartidos/` (mantener el filename — no
   versionar con `-v2` salvo que querramos conservar el viejo).
2. Si el ID cambia, actualizar este README.
3. Avisar al equipo para que re-bajen localmente.

---

## Hallazgos — assembly post-final

### Normalizar TODOS los clips a stereo antes del `concat`

**Regla operativa**: antes de concatenar los clips por escena (`videos/preview/<escena>.mp4`), normalizarlos a las **mismas specs de audio** — stereo 2ch, 44.1 kHz, 192 kbps AAC.

**Por qué**: en `safety-loop-scissors-v3` (2026-06-18), el final compilado tenía un golpeteo rítmico tipo morse a partir del segundo 41. Diagnóstico tras varias horas: los 9 clips del concat venían con channels mixtos (7 en mono, 2 en stereo — `e3ii` y el cierre brand E5). Al re-encodar AAC en las transiciones mono↔stereo, ffmpeg metía artefactos rítmicos en el clip siguiente al cambio de channel layout. El "morse" empezaba EXACTAMENTE en la transición `e3ii (stereo) → e3iii (mono)`.

Seedance 2.0 devuelve clips con `channels` que dependen del audio que se le pase: si el clip va `silent` (sin `--audio`) o con un VO mono, el output sale mono; si lleva música o un audio stereo, sale stereo. **No asumir uniformidad.**

**Cómo aplicar**:

1. Después de Paso 4 (overlay audio FFmpeg per-escena), verificar specs:
   ```bash
   for f in productos/<slug>/videos/preview/*.mp4; do
     ffprobe -v error -select_streams a -show_entries stream=codec_name,sample_rate,channels -of csv=p=0 "$f"
   done
   ```
2. Si hay mismatch, hacer un loop de normalización a `preview-norm/` antes del concat:
   ```bash
   mkdir -p productos/<slug>/videos/preview-norm
   for SRC in productos/<slug>/videos/preview/*.mp4; do
     ffmpeg -y -i "$SRC" -c:v copy -c:a aac -ac 2 -ar 44100 -b:a 192k \
       productos/<slug>/videos/preview-norm/$(basename "$SRC")
   done
   ```
3. Concatenar desde `preview-norm/` con `-c:a copy` (sin re-encode adicional, los clips ya están alineados):
   ```bash
   ffmpeg -y -f concat -safe 0 -i concat-list.txt \
     -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
     -c:a copy \
     productos/<slug>/final/contenido-principal.mp4
   ```
4. El concat con `intro` + `outro` y el mix del bed musical también deben forzar `-c:a aac -ac 2 -ar 44100 -b:a 192k` explícitamente.

**Pista para diagnosticar**: si reportan "morse" / "código morse" / "golpeteo rítmico" en un final ya compilado, lo primero es revisar `ffprobe -select_streams a` sobre los clips fuente — antes de tocar bed musical, sidechain, o cualquier otra cosa. Caminos que NO son la causa (ya descartados en safety-loop-scissors v3): bed musical, sidechain compress agresivo, concat con intro/outro, re-generación del clip individual. El standalone del clip suena limpio porque el morse aparece sólo al concatenar.
