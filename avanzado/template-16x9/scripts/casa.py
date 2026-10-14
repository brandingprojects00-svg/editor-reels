#!/usr/bin/env python3
"""La carpeta de trabajo del usuario («la casa»): ahí se guarda TODO lo de la skill.

  python <skill>/template/scripts/casa.py                 # dice cuál es y si existe
  python <skill>/template/scripts/casa.py "C:/Reels"      # la fija (y crea su estructura)

Debe ser la carpeta que el usuario abrió en Claude Code / Codex (a la que dio acceso):
así marca, proyectos y vídeos finales quedan donde él los ve y el agente puede escribir
sin pedir permisos fuera. La ruta se guarda en ~/.editor-reels-home para las próximas
sesiones. Evita carpetas de OneDrive/iCloud y rutas largas (Windows).
"""
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from perfil import CASA, PUNTERO  # noqa: E402

SUB = ["marca/fuentes", "marca/logos", "marca/sfx", "marca/musica", "marca/referencias", "proyectos"]


def main():
    if len(sys.argv) > 1:
        casa = pathlib.Path(sys.argv[1]).expanduser().resolve()
        for s in SUB:
            (casa / s).mkdir(parents=True, exist_ok=True)
        PUNTERO.write_text(str(casa).replace("\\", "/"), encoding="utf-8")
        avisos = []
        if "onedrive" in str(casa).lower() or "icloud" in str(casa).lower():
            avisos.append("está dentro de OneDrive/iCloud: la sincronización puede volverlo muy lento")
        if len(str(casa)) > 60:
            avisos.append("la ruta es larga: en Windows conviene algo corto como C:/Reels")
        print(f"casa fijada: {casa}")
        for a in avisos:
            print(f"  aviso: {a}")
    else:
        print(f"casa: {CASA}  ({'existe' if CASA.exists() else 'NO existe todavía'})")
        print(f"perfil: {'sí' if (CASA / 'marca' / 'perfil.json').exists() else 'no (falta la entrevista)'}")


if __name__ == "__main__":
    main()
