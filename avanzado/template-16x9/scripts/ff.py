"""Dónde está ffmpeg/ffprobe.

Orden: el del sistema (PATH) → el que trae Remotion en node_modules/@remotion/compositor-*.
El de Remotion es una versión RECORTADA: corta, une, escala, codifica h264/aac y tiene
loudnorm y silencedetect, pero NO tiene acompressor, alimiter, highpass, tile ni select.
Por eso `completo=True` exige el del sistema y, si no está, dice cómo instalarlo.
"""
import pathlib, platform, shutil, subprocess, sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
EXE = ".exe" if platform.system() == "Windows" else ""

INSTALAR = {
    "Windows": "winget install Gyan.FFmpeg   (y abre una terminal nueva)",
    "Darwin": "brew install ffmpeg",
    "Linux": "sudo apt install ffmpeg   (o el gestor de tu distribución)",
}


def _remotion(nombre):
    for d in sorted((RAIZ / "node_modules" / "@remotion").glob("compositor-*")):
        p = d / f"{nombre}{EXE}"
        if p.exists():
            return str(p)
    return None


def binario(nombre="ffmpeg", completo=False):
    """Ruta a ffmpeg o ffprobe. Con completo=True solo vale el del sistema."""
    p = shutil.which(nombre)
    if p:
        return p
    if not completo:
        p = _remotion(nombre)
        if p:
            return p
    sys.exit(f"No encuentro {nombre}{' (versión completa)' if completo else ''}. Instálalo: "
             f"{INSTALAR.get(platform.system(), 'https://ffmpeg.org/download.html')}")


def hay_completo():
    return shutil.which("ffmpeg") is not None


def run(args, nombre="ffmpeg", completo=False, check=False):
    r = subprocess.run([binario(nombre, completo), *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        sys.exit(f"{nombre} falló:\n{r.stderr[-1500:]}")
    return r


def duracion(archivo):
    r = run(["-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(archivo)],
            nombre="ffprobe", check=True)
    return float(r.stdout.strip())


def sonda(archivo):
    """ancho, alto, fps, duración, rotación y si tiene audio."""
    import json
    r = run(["-v", "error", "-show_streams", "-show_format", "-of", "json", str(archivo)],
            nombre="ffprobe", check=True)
    d = json.loads(r.stdout)
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), None)
    a = any(s["codec_type"] == "audio" for s in d["streams"])
    if not v:
        return {"video": False, "audio": a, "dur": float(d["format"].get("duration", 0))}
    rot = 0
    for sd in v.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = int(sd["rotation"])
    rot = int(v.get("tags", {}).get("rotate", rot))
    w, h = v["width"], v["height"]
    if abs(rot) in (90, 270):
        w, h = h, w
    num, den = (v.get("avg_frame_rate") or "30/1").split("/")
    fps = float(num) / float(den or 1) if float(den or 1) else 30.0
    return {"video": True, "audio": a, "w": w, "h": h, "fps": round(fps, 3), "rot": rot,
            "dur": float(d["format"].get("duration", 0))}


if __name__ == "__main__":
    print("ffmpeg :", binario("ffmpeg"))
    print("ffprobe:", binario("ffprobe"))
    print("completo:", "sí" if hay_completo() else "no (el de Remotion; instala el del sistema para exportar con compresor)")
