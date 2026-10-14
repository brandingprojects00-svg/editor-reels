#!/usr/bin/env python3
"""Analiza vídeos de referencia (los que le gustan al usuario) para proponer un estilo.

  python scripts/analiza_referencia.py ~/editor-reels/marca/referencias/*.mp4
  python scripts/analiza_referencia.py ref.mp4 --fotos 16

Por cada vídeo saca, en <casa>/marca/referencias/analisis/<nombre>/:
  - fNN.jpg       fotogramas repartidos por todo el vídeo (el agente los MIRA: ahí se ve
                  cómo son los subtítulos, el hook, si hay B-roll, zooms, emojis, cajas…)
  - corte_NN.jpg  el fotograma justo después de cada uno de los primeros cortes de plano
  - resumen.json  medidas: duración, cortes por minuto, plano medio, colores con más
                  presencia (los saturados suelen ser los del resalte o la marca)

Las medidas no deciden: dan contexto. La propuesta de estilo la hace el agente mirando
los fotogramas y se la enseña al usuario para que confirme.

Usa el ffmpeg del sistema o el que trae Remotion (vale el recortado). Sin dependencias.
"""
import argparse, colorsys, json, pathlib, subprocess, sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ff  # noqa: E402
from perfil import MARCA  # noqa: E402

SW, SH = 54, 96      # fotograma diminuto para medir cortes y color
MUESTRA_FPS = 6


def cortes(src):
    """Instantes con un salto grande de luminancia entre fotogramas seguidos (cambio de plano)."""
    p = subprocess.run([ff.binario("ffmpeg"), "-v", "error", "-i", str(src), "-vf", f"scale={SW}:{SH}",
                        "-r", str(MUESTRA_FPS), "-f", "image2pipe", "-c:v", "rawvideo", "-pix_fmt", "gray", "-"],
                       capture_output=True)
    data, n = p.stdout, SW * SH
    frames = [data[i:i + n] for i in range(0, len(data) - n + 1, n)]
    difs = [sum(abs(a - b) for a, b in zip(frames[i - 1], f)) / n for i, f in enumerate(frames) if i]
    if not difs:
        return [], 0
    base = sorted(difs)[len(difs) // 2]
    umbral = max(18.0, base * 4)
    out, ultimo = [], -1.0
    for i, d in enumerate(difs, start=1):
        t = i / MUESTRA_FPS
        if d > umbral and t - ultimo > 0.4:
            out.append(round(t, 2)); ultimo = t
    return out, len(frames) / MUESTRA_FPS


def colores(src):
    """Colores dominantes, separando los saturados (acento) de los neutros."""
    p = subprocess.run([ff.binario("ffmpeg"), "-v", "error", "-i", str(src), "-vf", f"scale={SW}:{SH}",
                        "-r", "1", "-f", "image2pipe", "-c:v", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    d = p.stdout
    sat, neu = Counter(), Counter()
    for i in range(0, len(d) - 2, 3):
        r, g, b = d[i], d[i + 1], d[i + 2]
        q = (r // 24 * 24, g // 24 * 24, b // 24 * 24)
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        piel = 0.0 <= h < 0.14 and s < 0.75 and l > 0.3     # tonos de piel: ni marca ni acento
        (sat if s > 0.45 and 0.25 < l < 0.85 and not piel else neu)[q] += 1
    tot = max(1, sum(sat.values()) + sum(neu.values()))
    hexa = lambda c: "#%02X%02X%02X" % c
    return ({"saturados": [{"hex": hexa(c), "pct": round(100 * k / tot, 2)} for c, k in sat.most_common(6)],
             "neutros": [{"hex": hexa(c), "pct": round(100 * k / tot, 1)} for c, k in neu.most_common(4)]})


def foto(src, t, dst):
    ff.run(["-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(src), "-frames:v", "1",
            "-vf", "scale=540:-2", "-q:v", "3", str(dst)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("videos", nargs="+")
    ap.add_argument("--fotos", type=int, default=12)
    ap.add_argument("--salida", default=str(MARCA / "referencias" / "analisis"))
    a = ap.parse_args()
    for v in a.videos:
        src = pathlib.Path(v)
        info = ff.sonda(src)
        dur = info["dur"]
        dst = pathlib.Path(a.salida) / src.stem
        dst.mkdir(parents=True, exist_ok=True)
        cs, _ = cortes(src)
        for i in range(a.fotos):
            foto(src, dur * (i + 0.5) / a.fotos, dst / f"f{i:02d}.jpg")
        for i, t in enumerate(cs[:8]):
            foto(src, min(dur - 0.05, t + 0.15), dst / f"corte_{i:02d}.jpg")
        planos = [b - a_ for a_, b in zip([0] + cs, cs + [dur])]
        res = {
            "video": src.name, "ancho": info.get("w"), "alto": info.get("h"), "fps": info.get("fps"),
            "duracion_s": round(dur, 1),
            "vertical": bool(info.get("h") and info["h"] > info["w"]),
            "cortes": len(cs), "cortes_por_minuto": round(len(cs) / max(dur, 1) * 60, 1),
            "plano_medio_s": round(sum(planos) / len(planos), 2) if planos else dur,
            "primeros_cortes_s": cs[:20],
            "colores": colores(src),
            "fotogramas": str(dst),
            "_lectura": "más de 25 cortes/min = ritmo frenético · 10-25 = dinámico · menos de 10 = tranquilo. "
                        "Los zooms (punch-ins) no cuentan como corte: búscalos en los fotogramas.",
        }
        (dst / "resumen.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n== {src.name}  {res['ancho']}x{res['alto']} · {res['duracion_s']}s")
        print(f"   {res['cortes']} cortes ({res['cortes_por_minuto']}/min) · plano medio {res['plano_medio_s']}s")
        print(f"   colores saturados: {', '.join(c['hex'] for c in res['colores']['saturados'][:4]) or '—'}")
        print(f"   fotogramas → {dst}   (míralos antes de proponer el estilo)")


if __name__ == "__main__":
    main()
