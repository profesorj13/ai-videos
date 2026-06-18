# Voice-board — Tijera adaptada (safety-loop-scissors v3)

> Producto: [`Product-rules-safety-loop-scissors.md`](Product-rules-safety-loop-scissors.md) (vigente al 2026-05-29)
> Voz: **AlizIA Malena Clone v1** `dlkqIuF0zNKHDiz5ajTG` (IVC clonada de Mercedes)
> Settings (FIJOS, no varían entre escenas): `stability=0.90`, `similarity_boost=0.75`, `style=0.15`, `use_speaker_boost=True`
> Modelo: `eleven_multilingual_v2` · language: `es`
> Post: padding final 0.5 s (`ffmpeg apad=pad_dur=0.5`)
> Guión pegado: 2026-05-28 por usuario (v3 — embebido en `storyboard.md`)
> Video ID en Sheet: `7` (slug `safety-loop-scissors-v3`)

---

## Fuente — guión v3 (referencia)

Pegado en [`storyboard.md` §"Fuente — guión"](storyboard.md). Acá solo las
frases de VO/avatar mapeadas a tracks de audio.

Total **7 audios** (E5 cierre brand no tiene VO — el título "Tijera adaptada / Encontrala en tu valija" se overlayea en post como overlay Pillow).

---

## Reglas de normalización aplicadas

Antes de pasar al modelo, ajustes hechos sobre el texto original:

1. **Cerrar cada frase con punto** — todas ✓
2. **Sin SSML / sin `<break>`** — ✓
3. **Seseo rioplatense** aplicado sobre palabras potencialmente problemáticas:

   | Original | Forzado | Aplica en |
   |---|---|---|
   | `presentar dificultades` | `presentar difisíon` (NO — suena raro). Pruebo SIN reemplazo primero. | E4 |
   | `precisa` | `presisa` (si aparece — chequeé y no aparece). | — |
   | `dificultades` | dejarlo (`dificultades` se pronuncia bien con esta voz IVC; ver hallazgos Mercedes-v1). | E4 |
   | `confianza` | no aparece | — |
   | `motricidad` | no aparece como problema en piloto. Dejar. | E4 |

   *(La voz IVC AlizIA Malena Clone v1 tiene seseo argentino natural en la mayoría de las palabras — el seseo forzado solo se aplica cuando la voz vuelve al ceceo peninsular en una palabra específica. Si en QA aparece un problema, agrego acá y a la skill.)*

4. **Acentos forzados** — no se aplica acá (no hay palabras técnicas como `bucle/buclé` ya que el guión v3 no usa esa palabra en VO; usa "mango continuo").

---

## vo-e1 — El problema (VO en off, inicio)

- **Frase normalizada**:
  > Hay alumnos y alumnas que tienen dificultades para usar este tipo de tijera. A veces cuesta entender qué está pasando realmente. Pero podríamos estar frente a una dificultad motriz que podemos acompañar.
- **Notas**: 3 oraciones, tono pedagógico observacional. Sin pausas largas marcadas (sin SSML).
- **Output esperado**: `audio/workspace/vo-e1-v1.mp3` (raw) → `audio/vo-e1-v1.mp3` (con apad).

---

## vo-e2-i — Mercedes presenta el material

- **Frase normalizada**:
  > Esta es la tijera adaptada.
- **Notas**: frase corta, tono presentador cálido.
- **Output esperado**: `audio/vo-e2i-v1.mp3`.

---

## vo-e2-ii — Explicación del mecanismo

- **Frase normalizada**:
  > Está diseñada para que el movimiento de corte sea mucho más simple. En lugar de tener dos aros separados, tiene un mango continuo que solo necesita presión para abrir y cerrar.
- **Notas**: descriptiva técnica. La palabra clave es "mango continuo" — chequear pronunciación natural en QA. Si suena raro, probar "mango continuo en forma de gota".
- **Output esperado**: `audio/vo-e2ii-v1.mp3`.

---

## vo-e3-i — Beneficio motriz (VO en off)

- **Frase normalizada**:
  > No requiere coordinar los dedos ni ejercer fuerza para cortar.
- **Notas**: una oración. La palabra "coordinar" puede sonar dura — chequear en QA.
- **Output esperado**: `audio/vo-e3i-v1.mp3`.

---

## vo-e3-ii — Mercedes confirma el beneficio

- **Frase normalizada**:
  > Con esta tijera, el movimiento de corte es más accesible para quien la usa.
- **Notas**: tono Mercedes cercano y afirmativo.
- **Output esperado**: `audio/vo-e3ii-v1.mp3`.

---

## vo-e3-iii — Inclusión grupal (VO en off)

- **Frase normalizada**:
  > Así, logramos que el alumno o la alumna pueda participar de la actividad junto al resto del grupo.
- **Notas**: tono comunitario / inclusivo. La coma después de "Así" marca pausa natural.
- **Output esperado**: `audio/vo-e3iii-v1.mp3`.

---

## vo-e4 — El resultado (Mercedes + cierre conceptual)

- **Frase normalizada**:
  > Es un accesorio pensado para alumnos y alumnas que pueden presentar dificultades en la motricidad fina, en la fuerza de agarre o en la coordinación de ambas manos.
- **Notas**: oración larga con enumeración (3 ítems separados por comas / "o"). v1 decía "una herramienta" pero ElevenLabs lo pronunciaba elidiendo la "h" + vocales y se escuchaba como "una arma" — cambio a "un accesorio" (validado por usuario 2026-06-17).
- **Output esperado**: `audio/vo-e4-v2.mp3`.

---

## Plan de generación

- Generar las 7 voces **en paralelo** (background) — son ~1k chars total, ~$0.30 USD.
- Una vez generadas, aplicar `apad=pad_dur=0.5` a cada una.
- Tracking inmediato en Sheet `generations` (`tipo=audio`, `modelo=elevenlabs/eleven_multilingual_v2`).
- QA por audio (uno por uno) tras subir a Drive `audio-preview/`.

---

## Aprendizajes (se llenan al cierre del lote)

*(reservado — al cierre del Paso 5, mover acá lo generalizable a la skill vs lo específico de este producto que va al Product Rules. Cosas posibles a anotar: pronunciaciones que el modelo no clavó, tonos que tuvimos que ajustar, palabras que tuvimos que reescribir.)*
