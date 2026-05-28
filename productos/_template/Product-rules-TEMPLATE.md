# Product Rules — <Nombre del producto> (<slug>)

> Contrato vivo del producto. Lo lee la skill `product-images-generation` en el
> **GATE 0.5** (obligatorio). Toda corrección del usuario sobre el producto se
> anota acá *en el momento*, no al final.
>
> Renombrá este archivo a `Product-rules-<slug>.md` al copiar el template.

---

## 1. Qué es

<1 párrafo: qué objeto es, para qué inclusión sirve, contexto de uso típico>

## 2. Anatomía

<componentes del producto descritos uno a uno: forma, color, material, escala>

- componente A: …
- componente B: …
- componente C: …

## 3. Restricciones

<lista de lo que NO debe verse en las stills: deformaciones, errores comunes
del modelo, anti-patterns visuales>

- no fusionar dos unidades en una forma simétrica (mariposa / pétalos / labios)
- no rotar más de 30°
- no mostrar piezas internas
- …

## 4. Uso (grip / interacción)

<cómo se sostiene / usa el producto físicamente — explícito para el modelo>

- grip humano: dedos sobre <parte X>, pulgar <descripción>
- escala respecto a una mano adulta: …

## 5. Prompt base — descripción exhaustiva del producto (EN)

<bloque en inglés copy-paste, listo para incrustar en cualquier prompt de
escena con el producto. Tan detallado que un modelo que solo lea este bloque
pueda reconstruir el producto sin ver ninguna imagen.>

```
<prompt en inglés, ~80-150 palabras>
```

## 6. Product Hero

- Path local: `product-hero.png`
- Job ID Higgsfield: `<uuid>`
- URL CDN: `<https://...cloudfront...png>`
- Versión aprobada: `v<N>` (anteriores: descartadas en `workspace/hero/discarded/`)
- Fecha de aprobación: `YYYY-MM-DD`

---

## Tabla de refs canónicas (UUIDs CDN reusables)

> Subir cada ref UNA SOLA VEZ y reusar el UUID. Evita `AccessDenied` transitorio.

| Slug | Path local | UUID CDN | Uso |
|---|---|---|---|
| hero | `product-hero.png` | `<uuid>` | Ref canónica de escenas con producto |
| ref-fabricante | `referencias/ref-images/<archivo>.jpg` | `<uuid>` | Ref real para Paso 1.5 |
| edicion-photoshop | `workspace/<archivo>.png` | `<uuid>` | Edición manual del usuario, válida como ref |
