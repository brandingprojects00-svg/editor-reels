#!/usr/bin/env python3
"""out/*.mp4 -> final/*.mp4 normalizado a -14 LUFS (export.sh + fixaudio.sh en uno, multiplataforma).

  python scripts/export.py
  python scripts/export.py --video copy --only MiCorte     # no recomprime la imagen
  python scripts/export.py --pre "highpass=f=80"           # micro cercano: sin compresor

POR QUÉ COMPRIME ANTES DE NORMALIZAR: el audio de sala tiene cresta de 19-22 dB. Subir 22 dB
para llegar a -14 dejaría el pico en +5..+8 dBFS y loudnorm bajaría la ganancia: el archivo
se quedaría 1-2 LU corto. Se REDUCE la cresta antes y solo después se normaliza, con las dos
pasadas medidas sobre la cadena ya comprimida. Con micro cercano (audio.micro = "cercano")
usa --pre "highpass=f=80": comprimir de más aplasta la voz.

Mejor con el ffmpeg del sistema (scripts/ff.py dice cómo instalarlo). Sin él usa el que trae
Remotion, que no tiene compresor ni limitador: entonces normaliza solo con loudnorm (lineal),
que funciona bien con micro cercano y algo peor con audio de sala.
"""
import argparse, json, os, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ff

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PRE_DEF = "highpass=f=80,acompressor=threshold=-26dB:ratio=3:attack=5:release=140:makeup=1"
LOUD = "loudnorm=I=-14:TP=-1.5:LRA=11"


COMPLETO = ff.hay_completo()


def ffmpeg(*args):
    return ff.run(["-hide_banner", "-nostats", *args])


def mide(archivo, cadena):
    """Medida de loudnorm (JSON) de la cadena de audio dada, o None."""
    r = ffmpeg("-i", str(archivo), "-vn", "-af", f"{cadena}{LOUD}:print_format=json", "-c:a", "pcm_s16le", "-f", "null", "-")
    m = re.search(r"\{[^{]*input_i.*?\}", r.stderr, re.S)
    return json.loads(m.group(0)) if m else None


def lufs(archivo):
    m = mide(archivo, "")
    return float(m["input_i"]) if m else 0.0


def exporta(pre, video, only):
    (RAIZ / "final").mkdir(exist_ok=True)
    vargs = (["-c:v", "copy"] if video == "copy" else
             ["-c:v", "libx264", "-b:v", "6M", "-maxrate", "8M", "-bufsize", "12M", "-preset", "slow",
              "-pix_fmt", "yuv420p", "-x264-params", "colorprim=bt709:transfer=bt709:colormatrix=bt709"])
    fuentes = sorted((RAIZ / "out").glob("*.mp4"))
    if not fuentes:
        sys.exit("no hay nada en out/")
    for f in fuentes:
        if only and f.stem not in only:
            continue
        d = mide(f, pre + "," if pre else "")
        if not d:
            print(f"!! {f.stem} sin medida"); continue
        cadena = (f"{pre + ',' if pre else ''}{LOUD}:measured_I={d['input_i']}:measured_TP={d['input_tp']}:"
                  f"measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:linear=false,aresample=48000")
        r = ffmpeg("-v", "error", "-y", "-i", str(f), "-af", cadena, *vargs,
                   "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                   "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart",
                   str(RAIZ / "final" / f"{f.stem}.mp4"))
        if r.returncode != 0:
            sys.exit(f"!! ffmpeg falló con {f.stem}:\n{r.stderr}")
        print(f"  {f.stem}: tras comprimir I={d['input_i']} TP={d['input_tp']}")


def repaso(only):
    """Loudness a ±0.3 LU SIN recodificar el vídeo: se mide, se aplica ganancia + alimiter y se itera."""
    for f in sorted((RAIZ / "final").glob("*.mp4")):
        if only and f.stem not in only:
            continue
        for i in (1, 2, 3):
            cur = lufs(f); g = round(-14.0 - cur, 3)
            if abs(g) <= 0.3:
                print(f"  {f.stem}: {cur} LUFS OK (iter {i})"); break
            tmp = f.with_name(f.stem + "__t.mp4")
            lim = ",alimiter=level_in=1:level_out=1:level=0:limit=0.84:attack=5:release=50" if COMPLETO else ""
            r = ffmpeg("-v", "error", "-y", "-i", str(f), "-c:v", "copy", "-af", f"volume={g}dB{lim}",
                       "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", str(tmp))
            if r.returncode != 0:
                sys.exit(f"!! ffmpeg falló en el repaso de {f.stem}:\n{r.stderr}")
            os.replace(tmp, f)
            print(f"  {f.stem}: iter {i}  medido {cur} -> ganancia {g} dB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pre", default=os.environ.get("PRE", PRE_DEF))
    ap.add_argument("--video", default=os.environ.get("VIDEO", "x264"), choices=["x264", "copy"])
    ap.add_argument("--only", default=os.environ.get("ONLY", ""), help='ids separados por espacios')
    a = ap.parse_args()
    only = set(a.only.split())
    pre = a.pre
    if not COMPLETO and pre:
        print("  aviso: ffmpeg recortado (el de Remotion): sin compresor; solo loudnorm. "
              "Para la cadena completa instala ffmpeg (python scripts/ff.py)")
        pre = ""
    exporta(pre, a.video, only)
    # con audio ya limitado (CapCut) + efectos, loudnorm se queda 0.4-0.5 LU corto: se mide y se corrige
    fuera = [f.stem for f in (RAIZ / "final").glob("*.mp4")
             if (not only or f.stem in only) and abs(-14.0 - lufs(f)) > 0.3]
    if fuera:
        print(f"  fuera de ±0.3 LU: {', '.join(fuera)} -> repaso")
        repaso(only)
    print("EXPORT_DONE")


if __name__ == "__main__":
    main()
