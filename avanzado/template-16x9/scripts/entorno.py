"""Si a este Python le faltan módulos (cv2, numpy, faster_whisper), relanza el script con
el del entorno de la skill (<casa>/.venv, lo crea scripts/setup_entorno.py).

    import entorno; entorno.necesita("cv2", "numpy")      # al principio del script

Así cualquier script se corre siempre con `python scripts/x.py`, sin acordarse de rutas.
"""
import importlib.util, pathlib, platform, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from perfil import CASA  # noqa: E402

VENV_PY = CASA / ".venv" / ("Scripts/python.exe" if platform.system() == "Windows" else "bin/python")


def necesita(*modulos):
    faltan = [m for m in modulos if importlib.util.find_spec(m) is None]
    if not faltan:
        return
    if VENV_PY.exists() and pathlib.Path(sys.executable).resolve() != VENV_PY.resolve():
        sys.exit(subprocess.call([str(VENV_PY), *sys.argv]))
    sys.exit(f"Faltan módulos de Python ({', '.join(faltan)}). Corre: python scripts/setup_entorno.py")
