#!/usr/bin/env python3
"""Render de composiciones a out/ (equivalente a render.sh, para Windows y cualquier SO).

  python scripts/render.py                 # todas las que declare cuts.ts
  python scripts/render.py Corte1 Corte2   # solo esas
  HQ=1 python scripts/render.py Corte1     # PNG + crf 10, para fuentes ya comprimidas

Typecheck primero y con la salida ENTERA: el render de Remotion no avisa de errores de tipos.
bt709 explícito: sin esto Instagram reinterpreta el color y lava la imagen.
"""
import os, pathlib, re, shutil, subprocess, sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
NPX = shutil.which("npx") or shutil.which("npx.cmd") or "npx"


def run(args, **kw):
    return subprocess.run([NPX, *args], cwd=RAIZ, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", **kw)


def composiciones():
    out = run(["remotion", "compositions", "src/index.ts"]).stdout
    out = re.sub(r"\x1b\[[0-9;]*m", "", out)
    ids = []
    for linea in out.splitlines():
        c = linea.split()
        if len(c) >= 3 and c[1].isdigit() and re.fullmatch(r"\d+x\d+", c[2]):
            ids.append(c[0])
    return ids


def main():
    cuts = sys.argv[1:] or composiciones()
    if not cuts:
        sys.exit("no se encontraron composiciones")
    (RAIZ / "out").mkdir(exist_ok=True)

    tsc = run(["tsc", "--noEmit", "-p", "."])
    if tsc.returncode != 0:
        print("\n".join(l for l in (tsc.stdout + tsc.stderr).splitlines() if "npm notice" not in l))
        sys.exit("!! typecheck con errores: no se renderiza")

    hq = os.environ.get("HQ", "0") == "1"
    calidad = ["--crf", "10", "--image-format=png"] if hq else ["--crf", "18"]
    hilos = os.environ.get("CONCURRENCY", "3")
    for c in cuts:
        print(f"=== {c} ===", flush=True)
        args = ["remotion", "render", c, f"out/{c}.mp4", "--codec", "h264", *calidad,
                "--audio-bitrate", "320k", "--color-space=bt709"]
        r = run([*args, f"--concurrency={hilos}"])
        log = r.stdout + r.stderr
        # En algunos equipos (visto en Windows) varios hilos piden fotogramas del mismo vídeo a
        # la vez y el compositor responde «No frame found at position…». Con un hilo no pasa.
        if r.returncode != 0 and "No frame found" in log and hilos != "1":
            print("  el compositor falló en paralelo: reintento con un solo hilo (más lento)", flush=True)
            r = run([*args, "--concurrency=1"])
            log = r.stdout + r.stderr
        if r.returncode != 0:
            err = [l for l in log.splitlines() if "rror" in l][:6]
            print("\n".join(err or log.splitlines()[-12:]))
            sys.exit(f"!! falló el render de {c}")
        print("\n".join(log.splitlines()[-2:]))
    print("RENDER_DONE")


if __name__ == "__main__":
    main()
