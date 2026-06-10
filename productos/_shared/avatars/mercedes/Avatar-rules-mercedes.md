# Avatar Rules — Mercedes (avatar canónico AlizIA)

> Contrato vivo del avatar. Análogo al `Product-rules-<slug>.md` pero compartido
> entre todos los productos donde aparece Mercedes (en lugar de duplicarse en
> cada carpeta de producto).
>
> Lo lee la skill `product-images-generation` cuando el storyboard tiene una
> escena con avatar humano. Toda corrección del usuario sobre Mercedes se
> anota acá *en el momento*, no al final.

---

## 1. Identidad

Mercedes — psicopedagoga argentina, voz canónica AlizIA ([generate-audio](.claude/skills/generate-audio/SKILL.md): voice ID `aKtTSeLwi8u4QiEEtGZ0`, AlizIA Malena Clone v1, re-clonada 2026-06-08 con 3 samples de WhatsApp). Es el avatar narrador-presentador que aparece en los videos de productos de inclusión educativa.

## 2. Apariencia física (descrita desde la ref, NO desde memoria)

- **Edad**: mid-30s (~32-38 años).
- **Pelo**: **castaño medio caramelo con highlights naturales sun-lit** (warm medium-brown / caramelo claro, NO oscuro, NO negro, NO rubio). Largo (hasta los hombros / poco más abajo), ondulado natural, raya al medio o ligeramente al costado, look natural sin peinado armado.
- **Tez**: clara con tono cálido (Argentine fair-skinned warm tone).
- **Facciones**: ovaladas, suaves, cejas naturales bien definidas, ojos castaños.
- **Sonrisa canónica**: **warm closed-mouth gentle smile**. Cerrada o muy levemente entreabierta, **NUNCA articulando palabras / hablando con la boca abierta**. Razón: los videos no llevan lipsync real (ver [generate-video](.claude/skills/generate-video/SKILL.md) §A — decisión "narración-sobre-gesto"), por lo que cualquier still donde aparezca "hablando" rompe la coherencia con el VO.
- **Mirada canónica**: **al objeto que está usando o presentando**, NO a cámara — salvo que el guión pida explícitamente "mira a cámara".

## 3. Ropa típica

- **Estilo**: simple, cotidiano, look docente argentino contemporáneo. NO usar pinta de "modelo de catálogo" ni "psicóloga de consultorio formal".
- **Prendas típicas que funcionan bien con la estética documental**:
  - Remera (t-shirt) lisa gris claro, gris cálido, blanco roto o beige.
  - Blusa de algodón color claro (crema, beige, celeste muy lavado, lila pálido).
  - Ocasionalmente un cárdigan o sweater liviano si el guión lo justifica.
- **NO**: estampados ruidosos, accesorios llamativos, marcas, logos.

## 4. Postura y gestualidad

- **Postura**: abierta, segura, calma. Hombros relajados.
- **Manos**: muestran/sostienen el producto con naturalidad — gesto pedagógico, no rígido.
- **Energía**: cálida, contenida, profesional pero cercana. Argentine teacher / psicopedagogist vibe — no influencer.

## 5. Prompt base — descripción exhaustiva del avatar (EN)

Bloque copy-paste listo para incrustar en cualquier prompt con Mercedes. **Siempre usar `mercedes-base.webp` como `--image`** además de este bloque.

```
The same woman as in the reference image (Mercedes): an Argentine
psychopedagogist in her mid-30s, warm medium-brown wavy long hair with
subtle natural sun-lit highlights (NOT dark, NOT black, NOT blonde — soft
caramel brown), fair warm Argentine skin tone, oval soft features,
expressive natural eyebrows, brown eyes, calm warm professional presence.
She wears a simple everyday outfit — light cotton blouse OR plain soft
grey t-shirt (no loud prints, no logos, no accessories). She carries a
warm closed-mouth gentle smile (NOT articulating words, NOT speaking,
mouth closed and soft) and looks at the object she is using / presenting,
NOT at the camera (unless the scene explicitly calls for camera contact).
Posture is open, hands move naturally to accompany teaching gestures.
Documentary smartphone candid feel, never a posed catalog look.
```

## 6. Identidad consistente entre escenas

Cuando hay múltiples escenas con Mercedes en el mismo video (típico: E2-i, E3-ii, E4, etc.), **TODAS** deben verse como la misma persona. Reglas:

- Siempre pasar `mercedes-base.webp` como primer `--image`.
- Mantener el mismo color/largo de pelo entre escenas (no variar entre v1 y v2 del lote).
- Ropa puede cambiar entre escenas, pero dentro del rango §3.
- Si una escena sale con identidad muy diferente al resto → regenerar esa antes de pasar a Paso 4. La inconsistencia se NOTA mucho cuando se ven las escenas seguidas en el video final.

## 7. Refs canónicas

| Slug | Path local | Uso |
|---|---|---|
| `mercedes-base` | `productos/_shared/avatars/mercedes/mercedes-base.webp` | Ref de identidad obligatoria en TODAS las escenas con Mercedes (siempre como primer `--image`) |

> Si en algún video Mercedes sale con look diferente que sea aprobado por el usuario, **subirlo acá** con un sufijo descriptivo (ej. `mercedes-aula-luz-suave.png`) y referenciarlo en la tabla — así sirve como ref futura.

---

## Notas para nuevos avatares

Cuando aparezca un avatar nuevo (otro psicopedagogo/a, niño/a recurrente,
docente diferente), copiar este archivo como plantilla bajo
`productos/_shared/avatars/<slug>/Avatar-rules-<slug>.md` y completar los 7
bloques. **La regla #1 es siempre la misma: describir el avatar leyendo la
ref base, NO desde memoria del modelo o asumiendo de un nombre.**
