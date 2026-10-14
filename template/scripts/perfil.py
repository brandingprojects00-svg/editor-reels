"""Lee el perfil del creador (lo escribe la entrevista de la skill).

Orden: $REEL_PERFIL → ./perfil.json del proyecto → <casa>/marca/perfil.json.
La casa es $EDITOR_REELS_HOME o, si no está, ~/editor-reels.
Sin perfil todo funciona con valores neutros.
"""
import json, os, pathlib, sys

# consola de Windows: que los acentos y las flechas no revienten un print
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CASA = pathlib.Path(os.path.expanduser(os.environ.get("EDITOR_REELS_HOME", "~/editor-reels")))
MARCA = CASA / "marca"


def carga():
    for p in (os.environ.get("REEL_PERFIL"),
              pathlib.Path(__file__).resolve().parent.parent / "perfil.json",
              MARCA / "perfil.json"):
        if p and pathlib.Path(p).exists():
            return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
    return {}


def ruta(clave, defecto):
    """Ruta de la biblioteca de audio: perfil.audio.<clave> o el valor por defecto."""
    v = carga().get("audio", {}).get(clave) or defecto
    return pathlib.Path(os.path.expanduser(str(v)))


BIBLIOTECA = ruta("biblioteca", str(MARCA))
KIT = ruta("sfx", str(BIBLIOTECA / "sfx"))           # kit de efectos compartido entre piezas
MUSICA = ruta("musica", str(BIBLIOTECA / "musica"))  # tus pistas de música (CC0 o con licencia)
