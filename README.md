# ai-video

Repo de trabajo del equipo de producción de videos cortos verticales (9:16) para
productos de inclusión educativa de **AlizIA / Educabot**, usando IA generativa.

Stack canónico: **Higgsfield + ElevenLabs + FFmpeg**.

---

## Qué hay acá

Este repo es el **saber compartido** del equipo. NO contiene assets binarios
pesados — esos los genera cada uno local corriendo las skills.

```
ai-video/
├── CLAUDE.md                          # Instrucciones del proyecto (leer SIEMPRE primero)
├── README.md                          # Este archivo
├── .gitignore
├── .claude/skills/                    # Skills compartidas del workflow
│   ├── ai-inclusion-videos/           # Workflow gated end-to-end (legacy + montaje final)
│   ├── product-images-generation/     # Etapa 1: imágenes
│   ├── generate-audio/                # Etapa 2: audios (ElevenLabs)
│   └── generate-video/                # Etapa 3: videos por escena (Seedance)
└── productos/
    ├── _template/                     # Plantilla — copiar para arrancar un producto nuevo
    └── <producto-slug>/               # Un producto = un video
        ├── Product-rules-<slug>.md    # ✅ trackeado (contrato del producto)
        ├── storyboard.md              # ✅ trackeado (plan del lote)
        ├── referencias/ref-images/    # ✅ trackeado si pesa < 500 KB
        ├── product-hero.png           # ❌ local (regenerable)
        ├── workspace/                 # ❌ local (iteración)
        ├── imagenes-aprobadas/        # ❌ local
        └── audio/ videos/ final/      # ❌ local
```

---

## Cómo arrancar (clone fresco)

```bash
git clone git@github.com:profesorj13/ai-videos.git ai-video
cd ai-video

# Verificá el entorno (ver "Pre-flight" en CLAUDE.md)
higgsfield account status
gws --version
ffmpeg -version | head -1
```

No hace falta bajar nada más — las skills lo generan todo en tu máquina.

---

## Cómo contribuir

1. **Si mejorás una skill**: editá su `SKILL.md`, commit, push. El resto del
   equipo la levanta en el próximo `pull`.
2. **Si arrancás un producto nuevo**: creá `productos/<slug>/` siguiendo la
   estructura del CLAUDE.md. Subí `referencias/` chicas + `product-rules.md` +
   `storyboard.md`. Los outputs pesados quedan local.
3. **Si descubrís un patrón nuevo**: anotalo en la sección "Regla #6 —
   Hallazgos críticos" del CLAUDE.md. Esa es la memoria colectiva.

> Toda generación se registra en el Sheet `1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE`
> ("AV3 Videos Tracker"). Ver Regla #1 del CLAUDE.md — no hay excepciones.

---

## Qué NO subir al repo

- Cualquier `.mp4`, `.mov`, `.mp3`, `.opus`, `.wav`, `.pdf`
- Imágenes > 500 KB (regeneralas con la skill)
- Archivos `.env` o cualquier secreto
- Backups `.zip`, `.DS_Store`
- Outputs de las carpetas `workspace/`, `imagenes-aprobadas/`, `audio/`, `videos/`, `final/`

Todo eso está cubierto por `.gitignore`. Si `git status` muestra algo que no
debería viajar, ajustar `.gitignore` antes de seguir.

---

## Drive del equipo (assets a validar)

Root: <https://drive.google.com/drive/folders/16rGUnSWWMtnlAumavbZtDoOpegKqalUv>

Cada lote de imágenes/audios/videos para validación humana sube a
`<root>/<producto-slug>/<carpeta>/`.
