#!/usr/bin/env python3
"""Transcribe un vídeo/audio con faster-whisper (local, sin nube) al formato de whisper
que lee `words.py --convert`: segments[].words[] con word/start/end.

  python scripts/transcribe.py public/c1.mp4 work/c1.json --prompt "Notion, Canva"
  python scripts/transcribe.py input/clip2.mov work/clip2.json --modelo medium --idioma en

- Si este Python no tiene faster-whisper, se relanza solo con el del entorno que crea
  `scripts/setup_entorno.py` (<casa>/.venv). No hace falta acordarse de la ruta.
- El modelo es un NOMBRE (tiny, base, small, medium, large-v3-turbo) o una CARPETA local.
  Por nombre se busca en <casa>/models; si no está, faster-whisper lo descarga ahí la
  primera vez (pide permiso al usuario antes: son 0,5-1,6 GB).
- faster-whisper lee el audio con PyAV: NO necesita ffmpeg del sistema.
- Un fichero por llamada. Comprueba que la duración del transcript cuadre con la del audio.
"""
import argparse, json, os, pathlib, platform, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from perfil import CASA, carga  # noqa: E402

VENV_PY = CASA / ".venv" / ("Scripts/python.exe" if platform.system() == "Windows" else "bin/python")


def relanza_en_venv():
    if VENV_PY.exists() and pathlib.Path(sys.executable).resolve() != VENV_PY.resolve():
        sys.exit(subprocess.call([str(VENV_PY), *sys.argv]))
    sys.exit("faster-whisper no está instalado. Corre primero: python scripts/setup_entorno.py")


def main():
    perfil = carga()
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada"); ap.add_argument("salida")
    ap.add_argument("--modelo", default=perfil.get("transcripcion_modelo", "small"))
    ap.add_argument("--idioma", default=perfil.get("idioma", "es"))
    ap.add_argument("--prompt", default="", help="vocabulario para sesgar: marcas y términos (Claude, Notion…)")
    a = ap.parse_args()
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        relanza_en_venv()

    os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
    modelo = a.modelo   # nombre (se busca/descarga en <casa>/models) o carpeta local
    # vocabulario: marcas frecuentes del perfil + las del vídeo
    vocab = ", ".join(x for x in [a.prompt, ", ".join(perfil.get("marcas_frecuentes", []))] if x)

    m = WhisperModel(modelo, device="auto", compute_type="int8",
                     download_root=str(CASA / "models"))
    segs, info = m.transcribe(a.entrada, language=a.idioma, word_timestamps=True,
                              vad_filter=True, initial_prompt=vocab or None)
    out = {"language": info.language, "duration": round(info.duration, 3), "segments": []}
    for s in segs:
        out["segments"].append({
            "start": round(s.start, 3), "end": round(s.end, 3), "text": s.text,
            "words": [{"word": w.word, "start": round(w.start, 3), "end": round(w.end, 3)} for w in (s.words or [])],
        })
    pathlib.Path(a.salida).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.salida).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    n = sum(len(s["words"]) for s in out["segments"])
    fin = out["segments"][-1]["end"] if out["segments"] else 0
    print(f"{n} palabras · transcript hasta {fin:.1f}s de {info.duration:.1f}s de audio -> {a.salida}")


if __name__ == "__main__":
    main()
