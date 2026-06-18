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
├── educabot-logo-overlay.png                 (en git — chico, 38 KB)
├── intro.mp4                                 (descargar de Drive)
├── outro.mp4                                 (descargar de Drive)
└── bed-canonico-the-mountain.mp3             (descargar de Drive)
```

## Assets

| Archivo | Specs | Drive ID |
|---|---|---|
| `intro.mp4` | 720×1280, 23.976 fps, 7.8s, **sin audio** | [`1rU80YQAjoFog47jFZWYkxSfWxBFtzBav`](https://drive.google.com/file/d/1rU80YQAjoFog47jFZWYkxSfWxBFtzBav/view) |
| `outro.mp4` | 720×1280, 23.976 fps, 5.05s, **sin audio** | [`1dSck-x8FUVC_6bS_FH0Oovm7BVHwEGH0`](https://drive.google.com/file/d/1dSck-x8FUVC_6bS_FH0Oovm7BVHwEGH0/view) |
| `bed-canonico-the-mountain.mp3` | 145s, 44.1 kHz stereo, instrumental cálido | [`1VQEQdTSohE8DAZfKQ4Ci2nv3KGgMLKNl`](https://drive.google.com/file/d/1VQEQdTSohE8DAZfKQ4Ci2nv3KGgMLKNl/view) |
| `educabot-logo-overlay.png` | 720×1280, RGBA, logo "EDUCABOT — TECNOLOGÍA EDUCATIVA" en top 8-14%, resto transparente, 38 KB | **vive en el repo** (chico) — no requiere bajada Drive |

Drive folder: [`_compartidos/`](https://drive.google.com/drive/folders/1LnZsVuLXKqNF2DLsngRYDiuWNnECiuTO) (dentro del root del equipo `16rGUnSWWMtnlAumavbZtDoOpegKqalUv`).

## Bajada local (una vez por máquina)

### Opción A — Browser

Abrí los 3 links Drive de arriba, "Descargar" en cada uno, mové los archivos a
`productos/_compartidos/`.

### Opción B — `gws` CLI

```bash
mkdir -p productos/_compartidos
gws drive files get --params '{"fileId":"1rU80YQAjoFog47jFZWYkxSfWxBFtzBav","alt":"media"}' --output productos/_compartidos/intro.mp4
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
# duration=7.799458

ffprobe -v error -show_entries format=duration productos/_compartidos/outro.mp4
# duration=5.046708

ffprobe -v error -show_entries format=duration productos/_compartidos/bed-canonico-the-mountain.mp3
# duration=145.084063
```

## Cuándo se usan

En la **Etapa 5 — Post-final assembly** de la skill
[`ai-inclusion-videos`](../../.claude/skills/ai-inclusion-videos/SKILL.md).
Concretamente:

1. `educabot-logo-overlay.png` → overlay sobre el contenido principal
   (entre intro y outro, NUNCA sobre intro/outro porque ya traen branding propio).
2. `intro.mp4` + `<contenido-con-logo>.mp4` + `outro.mp4` → concat con FFmpeg.
3. `bed-canonico-the-mountain.mp3` → mix con ducking automático bajo la VO.

### FFmpeg — aplicar overlay del logo al contenido principal

El PNG ya está dimensionado a 720×1280 con el logo en la zona superior y el
resto transparente. No requiere scale ni position — se aplica full-frame:

```bash
ffmpeg -i <contenido-principal>.mp4 -i productos/_compartidos/educabot-logo-overlay.png \
  -filter_complex "[0:v][1:v]overlay=0:0:format=auto" \
  -c:v libx264 -crf 18 -preset slow -c:a copy \
  <contenido-con-logo>.mp4
```

Después concatenar con intro/outro y aplicar el bed musical como siempre.
**Importante**: el overlay solo va sobre el contenido principal — las placas
intro/outro ya traen branding y aplicarles el logo encima genera ruido visual.

Si querés cambiar el bed musical para un video puntual, pasarlo como override
local — pero **no** reemplaces el canónico sin acuerdo del equipo: la
coherencia de marca depende de que todos los videos suenen igual.

## Actualizar un asset

Si rehacemos intro/outro o cambiamos el bed canónico:

1. Subir nueva versión a Drive `_compartidos/` (mantener el filename — no
   versionar con `-v2` salvo que querramos conservar el viejo).
2. Si el ID cambia, actualizar este README.
3. Avisar al equipo para que re-bajen localmente.
