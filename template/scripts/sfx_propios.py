#!/usr/bin/env python3
"""Mete TUS efectos de sonido en el kit (los que el usuario ya usa y le gustan).

  python scripts/sfx_propios.py ~/Descargas/swoosh.mp3:whoosh_in ~/Descargas/boom.wav:impact
  python scripts/sfx_propios.py mi_risa.mp3:risa          # hueco propio: cualquier nombre vale
  python scripts/sfx_propios.py --lista                     # huecos estándar y qué hay en el kit

Cada archivo se procesa igual que el kit CC0 (sfx_fetch.py), para que las ganancias del
montaje sean comparables:
  1. fuera el silencio de cabeza (si no, el golpe llega tarde)
  2. pico a -3 dBFS
  3. WAV 48 kHz estéreo en <casa>/marca/sfx/<hueco>.wav
Si das whoosh_in y no whoosh_out, la salida se deriva invirtiendo la entrada.

Funciona con cualquier ffmpeg (también el que trae Remotion): el proceso es Python puro.
OJO con la licencia: si el efecto no es tuyo ni CC0, puede dar reclamaciones en redes.
"""
import argparse, array, json, math, pathlib, subprocess, sys, wave

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ff  # noqa: E402
from perfil import KIT  # noqa: E402

HUECOS = {
    "impact": "entra el título o el hook: golpe que dice «esto va en serio»",
    "hit": "choque seco (el «VS» de una comparación, un sello)",
    "whoosh_in": "entra una tarjeta o un B-roll",
    "whoosh_out": "sale una tarjeta (si falta, se deriva de whoosh_in)",
    "tick": "entra un chip, una fila, un nodo de diagrama",
    "pop": "aparece un elemento pequeño (icono, emoji, palabra clave)",
    "riser": "sube la tensión antes de la idea principal",
    "sub_drop": "golpe grave en un punch-in o una revelación",
    "notify_a": "llega un aviso / mensaje",
    "chime": "el CTA: invitación a comentar",
    "close": "cierre con cola",
}
SR, CH, UMBRAL_DB, PICO_DB = 48000, 2, -50.0, -3.0


def decodifica(src):
    """A WAV temporal (el ffmpeg de Remotion no tiene salida s16le cruda) y de ahí a muestras."""
    tmp = KIT / ".tmp_decodifica.wav"
    p = subprocess.run([ff.binario("ffmpeg"), "-v", "error", "-y", "-i", str(src), "-vn", "-ac", str(CH),
                        "-ar", str(SR), "-c:a", "pcm_s16le", str(tmp)], capture_output=True)
    if p.returncode != 0:
        sys.exit(f"No pude leer {src}:\n{p.stderr.decode(errors='replace')[-400:]}")
    with wave.open(str(tmp)) as w:
        a = array.array("h"); a.frombytes(w.readframes(w.getnframes()))
    tmp.unlink()
    return a


def procesa(a):
    umbral = 32767 * 10 ** (UMBRAL_DB / 20)
    ini = next((i for i, v in enumerate(a) if abs(v) > umbral), 0)
    ini -= ini % CH
    a = a[ini:]
    pico = max((abs(v) for v in a), default=0)
    if not pico:
        sys.exit("el archivo está en silencio")
    k = (32767 * 10 ** (PICO_DB / 20)) / pico
    return array.array("h", (max(-32768, min(32767, int(v * k))) for v in a)), 20 * math.log10(k)


def escribe(a, dst):
    with wave.open(str(dst), "wb") as w:
        w.setnchannels(CH); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.tobytes())


def invierte(a):
    fr = [a[i:i + CH] for i in range(0, len(a), CH)]
    out = array.array("h")
    for f in reversed(fr):
        out.extend(f)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pares", nargs="*", help="archivo:hueco")
    ap.add_argument("--lista", action="store_true")
    a = ap.parse_args()
    KIT.mkdir(parents=True, exist_ok=True)
    man_p = KIT / "manifest.json"
    man = json.loads(man_p.read_text(encoding="utf-8")) if man_p.exists() else {}
    if a.lista or not a.pares:
        print(f"kit: {KIT}")
        for h, para in HUECOS.items():
            print(f"  {'OK ' if (KIT / f'{h}.wav').exists() else '   '} {h:<11} {para}")
        extra = sorted(p.stem for p in KIT.glob("*.wav") if p.stem not in HUECOS)
        if extra:
            print(f"  además: {', '.join(extra)}")
        return
    hechos = set()
    for par in a.pares:
        src, _, hueco = par.rpartition(":")
        if not src or not hueco or not pathlib.Path(src).exists():
            sys.exit(f"«{par}» no vale: usa ruta/al/archivo.mp3:hueco (y que el archivo exista)")
        datos, g = procesa(decodifica(src))
        escribe(datos, KIT / f"{hueco}.wav")
        man[hueco] = {"origen": "propio", "archivo": pathlib.Path(src).name,
                      "para": HUECOS.get(hueco, "hueco propio"), "duracion": round(len(datos) / CH / SR, 3),
                      "ganancia_aplicada_db": round(g, 2)}
        hechos.add(hueco)
        print(f"  {hueco:<11} {man[hueco]['duracion']:5.2f}s  gain {g:+6.2f} dB  ← {pathlib.Path(src).name}")
    if "whoosh_in" in hechos and "whoosh_out" not in hechos:
        w = wave.open(str(KIT / "whoosh_in.wav")); d = array.array("h"); d.frombytes(w.readframes(w.getnframes())); w.close()
        escribe(invierte(d), KIT / "whoosh_out.wav")
        man["whoosh_out"] = {"derivado_de": "whoosh_in", "proceso": "invertido", "para": HUECOS["whoosh_out"]}
        print("  whoosh_out  derivado de whoosh_in (invertido)")
    man_p.write_text(json.dumps(man, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"→ {KIT}")


if __name__ == "__main__":
    main()
