# Template de producto

Estructura canónica para arrancar un producto nuevo. Esta carpeta es **plantilla**,
no un producto real — el guión bajo (`_`) la separa visualmente.

## Cómo arrancar un producto nuevo

```bash
# Desde el root del repo
cp -r productos/_template productos/<mi-producto-slug>

# Renombrá el archivo del Product Rules con el slug del producto
mv productos/<mi-producto-slug>/Product-rules-TEMPLATE.md \
   productos/<mi-producto-slug>/Product-rules-<mi-producto-slug>.md

# Subí 1-3 fotos reales del producto a referencias/ref-images/
# (web del fabricante, foto física, render oficial, etc.)
```

**PowerShell**:

```powershell
Copy-Item -Recurse productos/_template productos/<mi-producto-slug>
Rename-Item productos/<mi-producto-slug>/Product-rules-TEMPLATE.md `
            Product-rules-<mi-producto-slug>.md
```

Después invocá la skill `product-images-generation <slug>` y ella hace el
resto (storyboard, hero, escenas).

## Qué tiene este template

```
_template/
├── README.md                         # este archivo (no copiar al producto, o sí — da igual)
├── Product-rules-TEMPLATE.md         # esqueleto de los 6 bloques (renombrar al copiar)
├── referencias/ref-images/           # 📥 acá van tus fotos reales del producto
├── workspace/                        # 🖼️ product-images-generation
│   ├── hero/                         #    versiones del hero durante iteración
│   ├── logs/                         #    JSON por job de Higgsfield
│   └── discarded/                    #    versiones rechazadas (al cierre del flujo)
├── imagenes-aprobadas/               # ✅ finales locales por escena
├── imagenes-a-validar/               # ↗️ espejo de lo que sube a Drive
├── audio/                            # 🎙️ generate-audio (ElevenLabs)
│   ├── workspace/                    #    raw pre-padding
│   ├── logs/                         #    JSON por job
│   ├── discarded/
│   └── aprobados/                    #    finales con nombre limpio `vo-<escena>.mp3`
├── videos/                           # 🎬 generate-video (Seedance 2.0)
│   ├── workspace/                    #    `.mp4` silent por escena
│   ├── logs/                         #    JSON por job + plans
│   ├── preview/                      #    `.mp4` con audio overlay (validación)
│   └── discarded/
└── final/                            # 🎞️ render único final (skill legacy)
```

> `product-hero.png`, `storyboard.md`, `voice-board.md` y `motion-board.md` los
> generan las skills — no aparecen en el template porque no son input del usuario.

## Qué viaja al repo cuando copiás el template

Cuando creás `productos/<mi-slug>/` y commiteás:

| Archivo / carpeta | Viaja al repo |
|---|---|
| `Product-rules-<slug>.md` | ✅ contrato del producto |
| `storyboard.md` | ✅ plan del lote (lo genera la skill) |
| `referencias/ref-images/*.{png,jpg,webp}` | ✅ si pesan < 500 KB |
| `product-hero.png` | ❌ regenerable; pesa por encima del umbral |
| `workspace/`, `imagenes-*`, `audio/`, `videos/`, `final/` | ❌ outputs locales |

Si una ref pesa > 500 KB, subila al Drive y anotá el link en
`referencias/ref-images/README.md`.

Ver `CLAUDE.md` → "Regla #7 — Repo Git" para el detalle completo.
