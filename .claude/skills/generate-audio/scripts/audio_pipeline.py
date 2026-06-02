#!/usr/bin/env python3
"""
audio_pipeline.py — pipeline canónico de generación de audios para videos AlizIA.

Pipeline (por cada track del voice-board):
1. Texto enviado a ElevenLabs = <frase normalizada> + " Listo."
2. Generar con voz canónica AlizIA Malena Clone v1 + settings canónicos
3. Cortar "Listo." con atrim=0:total-0.7s + apad 0.5s
4. Trackear inmediato al Sheet generations (tipo=audio)

Idempotente: salta si el output ya existe. Para forzar regen, usar --regen <slug>.

Uso:
    python3 audio_pipeline.py \\
        --slug "<producto-slug>" \\
        --video-id <id_int> \\
        --voice-board "productos/<slug>/voice-board.md"

Convenciones:
- Voz: AlizIA Malena Clone v1 dlkqIuF0zNKHDiz5ajTG (IVC, ~2 min de audio fuente)
- Settings canónicos v2 (2026-05): stab=0.70, sim=0.75, style=0.50, speaker_boost=true
- Cut fallback fijo: total - 0.7s (NO usar silencedetect; ver SKILL.md anti-patterns)
- Apad final: 0.5s
- Sheet: 1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE, tab `generations` col A:K

Requiere:
- ELEVENLABS_API_KEY en el entorno
- ffmpeg + ffprobe en PATH
- python3 con `elevenlabs` SDK instalado
- gws CLI autenticado (para tracking en Sheet)
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

# ============================================================================
# Constants
# ============================================================================
VOICE_ID = "dlkqIuF0zNKHDiz5ajTG"  # AlizIA Malena Clone v1
SETTINGS = {
    "stability": 0.70,
    "similarity_boost": 0.75,
    "style": 0.50,
    "use_speaker_boost": True,
}
MODEL_ID = "eleven_multilingual_v2"
LANGUAGE = "es"
OUTPUT_FORMAT = "mp3_44100_128"
FILLER = " Listo."  # se agrega al final de cada frase
CUT_OFFSET_DEFAULT = 0.7  # cortar last 0.7s (donde está el "Listo." en contexto)
APAD = 0.5  # padding final del audio en segundos
SHEET_ID = "1AZ2Hl3aUCFJDodKYp33DP7cA7KMgIWYrZPDSdWZ9OBE"


# ============================================================================
# Voice-board parser
# ============================================================================
def parse_voice_board(path: Path) -> list[dict]:
    """
    Extrae los tracks del voice-board.md.

    Espera bloques tipo:
        ## vo-<escena>
        - **Frase normalizada**:
          > <texto>
        - **Output esperado**: `audio/<slug>-v1.mp3` (opcional)

    Retorna: [{"slug": "vo-e1", "text": "...", "notes": "..."}]
    """
    content = path.read_text(encoding="utf-8")
    tracks = []
    # Match bloques desde ## vo-<algo> hasta el siguiente ## o --- (el header puede tener
    # texto extra después del slug, ej: "## vo-e1 — El problema (VO en off)").
    pattern = re.compile(
        r"^## (vo-[\w-]+)[^\n]*\n(.*?)(?=^## |^---\s*$|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    for m in pattern.finditer(content):
        slug = m.group(1).strip()
        body = m.group(2)
        # Extraer frase normalizada (línea citada después de "Frase normalizada")
        frase_match = re.search(
            r"\*\*Frase normalizada\*\*:\s*\n\s*>\s*(.+?)(?:\n\s*-|\n\s*\n|$)",
            body,
            re.DOTALL,
        )
        if not frase_match:
            print(f"  WARN: {slug} no tiene 'Frase normalizada' parseable, skip")
            continue
        text = frase_match.group(1).strip()
        # Limpiar saltos de línea internos
        text = re.sub(r"\s*\n\s*", " ", text)
        tracks.append({"slug": slug, "text": text})
    return tracks


# ============================================================================
# ElevenLabs generation
# ============================================================================
def generate_audio(text: str, out_path: Path) -> None:
    """Llama a ElevenLabs y guarda el MP3 en out_path."""
    from elevenlabs.client import ElevenLabs

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY no está en el entorno")

    client = ElevenLabs(api_key=api_key)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    audio = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        text=text,
        model_id=MODEL_ID,
        language_code=LANGUAGE,
        voice_settings=SETTINGS,
        output_format=OUTPUT_FORMAT,
    )
    with open(out_path, "wb") as f:
        for chunk in audio:
            if chunk:
                f.write(chunk)


# ============================================================================
# FFmpeg post-processing
# ============================================================================
def get_duration(audio_path: Path) -> float:
    """Duración en segundos."""
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(audio_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


def cut_and_pad(raw_path: Path, out_path: Path, cut_offset: float = CUT_OFFSET_DEFAULT) -> dict:
    """
    Corta el filler "Listo." y aplica apad.

    Usa atrim+apad en filter_complex (NUNCA -t {cut} -af apad — trunca el padding).
    """
    total = get_duration(raw_path)
    cut_at = total - cut_offset
    if cut_at <= 0:
        raise ValueError(f"cut_at={cut_at} <= 0; audio demasiado corto ({total}s) para cortar {cut_offset}s")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(raw_path),
            "-af", f"atrim=0:{cut_at},apad=pad_dur={APAD}",
            "-c:a", "libmp3lame", "-b:a", "192k",
            str(out_path),
        ],
        capture_output=True,
        check=True,
    )
    final = get_duration(out_path)
    return {
        "raw_duration": total,
        "cut_at": cut_at,
        "final_duration": final,
        "cut_offset": cut_offset,
    }


# ============================================================================
# Sheet tracking
# ============================================================================
"""
Tracking strategy:

El Python de Microsoft Store en Windows corre en sandbox que NO puede invocar
`gws` (.cmd npm wrapper) — ni directo, ni via bash, ni con el path canónico.

Solución: el script NO trackea al Sheet directamente. En su lugar, emite un
shell script (`track-batch-v<N>.sh`) que el usuario corre en bash para hacer el
append. Es portable y funciona en cualquier plataforma con gws accesible.
"""


def build_tracking_row(
    video_id: int,
    slug: str,
    text_with_filler: str,
    asset_local: str,
    cut_info: dict,
) -> list[str]:
    """Construye una row para `generations` (sin id — se asigna al emitir el shell)."""
    prompt_summary = (
        f"{text_with_filler} "
        f"[stab={SETTINGS['stability']} sim={SETTINGS['similarity_boost']} "
        f"style={SETTINGS['style']} apad={APAD}s cut=total-{cut_info['cut_offset']}s]"
    )
    return [
        "<id>",  # placeholder — se reemplaza al emitir el shell
        str(video_id),
        slug,
        "audio",
        f"elevenlabs/{MODEL_ID}",
        prompt_summary,
        "completed",
        "local",
        "",
        asset_local,
        date.today().isoformat(),
    ]


def emit_tracking_shell(rows: list[list[str]], out_path: Path, video_id: int) -> None:
    """
    Emite un shell script + un JSON auxiliar.

    - `track-batch-v<N>.sh`: orquesta el append (lee próximo id, reemplaza placeholders, llama gws)
    - `track-batch-v<N>.json`: payload con rows y `<id_N>` placeholders consecutivos
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    json_path = out_path.with_suffix(".json")

    # Reemplazar el placeholder "<id>" con "<id_0>", "<id_1>", etc.
    rows_with_indexed_placeholders = []
    for i, row in enumerate(rows):
        new_row = list(row)
        new_row[0] = f"<id_{i}>"
        rows_with_indexed_placeholders.append(new_row)

    payload = {"values": rows_with_indexed_placeholders}
    # Normalizar paths (Windows usa \, JSON debería tener / para portabilidad)
    payload_text = json.dumps(payload, ensure_ascii=False)
    payload_text = payload_text.replace("\\\\", "/").replace("\\", "/")
    json_path.write_text(payload_text, encoding="utf-8")

    params = {
        "spreadsheetId": SHEET_ID,
        "range": "generations!A:K",
        "valueInputOption": "USER_ENTERED",
    }
    params_json = json.dumps(params)
    n = len(rows)

    shell = f"""#!/bin/bash
# Auto-generated by audio_pipeline.py — appends {n} row(s) to generations tab.
# Usage: bash {out_path.name}
set -euo pipefail

cd "$(dirname "$0")"
SHEET="{SHEET_ID}"
PAYLOAD_TEMPLATE="$(cat {json_path.name})"

# Read next id from generations col A
NEXT_ID=$(gws sheets +read --spreadsheet "$SHEET" --range 'generations!A:A' 2>&1 \\
  | sed '/^Using keyring backend/d' \\
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(max(int(r[0]) for r in d['values'][1:] if r and r[0].isdigit())+1)")

echo "Next id: $NEXT_ID (asignando a {n} row(s))"

# Replace placeholders <id_0>, <id_1>... with consecutive ids
PAYLOAD="$PAYLOAD_TEMPLATE"
for i in $(seq 0 $(({n} - 1))); do
  ID=$((NEXT_ID + i))
  PAYLOAD=$(echo "$PAYLOAD" | sed "s/<id_$i>/$ID/")
done

# Append
gws sheets spreadsheets values append \\
  --params '{params_json}' \\
  --json "$PAYLOAD" 2>&1 | tail -6

echo ""
echo "OK: {n} row(s) appendeadas al Sheet (video_id={video_id})."
"""
    out_path.write_text(shell, encoding="utf-8")


# ============================================================================
# Main pipeline
# ============================================================================
def process_track(
    track: dict,
    slug: str,
    video_id: int,
    version: int = 1,
    cut_offset: float = CUT_OFFSET_DEFAULT,
    force: bool = False,
) -> dict:
    """Procesa un track del voice-board: generar + cortar. NO trackea (eso va al shell)."""
    workspace = Path(f"productos/{slug}/audio/workspace")
    final_dir = Path(f"productos/{slug}/audio")
    raw_path = workspace / f"{track['slug']}-v{version}-raw.mp3"
    out_path = final_dir / f"{track['slug']}-v{version}.mp3"

    if out_path.exists() and not force:
        print(f"  {track['slug']} v{version}: ya existe, skip (usar --regen para forzar)")
        return {"skipped": True, "path": str(out_path)}

    # Texto + filler
    text_with_filler = track["text"].rstrip(".") + "." + FILLER

    # Generar
    print(f"  {track['slug']} v{version}: generando...")
    generate_audio(text_with_filler, raw_path)

    # Cortar + apad
    info = cut_and_pad(raw_path, out_path, cut_offset=cut_offset)
    print(
        f"    raw={info['raw_duration']:.2f}s, "
        f"cut@{info['cut_at']:.2f}s (-{cut_offset}s), "
        f"final={info['final_duration']:.2f}s"
    )

    return {
        "skipped": False,
        "slug": track['slug'],
        "version": version,
        "path": str(out_path),
        "duration": info['final_duration'],
        "text_with_filler": text_with_filler,
        "cut_info": info,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--slug", required=True, help="producto slug (ej: safety-loop-scissors)")
    parser.add_argument("--video-id", required=True, type=int, help="id del video en el Sheet videos!A")
    parser.add_argument("--voice-board", required=True, help="path al voice-board.md")
    parser.add_argument("--cut-offset", type=float, default=CUT_OFFSET_DEFAULT,
                        help=f"segundos a cortar desde el final (default: {CUT_OFFSET_DEFAULT}). "
                             "Si el Listo queda audible, subir a 0.8.")
    parser.add_argument("--version", type=int, default=1, help="versión de salida (default: 1)")
    parser.add_argument("--regen", action="append", default=[],
                        help="slugs a regenerar aunque existan (puede repetirse)")
    parser.add_argument("--only", action="append", default=[],
                        help="procesar solo estos slugs (puede repetirse)")
    args = parser.parse_args()

    vb_path = Path(args.voice_board)
    if not vb_path.exists():
        print(f"ERROR: voice-board no encontrado: {vb_path}", file=sys.stderr)
        return 1

    tracks = parse_voice_board(vb_path)
    if args.only:
        tracks = [t for t in tracks if t["slug"] in args.only]
    print(f"Tracks a procesar: {len(tracks)} ({', '.join(t['slug'] for t in tracks)})")

    results = []
    tracking_rows = []
    for track in tracks:
        force = track["slug"] in args.regen
        result = process_track(
            track,
            slug=args.slug,
            video_id=args.video_id,
            version=args.version,
            cut_offset=args.cut_offset,
            force=force,
        )
        results.append(result)
        if not result.get("skipped"):
            row = build_tracking_row(
                video_id=args.video_id,
                slug=track['slug'],
                text_with_filler=result['text_with_filler'],
                asset_local=result['path'],
                cut_info=result['cut_info'],
            )
            tracking_rows.append(row)

    print(f"\nResumen:")
    for r in results:
        if r.get("skipped"):
            print(f"  ⏭  {r['path']}")
        else:
            print(f"  ✓ {r['slug']} v{r['version']} → {r['path']} ({r['duration']:.2f}s)")

    if tracking_rows:
        shell_path = Path(f"productos/{args.slug}/audio/logs/track-batch-v{args.version}.sh")
        emit_tracking_shell(tracking_rows, shell_path, args.video_id)
        print(f"\n→ Tracking shell escrito: {shell_path}")
        print(f"   Corré: bash {shell_path}")
        print(f"   (Esto appendea {len(tracking_rows)} rows al Sheet `generations`.)")
    else:
        print("\nNo hay rows nuevas para trackear (todos skipped).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
