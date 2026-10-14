#!/usr/bin/env python3
"""Fotogramas de control de un render para MIRARLOS antes de entregar.

  python scripts/qa.py out/MiCorte.mp4                    # uno cada 3 s → qa/MiCorte/ritmo_NN.jpg
  python scripts/qa.py out/MiCorte.mp4 --cada 1.5
  python scripts/qa.py out/MiCorte.mp4 --desde 20.9 --fps 15 --n 6   # una animación, paso a paso

Con el ffmpeg del sistema además junta todo en una hoja (qa/MiCorte/hoja.jpg); con el de
Remotion deja los fotogramas sueltos (sirven igual: se miran uno a uno).

Qué buscar en la hoja de ritmo: si casi todos los fotogramas son el mismo plano con la misma
caja abajo, faltan eventos visuales (B-roll, un diagrama, un punch-in). En la tira de una
animación: que entre y salga limpia, sin parpadeos ni texto cortado.
"""
import argparse, pathlib, shutil, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ff  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--cada", type=float, default=3.0)
    ap.add_argument("--desde", type=float)
    ap.add_argument("--fps", type=float, default=15)
    ap.add_argument("--n", type=int, default=6)
    a = ap.parse_args()
    v = pathlib.Path(a.video)
    dur = ff.duracion(v)
    dst = RAIZ / "qa" / v.stem
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    if a.desde is not None:
        tiempos, nombre = [a.desde + i / a.fps for i in range(a.n)], "tira"
    else:
        n = max(1, int(dur / a.cada))
        tiempos, nombre = [a.cada * (i + 0.5) for i in range(n) if a.cada * (i + 0.5) < dur], "ritmo"
    for i, t in enumerate(tiempos):
        ff.run(["-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(v), "-frames:v", "1",
                "-vf", "scale=360:-2", "-q:v", "3", str(dst / f"{nombre}_{i:02d}.jpg")], check=True)
    print(f"{len(tiempos)} fotogramas → {dst}")
    if ff.hay_completo():
        cols = 6 if nombre == "ritmo" else len(tiempos)
        filas = -(-len(tiempos) // cols)
        r = ff.run(["-v", "error", "-y", "-i", str(dst / f"{nombre}_%02d.jpg"), "-vf",
                    f"scale=200:-2,tile={cols}x{filas}:padding=4", "-frames:v", "1", str(dst / "hoja.jpg")],
                   completo=True)
        if r.returncode == 0:
            print(f"hoja → {dst / 'hoja.jpg'}")


if __name__ == "__main__":
    main()
