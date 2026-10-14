#!/usr/bin/env python3
"""¿Está todo listo para editar? Revisa, NO instala nada.

  python scripts/doctor.py

Imprime una tabla OK/FALTA y, para lo que falte, el comando de instalación de tu sistema.
El agente enseña esos comandos al usuario y pide permiso antes de correr cualquiera.
"""
import os, pathlib, platform, re, shutil, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from perfil import CASA, MARCA  # noqa: E402

SO = platform.system()
INSTALA = {
    "node":   {"Windows": "winget install OpenJS.NodeJS.LTS", "Darwin": "brew install node",
               "Linux": "https://nodejs.org (o: sudo apt install nodejs npm)"},
    "ffmpeg": {"Windows": "winget install Gyan.FFmpeg", "Darwin": "brew install ffmpeg",
               "Linux": "sudo apt install ffmpeg"},
    "python": {"Windows": "winget install Python.Python.3.12", "Darwin": "brew install python@3.12",
               "Linux": "sudo apt install python3 python3-venv"},
}


def version(cmd, rx=r"(\d+)\.(\d+)"):
    exe = shutil.which(cmd)
    if not exe:
        return None
    try:
        out = subprocess.run([exe, "--version" if cmd != "ffmpeg" else "-version"],
                             capture_output=True, text=True, timeout=20).stdout
    except Exception:
        return None
    m = re.search(rx, out)
    return (int(m.group(1)), int(m.group(2))) if m else (0, 0)


def fila(ok, que, detalle="", arreglo=""):
    print(f"  {'OK   ' if ok else 'FALTA'}  {que:<26} {detalle}")
    if not ok and arreglo:
        print(f"         → {arreglo}")
    return ok


def main():
    print(f"\neditor-reels · doctor  ({SO} {platform.machine()})\n")
    esencial = True

    n = version("node", r"v(\d+)\.(\d+)")
    esencial &= fila(bool(n and n[0] >= 18), "Node.js 18+", f"v{n[0]}.{n[1]}" if n else "",
                     INSTALA["node"].get(SO, ""))
    esencial &= fila(shutil.which("npx") is not None or shutil.which("npx.cmd") is not None, "npx", "",
                     "viene con Node.js")
    py = sys.version_info
    esencial &= fila(py >= (3, 10), "Python 3.10+", f"{py.major}.{py.minor}", INSTALA["python"].get(SO, ""))

    f = version("ffmpeg", r"version (?:n)?(\d+)\.(\d+)")
    fila(bool(f), "ffmpeg (sistema)", "completo" if f else "",
         INSTALA["ffmpeg"].get(SO, "") + "   · sin él se usa el que trae Remotion (recortado: "
         "monta y exporta, pero sin compresor de voz ni efectos derivados)")

    venv_py = CASA / ".venv" / ("Scripts/python.exe" if SO == "Windows" else "bin/python")
    ok_env = venv_py.exists() and subprocess.run(
        [str(venv_py), "-c", "import faster_whisper, cv2, numpy"], capture_output=True).returncode == 0
    esencial &= fila(ok_env, "entorno (Whisper + OpenCV)", str(CASA / ".venv") if ok_env else "",
                     "python scripts/setup_entorno.py   (pide permiso: instala paquetes y baja ~0,5 GB)")
    modelos = list((CASA / "models").glob("models--Systran--faster-whisper-*"))
    fila(bool(modelos), "modelo de Whisper",
         ", ".join(m.name.split("-")[-1] for m in modelos) if modelos else "",
         "lo baja setup_entorno.py (o la primera transcripción)")

    libre = shutil.disk_usage(CASA if CASA.exists() else pathlib.Path.home()).free / 1e9
    fila(libre > 5, "espacio en disco", f"{libre:.0f} GB libres", "conviene tener 5 GB o más (node_modules + renders)")

    perfil = MARCA / "perfil.json"
    fila(perfil.exists(), "perfil de marca", str(perfil) if perfil.exists() else "",
         "aún no: la skill hace la entrevista la primera vez")

    if SO == "Windows":
        largo = len(str(CASA / "proyectos" / "nombre-largo-de-proyecto" / "node_modules" / "@remotion"))
        fila(largo < 120, "ruta corta", str(CASA), "usa una casa más corta: EDITOR_REELS_HOME=C:/reels")

    skills = [pathlib.Path.home() / ".claude" / "skills" / "remotion-best-practices",
              pathlib.Path.home() / ".agents" / "skills" / "remotion-best-practices",
              pathlib.Path.home() / ".codex" / "skills" / "remotion-best-practices"]
    if not any(s.exists() for s in skills):
        print("\n  opcional  skills oficiales de Remotion (ayudan a crear efectos nuevos):"
              "\n            npx skills add remotion-dev/skills")

    print("\nLISTO" if esencial else "\nFALTAN COSAS ESENCIALES (arriba, con su comando)")
    sys.exit(0 if esencial else 1)


if __name__ == "__main__":
    main()
