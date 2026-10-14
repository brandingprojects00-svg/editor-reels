#!/usr/bin/env python3
"""Prepara el entorno de Python de la skill: transcripción local (faster-whisper + modelo)
y visión (OpenCV + numpy, para detectar la cara y que nada la tape).

  python scripts/setup_entorno.py                 # entorno + modelo «small» (~0,5 GB)
  python scripts/setup_entorno.py --modelo medium # más preciso, más lento (~1,5 GB)
  python scripts/setup_entorno.py --comprobar     # solo dice qué falta, no instala nada

ANTES DE CORRERLO el agente pide permiso al usuario: instala paquetes de PyPI
(faster-whisper, numpy, opencv-python-headless) en <casa>/.venv y descarga el modelo desde
Hugging Face (Systran/faster-whisper-*) a <casa>/models. Todo queda en esa carpeta:
borrarla lo desinstala.

Modelos: small va bien en cualquier portátil (≈ 4-6 min por minuto de audio en CPU).
medium acierta más nombres propios. large-v3-turbo solo si hay GPU NVIDIA.
"""
import argparse, platform, subprocess, sys, venv, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from perfil import CASA  # noqa: E402

VENV = CASA / ".venv"
PY = VENV / ("Scripts/python.exe" if platform.system() == "Windows" else "bin/python")


PAQUETES = ["faster-whisper", "numpy", "opencv-python-headless"]


def tiene_fw():
    if not PY.exists():
        return False
    return subprocess.run([str(PY), "-c", "import faster_whisper, numpy, cv2"], capture_output=True).returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelo", default="small")
    ap.add_argument("--comprobar", action="store_true")
    a = ap.parse_args()

    if sys.version_info < (3, 9):
        sys.exit("Hace falta Python 3.9 o más nuevo.")
    modelo_dir = CASA / "models" / f"models--Systran--faster-whisper-{a.modelo}"
    estado = {"entorno": PY.exists(), "faster-whisper + opencv": tiene_fw(), f"modelo {a.modelo}": modelo_dir.exists()}
    for k, v in estado.items():
        print(f"  {'OK ' if v else 'FALTA'}  {k}")
    if a.comprobar:
        sys.exit(0 if all(estado.values()) else 1)

    if not PY.exists():
        print(f"creando entorno en {VENV} …")
        VENV.parent.mkdir(parents=True, exist_ok=True)
        venv.create(VENV, with_pip=True)
    if not tiene_fw():
        print(f"instalando {', '.join(PAQUETES)} (PyPI) …")
        subprocess.run([str(PY), "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([str(PY), "-m", "pip", "install", *PAQUETES], check=True)
    if not modelo_dir.exists():
        print(f"descargando el modelo {a.modelo} a {CASA / 'models'} …")
        codigo = ("import os; os.environ['HF_HUB_DISABLE_TELEMETRY']='1';"
                  "from faster_whisper import WhisperModel;"
                  f"WhisperModel({a.modelo!r}, device='cpu', compute_type='int8', download_root={str(CASA / 'models')!r})")
        subprocess.run([str(PY), "-c", codigo], check=True)
    print("ENTORNO_LISTO")


if __name__ == "__main__":
    main()
