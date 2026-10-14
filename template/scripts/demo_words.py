#!/usr/bin/env python3
"""Genera la DEMO: un guion ficticio con tiempos de palabra sintéticos.

  python scripts/demo_words.py                      # -> work/c1_words.json + work/c1_spans.json
  python scripts/demo_words.py --video              # + public/c1.mp4: fondo degradado en el color del perfil
  python scripts/demo_words.py --video --fondo clip.mp4   # + su propio clip de fondo (sin su audio)

Solo para ver la plantilla funcionando sin grabación propia (el render de demo de la
entrevista). En un reel real los tiempos salen de la transcripción.
Vale cualquier ffmpeg, también el que trae Remotion.
"""
import argparse, json, pathlib, struct, sys, zlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ff  # noqa: E402
from perfil import carga  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent

GUION = ("Hay tres tareas que ya no hago a mano, y te las enseño de la más fácil a la más rentable. "
         "Número uno: los correos. Cada mañana un agente lee la bandeja, separa lo urgente y me deja borradores. "
         "Yo solo reviso y envío. "
         "Número dos: las reuniones. La grabación se transcribe sola, sale un resumen y las tareas acaban en Notion. "
         "Número tres: el contenido. De un solo vídeo salen el guion, los subtítulos y el post. "
         "Lo que antes me llevaba una tarde ahora son diez minutos. "
         "¿Y tú qué le delegarías primero?")

def png_degradado(dst, c0, c1, w=1080, h=1920):
    """PNG vertical con degradado de c0 (arriba) a c1 (abajo), en Python puro."""
    rgb = lambda c: tuple(int(c.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    a, b = rgb(c0), rgb(c1)
    filas = bytearray()
    for y in range(h):
        k = y / (h - 1)
        px = bytes(int(a[i] + (b[i] - a[i]) * k) for i in range(3))
        filas += bytes(1) + px * w
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    png = bytes([137, 80, 78, 71, 13, 10, 26, 10]) + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(filas), 6)) + chunk(b"IEND", b"")
    pathlib.Path(dst).write_bytes(png)


def video_demo(dur, fondo=None):
    (RAIZ / "public").mkdir(exist_ok=True)
    out = RAIZ / "public" / "c1.mp4"
    if fondo:
        entrada = ["-stream_loop", "-1", "-i", str(fondo)]
        vf = "scale=1080:1920"
    else:
        col = carga().get("colores", {})
        png = RAIZ / "work" / "fondo_demo.png"
        png_degradado(png, col.get("line", "#3a4a5c"), col.get("ink", "#0B0F14"))
        entrada = ["-loop", "1", "-framerate", "30", "-i", str(png)]
        vf = "scale=1080:1920"
    ff.run(["-v", "error", "-y", *entrada, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
            "-map", "0:v", "-map", "1:a", "-t", f"{dur:.2f}", "-vf", vf, "-r", "30",
            "-c:v", "libx264", "-crf", "23", "-pix_fmt", "yuv420p", "-c:a", "aac", str(out)], check=True)
    print(f"fondo de demo -> {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", action="store_true")
    ap.add_argument("--fondo")
    a = ap.parse_args()
    t, out = 0.4, []
    for w in GUION.split():
        d = 0.16 + 0.035 * len(w)
        out.append({"text": w, "start": round(t, 2), "end": round(t + d, 2)})
        t += d + 0.04 + (0.35 if w[-1] in ".:?" else 0.12 if w[-1] == "," else 0)
    work = RAIZ / "work"
    work.mkdir(exist_ok=True)
    (work / "c1_words.json").write_text(json.dumps(out, ensure_ascii=False, indent=0), encoding="utf-8")
    dur = round(t + 1.2, 2)
    # un punch-in suave por bloque, como harías en un plano fijo real
    (work / "c1_spans.json").write_text(json.dumps([
        {"start": 0, "end": 7.45}, {"start": 7.45, "end": 17.2, "scale": 1.12},
        {"start": 17.2, "end": 25.1}, {"start": 25.1, "end": dur, "scale": 1.1}]), encoding="utf-8")
    print(f"demo: {len(out)} palabras, {dur:.1f} s")
    if a.video:
        video_demo(dur, a.fondo)
    for w in out:
        print(f"  {w['start']:6.2f} {w['text']}")

if __name__ == "__main__":
    main()
